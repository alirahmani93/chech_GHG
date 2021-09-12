def model_image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    file_type = filename.split(".")[-1]
    email = instance.product.supplier.email.split("@")[0]
    slug = instance.product.slug
    return f'{instance.__class__.__name__}/{instance.id}_{slug}_{email}.{file_type}'
