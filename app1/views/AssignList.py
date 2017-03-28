from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.contrib.auth.models import User

from app1.models import (
    AccessPoint, PasswordTrustedPartner)

from app1.utils.validation_functions import(
    is_pwd_id_and_ap_id_used)


class AssignList(LoginRequiredMixin, ListView):
    model = AccessPoint
    fields = ['user', 'name', 'purpose', 'creationDT']
    template_name = "app1/assign_list.html"

    def get_queryset(self):
        uid = self.request.user.id
        return AccessPoint.objects.filter(
            user_id=uid)

    def get_context_data(self, **kwargs):
        context = super(AssignList, self).get_context_data(**kwargs)

        # The following line of code is crucial. pk refers to the
        # primary key of the password model.
        password_id = self.kwargs['pk']
        context['password_id'] = password_id

        uid = self.request.user.id
        keys = AccessPoint.objects.filter(
            user_id=uid).values_list('id', flat=True)
        another_set = []
        for key1 in keys:
            if is_pwd_id_and_ap_id_used(password_id, key1):
                another_set.append(key1)
        context['used_ap_ids'] = another_set

        used_tp_user_ids = PasswordTrustedPartner.objects.filter(
            password_id=password_id).values_list(
            'trusted_partner_id', flat=True)
        used_tp_users = []
        for one_id in used_tp_user_ids:
            one_user_obj = User.objects.get(pk=one_id)
            used_tp_users.append(one_user_obj)

        context['used_trusted_partner_users'] \
            = used_tp_users

        return context