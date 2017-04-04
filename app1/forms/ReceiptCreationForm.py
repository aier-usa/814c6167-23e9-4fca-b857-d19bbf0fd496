from django.core.files.storage import FileSystemStorage
from django import forms
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from app1.models import Receipt
from django.db import models
fs = FileSystemStorage(location='media/photos')


class ReceiptCreationForm(forms.ModelForm):
    #name = forms.CharField(max_length=255, blank=True)
    #store_name = forms.CharField(max_length=255, blank=True)

    #amount = forms.DecimalField(max_digits=10, decimal_places=2, blank=True)

    #docfile = forms.FileField(
    #    label='Select a file',
    #    help_text='max. 42 megabytes'
    #)
    #comment = forms.CharField(max_length=200, blank=True)

    #creation_DT = forms.DateTimeField(null=True, blank=True)

    class Meta:
        model = Receipt
        fields = ("name", "store_name", "amount", "docfile",
                  "comment", "creation_DT", "modification_DT")
        labels = {
            'creation_DT': 'Created On',
            'modification_DT': 'Modified On',
        }
        help_texts = {
            'name':
                'Name given to the receipt',
            'store_name':
                'Name of the eyecare store',
            'amount':
                'Dollar amount spent for the item',
            'creation_DT':
                'Creation Date/Time. Format: YYYY-MM-DD [HH:MM:SS]',
            'modification_DT':
                'Modification Date/Time. Format: YYYY-MM-DD [HH:MM:SS]',
            'photo':
                'Thumbnail Picture',
        }
        error_messages = {
            'creation_DT': {
                'wrong_format':
                    "Wrong format. Correct one: YYYY-MM-DD [HH:MM:SS]",
            },
            'modification_DT': {
                'wrong_format':
                    "Wrong format. Correct one: YYYY-MM-DD [HH:MM:SS]",
            },
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if "," in name:
            raise ValidationError("Punctuation mark comma (,) is not allowed.")
        return name

    def clean_store_name(self):
        store_name = self.cleaned_data['store_name']
        if "," in store_name:
            raise ValidationError("Punctuation mark comma (,) is not allowed.")
        return store_name

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        return amount

    def clean_creation_DT(self):
        creation_DT = self.cleaned_data['creation_DT']
        return creation_DT

    def clean_modification_DT(self):
        modification_DT = self.cleaned_data['modification_DT']
        return modification_DT

    def clean_comment(self):
        comment = self.cleaned_data['comment']
        if "," in comment:
            raise ValidationError("Punctuation mark comma (,) is not allowed.")
        return comment

    def clean(self):
        cleaned_data = \
            super(ReceiptCreationForm, self).clean()

        temp_name = cleaned_data.get("name")
        cleaned_name = "" if (temp_name is None) else temp_name

        temp_username = cleaned_data.get("username")
        cleaned_username = "" if (temp_username is None) else temp_username

        temp_password = cleaned_data.get("password")
        cleaned_password = "" if (temp_password is None) else temp_password

        if len(cleaned_name) == 0 and \
            len(cleaned_username) == 0 and \
            len(cleaned_password) == 0:
            raise ValidationError(
                _('Invalid combo. ' +\
                'One of them must have value:'+\
                'name, username and password'),
                code='Invalid combo. ' + \
                'One of them must have value:'+\
                'name, username and password')

