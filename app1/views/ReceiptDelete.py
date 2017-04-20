from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic.edit import DeleteView
from app1.models import Receipt
from django.core.exceptions import ObjectDoesNotExist
from app1.utils.general import s3_delete_object


class ReceiptDelete(LoginRequiredMixin, DeleteView):
    model = Receipt
    success_url = reverse_lazy('receipts')
    template_name = "app1/receipt_confirm_delete.html"

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = reverse_lazy('receipts')
            return HttpResponseRedirect(url)
        else:
            print(request)
            print(kwargs)
            print("primary key is: ")
            print(kwargs['pk'])
            primary_key = kwargs['pk']

            try:
                one_receipt = Receipt.objects.get(pk=primary_key)
            except ObjectDoesNotExist:
                one_receipt = None

            if one_receipt:
                s3_object_key = one_receipt.filename
                print(
                    "filename inside ReceiptDelete.py is: " +
                    s3_object_key
                )
                if s3_object_key != "":
                    s3_delete_object(s3_object_key)

            return super(ReceiptDelete, self).post(
                request, *args, **kwargs)

