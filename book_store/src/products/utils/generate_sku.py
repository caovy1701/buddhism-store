from datetime import datetime


def generate_sku(instance):
    """
    Generate a unique SKU for a product
    """
    # get first Letter of Product Variant Name
    product_variant_name = instance.name.split(" ")[0]
    # get datetime string
    datetime_str = instance.created_at.strftime("%Y%m%d%H%M%S")
    # get product variant id
    product_variant_id = instance.id
    # get product id
    product_id = instance.product.id
    # get category id
    category_id = instance.product.category.id

    return f"{product_variant_name}-{datetime_str}-{product_variant_id}-{product_id}-{category_id}"
