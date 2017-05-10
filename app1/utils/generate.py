from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
from datetime import datetime


from app1.models import (
    Receipt,
    MaxNumReceipt)


def gen_daily_all_data():
    # the format is: 2017-01-01 34
    #                2017-03-21 40
    raw_data=[]

    date_map = {}

    for u in User.objects.all():
        date_j = u.date_joined
        only_date = date_j.date().strftime('%Y-%m-%d')

        if only_date not in date_map:
            date_map[only_date] = 1
        else:
            date_map[only_date] += 1

    for key, value in date_map.items():
        raw_data.append({'date': key, 'number': value})

    returned_data = sorted(raw_data, key=lambda k: k['date'], reverse=True)
    return returned_data


def create_max_receipt():
    receipt_item = Receipt.objects.all().values(
        "user_id").annotate(
        total=Count("user_id")).order_by("-total")

    number_receipt = 0
    if receipt_item.exists():
        number_receipt = receipt_item[0].get("total")

    max_num_receipt_obj = MaxNumReceipt(
        max_num_receipt=number_receipt, gen_date_time= datetime.now())
    max_num_receipt_obj.save()


def get_selected_users(a_date):
    users = User.objects.filter(date_joined__startswith=a_date)
    return users
