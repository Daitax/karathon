import hashlib
import os
import re

import cv2
import pytesseract

from django.conf import settings
from django.core.mail import send_mail

from project.settings import MEDIA_ROOT


def check_media_directory_exist(base_dir, sub_dir):
    new_dir = "{0}/{1}/{2}".format(MEDIA_ROOT, base_dir, sub_dir)
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)


def create_name_participant_path(participant):
    md5_str = "{}{}".format(participant.email, participant.id)
    md5_hash = hashlib.md5(md5_str.encode()).hexdigest()

    salt_first_simbol = md5_hash[5]
    salt_second_simbol = md5_hash[8]
    salt_third_simbol = md5_hash[13]
    salt_fourth_simbol = md5_hash[21]

    name_path = "{}_{}{}{}{}".format(
        participant.email,
        salt_first_simbol,
        salt_second_simbol,
        salt_third_simbol,
        salt_fourth_simbol,
    )

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


def format_date(date):
    print_date = (
            date.strftime("%d")
            + " "
            + print_month_ru(date.strftime("%m"))
            + " "
            + date.strftime("%Y")
            + " г."
    )
    return print_date

def get_choice_value(choices, choice_key):
    for choice in choices:
        if choice[0] == choice_key:
            return choice[1]


def get_participant_photo_path(instance, filename):
    base_dir = "photo"

    user_dir = create_name_participant_path(instance.participant)
    check_media_directory_exist(base_dir, user_dir)

    return "{0}/{1}/{2}".format(base_dir, user_dir, filename)


def get_report_image_path(instance, filename):
    base_dir = "reports"

    user_dir = create_name_participant_path(instance.participant)
    check_media_directory_exist(base_dir, user_dir)

    return "{0}/{1}/{2}".format(base_dir, user_dir, filename)


def print_month_ru(month):
    dict_months = {
        "01": "января",
        "02": "февраля",
        "03": "марта",
        "04": "апреля",
        "05": "мая",
        "06": "июня",
        "07": "июля",
        "08": "августа",
        "09": "сентября",
        "10": "октября",
        "11": "ноября",
        "12": "декабря",
    }
    return dict_months.get(month)


def text_from_screenshot(image_url, scale, thresh):
    img_grey = cv2.imread(
        image_url,
        cv2.IMREAD_GRAYSCALE,
    )
    # morph_kernel = np.ones((3, 3))
    # img_grey = cv2.erode(img_grey, kernel=morph_kernel, iterations=1)
    # sharp_filter = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    # img_grey = cv2.filter2D(img_grey, ddepth=-1, kernel=sharp_filter)
    img_grey = cv2.resize(img_grey, None, fx=scale, fy=scale)
    img_binary = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)[1]
    config = "--psm 6 -c tessedit_char_whitelist=0123456789"
    text = pytesseract.image_to_string(
        img_binary,
        lang="eng",
        config=config,
    )
    return re.sub("[^0-9]", "", text)


def checking(arr, val, photo, steps):
    # image_url = str(photo.temporary_file_path())
    image_url = "/home/sites/karathon/media/" + photo
    max_thresh = 200
    delta_thresh = 10
    value = val
    result = []
    if len(arr) == 1:
        result.append(
            str(steps) in text_from_screenshot(image_url, arr[0], value)
        )
        result.append(text_from_screenshot(image_url, arr[0], value))
        return result
    while value <= max_thresh:
        if str(steps) in text_from_screenshot(image_url, arr[0], value):
            result.append(
                [
                    True,
                    arr[0],
                    value,
                    text_from_screenshot(image_url, arr[0], value),
                ]
            )
            return result
        value += delta_thresh
    return checking(arr[1::], val, photo, steps)

def send_email_message(subject, message, to_email):
    send_result = send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [to_email],
        fail_silently=False,
    )

    if send_result == 1:
        return True
    else:
        return False
