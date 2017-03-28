from re import search
from app1.models import (
    Password,
    AccessPoint,
    PasswordAccessPoint)


def first_letter_than_alphanumeric(argument1):
    match = search(r'^[a-zA-Z][a-zA-Z0-9]*$', argument1)
    if match:
        return True
    else:
        return False

# print(first_letter_than_alphanumeric('5454fdafafd'))
# print(first_letter_than_alphanumeric('fdaf444'))
# print(first_letter_than_alphanumeric('###ddsadf$$$'))
# print(first_letter_than_alphanumeric('fdfdfd!fdfdf'))
# print(first_letter_than_alphanumeric('fdfdfd111fdfdf'))


def comma_in_the_string(string1):
    if "," in string1:
        return True
    else:
        return False


def are_all_three_empty(argument1, argument2, argument3):
    if (len(argument1) == 0 and
        len(argument2) == 0 and
        len(argument3) == 0):
        return True
    else:
        return False


def is_pwd_id_and_ap_id_used(password_id, ap_id):
    # establish the linkage between password and access_point
    pap = PasswordAccessPoint.objects.filter(
        password_id__exact=password_id).filter(
        access_point_id__exact=ap_id)
    if pap.count() == 0:
        return False
    else:
        return True
