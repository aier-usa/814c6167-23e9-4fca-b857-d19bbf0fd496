from app1.forms.PrescriptionUpdateForm \
    import PrescriptionUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView

from app1.models import Prescription


class PrescriptionUpdate(LoginRequiredMixin, UpdateView):
    model = Prescription
    form_class = PrescriptionUpdateForm

    template_name = "app1/Prescription_update.html"

    def get_context_data(self, **kwargs):
        context = super(
            PrescriptionUpdate, self
        ).get_context_data(**kwargs)

        # The following line of code is crucial. pk refers to the
        # primary key of the password model.
        password_id = self.kwargs['pk']
        item = Prescription.objects.get(pk=password_id)

        context['item'] = item

        return context
