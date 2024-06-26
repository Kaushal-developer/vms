from django.db import models
from django.db.models import ForeignObjectRel, ManyToManyRel, OneToOneRel, BooleanField, CharField
from model_utils.models import TimeStampedModel
from django_lifecycle import LifecycleModelMixin

'''Custom Base Model-> Fields which are common to all the table should be mention here.'''
class BaseModel(LifecycleModelMixin,TimeStampedModel):
    ORDERING = ("-created",)

    created_by = models.CharField(verbose_name="Created by", max_length=100, blank=True, null=True)
    updated_by = models.CharField(verbose_name="Updated by", max_length=100, blank=True, null=True)

    class Meta:
        abstract = True

    @property
    def added_on(self):
        return self.created

    @property
    def updated_on(self):
        return self.modified

    def save(self, *args, **kwargs):
        if self.pk:
            # If self.pk is not None then it's an update.
            cls = self.__class__
            old = cls.objects.get(pk=self.pk)
            new = self  # This gets the newly instantiated Model object with the new values.
            changed_fields = []
            for field in cls._meta.get_fields():
                field_name = field.name
                try:
                    if getattr(old, field_name) != getattr(new, field_name):
                        changed_fields.append(field_name)
                except Exception as ex:  # Catch field does not exist exception
                    pass
            kwargs["update_fields"] = changed_fields
        super().save(*args, **kwargs)
