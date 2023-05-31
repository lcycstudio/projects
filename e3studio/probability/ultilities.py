# from userprofile.models import Profile
# import probability.models as models


def chapter_image_path(instance, filename):
    return 'e3studio/images/probability/chapter/{0}/{1}'.format(instance.chapter, filename)


def latex_image_path(instance, filename):
    return 'e3studio/images/probability/latex/{0}/{1}/{2}'.format(instance.chapter, instance.section, filename)


def section_image_path(instance, filename):
    return 'e3studio/images/probability/section/{0}/{1}/{2}'.format(instance.chapter, instance.section, filename)

# def chapter_image_path(instance, filename):
#     chapter_path = '{0}/chapter/{1}'.format(
#         settings.MLEARN_ROOT, instance.chapter)
#     if os.path.isdir(chapter_path) is False:
#         os.makedirs(chapter_path)
#     if len(os.listdir(chapter_path)) != 0:
#         os.remove('{0}/{1}'.format(chapter_path,
#                                    os.listdir(chapter_path)[0]))
#     new_filename = '{0}{1}'.format(instance.chapter, filename[-4:])
#     chapter_directory = '{0}/chapter'.format(
#         settings.MLEARN_ROOT)
#     chapters_in_folder = os.listdir(chapter_directory)
#     chapters_in_db = models.Chapter.objects.all()
#     chapters_db_list = [x.chapter for x in chapters_in_db]
#     chapters_left = list(set(chapters_in_folder) - set(chapters_db_list))
#     if len(chapters_left) != 0:
#         for folder_del in chapters_left:
#             shutil.rmtree('{0}/{1}'.format(chapter_directory, folder_del))
#     return 'probability/chapter/{0}/{1}'.format(instance.chapter, new_filename)


# def section_image_path(instance, filename):
#     section_path = '{0}/section/{1}/{2}'.format(
#         settings.MLEARN_ROOT, instance.chapter, instance.section)
#     if os.path.isdir(section_path) is False:
#         os.makedirs(section_path)
#     if len(os.listdir(section_path)) != 0:
#         if filename in os.listdir(section_path):
#             os.remove('{0}/{1}'.format(section_path, filename))
#     # new_filename = '{0}{1}'.format('figure', filename[-4:])
#     # new_filename = filename
#     # delete folder if section title is changed
#     chapter_folder = '{0}/section/{1}'.format(
#         settings.MLEARN_ROOT, instance.chapter)
#     sections_in_folder = os.listdir(chapter_folder)
#     sections_in_db = models.Section.objects.filter(
#         chapter=instance.chapter)
#     sections_db_list = [x.section for x in sections_in_db]
#     sections_left = list(set(sections_in_folder) - set(sections_db_list))
#     if len(sections_left) != 0:
#         for folder_del in sections_left:
#             shutil.rmtree('{0}/{1}'.format(chapter_folder, folder_del))
#     return 'probability/section/{0}/{1}/{2}'.format(instance.chapter, instance.section, filename)
