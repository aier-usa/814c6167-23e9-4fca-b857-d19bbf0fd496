from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from app1.models import Receipt
from app1.forms.ReceiptCreationForm \
    import ReceiptCreationForm

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import os
import uuid

from botocore.client import Config
import boto3


class ReceiptCreate(LoginRequiredMixin, CreateView):
    model = Receipt
    form_class = ReceiptCreationForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ReceiptCreate, self).form_valid(form)

    def post(self, request, *args, **kwargs):

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

            files = request.FILES['file']
            two_parts = os.path.splitext(files.name)
            base_file_name = two_parts[0]
            file_extension = two_parts[1]

            print(base_file_name)
            print(file_extension)

            uuid4 = str(uuid.uuid4())
            content = files.read()


            long_name = base_file_name + \
                '-' + uuid4 + file_extension

            print("generated long file name is: "
                  + long_name)

            self.s3_put_object(long_name, content)

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

    def s3_put_object(self, name, content):

        print("Filename inside s2_put_object is: ")
        print(name)
        # other choices for signature_version: s3v4, v4, AWS4-HMAC-SHA256,
        s3_signature_version = os.environ['S3_SIGNATURE_VERSION']
        s3 = boto3.resource(
            's3',
            aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
            config=Config(
                signature_version=s3_signature_version)
        )
        bucket_name = os.environ['S3_BUCKET_NAME']
        s3.Bucket(bucket_name).put_object(
            ACL='public-read',
            Key=name,
            Body=content)