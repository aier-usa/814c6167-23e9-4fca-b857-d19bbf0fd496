from django.db.models import Count
from datetime import datetime


from app1.models import (
    Password,
    AccessPoint,
    MaxNumAccessPoint,
    MaxNumPassword)


def create_max_pwd_ap():
    pwd_item = Password.objects.all().values(
        "user_id").annotate(
        total=Count("user_id")).order_by("-total")
    number_pwd = pwd_item[0].get("total")
    max_num_pwd_obj = MaxNumPassword(
        max_num_pwd=number_pwd, gen_date_time= datetime.now())
    max_num_pwd_obj.save()

    ap_item = AccessPoint.objects.all().values(
        "user_id").annotate(
        total=Count("user_id")).order_by("-total")
    number_ap = ap_item[0].get("total")
    max_num_ap_obj = MaxNumAccessPoint(
        max_num_ap=number_ap, gen_date_time= datetime.now())
    max_num_ap_obj.save()

