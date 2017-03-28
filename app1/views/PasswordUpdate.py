from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from app1.models import Password
from app1.forms.PasswordUpdateForm \
    import PasswordUpdateForm


class PasswordUpdate(LoginRequiredMixin, UpdateView):
    model = Password
    form_class = PasswordUpdateForm

    template_name = "app1/password_update.html"

    def get_context_data(self, **kwargs):
        context = super(
            PasswordUpdate, self
        ).get_context_data(**kwargs)

        # The following line of code is crucial. pk refers to the
        # primary key of the password model.
        password_id = self.kwargs['pk']
        item = Password.objects.get(pk=password_id)

        context['item'] = item

        return context
