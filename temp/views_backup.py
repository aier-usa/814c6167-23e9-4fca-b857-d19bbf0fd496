from django.contrib import messages
from django.contrib.auth import (
    authenticate, get_user_model)
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    SetPasswordForm)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.validators import validate_email
from django.db.models import Count
from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import (
    render,
    resolve_url,
    redirect)
from django.template import RequestContext
from django.template import loader
from django.template.response import TemplateResponse
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.views.generic import FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from temp.forms_backup import (AvailableAccessPointForm,
                               PasswordCreationForm,
                               PasswordUpdateForm,
                               AccessPointCreationForm,
                               AccessPointUpdateForm,
                               UserCreationWithMoreForm,
                               ImportUserInfoForm,
                               CustomUserChangeForm)
from temp.forms_backup import PasswordResetRequestForm
from app1.models import (Password,
                         AccessPoint,
                         PasswordAccessPoint)


def main(request):
    return render(request, 'app1/main.html', {})


def register(request):
    if request.method == 'POST':
        form = UserCreationWithMoreForm(request.POST)
        if form.is_valid():
            form.save()
            # get the username and password
            username = request.POST['username']
            password = request.POST['password1']
            # authenticate user then login
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect("/")
    else:
        form = UserCreationWithMoreForm()
    return render(request, "registration/register.html", {
        'form': form,
    })


def profile(request):
    return HttpResponseRedirect("/")


def password_reset(request):
    return HttpResponseRedirect("/")


# from http://www.tangowithdjango.com/book/chapters/login.html
def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your IHP account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {0}, {1}".format(
                username, password))
            return render(
                request, "registration/invalid-login-info.html", {}
            )

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        form = AuthenticationForm()
        return render(
            request, "registration/login.html", {'form': form})


@login_required
def user_logout(request):
    logout(request)
    # return HttpResponseRedirect('/')
    return redirect(reverse('main'))


def get_all_ap_ids():
    keys = AccessPoint.objects.values_list('id', flat=True)
    return keys


def unlink_password_access_point(password_id, access_point_id):
    passwd = Password.objects.get(pk=password_id)
    ap = AccessPoint.objects.get(pk=access_point_id)

    # Find it and delete
    pap = PasswordAccessPoint.objects.filter(
        password_id__exact=passwd).filter(
        access_point_id__exact=ap).delete()


def link_password_access_point(password_id, access_point_id):
    passwd = Password.objects.get(pk=password_id)
    ap = AccessPoint.objects.get(pk=access_point_id)

    # establish the linkage between password and access_point
    PasswordAccessPoint.objects.create(
        password=passwd,
        access_point=ap,
        DT_established=timezone.now())


def is_pwd_id_and_ap_id_used(password_id, key1):
    passwd = Password.objects.get(pk=password_id)
    ap = AccessPoint.objects.get(pk=key1)

    # establish the linkage between password and access_point
    pap = PasswordAccessPoint.objects.filter(
        password_id__exact=passwd).filter(access_point_id__exact=ap)
    if pap.count() == 0:
        return False
    else:
        return True


def link_together(request):
    testing_data = ""
    testing1 = ""
    all_ids = ""
    if request.method == 'POST':
        form = AvailableAccessPointForm(request.POST)
        # testing1 = form.data['id_multiple']
        password_id = form.data['password_id']

        # get rid of old linkages
        keys = get_all_ap_ids()
        for key1 in keys:
            unlink_password_access_point(password_id, key1)

        # re-establish new linkages
        for key, value in form.data.items():
            if key.startswith('ap_id_'):
                all_ids += ' ' + value
                link_password_access_point(password_id, value)

    return render(request, "app1/assign_list_linking_finished.html", {
        'all_ids': all_ids,
    })


def accounts_profile(request):
    return render(request,
                  "registration/accounts-profile.html", {})


