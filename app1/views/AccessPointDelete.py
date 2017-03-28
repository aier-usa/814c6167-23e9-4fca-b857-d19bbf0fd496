from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic.edit import DeleteView
from app1.models import (
    AccessPoint)


class AccessPointDelete(LoginRequiredMixin, DeleteView):
    model = AccessPoint
    success_url = reverse_lazy('access_point_list')
    template_name = "app1/accesspoint_confirm_delete.html"

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = reverse_lazy('access_point_list')
            return HttpResponseRedirect(url)
        else:
            return super(AccessPointDelete, self).post(
                request, *args, **kwargs)

