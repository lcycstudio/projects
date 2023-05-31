# import os
# import shutil
# from django.conf import settings
# from django.contrib.auth.models import User
# from userprofile.models import Profile
# import courses.models as models


def subject_image_path_front(instance, filename):
    return 'e3studio/images/courses/{0}/{1}'.format(instance.subject, filename)
    # subject_path = '{0}/images/{1}'.format(
    #     settings.COURSE_ROOT, instance.subject)
    # if os.path.isdir(subject_path) is False:
    #     os.makedirs(subject_path)
    # new_filename = '{0}_front{1}'.format(
    #     instance.subject, filename[-4:]).replace(' ', '_')
    # print(new_filename)
    # if len(os.listdir(subject_path)) != 0:
    #     if new_filename in os.listdir(subject_path):
    #         os.remove('{0}/{1}'.format(subject_path, new_filename))
    # return 'courses/images/{0}/{1}'.format(instance.subject, new_filename)


def subject_image_path_top(instance, filename):
    return 'e3studio/images/courses/{0}/{1}'.format(instance.subject, filename)
    # subject_path = '{0}/images/{1}'.format(
    #     settings.COURSE_ROOT, instance.subject)
    # if os.path.isdir(subject_path) is False:
    #     os.makedirs(subject_path)
    # new_filename = '{0}_top{1}'.format(
    #     instance.subject, filename[-4:]).replace(' ', '_')
    # if len(os.listdir(subject_path)) != 0:
    #     if new_filename in os.listdir(subject_path):
    #         os.remove('{0}/{1}'.format(subject_path, new_filename))
    # return 'courses/images/{0}/{1}'.format(instance.subject, new_filename)


# def chapter_file_path(instance, filename):
#     return 'ok'


def public_file_path(instance, filename):
    return 'e3studio/public/{0}'.format(filename)


def public_icon_path(instance, filename):
    return 'e3studio/public/{0}'.format(filename)
    # public_path = '{0}'.format(settings.PUBLIC_ROOT)
    # if os.path.isdir(public_path) is False:
    #     os.makedirs(public_path)
    # if len(os.listdir(public_path)) != 0:
    #     if filename in os.listdir(public_path):
    #         os.remove('{0}/{1}'.format(public_path, filename))
    # return 'public/{0}'.format(filename)
