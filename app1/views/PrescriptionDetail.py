from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from app1.models import Prescription


class PrescriptionDetail(LoginRequiredMixin, DetailView):
    model = Prescription
    fields = ['name', 'store_name', 'amount', 'comment', 'creation_DT',
              'modification_DT']