def get_user_info(user_id):
    obj = User.objects.get(pk=user_id)
    ret = "######## Starting User ########\n"
    ret += "id,username,first_name,last_name,email\n"
    ret += str(obj.id) + "," + \
        obj.username + "," + \
        obj.first_name + "," + \
        obj.last_name + "," + \
        obj.email + "\n"
    ret += "######## Ending User ########\n"
    return ret


def get_password_info(user_id):
    ret = "######## Starting Password ########\n"
    ret += "id,website,username,password,creationDT,modificationDT," +\
           "comment,user_id\n"
    objs = Password.objects.filter(user__id=user_id)
    # "%Y-%m-%d %H:%M:%S%Z" or "%Y-%m-%d %H:%M:%S"???
    for obj in objs:
        if obj.website is None:
            website = ""
        else:
            website = obj.website

        if obj.username is None:
            username = ""
        else:
            username = obj.username

        if obj.password is None:
            password = ""
        else:
            password = obj.password

        if obj.creationDT is None:
            creationDT = ""
        else:
            creationDT = obj.creationDT. \
                strftime("%Y-%m-%d %H:%M:%S%z")

        if obj.modificationDT is None:
            modificationDT = ""
        else:
            modificationDT = obj.modificationDT. \
                strftime("%Y-%m-%d %H:%M:%S%z")

        if obj.comment is None:
            comment = ""
        else:
            comment = obj.comment

        ret += str(obj.id) + "," +\
            website + "," +\
            username + "," +\
            password + "," +\
            creationDT + "," + \
            modificationDT + "," +\
            comment + "," +\
            str(obj.user_id) + "\n"
    ret += "######## Ending Password ########\n"

    return ret


#             obj.modificationDT.__str__() + "," +\
def get_AP_info(user_id):
    ret = "######## Starting AccessPoint ########\n"
    ret += "id,name,purpose,creationDT,modificationDT," +\
           "user_id\n"
    objs = AccessPoint.objects.filter(user__id=user_id)
    for obj in objs:
        ret += str(obj.id) + "," +\
            obj.name + "," +\
            obj.purpose + "," +\
            obj.creationDT.strftime("%Y-%m-%d %H:%M:%S%z") + "," +\
            obj.modificationDT.strftime("%Y-%m-%d %H:%M:%S%z") + "," +\
            str(obj.user_id) + "\n"
    ret += "######## Ending AccessPoint ########\n"
    return ret


def get_PAP_info(user_id):
    ret = "######## Starting PasswordAccessPoint ########\n"
    ret += "id,password_id,access_point_id,DT_established\n"
    objs = PasswordAccessPoint.objects.filter(
        password__user_id=user_id).filter(
        access_point__user_id=user_id)

    for obj in objs:
        ret += str(obj.id) + "," + \
               str(obj.password_id) + "," + \
               str(obj.access_point_id) + "," + \
               obj.DT_established.strftime("%Y-%m-%d %H:%M:%S%z") + "\n"
    ret += "######## Ending PasswordAccessPoint ########\n"
    return ret


def export_one_user_info(request):
    user_id = request.user.id
    info = ""
    info += get_user_info(user_id) + "\n\n"
    info += get_password_info(user_id) + "\n\n"
    info += get_AP_info(user_id) + "\n\n"
    info += get_PAP_info(user_id) + "\n\n"

    return render(request,
                  "app1/accounts_export_one_user_info.html",
                  {'info': info})


def insert_pap(entry, current_pos, starting_pos, ending_pos):
    if entry == "id,password_id,access_point_id,DT_established":
        pass
    elif not(starting_pos < current_pos < ending_pos):
        print("Error: The entry appears to be a PasswordAccessPoint. " +
              "However, it appears in the wrong place.")
    else:
        # split the line and get different parts.
        # insert into DB using different parts
        parts = entry.split(',')
        # id, password_id, access_point_id, DT_established
        pap_id = parts[0].strip()
        password_id = parts[1].strip()
        access_point_id = parts[2].strip()
        DT_established = parts[3].strip()

        obj = None
        try:
            obj = PasswordAccessPoint.objects.get(pk=pap_id)
            # catch the DoesNotExist error
        except PasswordAccessPoint.DoesNotExist:
            obj = None
        if obj is None:
            obj = PasswordAccessPoint(password_id=password_id,
                                      access_point_id=access_point_id,
                                      DT_established=DT_established)
            obj.save()
        else:
            obj.password_id = password_id
            obj.access_point_id = access_point_id
            obj.DT_established = DT_established
            obj.save()


