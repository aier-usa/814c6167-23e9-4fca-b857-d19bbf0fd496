from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from app1.models import Receipt


class ReceiptDetail(LoginRequiredMixin, DetailView):
    model = Receipt
    fields = ['name', 'store_name', 'creation_DT',
              'modification_DT']
