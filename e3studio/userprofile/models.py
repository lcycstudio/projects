from django.db import models
from django.contrib.auth.models import User
from .ultilities import user_directory_path
from courses.models import Subject
# Create your models here.


class Avatar(models.Model):
    """ upload images """
    avatar = models.ImageField(
        upload_to=user_directory_path, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        storage, path = self.avatar.storage, self.avatar.path
        # Delete the model before the file
        super(Avatar, self).delete(*args, **kwargs)
        # Delete the file after the model
        storage.delete(path)


class Profile(models.Model):
    CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    PROVS = (
        ('Alberta', 'Alberta'),
        ('British Columbia', 'British Columbia'),
        ('Manitoba', 'Manitoba'),
        ('New Brunswick', 'New Brunswick'),
        ('Newfoundland and Labrador', 'Newfoundland and Labrador'),
        ('Northwest Territories', 'Northwest Territories'),
        ('Nova Scotia', 'Nova Scotia'),
        ('Nunavut', 'Nunavut'),
        ('Ontario', 'Ontario'),
        ('Prince Edward Island', 'Prince Edward Island'),
        ('Quebec', 'Quebec'),
        ('Saskatchewan', 'Saskatchewan'),
        ('Yukon', 'Yukon'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=False, null=True)
    last_name = models.CharField(max_length=50, blank=False, null=True)
    email = models.EmailField(max_length=100, blank=True, default="",
                              help_text="Warning: if you change this email here, you must first use the button below to change the email in Users.")
    subject = models.ManyToManyField(Subject, blank=True)
    city = models.CharField(max_length=30, blank=True)
    province = models.CharField(
        max_length=30, choices=PROVS, default='British Columbia', blank=True)
    # province = models.CharField(
    #     max_length=30, choices=YearInSchool.choices, default='BC', blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=10, choices=CHOICES, default='Male', blank=False)
    bio = models.TextField(max_length=500, blank=True)

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        try:
            user = User.objects.get(id=self.user.id)
            if self.first_name is not None:
                user.first_name = self.first_name
            if self.last_name is not None:
                user.last_name = self.last_name
            user.save()
        except Exception:
            pass
        super().save(*args, **kwargs)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)
    # skill = models.ManyToManyField(Skill, blank=True)
    # language = models.ManyToManyField(Language, blank=True)

    # def display_skill(self):
    #     """Creates a string for the Skill. This is required to display skill in Admin."""
    #     return ', '.join([skill.skill for skill in Skill.objects.filter(user=self.user)[:3]])

    # def display_language(self):
    #     """Creates a string for the Genre"""
    #     return ', '.join([language.language for language in Language.objects.filter(user=self.user)[:3]])

    # display_skill.short_description = 'Skill'
    # display_language.short_description = 'Language'

# class StudentUser(models.Model):
#     first_name = models.CharField(max_length=200, blank=True, default="")
#     last_name = models.CharField(max_length=200, blank=True, default="")
#     email = models.EmailField(max_length=200, blank=True, default="",
#                               help_text="Warning: if you change this email here, you must first use the button below to change the email in Users.")
#     tailored = models.CharField(max_length=2000, blank=True, default="")
#     user_id = models.OneToOneField(User, on_delete=models.CASCADE, blank=False, null=True,
#         help_text="Warning: if you change the email above, you must first use the button below to change the email in Users.")

#     class Meta:
#         ordering = ['first_name']

#     def __str__(self):
#         return str(self.first_name + " " + self.last_name)
