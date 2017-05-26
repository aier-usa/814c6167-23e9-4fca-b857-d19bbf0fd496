from django import forms
from app1.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('cell_phone',
                  'work_phone',
                  'home_phone',
                  'street',
                  'city',
                  'state',
                  'zip',
                  'country')

    def save(self, commit=True):
        profile = super(
            ProfileForm, self).save(
            commit=False)

        profile.cell_phone = self.cleaned_data["cell_phone"]
        profile.work_phone = self.cleaned_data["work_phone"]
        profile.home_phone = self.cleaned_data["home_phone"]
        profile.street = self.cleaned_data["street"]
        profile.city = self.cleaned_data["city"]
        profile.state = self.cleaned_data["state"]
        profile.zip = self.cleaned_data["zip"]
        profile.country = self.cleaned_data["country"]

        profile.user_id = self.user_id
        if commit:
            profile.save()
        return profile