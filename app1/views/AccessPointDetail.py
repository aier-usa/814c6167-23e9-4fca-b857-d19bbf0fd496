from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from app1.models import AccessPoint


class AccessPointDetail(LoginRequiredMixin, DetailView):
    model = AccessPoint
    fields = ['user', 'name', 'purpose', 'creationDT', 'modificationDT']

