import uuid
import os
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from .ultilities import appname_image_path_front, appname_image_path_top


class App(models.Model):
    appname = models.CharField(max_length=200, blank=False, null=True)
    content = models.TextField(max_length=200, blank=False, null=True)
    front_image = models.ImageField(
        upload_to=appname_image_path_front, verbose_name="front image", blank=True, null=True)
    top_image = models.ImageField(
        upload_to=appname_image_path_top, verbose_name="top image", blank=True, null=True)
    web = models.CharField(max_length=50, blank=False, null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return str(self.appname)
