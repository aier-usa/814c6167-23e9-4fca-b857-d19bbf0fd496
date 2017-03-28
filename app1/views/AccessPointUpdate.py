from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from app1.models import AccessPoint
from app1.forms.AccessPointUpdateForm \
    import AccessPointUpdateForm


class AccessPointUpdate(LoginRequiredMixin, UpdateView):
    model = AccessPoint
    form_class = AccessPointUpdateForm

    template_name = "app1/accesspoint_update.html"

    def get_context_data(self, **kwargs):
        context = super(AccessPointUpdate, self).\
            get_context_data(**kwargs)

        # The following line of code is crucial. pk refers to the
        # primary key of the password model.
        accesspoint_id = self.kwargs['pk']
        item = AccessPoint.objects.get(pk=accesspoint_id)
        context['item'] = item
        return context