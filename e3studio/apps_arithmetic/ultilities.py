import os
import shutil
from django.conf import settings
from django.contrib.auth.models import User
# from userprofile.models import Profile
import courses.models as models


def apps_arithmetic_image_path_front(instance, filename):
    return 'e3studio/images/apps/Arithmetic Apps/{0}/{1}'.format(instance.appname, filename)


def apps_arithmetic_image_path_top(instance, filename):
    return 'e3studio/images/apps/Arithmetic Apps/{0}/{1}'.format(instance.appname, filename)


def apps_arithmetic_image_path_right(instance, filename):
    return 'e3studio/images/apps/Arithmetic Apps/{0}/{1}'.format(instance.appname, filename)


# def apps_math_fig_path(instance):
    # apps_math_path = '{0}/images/{1}'.format(
    #     settings.APPS_MATH_ROOT, instance.appname)
    # if os.path.isdir(apps_math_path) is False:
    #     os.makedirs(apps_math_path)
    # new_filename = '{0}_figure.png'.format(instance.appname)
    # print(new_filename)
    # if len(os.listdir(apps_math_path)) != 0:
    #     if new_filename in os.listdir(apps_math_path):
    #         os.remove('{0}/{1}'.format(apps_math_path, new_filename))
    # return 'appsmath/images/{0}/{1}'.format(instance.appname, new_filename)

# def chapter_file_path(instance, filename):
#     return 'ok'


# def public_file_path(instance, filename):
#     public_path = '{0}'.format(settings.PUBLIC_ROOT)
#     if os.path.isdir(public_path) is False:
#         os.makedirs(public_path)
#     if len(os.listdir(public_path)) != 0:
#         if filename in os.listdir(public_path):
#             os.remove('{0}/{1}'.format(public_path, filename))
#     return 'public/{0}'.format(filename)


# def section_image_path(instance, filename):
#     section_path = '{0}/{1}/section/{2}/{3}'.format(
#         settings.COURSES_ROOT, instance.subject, instance.chapter, instance.section)
#     if os.path.isdir(section_path) is False:
#         os.makedirs(section_path)
#     if len(os.listdir(section_path)) != 0:
#         if filename in os.listdir(section_path):
#             os.remove('{0}/{1}'.format(section_path, filename))
#     # new_filename = '{0}{1}'.format('figure', filename[-4:])
#     # new_filename = filename
#     # delete folder if section title is changed
#     chapter_folder = '{0}/{1}/section/{2}'.format(
#         settings.COURSES_ROOT, instance.subject, instance.chapter)
#     sections_in_folder = os.listdir(chapter_folder)
#     sections_in_db = models.Section.objects.filter(
#         chapter=instance.chapter)
#     sections_db_list = [x.section for x in sections_in_db]
#     sections_left = list(set(sections_in_folder) - set(sections_db_list))
#     if len(sections_left) != 0:
#         for folder_del in sections_left:
#             shutil.rmtree('{0}/{1}'.format(chapter_folder, folder_del))
#     return 'courses/{0}/section/{1}/{2}/{3}'.format(instance.subject, instance.chapter, instance.section, filename)