def insert_user(entry, current_pos, starting_pos, ending_pos):
    if entry == "id,username,first_name,last_name,email":
        pass
    elif not(starting_pos < current_pos < ending_pos):
        print("Error: The entry appears to be a User. " +
              "However, it appears in the wrong place.")
    else:
        # split the line and get different parts.
        # insert into DB using different parts
        parts = entry.split(',')
        user_id = parts[0].strip()
        username = parts[1].strip()
        first_name = parts[2].strip()
        last_name = parts[3].strip()
        email = parts[4].strip()

        obj = None
        try:
            obj = User.objects.get(pk=user_id)
        except User.DoesNotExist:  # catch the DoesNotExist error
            obj = None
        if obj is None:
            obj = User(username=username,
                       first_name=first_name,
                       last_name=last_name,
                       email=email)
            obj.save()
        else:
            obj.username = username
            obj.first_name = first_name
            obj.last_name = last_name
            obj.email = email
            obj.save()


def insert_ap(entry, current_pos,
              starting_pos, ending_pos):
    if entry == "id,name,purpose,creationDT,modificationDT,user_id":
        pass
    elif not(starting_pos < current_pos < ending_pos):
        print("Error: The entry appears to be an AccessPoint. " +
              "However, it appears in the wrong place.")
    else:
        # split the line and get different parts.
        # insert into DB using different parts
        parts = entry.split(',')
        ap_id = parts[0].strip()
        name = parts[1].strip()
        purpose = parts[2].strip()
        creationDT = parts[3].strip()
        modificationDT = parts[4].strip()
        user_id = parts[5].strip()

        obj = None
        try:
            obj = AccessPoint.objects.get(pk=ap_id)
        except AccessPoint.DoesNotExist:  # catch the DoesNotExist error
            obj = None
        if obj is None:
            obj = AccessPoint(name=name,
                              purpose=purpose,
                              creationDT=creationDT,
                              modificationDT=modificationDT,
                              user_id=user_id)
            obj.save()
        else:
            obj.name = name
            obj.purpose = purpose
            obj.creationDT = creationDT
            obj.modificationDT = modificationDT
            obj.user_id = user_id
            obj.save()


def insert_password(entry, current_pos,
                    starting_pos, ending_pos):
    if entry == \
            "id,website,username,password,creationDT," +\
            "modificationDT,comment,user_id":
        pass
    elif not(starting_pos < current_pos < ending_pos):
        print("Error: The entry appears to be a Password. " +
              "However, it appears in the wrong place.")
    else:
        # split the line and get different parts.
        # insert into DB using different parts
        parts = entry.split(',')
        password_id = parts[0].strip()
        website = parts[1].strip()
        username = parts[2].strip()
        password = parts[3].strip()


        creationDT = None
        temp = parts[4].strip()
        if temp:
            creationDT = temp
        else:
            creationDT = None

        modificationDT = None
        temp = parts[5].strip()

        if temp:
            modificationDT = temp
        else:
            modificationDT = None

        comment = parts[6].strip()
        user_id = parts[7].strip()

        obj = None
        try:
            obj = Password.objects.get(pk=password_id)
        except Password.DoesNotExist:  # catch the DoesNotExist error
            obj = None
        if obj is None:
            obj = Password(website=website,
                           username=username,
                           password=password,
                           creationDT=creationDT,
                           modificationDT=modificationDT,
                           comment=comment,
                           user_id=user_id,
                           )
            obj.save()
        else:
            obj.website = website
            obj.username = username
            obj.password = password
            obj.creationDT = creationDT
            obj.modificationDT = modificationDT
            obj.comment = comment
            obj.user_id = user_id
            obj.save()


