from django.db import models
from categories.models import CategoryBase
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(CategoryBase, TimeStampedModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class News(TimeStampedModel):
    author = models.CharField(max_length=255, default="admin", blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True)
    thumbnail = models.ImageField(upload_to="news/thumbnails/", blank=True, null=True)
    content = RichTextField()

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="news"
    )

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(News, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.image.delete()
        super(News, self).delete(*args, **kwargs)
