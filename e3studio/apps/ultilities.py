import os
import shutil
from django.conf import settings
from django.contrib.auth.models import User
# from userprofile.models import Profile
import courses.models as models


def appname_image_path_front(instance, filename):
    return 'e3studio/images/apps/{0}/{1}'.format(instance.appname, filename)


def appname_image_path_top(instance, filename):
    return 'e3studio/images/apps/{0}/{1}'.format(instance.appname, filename)
