from django import forms
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from app1.models import Receipt


class ReceiptUpdateForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = (
            "name", "store_name",
            "creation_DT", "modification_DT",
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

    def clean_username(self):
        username = self.cleaned_data['username']
        if "," in username:
            raise ValidationError("Punctuation mark comma (,) is not allowed.")
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if "," in password:
            raise ValidationError("Punctuation mark comma (,) is not allowed.")
        return password

    def clean_comment(self):
        comment = self.cleaned_data['comment']
        if "," in comment:
            raise ValidationError("Punctuation mark comma (,) is not allowed.")
        return comment

    def clean_email(self):
        email = self.cleaned_data['email']
        if "," in email:
            raise ValidationError("Punctuation mark comma (,) is not allowed.")
        return email

    def clean_security_questions(self):
        security_questions = self.cleaned_data['security_questions']
        if "," in security_questions:
            raise ValidationError("Punctuation mark comma (,) is not allowed.")
        return security_questions

    def clean(self):
        cleaned_data = \
            super(ReceiptUpdateForm, self).clean()

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
                'One of them must have value: '+\
                'name, username and password'),
                code='Invalid combo. ' + \
                'One of them must have value: '+\
                'name, username and password')
