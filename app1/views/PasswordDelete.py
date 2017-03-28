from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic.edit import DeleteView
from app1.models import Password


class PasswordDelete(LoginRequiredMixin, DeleteView):
    model = Password
    success_url = reverse_lazy('password_list')
    template_name = "app1/password_confirm_delete.html"

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = reverse_lazy('password_list')
            return HttpResponseRedirect(url)
        else:
            return super(PasswordDelete, self).post(
                request, *args, **kwargs)

