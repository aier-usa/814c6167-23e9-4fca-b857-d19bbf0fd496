from django import forms


class CustomUserChangeForm(forms.Form):
    username = forms.CharField(
        required=True,
        max_length=255,
        min_length=1
    )

    first_name = forms.CharField(
        required=True,
        max_length=255,
        min_length=1
    )

    last_name = forms.CharField(
        required=True,
        max_length=255,
        min_length=1
    )

    email = forms.EmailField(
        required=True,
        max_length=255,
        min_length=1
    )

    street = forms.CharField(
        required=True,
        max_length=255,
        min_length=1
    )

    city = forms.CharField(
        required=True,
        max_length=255,
        min_length=1
    )

    state = forms.CharField(
        required=True,
        max_length=255,
        min_length=1
    )

    zip = forms.CharField(
        required=True,
        max_length=255,
        min_length=1
    )

    country = forms.CharField(
        required=True,
        max_length=255,
        min_length=1
    )

    cell_phone = forms.CharField(
        required=True,
        max_length=255,
        min_length=1
    )

    home_phone = forms.CharField(
        required=True,
        max_length=255,
        min_length=1
    )

    work_phone = forms.CharField(
        required=True,
        max_length=255,
        min_length=1
    )
