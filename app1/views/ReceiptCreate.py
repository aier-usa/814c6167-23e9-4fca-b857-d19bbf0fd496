from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from app1.models import Receipt
from app1.forms.ReceiptCreationForm \
    import ReceiptCreationForm

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import os
import uuid
from django.shortcuts import render
from app1.utils.general import s3_put_object


class ReceiptCreate(LoginRequiredMixin, CreateView):
    model = Receipt
    form_class = ReceiptCreationForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ReceiptCreate, self).form_valid(form)

    def post(self, request, *args, **kwargs):

        form = ReceiptCreationForm(request.POST, request.FILES)

        files = request.FILES['file']
        two_parts = os.path.splitext(files.name)

        max_uploaded_file_size = 30*1000*1000

        file_size = files.size
        base_file_name = two_parts[0]
        file_extension = (two_parts[1]).lower()

        print(base_file_name)
        print(file_extension)

        uuid4 = str(uuid.uuid4())
        content = files.read()

        long_name = base_file_name + \
                    '-' + uuid4 + file_extension

        print("generated long file name is: "
              + long_name)


        if file_size > max_uploaded_file_size:
            form.add_error(
                field=None,
                error="File exceeds 30MB. Too big! Reduce size and try again.")
            return render(request, 'app1/receipt_form.html', {'form': form})
            #return self.form_invalid(form)
            #raise form.ValidationError("Your file exceeds 30MB. Too big!")


        if file_extension == ".pdf":
            content_type = "application/pdf"
        elif file_extension == ".jpeg":
            content_type = "image/jpeg"
        elif file_extension == ".jpg":
            content_type = "image/jpg"
        elif file_extension == ".png":
            content_type = "image/png"
        elif file_extension == ".bm":
            content_type = "image/bmp"
        elif file_extension == ".bmp":
            content_type = "image/bmp"
        elif file_extension == ".docx":
            content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        elif file_extension == ".doc":
            content_type = "application/msword"
        else:
            content_type = "NotAcceptable"

        if content_type == "NotAcceptable":
            form.add_error(
                field=None,
                error="File type " +
                      file_extension +
                      " is not acceptable. Try a different file.")
            return render(request, 'app1/receipt_form.html', {'form': form})
            #raise form.ValidationError("Unknown file type!")

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

            s3_put_object(long_name, content, content_type)

            print("checkpoint 3")

            prefix = "https://s3.us-east-2.amazonaws.com/aierusa/"

            file_instance = Receipt(
                name=a_name,
                amount=an_amount,
                store_name=astore_name,
                creation_DT=acreation_DT,
                modification_DT=amodification_DT,
                filename=long_name,
                file_url=prefix + long_name,
                user_id=id)
            file_instance.save()

            return HttpResponseRedirect(reverse('receipts'))
        else:
            return self.form_invalid(form)
