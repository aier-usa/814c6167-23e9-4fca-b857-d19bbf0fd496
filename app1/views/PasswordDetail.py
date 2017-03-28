from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from app1.models import Password


class PasswordDetail(LoginRequiredMixin, DetailView):
    model = Password
    fields = ['website', 'username', 'password', 'creationDT',
              'modificationDT', 'comment']
