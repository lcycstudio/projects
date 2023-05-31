
def user_directory_path(instance, filename):
    return 'e3studio/images/avatars/{0}/{1}'.format(instance.user.username, filename)
    # avatarFilename = 'avatar_{0}{1}'.format(
    #     instance.user.username, filename[-4:])
    # user_path = '{0}/{1}/'.format(settings.AVATAR_ROOT, instance.user.username)
    # if not os.path.isdir(user_path):
    #     os.makedirs(user_path)
    # if len(os.listdir(user_path)) != 0:
    #     for file in os.listdir(user_path):
    #         os.remove('{0}/{1}'.format(user_path, file))
    # return 'avatars/{0}/{1}'.format(instance.user.username, avatarFilename)
