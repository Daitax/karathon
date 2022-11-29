import hashlib
import os

from project.settings import MEDIA_ROOT


def check_media_directory_exist(base_dir, sub_dir):
    new_dir = '{0}/{1}/{2}'.format(MEDIA_ROOT, base_dir, sub_dir)
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)


def create_name_participant_path(participant):
    md5_str = '{}{}'.format(participant.phone, participant.id)
    md5_hash = hashlib.md5(md5_str.encode()).hexdigest()

    salt_first_simbol = md5_hash[5]
    salt_second_simbol = md5_hash[8]
    salt_third_simbol = md5_hash[13]
    salt_fourth_simbol = md5_hash[21]

    format_phone = str(participant.phone)[-10:]

    name_path = '{}_{}{}{}{}'.format(format_phone, salt_first_simbol, salt_second_simbol,
                                     salt_third_simbol, salt_fourth_simbol)

    return name_path


def ending_numbers(number, words_list):
    num = number % 100
    if num > 19:
        num = num % 10

    if num == 1:
        return words_list[0]
    elif num == 2 or num == 3 or num == 4:
        return words_list[1]
    else:
        return words_list[2]


def get_choice_value(choices, choice_key):
    for choice in choices:
        if choice[0] == choice_key:
            return choice[1]


def get_participant_photo_path(instance, filename):
    base_dir = 'photo'

    user_dir = create_name_participant_path(instance.participant)
    check_media_directory_exist(base_dir, user_dir)

    return '{0}/{1}/{2}'.format(base_dir, user_dir, filename)


def get_report_image_path(instance, filename):
    base_dir = 'reports'

    user_dir = create_name_participant_path(instance.participant)
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
