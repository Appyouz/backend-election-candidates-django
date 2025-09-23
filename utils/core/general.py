import random
import string

from django_countries import countries
from utils.core.exceptions import InternalApplicationError
from django.utils.text import slugify


def check_and_generate_slug(
    instance, field_name, slug_field, fail_silently=False, max_length=50
):
    """
    Checks if the instance already has a pk or slug, and if so, returns the slug if fail_silently is True, otherwise raises an InternalApplicationError.

    Generates a slug from the specified field, truncates it to fit within the max_length, and checks if the generated slug already exists in the database. If it does, appends a random suffix to the base slug and tries again until a unique slug is found.

    Args:
        instance (models.Model): The instance to generate a slug for.
        field_name (str): The name of the field to generate the slug from (for example, 'name').
        slug_field (str): The name of the field to store the generated slug in (for example, 'slug').
        fail_silently (bool, optional): Defaults to False. If True, returns the slug if it already exists, otherwise raises an InternalApplicationError.
        max_length (int, optional): Defaults to 50. The maximum length of the generated slug.

    Returns:
        str: The generated slug.
    """
    if instance.pk or instance.slug:

        if fail_silently:
            return instance.slug

        raise InternalApplicationError(
            "pk of this instance is not None or Slug already exists"
        )

    from safedelete.models import SafeDeleteModel

    # Generate a slug from the specified field
    base_slug = slugify(getattr(instance, field_name))[:max_length]
    slug = base_slug

    # Truncate the slug to fit within the max length
    slug = slug[:max_length]

    model = instance.__class__

    # check if it is a safe delete model cause we're checking unique=True in entire table where SlugField is used
    is_safe_delete_model = isinstance(instance, SafeDeleteModel)
    if is_safe_delete_model:
        queryset = model.all_objects.filter()
    else:
        queryset = model.objects.filter()
    # Check if the generated slug already exists in the database
    while queryset.filter(**{slug_field: slug}).exists():
        random_suffix = "".join(random.choices(string.ascii_lowercase, k=5))
        trimmed_base = base_slug[: max_length - 6]  # 5 for random chars, 1 for hyphen
        slug = f"{trimmed_base}-{random_suffix}"

    return slug


def get_country_list():
    data = [{"code": c, "name": n} for c, n in countries]
    return data


def update_model_instance(instance, **kwargs):
    from django.core.exceptions import FieldError

    # Validate that fields exist on the model
    model_fields = {field.name for field in instance._meta.get_fields()}
    for key in kwargs:
        if key not in model_fields:
            raise FieldError(
                f"Field '{key}' does not exist on {instance.__class__.__name__}"
            )
    for key, value in kwargs.items():
        setattr(instance, key, value)
    instance.save()
    return instance
