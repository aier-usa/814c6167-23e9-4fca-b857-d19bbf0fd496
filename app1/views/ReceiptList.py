from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from app1.models import (
    Receipt,
    MaxNumReceipt)


class ReceiptList(LoginRequiredMixin, ListView):
    model = Receipt
    fields = ['id', 'name', 'store_name', 'amount', 'creation_DT',
              'modification_DT', 'filename', 'file_url']

    def get_queryset(self):
        uid = self.request.user.id
        temp_variable = Receipt.objects.filter(
            user_id=uid).order_by(
            "-modification_DT", "-id")
        for t in temp_variable:
            double_dash = t.filename.rfind('--')
            starting_pos = 11
            t.short_filename = \
                t.filename[starting_pos:double_dash]
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

        total_receipt_amount = \
            temp_variable.aggregate(sum=Sum('amount'))['sum']
        context['total_receipt_amount'] = total_receipt_amount

        total_credit = 0.00
        if total_receipt_amount >= 3000.00:
            total_credit = 3000.00
        else:
            total_credit = total_receipt_amount

        context['total_credit'] = total_credit



        return context
