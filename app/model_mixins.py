"""
kamal.py
model_mixins.py


Mixins for models, these mixins contains
most commonly used fields in more than one model.
"""
from django.db import models
from django.contrib.auth.models import User


class CreatedUpdatedMixin(models.Model):
    """
    generic mixing to update who and when was created or modified.
    this is a abstract class
    """
    created_by = models.ForeignKey(User,
                                   related_name="%(app_label)s_%(class)s_adder",
                                   on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    modified_by = models.ForeignKey(User,
                                    related_name="%(app_label)s_%(class)s_editor",
                                    on_delete=models.PROTECT)
    modified_date = models.DateTimeField(auto_now=True, auto_now_add=True,
                                         editable=False)

    class Meta:
        """
        options to define the class
        """
        abstract = True


class IsActiveMixin(models.Model):
    """
    generic mixing to update to show whether record is valid or not.
    this is a abstract class
    """
    is_active = models.BooleanField(default=True)

    class Meta:
        """
        options to define the class
        """
        abstract = True