def import_one_user_info(request):
    if request.method == "GET":
        form = ImportUserInfoForm()
        return render(request, "registration/accounts-import.html", {
            'form': form})
    elif request.method == "POST":
        form = ImportUserInfoForm(request.POST)
        if form.is_valid():
            result = form.cleaned_data["all_info"]
            lines = result.splitlines()
            for one_line in lines:
                print("line is: *" + one_line + "*")

            error_flag = False
            starting_user = -1
            ending_user = -1
            starting_pwd = -1
            ending_pwd = -1
            starting_ap = -1
            ending_ap = -1
            starting_pap = -1
            ending_pap = -1

            counter = 0
            for a_line in lines:
                if a_line == \
                        "######## Starting User ########":
                    starting_user = counter
                elif a_line == \
                        "######## Ending User ########":
                    ending_user = counter
                elif a_line == \
                        "######## Starting Password ########":
                    starting_pwd = counter
                elif a_line == \
                        "######## Ending Password ########":
                    ending_pwd = counter
                elif a_line == \
                        "######## Starting AccessPoint ########":
                    starting_ap = counter
                elif a_line == \
                        "######## Ending AccessPoint ########":
                    ending_ap = counter
                elif a_line == \
                        "######## Starting PasswordAccessPoint ########":
                    starting_pap = counter
                elif a_line == \
                        "######## Ending PasswordAccessPoint ########":
                    ending_pap = counter
                counter += 1

            counter2 = 0
            for line2 in lines:
                # If the number of commas is 3, it must be PAP
                # If the number of commas is 4, it must be User
                # If the number of commas is 5, it must be AP
                # If the number of commas is 7, it must be Password
                if line2.strip() == "":
                    pass
                elif line2.startswith("####") and \
                        line2.endswith("####"):
                    pass
                elif line2.count(",") == 3:
                    # process PAP. The index must be greater
                    # than starting_pap and less than ending_pap
                    insert_pap(
                        line2, counter2, starting_pap, ending_pap)
                elif line2.count(",") == 4:
                    insert_user(
                        line2, counter2, starting_user, ending_user)
                elif line2.count(",") == 5:
                    insert_ap(
                        line2, counter2, starting_ap, ending_ap)
                elif line2.count(",") == 7:
                    insert_password(
                        line2, counter2, starting_pwd, ending_pwd)
                else:
                    error_flag = True
                    error_message = \
                        "Unrecognized line[#" + \
                        str(int(counter2) + 1) + "]: " + line2
                    break

                counter2 += 1

            if error_flag:
                result = error_message
            else:
                result = "Processed Successfully. Thank you."

            return HttpResponse(
                result, content_type='text/plain')
        else:
            pass
    else:
        pass


def accounts_password_change(request):
    if request.method == 'GET':
        form = PasswordChangeForm(request.user.username)
        # form = UserChangeForm(request.user.username)
        return render(request,
                      "registration/accounts-password-change.html",
                      {'form': form})
    elif request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('password_change_done'))


