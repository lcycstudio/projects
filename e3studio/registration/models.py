from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# class CustomUser(models.Model):
#     title = models.CharField(max_length=120)
#     content = models.TextField()

#     def __str__(self):
#         return self.title

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