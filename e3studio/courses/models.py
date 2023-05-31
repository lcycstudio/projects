# Create your models here.
import uuid
import os
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from .ultilities import subject_image_path_front, subject_image_path_top, public_file_path
from cloudinary_storage.storage import RawMediaCloudinaryStorage


class Subject(models.Model):
    subject = models.CharField(max_length=200, blank=False, null=True)
    content = models.TextField(max_length=200, blank=False, null=True)
    front_image = models.ImageField(
        upload_to=subject_image_path_front, verbose_name="front image", blank=True, null=True)
    top_image = models.ImageField(
        upload_to=subject_image_path_top, verbose_name="top image", blank=True, null=True)
    web = models.CharField(max_length=50, blank=False, null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return str(self.subject)


class Public(models.Model):
    file = models.ImageField(
        upload_to=public_file_path, verbose_name="public file", blank=True, null=True, storage=RawMediaCloudinaryStorage())

    class Meta:
        ordering = ['id']

    def __str__(self):
        return str(self.id)
    # def save(self, *args, **kwargs):
    #     try:
    #         this = Public.objects.get(id=self.id)  # get the system file
    #         this.file.delete(save=False)  # delete the system file
    #     except Exception:
    #         pass
    #     super().save(*args, **kwargs)

    # def delete(self, *args, **kwargs):
    #     storage, path = self.file.storage, self.file.path
    #     super(Public, self).delete(*args, **kwargs)
    #     storage.delete(path)
