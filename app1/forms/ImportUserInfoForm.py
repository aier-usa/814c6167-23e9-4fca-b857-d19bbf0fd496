from django import forms


class ImportUserInfoForm(forms.Form):
    all_info = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={'rows': 10,
                   'cols': 80,
                   'placeholder':
                       "Export your own information at first, " +
                       "then add new data following the format." +
                       "Do NOT delete special delimiters."
                   }
        )
    )

