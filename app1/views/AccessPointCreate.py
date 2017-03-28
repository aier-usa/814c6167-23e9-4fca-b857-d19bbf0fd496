from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView

from app1.models import (AccessPoint)

from app1.forms.AccessPointCreationForm import (
    AccessPointCreationForm)


# The following is for AccessPoint
class AccessPointCreate(LoginRequiredMixin, CreateView):
    model = AccessPoint
    form_class = AccessPointCreationForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AccessPointCreate, self).form_valid(form)

