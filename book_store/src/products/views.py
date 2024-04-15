from typing import Any
from django.shortcuts import redirect
from django.http import HttpRequest, HttpResponse
from django.views.generic.base import TemplateView
from django.contrib.contenttypes.models import ContentType
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth import get_user_model
from src.products.models import (
    Category,
    Product,
    ProductVariant,
    GenericActivity,
)
from src.news.models import News


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


class CategoryView(ListView):
    """
    View to display all categories
    """

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        # Get the product slug from the URL and check if it exists
        if product_slug := self.kwargs.get("slug"):
            product = Product.objects.get(slug=product_slug)
            context["related_products"] = Product.objects.filter(
                category=product.category
            )
        return context


class CategoryView(ListView):
    template_name = "categories.html"
    model = Category
    context_object_name = "categories"

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        context["categories"] = Category.objects.all().distinct()
        print(context["categories"])
        return context


class ProductListView(IncludeCategoryMixin, ListView):
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


def wishlist(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect("login")
    product_variant_id = kwargs.get("id")
    product_variant = ProductVariant.objects.get(pk=product_variant_id)
    user = request.user
    activity = product_variant.activities.create(
        user=user, type=GenericActivity.Type.WISHLIST
    )
    return redirect(
        "product-variant-detail",
        slug=product_variant.product.slug,
        pk=product_variant.pk,
    )


def un_wishlist(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect("login")
    product_variant_id = kwargs.get("id")
    product_variant = ProductVariant.objects.get(pk=product_variant_id)
    user = request.user
    activity = product_variant.activities.get(user=user)
    activity.delete()
    return redirect(
        "product-variant-detail",
        slug=product_variant.product.slug,
        pk=product_variant.pk,
    )
