from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from app1.models import Receipt
from app1.forms.ReceiptCreationForm \
    import ReceiptCreationForm

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

class ReceiptCreate(LoginRequiredMixin, CreateView):
    model = Receipt
    form_class = ReceiptCreationForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ReceiptCreate, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = ReceiptCreationForm(request.POST, request.FILES)
        if form.is_valid():
            a_name = form.cleaned_data['name']
            print(a_name)

            astore_name = form.cleaned_data['store_name']
            print(astore_name)

            an_amount = form.cleaned_data['amount']
            print(an_amount)

            acreation_DT = form.cleaned_data['creation_DT']
            print(acreation_DT)

            amodification_DT = form.cleaned_data['modification_DT']
            print(amodification_DT)

            id = request.user.id

            #print(aname)
            print("checkpoint 1")
            file_instance = Receipt(
                name=a_name,
                amount=an_amount,
                store_name=astore_name,
                creation_DT=acreation_DT,
                modification_DT=amodification_DT,
                user_id=id,
                docfile=request.FILES['docfile'])
            print("checkpoint 2")
            file_instance.save()

            print("checkpoint 3")

            return HttpResponseRedirect(reverse('receipts'))
        else:
            return self.form_invalid(form)