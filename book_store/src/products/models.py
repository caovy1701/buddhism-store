import uuid

from categories.models import CategoryBase
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.text import slugify

User = get_user_model()


def upload_category_icon(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    category_id = instance.id
    return f"categories/{category_id}/{filename}"


def product_image_upload(instance, filename):
    category_id = instance.category_id
    product_slug = instance.slug
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f"categories/{category_id}/{product_slug}/{filename}"


def product_variant_image_upload(instance, filename):
    category = instance.product.category_id
    product_slug = instance.product.slug
    product_variant_slug = instance.slug
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    print(f"categories/{category}/{product_slug}/{product_variant_slug}/{filename}")
    return f"categories/{category}/{product_slug}/{product_variant_slug}/{filename}"


def path_media(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    product_variant_slug = instance.content_object.slug
    product_slug = instance.content_object.product.slug
    category_id = instance.content_object.product.category_id
    return f"categories/{category_id}/{product_slug}/{product_variant_slug}/{filename}"


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class GenericActivity(TimeStampModel):

    class Type(models.TextChoices):
        WISHLIST = "wishlist"
        RATE = "rate"
        REVIEW = "review"

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="activities", null=True
    )
    type = models.CharField(max_length=10, choices=Type.choices)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name="activities"
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    rating = models.PositiveIntegerField(default=0, blank=True, null=True)

    class Meta:
        verbose_name = "Generic Activity"
        verbose_name_plural = "Generic Activities"

    def __str__(self):
        return f"<{self.type}> {self.user} - {self.content_object}"

    def wishlist_activity(self, user, object_id):
        return self.objects.filter(
            user=user, object_id=object_id, type=self.Type.WISHLIST
        ).first()


class Category(CategoryBase, TimeStampModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True)
    icon = models.ImageField(upload_to=upload_category_icon, blank=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Product(TimeStampModel):
    name = models.CharField(max_length=255)
    summary = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=product_image_upload, blank=True, null=True)
    active = models.BooleanField(default=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="products",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)


class ProductVariant(TimeStampModel):
    sku = models.CharField(max_length=255, unique=True, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    about_brand = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField(
        upload_to=product_variant_image_upload, blank=True, null=True
    )

    activities = GenericRelation(
        GenericActivity,
        related_query_name="product_variant",
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variants"
    )
    media_order = ArrayField(models.IntegerField(), default=list, blank=True, null=True)
    media = GenericRelation("Media", related_query_name="product_variant")

    stock = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=100, decimal_places=0, default=0)
    active = models.BooleanField(default=True)
    total_rating = models.PositiveIntegerField(default=0)
    unit_sold = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Product Variant"
        verbose_name_plural = "Product Variants"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(ProductVariant, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/shop/product/{self.product.slug}/variant/{self.pk}"


class Media(TimeStampModel):

    class Type(models.TextChoices):
        VIDEO = "video"
        IMAGE = "image"

    type = models.CharField(max_length=5, choices=Type.choices, default=Type.IMAGE)
    file = models.FileField(upload_to=path_media, blank=True, null=True)
    alt = models.CharField(max_length=255, blank=True, null=True)
    extra = models.JSONField(blank=True, null=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True
    )
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return self.file.name


class Review(TimeStampModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews", null=True
    )
    product_variant = models.ForeignKey(
        ProductVariant, on_delete=models.CASCADE, related_name="reviews"
    )
    review = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def __str__(self):
        return f"{self.user} - {self.product_variant}"
