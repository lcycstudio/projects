import uuid
import os
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from .ultilities import apps_math_image_path_front, apps_math_image_path_top, apps_math_image_path_right

# Create your models here.


class AppsMath(models.Model):
    appname = models.CharField(max_length=200, blank=False, null=True)
    front_image = models.ImageField(
        upload_to=apps_math_image_path_front, verbose_name="front image", blank=True, null=True)
    top_image = models.ImageField(
        upload_to=apps_math_image_path_top, verbose_name="top image", blank=True, null=True)
    right_image = models.ImageField(
        upload_to=apps_math_image_path_right, verbose_name="right image", blank=True, null=True)
    right_image_web = models.CharField(max_length=200, blank=False, null=True)
    icon = models.CharField(max_length=200, blank=False, null=True)
    web = models.CharField(max_length=50, blank=False, null=True)
    description = models.TextField(max_length=300, blank=False, null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return str(self.appname)


class Function(models.Model):
    appname = models.ForeignKey(AppsMath, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, blank=False, null=True)
    note = models.CharField(max_length=200, blank=False, null=True)
    latex = models.CharField(max_length=200, blank=False, null=True)

    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        self.latex = '"use strict"; this.setLatexEdit(this.ilatex)'
        super(Function, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)


class Parameter(models.Model):
    appname = models.ForeignKey(AppsMath, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, blank=False, null=True)
    note = models.CharField(max_length=200, blank=False, null=True)
    latex = models.CharField(max_length=200, blank=False, null=True)

    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        self.latex = '"use strict"; this.setLatexEdit(this.ilatex)'
        super(Parameter, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)


class InitialFunctionValue(models.Model):
    appname = models.ForeignKey(AppsMath, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, blank=False, null=True)
    note = models.CharField(max_length=200, blank=False, null=True)
    latex = models.CharField(max_length=200, blank=False, null=True)

    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        self.latex = '"use strict"; this.setLatexEdit(this.ilatex)'
        super(InitialFunctionValue, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)


class InitialDerivativeValue(models.Model):
    appname = models.ForeignKey(AppsMath, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, blank=False, null=True)
    note = models.CharField(max_length=200, blank=False, null=True)
    latex = models.CharField(max_length=200, blank=False, null=True)

    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        self.latex = '"use strict"; this.setLatexEdit(this.ilatex)'
        super(InitialDerivativeValue, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)


class LeftBound(models.Model):
    appname = models.ForeignKey(AppsMath, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, blank=False, null=True)
    note = models.CharField(max_length=200, blank=False, null=True)
    latex = models.CharField(max_length=200, blank=False, null=True)

    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        self.latex = '"use strict"; this.setLatexEdit(this.ilatex)'
        super(LeftBound, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)


class RightBound(models.Model):
    appname = models.ForeignKey(AppsMath, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, blank=False, null=True)
    note = models.CharField(max_length=200, blank=False, null=True)
    latex = models.CharField(max_length=200, blank=False, null=True)

    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        self.latex = '"use strict"; this.setLatexEdit(this.ilatex)'
        super(RightBound, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)


class Title(models.Model):
    appname = models.ForeignKey(AppsMath, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, blank=False, null=True)
    note = models.CharField(max_length=200, blank=False, null=True)
    latex = models.CharField(max_length=200, blank=False, null=True)

    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        self.latex = '"use strict"; this.setLatexEdit(this.ilatex)'
        super(Title, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)


class HorizontalLabel(models.Model):
    appname = models.ForeignKey(AppsMath, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, blank=False, null=True)
    note = models.CharField(max_length=200, blank=False, null=True)
    latex = models.CharField(max_length=200, blank=False, null=True)

    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        self.latex = '"use strict"; this.setLatexEdit(this.ilatex)'
        super(HorizontalLabel, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)


class VerticalLabel(models.Model):
    appname = models.ForeignKey(AppsMath, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, blank=False, null=True)
    note = models.CharField(max_length=200, blank=False, null=True)
    latex = models.CharField(max_length=200, blank=False, null=True)

    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        self.latex = '"use strict"; this.setLatexEdit(this.ilatex)'
        super(VerticalLabel, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)

    # left_bound = models.CharField(max_length=200, blank=False, null=True)
    # lb_note = models.CharField(max_length=200, blank=False, null=True)

    # right_bound = models.CharField(max_length=200, blank=False, null=True)
    # rb_note = models.CharField(max_length=200, blank=False, null=True)

    # title = models.CharField(max_length=200, blank=False, null=True)
    # title_note = models.CharField(max_length=200, blank=False, null=True)

    # horizontal_label = models.CharField(max_length=200, blank=False, null=True)
    # hl_note =models.CharField(max_length=200, blank=False, null=True)

    # vertical_label = models.CharField(max_length=200, blank=False, null=True)
    # vl_note = models.CharField(max_length=200, blank=False, null=True)
