from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from app1.models import (
    AccessPoint,
    MaxNumAccessPoint
)


class AccessPointList(LoginRequiredMixin, ListView):
    model = AccessPoint
    fields = ['user', 'name', 'purpose', 'creationDT', 'modificationDT']

    def get_queryset(self):
        uid = self.request.user.id
        temp_variable = AccessPoint.objects.filter(
            user_id=uid).order_by(
            "-modificationDT", "name")
        return temp_variable

    def get_context_data(self, **kwargs):
        context = super(AccessPointList, self).get_context_data(**kwargs)

        # item = AccessPoint.objects.all().values(
        #     "user_id").annotate(
        #     total=Count("user_id")).order_by("-total")
        # context['max_num_ap'] = item[0].get("total")


        item = MaxNumAccessPoint.objects.all().order_by("-gen_date_time")
        context['max_num_ap'] = item[0].max_num_ap



        uid = self.request.user.id
        temp_variable = AccessPoint.objects.filter(
            user_id=uid)
        context['your_own_num_ap'] = temp_variable.count()

        return context
