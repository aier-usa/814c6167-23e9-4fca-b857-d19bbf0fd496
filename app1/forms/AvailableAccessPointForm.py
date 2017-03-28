from django import forms


class AvailableAccessPointForm(forms.Form):
    any_field = forms.CharField()

