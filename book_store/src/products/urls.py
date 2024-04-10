from src.products.views import HomeView, CategoryView, ProductListView, ProductDetailView, ContactView

from django.urls import path

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('shop/category/', CategoryView.as_view(), name='category'),
    path('shop/category/<int:pk>/', ProductListView.as_view(), name='products-list'),
    # {% url 'product-detail' slug=product.slug %}
    path('shop/product/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    # {% url 'product-variant-detail' slug=product.slug pk=product_variant.pk %}
    path('shop/product/<slug:slug>/variant/<int:pk>/', ProductDetailView.as_view(), name='product-variant-detail'),

]