def accounts_user_change(request):
    if request.method == 'GET':
        form = CustomUserChangeForm()
        passed_username = request.user.username
        passed_first_name = request.user.first_name
        passed_last_name = request.user.last_name
        passed_email = request.user.email

        # form = UserChangeForm(instance=request.user)
        # form = UserProfileForm(instance=request.user)
        return render(request,
                      "registration/accounts-user-change.html",
                      {'form': form,
                       'passed_username': passed_username,
                       'passed_first_name': passed_first_name,
                       'passed_last_name': passed_last_name,
                       'passed_email': passed_email
                       })
    elif request.method == 'POST':
        form = CustomUserChangeForm(request.POST)
        print("value of form.is_valid() is: ")
        print(form.is_valid())
        print(form)
        print(form.data)
        if form.is_valid():
            # form.save()
            entered_username = \
                form.cleaned_data['username']
            entered_first_name = \
                form.cleaned_data['first_name']
            entered_last_name = \
                form.cleaned_data['last_name']
            entered_email = \
                form.cleaned_data['email']

            current_user_id = request.user.id
            same_username_entered = False
            if entered_username == request.user.username:
                same_username_entered = True

            username_query_result = User.objects.filter(
                username=entered_username).exclude(
                pk=current_user_id)
            if username_query_result.count() >= 1:
                form.add_error('username',
                               "Username you have chosen already exists. " +
                               "Please try again.")
                return render(request,
                              "registration/accounts-user-change.html",
                              {'form': form})

            email_query_result = User.objects.filter(
                email=entered_email).exclude(
                pk=current_user_id)
            if email_query_result.count() >= 1:
                form.add_error('email',
                               "Email you have chosen already exists. " +
                               "Please try again.")
                return render(request,
                              "registration/accounts-user-change.html",
                              {'form': form})
            retrieved_user = request.user
            retrieved_user.username = entered_username
            retrieved_user.first_name = entered_first_name
            retrieved_user.last_name = entered_last_name
            retrieved_user.email = entered_email
            retrieved_user.save()

            if same_username_entered:
                return HttpResponseRedirect(
                    reverse('user_change_done'))
            else:
                logout(request)
                return HttpResponseRedirect(reverse('main'))

        else:
            form = CustomUserChangeForm
            return render(request,
                          "registration/accounts-user-change.html",
                          {'form': form})


def accounts_user_change_done(request):
    return render(request,
                  "registration/accounts-user-change-done.html", {})


def accounts_password_change_done(request):
    return render(request,
                  "registration/accounts-password-change-done.html", {})


def accounts_password_reset(request):
    return render(request,
                  "registration/TODO-accounts-password-reset.html", {})


def accounts_password_reset_done(request):
    return render(request,
                  "registration/accounts-password-reset-done.html", {})


def accounts_password_reset_confirm(request):
    return render(request,
                  "registration/accounts-password-reset-confirm.html", {})


def accounts_password_reset_complete(request):
    return render(request,
                  "registration/accounts-password-reset-complete.html", {})


# the following is for Password


class PasswordCreate(LoginRequiredMixin, CreateView):
    model = Password
    form_class = PasswordCreationForm
    initial = {}

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PasswordCreate, self).form_valid(form)


class PasswordUpdate(LoginRequiredMixin, UpdateView):
    model = Password
    form_class = PasswordUpdateForm

    template_name = "app1/password_update.html"

    def get_context_data(self, **kwargs):
        context = super(PasswordUpdate, self).get_context_data(**kwargs)

        # The following line of code is crucial. pk refers to the
        # primary key of the password model.
        password_id = self.kwargs['pk']
        item = Password.objects.get(pk=password_id)

        context['item'] = item

        return context


class PasswordDelete(LoginRequiredMixin, DeleteView):
    model = Password
    success_url = reverse_lazy('password_list')
    template_name = "app1/password_confirm_delete.html"

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = reverse_lazy('password_list')
            return HttpResponseRedirect(url)
        else:
            return super(PasswordDelete, self).post(
                request, *args, **kwargs)


class PasswordDetail(LoginRequiredMixin, DetailView):
    model = Password
    fields = ['website', 'username', 'password', 'creationDT',
              'modificationDT', 'comment']


class PasswordList(LoginRequiredMixin, ListView):
    model = Password
    fields = ['website', 'username', 'password', 'creationDT',
              'modificationDT', 'comment']

    def get_queryset(self):
        user_name = self.request.user.username
        temp1 = Password.objects.filter(
            user__username=user_name).order_by(
            "-modificationDT", "website")
        return temp1

    def get_context_data(self, **kwargs):
        context = super(PasswordList, self).get_context_data(**kwargs)

        # The following line of code is crucial. pk refers to the
        # primary key of the password model.
        item = Password.objects.all().values("user_id").annotate(
            total=Count("user_id")).order_by("-total")

        context['max_num_pwd'] = item[0].get("total")

        return context

