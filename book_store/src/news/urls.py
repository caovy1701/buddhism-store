from django.urls import path
from src.news.views import NewsListView, NewsDetailView


urlpatterns = [
    path("", NewsListView.as_view(), name="news"),
    path("<slug:slug>/", NewsListView.as_view(), name="news"),
    path("<slug:slug>/<int:pk>/", NewsDetailView.as_view(), name="news_detail"),
]
