from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from app1.models import (
    Password,
    MaxNumAccessPoint,
    MaxNumPassword
)

class PasswordList(LoginRequiredMixin, ListView):
    model = Password
    fields = ['website', 'username', 'password', 'creationDT',
              'modificationDT', 'comment']

    def get_queryset(self):
        uid = self.request.user.id
        temp_variable = Password.objects.filter(
            user_id=uid).order_by(
            "-modificationDT", "website")

        return temp_variable

    def get_context_data(self, **kwargs):
        context = super(PasswordList, self).get_context_data(**kwargs)

        # item = Password.objects.all().values(
        #     "user_id").annotate(
        #     total=Count("user_id")).order_by("-total")
        # context['max_num_pwd'] = item[0].get("total")
        item = MaxNumPassword.objects.all().order_by("-gen_date_time")
        context['max_num_pwd'] = item[0].max_num_pwd

        uid = self.request.user.id
        temp_variable = Password.objects.filter(
            user_id=uid)
        context['your_own_num_pwd'] = temp_variable.count()

        return context
