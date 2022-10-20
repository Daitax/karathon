import os

from project.settings import MEDIA_ROOT


def check_media_directory_exist(base_dir, sub_dir):
    new_dir = '{0}/{1}/{2}'.format(MEDIA_ROOT, base_dir, sub_dir)
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)


def get_choice_value(choices, choice_key):
    for choice in choices:
        if choice[0] == choice_key:
            return choice[1]


def get_report_image_path(instance, filename):
    base_dir = 'reports'
    user_dir = str(instance.participant.phone) + "." + str(instance.participant.id)
    check_media_directory_exist(base_dir, user_dir)

    return '{0}/{1}/{2}'.format(base_dir, user_dir, filename)
