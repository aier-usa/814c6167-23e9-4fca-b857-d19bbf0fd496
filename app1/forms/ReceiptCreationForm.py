from django import forms
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from app1.models import Receipt
from decimal import Decimal

class ReceiptCreationForm(forms.ModelForm):

    class Meta:
        model = Receipt
        fields = ("name", "store_name", "amount", "filename",
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

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        try:
            x = Decimal(amount)
        except ValueError:
                raise ValidationError("Amount field is not valid. Try again.")
        return x

    def clean(self):
        cleaned_data = \
            super(ReceiptCreationForm, self).clean()

        temp_name = cleaned_data.get("name")
        cleaned_name = "" if (temp_name is None) else temp_name

        if len(cleaned_name) == 0:
            raise ValidationError(
                _('Name cannot be empty'),
                code='Name cannot be empty')

