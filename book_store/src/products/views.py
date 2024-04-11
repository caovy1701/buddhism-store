from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, DetailView, TemplateView
from django.core.paginator import Paginator
from django.views.generic.base import TemplateView
from src.products.models import Category, Product, ProductVariant, Media
from src.news.models import News

# Create your views here.


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


class IncludeRelatedProductsMixin(object):
    """
    Mixin to include related products in context data
    """

    def get_context_data(self, **kwargs):
        context = super(IncludeRelatedProductsMixin, self).get_context_data(**kwargs)
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


class ProductDetailView(DetailView, IncludeCategoryMixin):
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
