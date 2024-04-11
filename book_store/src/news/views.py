from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import News, Category

# Create your views here.


class CategoryMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class NewsListView(CategoryMixin, ListView):
    model = News
    template_name = "news/news_list.html"
    context_object_name = "news"
    paginate_by = 10

    def get_queryset(self):
        if "slug" in self.kwargs:
            category = Category.objects.get(slug=self.kwargs["slug"])
            return News.objects.filter(category=category)
        return News.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest_news"] = News.objects.all().order_by("-created")[:5]
        return context


class NewsDetailView(CategoryMixin, DetailView):
    model = News
    template_name = "news/news_detail.html"
    context_object_name = "news"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest_news"] = News.objects.all().order_by("-created")[:5]
        return context

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return News.objects.filter(pk=pk)
