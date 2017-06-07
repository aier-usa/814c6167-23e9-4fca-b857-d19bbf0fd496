from django import forms
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from app1.models import Prescription
from decimal import Decimal

class PrescriptionCreationForm(forms.ModelForm):

    class Meta:
        model = Prescription
        fields = ("name",
                  "doctor_name",
                  "filename",
                  "left_eye_sphere",
                  "left_eye_cylinder",
                  "left_eye_axis",
                  "right_eye_sphere",
                  "right_eye_cylinder",
                  "right_eye_axis",
                  "comment",
                  "creation_DT",
                  "modification_DT")
        labels = {
            'creation_DT': 'Created On',
            'modification_DT': 'Modified On',
        }
        help_texts = {
            'name':
                'Name given to the Prescription',
            'store_name':
                'Name of the eyecare store',
            'amount':
                'Dollar amount spent for the item',
            'creation_DT':
                'Creation Date/Time. Format: YYYY-MM-DD [HH:MM:SS]',
            'modification_DT':
                'Modification Date/Time. Format: YYYY-MM-DD [HH:MM:SS]',
            'photo':
                'Thumbnail Picture',
        }
        error_messages = {
            'creation_DT': {
                'wrong_format':
                    "Wrong format. Correct one: YYYY-MM-DD [HH:MM:SS]",
            },
            'modification_DT': {
                'wrong_format':
                    "Wrong format. Correct one: YYYY-MM-DD [HH:MM:SS]",
            },
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if "," in name:
            raise ValidationError("Punctuation mark comma (,) is not allowed.")
        return name

    def clean_store_name(self):
        store_name = self.cleaned_data['store_name']
        if "," in store_name:
            raise ValidationError("Punctuation mark comma (,) is not allowed.")
        return store_name


    def clean_left_eye_sphere(self):
        left_eye_sphere = self.cleaned_data['left_eye_sphere']
        return left_eye_sphere

    def clean_left_eye_cylinder(self):
        left_eye_cylinder = self.cleaned_data['left_eye_cylinder']
        return left_eye_cylinder

    def clean_left_eye_axis(self):
        left_eye_axis = self.cleaned_data['left_eye_axis']
        return left_eye_axis

    def clean_right_eye_sphere(self):
        right_eye_sphere = self.cleaned_data['right_eye_sphere']
        return right_eye_sphere

    def clean_right_eye_cylinder(self):
        right_eye_cylinder = self.cleaned_data['right_eye_cylinder']
        return right_eye_cylinder

    def clean_right_eye_axis(self):
        right_eye_axis = self.cleaned_data['right_eye_axis']
        return right_eye_axis

    def clean_creation_DT(self):
        creation_DT = self.cleaned_data['creation_DT']
        return creation_DT

    def clean_modification_DT(self):
        modification_DT = self.cleaned_data['modification_DT']
        return modification_DT

    def clean_comment(self):
        comment = self.cleaned_data['comment']
        if "," in comment:
            raise ValidationError("Punctuation mark comma (,) is not allowed.")
        return comment

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        try:
            x = Decimal(amount)
        except ValueError:
                raise ValidationError("Amount field is not valid. Try again.")
        return x

    def clean(self):
        cleaned_data = \
            super(PrescriptionCreationForm, self).clean()

        temp_name = cleaned_data.get("name")
        cleaned_name = "" if (temp_name is None) else temp_name

        if len(cleaned_name) == 0:
            raise ValidationError(
                _('Name cannot be empty'),
                code='Name cannot be empty')

