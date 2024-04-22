from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
)
from django.views.generic.base import TemplateView

from src.news.models import News
from src.products.models import Category, GenericActivity, Product, ProductVariant

User = get_user_model()
# Create your views here.


def get_activity_class(obj):
    try:
        activity = obj
    except NotImplementedError:
        activity = None
    return activity


class WishListMixin:
    """
    Mixin to include wishlist in context data
    """

    def get_context_data(self, **kwargs):
        print("WishListMixin")
        context = super(WishListMixin, self).get_context_data(**kwargs)
        content_type = ContentType.objects.get_for_model(model=self.model)
        object_id = self.kwargs.get("pk")
        user = self.request.user
        if user.is_authenticated:

            context["activities"] = user.activities.filter(
                type=GenericActivity.Type.WISHLIST,
                content_type=content_type,
                object_id=object_id,
            ).first()
        print(context["activities"])
        return context


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context["news"] = News.objects.all()
        return context


class ContactView(TemplateView):
    template_name = "contact.html"


class IncludeCategoryMixin(object):
    """
    Mixin to include categories in context data
    """

    def get_context_data(self, **kwargs):
        context = super(IncludeCategoryMixin, self).get_context_data(**kwargs)
        if cate_id := self.kwargs.get("pk"):
            context["category"] = Category.objects.get(pk=cate_id)
        context["categories"] = Category.objects.all()
        return context


class CategoryView(WishListMixin, ListView):
    template_name = "categories.html"
    model = Category
    context_object_name = "categories"

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        context["categories"] = Category.objects.all().distinct()
        print(context["categories"])
        return context


class ProductListView(WishListMixin, IncludeCategoryMixin, ListView):
    template_name = "products.html"
    model = Product
    context_object_name = "products"
    paginate_by = 6

    def get_queryset(self):
        category_id = self.kwargs.get("pk")
        return Product.objects.filter(category_id=category_id)

    def get_context_data(self, **kwargs):
        category_id = self.kwargs.get("pk")
        context = super(ProductListView, self).get_context_data(**kwargs)
        context["products"] = Product.objects.filter(category_id=category_id)
        context["category"] = Category.objects.get(pk=category_id)
        return context


class ProductDetailView(WishListMixin, DetailView):
    template_name = "product_detail.html"
    model = ProductVariant
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        product_variant_id = self.kwargs.get("pk")
        product_slug = self.kwargs.get("slug")
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        products_variants = ProductVariant.objects.filter(
            product__slug=product_slug
        ).select_related("product")
        context["product_variants"] = products_variants
        context["product_variant"] = products_variants.get(pk=product_variant_id)
        context["products_related"] = Product.objects.exclude(slug=product_slug)
        return context

    def get_queryset(self):
        product_slug = self.kwargs.get("slug")
        return ProductVariant.objects.filter(product__slug=product_slug)


class WishListView(CreateView):
    model = ProductVariant
    fields = ["type", "content_type", "object_id"]
    template_name = "product_detail.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        user = request.user
        product_variant = self.get_queryset().first()
        activity = product_variant.activities.create(
            user=user, type=GenericActivity.Type.WISHLIST
        )
        activity.save()
        return redirect(
            "product-variant-detail",
            slug=product_variant.product.slug,
            pk=product_variant.pk,
        )

    def get_queryset(self):
        product_variant_id = self.kwargs.get("id")
        return ProductVariant.objects.filter(pk=product_variant_id)


class WishListDeleteView(DeleteView):
    model = ProductVariant
    template_name = "product_detail.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        user = request.user
        product_variant = self.get_queryset().first()
        activity = product_variant.activities.filter(
            user=user, type=GenericActivity.Type.WISHLIST
        ).first()
        activity.delete()

        return redirect(
            "product-variant-detail",
            slug=activity.content_object.product.slug,
            pk=activity.content_object.pk,
        )

    def get_queryset(self):
        product_variant_id = self.kwargs.get("id")
        return ProductVariant.objects.filter(pk=product_variant_id)
