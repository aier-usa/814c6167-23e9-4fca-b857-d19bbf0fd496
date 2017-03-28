from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from app1.models import Password
from app1.forms.PasswordCreationForm \
    import PasswordCreationForm


class PasswordCreate(LoginRequiredMixin, CreateView):
    model = Password
    form_class = PasswordCreationForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PasswordCreate, self).form_valid(form)

