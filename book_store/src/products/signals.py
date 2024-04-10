from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from src.products.models import Media, ProductVariant


@receiver(post_save, sender=Media)
def media_pre_save(sender, instance, created, **kwargs):
    if created:
        print("Media created")
        print(instance.content_object)
        if isinstance(instance.content_object, ProductVariant):
            product_variant = instance.content_object
            product_variant.media_order.append(instance.pk)
            product_variant.save()
            print("Media added to product variant")
            print(product_variant.media_order)


@receiver(post_delete, sender=Media)
def media_post_delete(sender, instance, **kwargs):
    if isinstance(instance.content_object, ProductVariant):
        product_variant = instance.content_object
        product_variant.media_order.remove(instance.pk)
        product_variant.save()
        print("Media removed from product variant")
