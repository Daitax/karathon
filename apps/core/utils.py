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


def print_month_ru(month):
    dict_months = {
        '01': 'января',
        '02': 'февраля',
        '03': 'марта',
        '04': 'апреля',
        '05': 'мая',
        '06': 'июня',
        '07': 'июля',
        '08': 'августа',
        '09': 'сентября',
        '10': 'октября',
        '11': 'ноября',
        '12': 'декабря',
    }
    return dict_months.get(month)
