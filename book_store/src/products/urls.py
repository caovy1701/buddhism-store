from django.urls import path
from src.products.views import (
    CategoryView,
    ContactView,
    HomeView,
    ProductDetailView,
    ProductListView,
    un_wishlist,
    wishlist,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("shop/category/", CategoryView.as_view(), name="category"),
    path("shop/category/<int:pk>/", ProductListView.as_view(), name="products-list"),
    path(
        "shop/product/<slug:slug>/", ProductDetailView.as_view(), name="product-detail"
    ),
    path(
        "shop/product/<slug:slug>/variant/<int:pk>/",
        ProductDetailView.as_view(),
        name="product-variant-detail",
    ),
    path("wishlist/<int:id>/", wishlist, name="wishlist"),
    path("un-wishlist/<int:id>/", un_wishlist, name="unwishlist"),
]
