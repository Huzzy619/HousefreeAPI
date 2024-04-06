from django.db import models
from django.forms.models import model_to_dict
from django_lifecycle.mixins import LifecycleModelMixin


class BaseModel(LifecycleModelMixin, models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def to_dict(self) -> dict:
        return model_to_dict(self)
