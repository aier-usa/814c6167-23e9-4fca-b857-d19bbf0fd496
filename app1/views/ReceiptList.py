from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from app1.models import (
    Receipt,
    MaxNumReceipt)


class ReceiptList(LoginRequiredMixin, ListView):
    model = Receipt
    fields = ['id', 'name', 'store_name', 'creation_DT',
              'modification_DT', 'photo']

    def get_queryset(self):
        uid = self.request.user.id
        temp_variable = Receipt.objects.filter(
            user_id=uid).order_by(
            "-modification_DT", "name")

        return temp_variable

    def get_context_data(self, **kwargs):
        context = super(ReceiptList, self).get_context_data(**kwargs)

        # item = Password.objects.all().values(
        #     "user_id").annotate(
        #     total=Count("user_id")).order_by("-total")
        # context['max_num_pwd'] = item[0].get("total")
        item = MaxNumReceipt.objects.all().order_by("-gen_date_time")

        if not item.exists():
            context['max_num_receipt'] = 0
        else:
            context['max_num_receipt'] = item[0].max_num_receipt

        uid = self.request.user.id
        temp_variable = Receipt.objects.filter(
            user_id=uid)
        context['your_own_num_receipt'] = temp_variable.count()

        return context
