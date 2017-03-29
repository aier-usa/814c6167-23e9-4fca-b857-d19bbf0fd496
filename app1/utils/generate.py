from django.db.models import Count
from datetime import datetime


from app1.models import (
    Receipt,
    MaxNumReceipt)


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


