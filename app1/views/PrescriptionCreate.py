import os
import uuid
from datetime import datetime

from app1.forms.PrescriptionCreationForm \
    import PrescriptionCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.edit import CreateView

from app1.models import Prescription
from app1.utils.general import s3_put_object

from django.utils.datastructures import MultiValueDictKeyError


class PrescriptionCreate(LoginRequiredMixin, CreateView):
    model = Prescription
    form_class = PrescriptionCreationForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PrescriptionCreate, self).form_valid(form)

    def post(self, request, *args, **kwargs):

        form = PrescriptionCreationForm(request.POST, request.FILES)

        has_uploaded_file = True
        long_name = None
        content = None
        content_type = None
        files = None

        try:
            files = request.FILES['file']
            has_uploaded_file = True
        except MultiValueDictKeyError as error:
            print("file is empty!!!!")
            has_uploaded_file = False

        if has_uploaded_file:
            two_parts = os.path.splitext(files.name)

            max_uploaded_file_size = 30*1000*1000

            file_size = files.size
            base_file_name = two_parts[0]
            file_extension = (two_parts[1]).lower()

            print(base_file_name)
            print(file_extension)

            uuid4 = str(uuid.uuid4())
            content = files.read()

            # date directory information such as 2099/08/08/
            today = datetime.now()

            today_path = today.strftime("%Y/%m/%d/")

            long_name = today_path + base_file_name + \
                        '--' + uuid4 + file_extension

            print("generated long file name is: "
                  + long_name)


            if file_size > max_uploaded_file_size:
                form.add_error(
                    field=None,
                    error="File exceeds 30MB. Too big! Reduce size and try again.")
                return render(request, 'app1/Prescription_form.html', {'form': form})
                #return self.form_invalid(form)
                #raise form.ValidationError("Your file exceeds 30MB. Too big!")


            if file_extension == ".pdf":
                content_type = "application/pdf"
            elif file_extension == ".jpeg":
                content_type = "image/jpeg"
            elif file_extension == ".jpg":
                content_type = "image/jpg"
            elif file_extension == ".png":
                content_type = "image/png"
            elif file_extension == ".bm":
                content_type = "image/bmp"
            elif file_extension == ".bmp":
                content_type = "image/bmp"
            elif file_extension == ".docx":
                content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            elif file_extension == ".doc":
                content_type = "application/msword"
            else:
                content_type = "NotAcceptable"

            if content_type == "NotAcceptable":
                form.add_error(
                    field=None,
                    error="File type " +
                          file_extension +
                          " is not acceptable. Try a different file.")
                return render(request, 'app1/Prescription_form.html', {'form': form})
        else:
            long_name = None
            content = None
            content_type = None


        if form.is_valid():
            a_name = form.cleaned_data['name']
            print(a_name)

            adoctor_name = form.cleaned_data['doctor_name']
            print(adoctor_name)

            a_left_eye_sphere = form.cleaned_data['left_eye_sphere']
            a_left_eye_cylinder = form.cleaned_data['left_eye_cylinder']
            a_left_eye_axis = form.cleaned_data['left_eye_axis']
            a_right_eye_sphere = form.cleaned_data['right_eye_sphere']
            a_right_eye_cylinder = form.cleaned_data['right_eye_cylinder']
            a_right_eye_axis = form.cleaned_data['right_eye_axis']

            acreation_DT = form.cleaned_data['creation_DT']
            print(acreation_DT)

            amodification_DT = form.cleaned_data['modification_DT']
            print(amodification_DT)

            id = request.user.id

            prefix = "https://s3.us-east-2.amazonaws.com/aierusa/"
            if has_uploaded_file:
                s3_put_object(long_name, content, content_type)
                file_instance = Prescription(
                    name=a_name,
                    doctor_name=adoctor_name,
                    left_eye_sphere = a_left_eye_sphere,
                    left_eye_cylinder=a_left_eye_cylinder,
                    left_eye_axis=a_left_eye_axis,
                    right_eye_sphere=a_right_eye_sphere,
                    right_eye_cylinder=a_right_eye_cylinder,
                    right_eye_axis=a_right_eye_axis,
                    creation_DT=acreation_DT,
                    modification_DT=amodification_DT,
                    filename=long_name,
                    file_url=prefix + long_name,
                    user_id=id)
            else:
                file_instance = Prescription(
                    name=a_name,
                    doctor_name=adoctor_name,
                    left_eye_sphere=a_left_eye_sphere,
                    left_eye_cylinder=a_left_eye_cylinder,
                    left_eye_axis=a_left_eye_axis,
                    right_eye_sphere=a_right_eye_sphere,
                    right_eye_cylinder=a_right_eye_cylinder,
                    right_eye_axis=a_right_eye_axis,
                    creation_DT=acreation_DT,
                    modification_DT=amodification_DT,
                    filename="",
                    file_url="",
                    user_id=id)

            print("checkpoint 3")
            file_instance.save()

            return HttpResponseRedirect(reverse('prescriptions'))
        else:
            return self.form_invalid(form)