# The following is for AccessPoint
class AccessPointCreate(LoginRequiredMixin, CreateView):
    model = AccessPoint
    form_class = AccessPointCreationForm
    initial = {}

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AccessPointCreate, self).form_valid(form)


class AccessPointUpdate(LoginRequiredMixin, UpdateView):
    model = AccessPoint
    form_class = AccessPointUpdateForm
    initial = {}

    template_name = "app1/accesspoint_update.html"

    def get_context_data(self, **kwargs):
        context = super(AccessPointUpdate, self).get_context_data(**kwargs)

        # The following line of code is crucial. pk refers to the
        # primary key of the password model.
        accesspoint_id = self.kwargs['pk']
        item = AccessPoint.objects.get(pk=accesspoint_id)

        context['item'] = item

        return context


class AccessPointDelete(LoginRequiredMixin, DeleteView):
    model = AccessPoint
    success_url = reverse_lazy('access_point_list')
    template_name = "app1/accesspoint_confirm_delete.html"

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = reverse_lazy('access_point_list')
            return HttpResponseRedirect(url)
        else:
            return super(AccessPointDelete, self).post(request, *args, **kwargs)


class AccessPointDetail(LoginRequiredMixin, DetailView):
    model = AccessPoint
    fields = ['user', 'name', 'purpose', 'creationDT', 'modificationDT']


class AccessPointList(LoginRequiredMixin, ListView):
    model = AccessPoint
    fields = ['user', 'name', 'purpose', 'creationDT', 'modificationDT']

    def get_queryset(self):
        user_name = self.request.user.username
        temp1 = AccessPoint.objects.filter(
            user__username=user_name).order_by(
            "-modificationDT", "name")
        return temp1


# for ShowMeList, NEVER use LoginRequiredMixin because
# login is NOT required at all.
class ShowMeList(ListView):
    print("__name__ is: " + __name__)
    model = Password
    template_name = "app1/show_me_list.html"
    fields = ['id', 'website', 'username', 'password', 'creationDT',
              'modificationDT', 'comment']
    # TODO: change the below later on
    # based on 'name' field, find AccessPoint, from AccessPoint,
    # find Password

    def get_queryset(self):
        name_ap = self.kwargs['nameAP']
        print('nameAP is: ' + name_ap)
        temp1 = Password.objects.filter(
            access_points__name__iexact=name_ap)

        return temp1


class AssignList(LoginRequiredMixin, ListView):
    model = AccessPoint
    fields = ['user', 'name', 'purpose', 'creationDT']

    # TODO: change the below later on
    queryset = AccessPoint.objects.all()
    template_name = "app1/assign_list.html"

    def get_context_data(self, **kwargs):
        context = super(AssignList, self).get_context_data(**kwargs)

        # The following line of code is crucial. pk refers to the
        # primary key of the password model.
        password_id = self.kwargs['pk']
        context['password_id'] = password_id
        keys = AccessPoint.objects.values_list('id', flat=True)
        another_set = []
        for key1 in keys:
            if is_pwd_id_and_ap_id_used(password_id, key1):
                another_set.append(key1)

        context['used_ap_ids'] = another_set

        return context


