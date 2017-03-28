from django import forms
from django.core.exceptions import ValidationError
from app1.models import AccessPoint

from app1.utils.validation_functions import (
    first_letter_than_alphanumeric)

class AccessPointUpdateForm(forms.ModelForm):
    class Meta:
        model = AccessPoint
        fields = ("name", "purpose",
                  "creationDT", "modificationDT")
        labels = {
            'creationDT': 'Created On',
            'modificationDT': 'Modified On',
        }
        help_texts = {
            'name':
                'Format: First character must be a letter. Others are alphanumeric',
            'purpose':
                'Stated purpose. Examples: for my kids, for colleagues, public access',
            'creationDT':
                'Creation Date/Time. Format: YYYY-MM-DD HH:MM:SS',
            'modificationDT':
                'Modification Date/Time. Format: YYYY-MM-DD HH:MM:SS',
        }
        error_messages = {
            'creationDT': {
                'wrong_format':
                    "Wrong format. Correct one: YYYY-MM-DD HH:MM:SS",
            },
            'modificationDT': {
                'wrong_format':
                    "Wrong format. Correct one: YYYY-MM-DD HH:MM:SS",
            },
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if "," in name:
            raise ValidationError(
                "Punctuation mark comma (,) is not allowed.")
        if not first_letter_than_alphanumeric(name):
            raise ValidationError(
                "Does not follow the format rule: " +
                "first letter then alphanumeric.")
        return name

    def clean_purpose(self):
        purpose = self.cleaned_data['purpose']
        if "," in purpose:
            raise ValidationError("Punctuation mark comma (,) is not allowed.")
        return purpose
