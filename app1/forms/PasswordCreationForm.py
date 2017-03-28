from django import forms
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from app1.models import Password


class PasswordCreationForm(forms.ModelForm):
    class Meta:
        model = Password
        fields = ("website", "username", "password",
                  "creationDT", "modificationDT",
                  "email", "security_questions", "comment")
        labels = {
            'creationDT': 'Created On',
            'modificationDT': 'Modified On',
        }
        help_texts = {
            'website':
                'Website name or computer name or organization name',
            'username':
                'Username or email or phone number',
            'password':
                'Password hint works perfect. Full honesty optional',
            'creationDT':
                'Creation Date/Time. Format: YYYY-MM-DD [HH:MM:SS]',
            'modificationDT':
                'Modification Date/Time. Format: YYYY-MM-DD [HH:MM:SS]',
            'comment':
                'Any comments are welcome',
        }
        error_messages = {
            'creationDT': {
                'wrong_format':
                    "Wrong format. Correct one: YYYY-MM-DD [HH:MM:SS]",
            },
            'modificationDT': {
                'wrong_format':
                    "Wrong format. Correct one: YYYY-MM-DD [HH:MM:SS]",
            },
        }

    def clean_website(self):
        website = self.cleaned_data['website']
        if "," in website:
            raise ValidationError("Punctuation mark comma (,) is not allowed.")
        return website

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

    def clean(self):
        cleaned_data = \
            super(PasswordCreationForm, self).clean()

        temp_website = cleaned_data.get("website")
        cleaned_website = "" if (temp_website is None) else temp_website

        temp_username = cleaned_data.get("username")
        cleaned_username = "" if (temp_username is None) else temp_username

        temp_password = cleaned_data.get("password")
        cleaned_password = "" if (temp_password is None) else temp_password

        if len(cleaned_website) == 0 and \
            len(cleaned_username) == 0 and \
            len(cleaned_password) == 0:
            raise ValidationError(
                _('Invalid combo. ' +\
                'One of them must have value:'+\
                'website, username and password'),
                code='Invalid combo. ' + \
                'One of them must have value:'+\
                'website, username and password')

