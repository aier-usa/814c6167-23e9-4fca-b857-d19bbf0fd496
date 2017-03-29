from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic.edit import DeleteView
from app1.models import Receipt


class ReceiptDelete(LoginRequiredMixin, DeleteView):
    model = Receipt
    success_url = reverse_lazy('receipts')
    template_name = "app1/password_confirm_delete.html"

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = reverse_lazy('receipts')
            return HttpResponseRedirect(url)
        else:
            return super(ReceiptDelete, self).post(
                request, *args, **kwargs)

