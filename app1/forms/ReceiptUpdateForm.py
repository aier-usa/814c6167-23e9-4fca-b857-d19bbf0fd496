from django import forms
from django.core.exceptions import ValidationError
from app1.models import Receipt


class ReceiptUpdateForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = (
            "name", "store_name", "amount",
            "creation_DT", "modification_DT",
            "comment"
        )
        labels = {
            'creation_DT': 'Created On',
            'modification_DT': 'Modified On',
        }
        help_texts = {
            'name':
                'Memorable name given to the receipt',
            'store_name':
                'name of the store that sold the item to you',
            'creation_DT':
                'Creation Date/Time. Format: YYYY-MM-DD HH:MM:SS',
            'modification_DT':
                'Modification Date/Time. Format: YYYY-MM-DD HH:MM:SS',
        }
        error_messages = {
            'creation_DT': {
                'wrong_format':
                    "Wrong format. Correct one: YYYY-MM-DD HH:MM:SS",
            },
            'modification_DT': {
                'wrong_format':
                    "Wrong format. Correct one: YYYY-MM-DD HH:MM:SS",
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

    def clean_comment(self):
        comment = self.cleaned_data['comment']
        if "," in comment:
            raise ValidationError("Punctuation mark comma (,) is not allowed.")
        return comment

    def clean(self):
        cleaned_data = \
            super(ReceiptUpdateForm, self).clean()