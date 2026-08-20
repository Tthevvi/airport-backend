from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError


def get_object_or_400(model, **kwargs):
    """
    Аналог стандартного get_object_or_404, но для случаев, когда 404 не подходит по смыслу
    (например, входные данные пришли в теле POST-запроса, а не в URL) —
    возвращает понятную ошибку 400 вместо "сырого" 500 с трейсбеком.
    """
    try:
        return model.objects.get(**kwargs)
    except ObjectDoesNotExist:
        name = getattr(model._meta, "verbose_name", model.__name__)
        raise ValidationError(f"{name} с указанным id не найден(а).")