class ResetPasswordRequestView(FormView):
    template_name = "registration/accounts-password-reset.html"
    # success_url = '/accounts/login'
    success_url = 'done'

    form_class = PasswordResetRequestForm

    @staticmethod
    def validate_email_address(email):
        '''
        This method here validates
        if the input is an email address or not.
        Its return type is boolean,
        True if the input is a email address or
        False if its not.
        '''

        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    def post(self, request, *args, **kwargs):
        '''
        A normal post request which takes input from
        field "email_or_username" (in ResetPasswordRequestForm).
        '''

        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data["email_or_username"]
        if self.validate_email_address(data) is True:
            # uses the method written above
            '''
            If the input is an valid email address,
            then the following code will lookup for
            users associated with that email address.
            If found then an email will be sent to
             the address, else an error message
             will be printed on the screen.
            '''
            associated_users = User.objects.filter(
                Q(email=data) | Q(username=data))
            if associated_users.exists():
                for user in associated_users:
                    c = {
                        'email': user.email,
                        'domain': request.META['HTTP_HOST'],
                        'site_name': 'ihatepassword.com',
                        'uidb64': urlsafe_base64_encode(
                            force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(
                            user),
                        'protocol': 'http',
                    }
                    subject_template_name = \
                        'registration/' + \
                        'accounts-password-reset-subject.txt'
                    # copied from django/contrib/admin/templates/registration/password_reset_subject.txt
                    #  to templates directory
                    email_template_name = \
                        'registration/' + \
                        'accounts-password-reset-email.html'
                    # copied from django/contrib/admin/templates/registration/password_reset_email.html
                    #  to templates directory
                    subject = loader.render_to_string(
                        subject_template_name, c)
                    # Email subject *must not* contain newlines
                    subject = ''.join(
                        subject.splitlines())
                    email = loader.render_to_string(
                        email_template_name, c)
                    # DEFAULT_FROM_EMAIL
                    send_mail(subject, email, "maxhaifeili@gmail.com", [
                        user.email], fail_silently=False)
                result = self.form_valid(form)
                return result
            result = self.form_invalid(form)
            messages.error(request,
                           'No user is associated with this email address')
            return result
        else:
            '''
            If the input is an username,
            then the following code will lookup
            for users associated with that user.
            If found then an email will be sent
            to the user's address, else
            an error message will be printed
            on the screen.
            '''
            associated_users = User.objects.filter(username=data)
            if associated_users.exists():
                for user in associated_users:
                    c = {
                        'email': user.email,
                        'domain': 'ihatepassword.com',  # or your domain
                        'site_name': 'ihatepassword.com',
                        'uidb64': urlsafe_base64_encode(
                            force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(
                            user),
                        'protocol': 'http',
                    }
                    subject_template_name = \
                        'registration/' + \
                        'accounts-password-reset-subject.txt'
                    email_template_name = \
                        'registration/' + \
                        'accounts-password-reset-email.html'
                    subject = loader.render_to_string(
                        subject_template_name, c)
                    # Email subject *must not* contain newlines
                    subject = ''.join(
                        subject.splitlines())
                    email = loader.render_to_string(
                        email_template_name, c)
                    # DEFAULT_FROM_EMAIL
                    send_mail(subject, email, "maxhaifeili@gmail.com", [
                        user.email], fail_silently=False)
                result = self.form_valid(form)
                return result
            result = self.form_invalid(form)
            messages.error(request,
                           'This username does not' +
                           ' exist in the system.')
            return result
            messages.error(request, 'Invalid Input')
        return self.form_invalid(form)


def accounts_password_reset_confirm(
        request, uidb64=None, token=None,
        template_name='registration/' +
                      'accounts-password-reset-confirm.html',
        token_generator=default_token_generator,
        set_password_form=SetPasswordForm,
        post_reset_redirect=None,
        extra_context=None):
    """
    View that checks the hash in a password reset link and presents a
    form for entering a new password.
    """

    UserModel = get_user_model()
    assert uidb64 is not None and token is not None  # checked by URLconf
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_complete')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    try:
        # urlsafe_base64_decode() decodes to bytestring on Python 3
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError,
            UserModel.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(
            user, token):
        validlink = True
        title = 'Enter new password'
        if request.method == 'POST':
            form = set_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(post_reset_redirect)
        else:
            form = set_password_form(user)
    else:
        validlink = False
        form = None
        title = 'Password reset unsuccessful'
    context = {
        'form': form,
        'title': title,
        'validlink': validlink,
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)
