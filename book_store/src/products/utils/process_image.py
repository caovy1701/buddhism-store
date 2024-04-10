import os


def process_delete_image(instance):
    """
    Delete image from storage
    """
    if instance.type == "image":
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
    else:
        if os.path.isfile(instance.file):
            os.remove(instance.file)
    print("Image deleted")
