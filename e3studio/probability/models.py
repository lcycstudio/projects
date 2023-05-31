# Create your models here.
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from probability.ultilities import chapter_image_path, section_image_path


def chapter_cover_path(instance, filename):
    return 'e3studio/images/probability/chapter/{0}/{1}'.format(instance.chapter, filename)


def section_image_path(instance, filename):
    return 'e3studio/images/probability/section/{0}/{1}/{2}'.format(instance.chapter, instance.section, filename)


class Chapter(models.Model):
    chapter = models.CharField(max_length=100, blank=False, null=True)
    icon = models.CharField(max_length=100, blank=True, null=True)
    cover = models.ImageField(
        upload_to=chapter_cover_path, verbose_name="chapter cover", blank=True, null=True)
    top = models.ImageField(
        upload_to=chapter_cover_path, verbose_name="chapter top", blank=True, null=True)

    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        try:
            this = Chapter.objects.get(id=self.id)  # get the system image
            this.image.delete(save=False)  # delete the system image
        except Exception:
            pass
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        storage, path = self.image.storage, self.image.path
        super(Chapter, self).delete(*args, **kwargs)
        storage.delete(path)

    def __str__(self):
        return self.chapter


class Section(models.Model):
    section = models.CharField(max_length=200, blank=False, null=True)
    chapter = models.ForeignKey(
        Chapter, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['id']

    def delete(self, *args, **kwargs):
        storage, path = self.image.storage, self.image.path
        super(Section, self).delete(*args, **kwargs)
        storage.delete(path)

    def __str__(self):
        return str(self.section)


class Paragraph(models.Model):
    paragraph = models.TextField(max_length=5000, blank=False, null=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return str(self.paragraph)


# class Equation(models.Model):
#     equation = models.TextField(max_length=5000, blank=False, null=True)
#     chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True)
#     section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)

#     class Meta:
#         ordering = ['id']

#     def __str__(self):
#         return str(self.equation)


class Image(models.Model):
    section_image = models.ImageField(upload_to=section_image_path,
                                      verbose_name="section image", blank=True, null=True)
    caption = models.TextField(max_length=5000, blank=True, null=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return str(self.section_image)


class Exercise(models.Model):
    exercise = models.TextField(max_length=5000, blank=False, null=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return str(self.exercise)


class Choice(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)
    exercise = models.ForeignKey(
        Exercise, on_delete=models.SET_NULL, null=True)
    choice_1 = models.TextField(max_length=500, blank=False, null=True)
    choice_2 = models.TextField(max_length=500, blank=False, null=True)
    choice_3 = models.TextField(max_length=500, blank=False, null=True)
    pick_1 = 'A'
    pick_2 = 'B'
    pick_3 = 'C'
    STATUS = [
        (pick_1, choice_1),
        (pick_2, choice_2),
        (pick_3, choice_3),
    ]
    answer = models.CharField(
        max_length=1, choices=STATUS, default=pick_1, blank=False, null=True)
    comment_1 = models.TextField(max_length=500, blank=True, null=True)
    equation_1 = models.TextField(max_length=500, blank=True, null=True)
    comment_2 = models.TextField(max_length=500, blank=True, null=True)
    equation_2 = models.TextField(max_length=500, blank=True, null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return str(self.answer)


class Answer(models.Model):
    answer = models.TextField(
        max_length=2, blank=True, null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return str(self.answer)


# class CodeText(models.Model):
#     codetext = models.TextField(max_length=500, blank=True, null=True)
#     plot = models.CharField(max_length=500, blank=True, null=True)
#     value = models.CharField(max_length=500, blank=True, null=True)
#     chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True)
#     section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)

#     class Meta:
#         ordering = ['id']

#     def __str__(self):
#         return str(self.id)


# class Plot(models.Model):
#     plot = models.CharField(max_length=500, blank=True, null=True)
#     chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True)
#     section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)

#     class Meta:
#         ordering = ['id']

#     def __str__(self):
#         return str(self.id)
