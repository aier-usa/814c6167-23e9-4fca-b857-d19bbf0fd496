from django import forms


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