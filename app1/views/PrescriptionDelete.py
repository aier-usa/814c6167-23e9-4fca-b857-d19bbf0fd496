from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic.edit import DeleteView
from app1.models import Prescription
from django.core.exceptions import ObjectDoesNotExist
from app1.utils.general import s3_delete_object


class PrescriptionDelete(LoginRequiredMixin, DeleteView):
    model = Prescription
    success_url = reverse_lazy('Prescriptions')
    template_name = "app1/Prescription_confirm_delete.html"

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = reverse_lazy('Prescriptions')
            return HttpResponseRedirect(url)
        else:
            print(request)
            print(kwargs)
            print("primary key is: ")
            print(kwargs['pk'])
            primary_key = kwargs['pk']

            try:
                one_Prescription = Prescription.objects.get(pk=primary_key)
            except ObjectDoesNotExist:
                one_Prescription = None

            if one_Prescription:
                s3_object_key = one_Prescription.filename
                print(
                    "filename inside PrescriptionDelete.py is: " +
                    s3_object_key
                )
                if s3_object_key != "":
                    s3_delete_object(s3_object_key)

            return super(PrescriptionDelete, self).post(
                request, *args, **kwargs)

