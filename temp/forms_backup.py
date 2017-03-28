from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.forms import (
    UserChangeForm,
    UserCreationForm,
    AuthenticationForm,
    ReadOnlyPasswordHashField)

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from app1.models import Password, AccessPoint

from app1.utils.validation_functions import first_letter_than_alphanumeric

class UserCreationWithMoreForm(UserCreationForm):
    email = forms.EmailField(
        required=True, help_text="Required. A valid email address")
    first_name = forms.CharField(
        max_length=30, required=False, help_text="Optional. Max # of characters: 30")
    last_name = forms.CharField(
        max_length=30, required=False, help_text="Optional. Max # of characters: 30")

    class Meta:
        model = User
        fields = ("username", "email",
                  "first_name", "last_name",
                  "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "ERROR: Email already exists")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "ERROR: Username already exists")
        return username

    def save(self, commit=True):
        user = super(
            UserCreationWithMoreForm, self).save(
            commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        if commit:
            user.save()
        return user


class AvailableAccessPointForm(forms.Form):
    any_field = forms.CharField()


class PasswordUpdateForm(forms.ModelForm):
    class Meta:
        model = Password
        fields = ("website", "username", "password",
                  "creationDT", "modificationDT", "comment")
        labels = {
            'creationDT': 'Created On',
            'modificationDT': 'Modified On',
        }
        help_texts = {
            'website':
                'Website name or computer name',
            'username':
                'Username or email address or phone number',
            'password':
                'Password hint works perfect. Full honesty optional',
            'creationDT':
                'Creation Date/Time. Format: YYYY-MM-DD HH:MM:SS',
            'modificationDT':
                'Modification Date/Time. Format: YYYY-MM-DD HH:MM:SS',
            'comment':
                'Any comments are welcome',
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
            super(PasswordUpdateForm, self).clean()

        cleaned_website = cleaned_data.get("website")
        cleaned_username = cleaned_data.get("username")
        cleaned_password = cleaned_data.get("password")

        if len(cleaned_website) == 0 and \
                        len(cleaned_username) == 0 and \
                        len(cleaned_password) == 0:
            raise ValidationError(
                _('Invalid combinations. ' + \
                  'At least one of them must have value:' + \
                  'website, username and password'),
                code='Invalid combinations. ' + \
                     'At least one of them must have value:' + \
                     'website, username and password')


class PasswordCreationForm(forms.ModelForm):
    class Meta:
        model = Password
        fields = ("website", "username", "password",
                  "creationDT", "modificationDT", "comment")
        labels = {
            'creationDT': 'Created On',
            'modificationDT': 'Modified On',
        }
        help_texts = {
            'website':
                'Website name or computer name or orgnization name',
            'username':
                'Username or email or phone number',
            'password':
                'Password hint works perfect. Full honesty optional',
            'creationDT':
                'Creation Date/Time. Format: YYYY-MM-DD HH:MM:SS',
            'modificationDT':
                'Modification Date/Time. Format: YYYY-MM-DD HH:MM:SS',
            'comment':
                'Any comments are welcome',
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

        cleaned_website = cleaned_data.get("website")
        cleaned_username = cleaned_data.get("username")
        cleaned_password = cleaned_data.get("password")

        if len(cleaned_website) == 0 and \
            len(cleaned_username) == 0 and \
            len(cleaned_password) == 0:
            raise ValidationError(
                _('Invalid combinations. ' +\
                'At least one of them must have value:'+\
                'website, username and password'),
                code='Invalid combinations. ' + \
                'At least one of them must have value:'+\
                'website, username and password')


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

class AccessPointCreationForm(forms.ModelForm):
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
                'Stated purpose. Examples: for kids, for colleagues, public access',
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
        if AccessPoint.objects.filter(
                name=name).exists():
            raise forms.ValidationError(
                "ERROR: AccessPoint name already exists")
        if "," in name:
            raise ValidationError("Punctuation mark comma (,) is not allowed.")
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


class PasswordResetRequestForm(forms.Form):
    email_or_username = forms.CharField(
            label="Email Or Username", max_length=254)


class ImportUserInfoForm(forms.Form):
    all_info = forms.CharField(
        required=True, widget=forms.Textarea(
            attrs={'rows': 10, 'cols': 80}))


class CustomUserChangeForm(forms.Form):
    username = forms.CharField(required=True,
                               max_length=255,
                               min_length=1,)
    first_name = forms.CharField(required=True,
                                 max_length=255,
                                 min_length=1,)
    last_name = forms.CharField(required=True,
                                max_length=255,
                                min_length=1)
    email = forms.EmailField(required=True,
                             max_length=255,
                             min_length=1)


class UserProfileForm(UserChangeForm):
    '''
    password = ReadOnlyPasswordHashField(label="Password",
        help_text="Raw passwords are not stored, " +
                  "so there is no way to view " +
                    "this user's password, " +
                  "but you can change the password " +
                    "using Change Password ONLY function.")
    '''

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        exclude = ('password',)


