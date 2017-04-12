from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from app1.models import Receipt
from app1.forms.ReceiptCreationForm \
    import ReceiptCreationForm

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import os

from botocore.client import Config
import boto3

from urllib.request import urlopen



class ReceiptCreate(LoginRequiredMixin, CreateView):
    model = Receipt
    form_class = ReceiptCreationForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ReceiptCreate, self).form_valid(form)

    def post(self, request, *args, **kwargs):

        form_class = self.get_form_class()
        form = ReceiptCreationForm(request.POST, request.FILES)
        print('form is: ')
        print(form)
        print('value of form.is_valid() is: ')
        print(form.is_valid())
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
                user_id=id)

            files = request.FILES['file']
            for f in files:
                print(f)

            print("checkpoint 2")
            file_instance.save()

            print("File name is: ")
            #print(request.FILES['files'][0])
            self.s3_put_object('filename1.jpg')

            print("checkpoint 3")

            return HttpResponseRedirect(reverse('receipts'))
        else:
            return self.form_invalid(form)

    def s3_put_object(self, name):

        print("Filename inside s2_put_object is: ")
        print(name)
        # other choices for signature_version: s3v4, v4, AWS4-HMAC-SHA256,
        s3 = boto3.resource(
            's3',
            #aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
            aws_access_key_id="AKIAJISDRHQNH3AWMANA",
            #aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
            aws_secret_access_key="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",
            config=Config(
                signature_version='s3v4')
        )
        # Print out bucket names
        for bucket in s3.buckets.all():
            print(bucket.name)
        webf = urlopen(
            'https://upload.wikimedia.org/wikipedia/en/0/07/ByzantinePurple_test.jpg')
        txt = webf.read()
        s3.Bucket('aierusa').put_object(
            ACL='public-read',
            Key='ByzantinePurple_test.jpg',
            Body=txt)