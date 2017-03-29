from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from app1.models import Receipt
from app1.forms.ReceiptUpdateForm \
    import ReceiptUpdateForm


class ReceiptUpdate(LoginRequiredMixin, UpdateView):
    model = Receipt
    form_class = ReceiptUpdateForm

    template_name = "app1/receipt_update.html"

    def get_context_data(self, **kwargs):
        context = super(
            ReceiptUpdate, self
        ).get_context_data(**kwargs)

        # The following line of code is crucial. pk refers to the
        # primary key of the password model.
        password_id = self.kwargs['pk']
        item = Receipt.objects.get(pk=password_id)

        context['item'] = item

        return context
