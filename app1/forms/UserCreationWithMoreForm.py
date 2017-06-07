from django import forms
from django.contrib.auth.forms import (
    UserCreationForm)

from django.contrib.auth.models import User

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


