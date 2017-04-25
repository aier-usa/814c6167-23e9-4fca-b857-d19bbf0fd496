from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from app1.models import (
    Prescription)


class PrescriptionList(LoginRequiredMixin, ListView):
    model = Prescription
    fields = ['id',
              'name',
              'creation_DT',
              'left_eye_cylinder',
              'left_eye_sphere',
              'modification_DT',
              'filename',
              'file_url']

    def get_queryset(self):
        uid = self.request.user.id
        temp_variable = Prescription.objects.filter(
            user_id=uid).order_by(
            "-modification_DT", "-id")
        for t in temp_variable:
            double_dash = t.filename.rfind('--')
            starting_pos = 11
            t.short_filename = \
                t.filename[starting_pos:double_dash]
        return temp_variable

    def get_context_data(self, **kwargs):
        context = super(PrescriptionList, self).get_context_data(**kwargs)

        return context
