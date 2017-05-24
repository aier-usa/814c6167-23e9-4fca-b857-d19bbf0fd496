from django.shortcuts import (
    render,
    redirect,
    resolve_url)
from django.contrib.auth import (
    login,
    logout,
    update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    SetPasswordForm)
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import (
    authenticate,
    get_user_model)
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_text

from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse


from app1.forms.UserCreationWithMoreForm import (
    UserCreationWithMoreForm)
from app1.forms.CustomUserChangeForm import (
    CustomUserChangeForm)
from app1.forms.ProfileForm import ProfileForm

from app1.models import Profile
from django.contrib.auth.models import User


def accounts_profile(request):
    uid = request.user.id
    a_profile = Profile.objects.get(user_id=uid)
    cell_phone = a_profile.cell_phone
    return render(request,
                  "registration/accounts-profile.html", {'cell_phone': cell_phone})


def register(request):
    if request.method == 'POST':
        form = UserCreationWithMoreForm(
            request.POST)
        profile_form = ProfileForm(
            request.POST)
        print(form)
        print(form.is_valid())
        print(profile_form)
        print(profile_form.is_valid())

        if form.is_valid() and profile_form.is_valid():
            form.save()

            # get the username and password
            username = request.POST['username']
            password = request.POST['password1']
            # authenticate user then login
            user = authenticate(username=username, password=password)

            profile_form.user_id = user.id
            profile_form.save()

            login(request, user)
            return HttpResponseRedirect("/")
    else:
        form = UserCreationWithMoreForm()
        profile_form = ProfileForm()
    return render(request, "registration/register.html", {
        'form': form,
        'profile_form': profile_form
    })


def accounts_password_change(request):
    if request.method == 'GET':
        form = PasswordChangeForm(user=request.user)
        return render(request,
                      "registration/accounts-password-change.html",
                      {'form': form})
    elif request.method == 'POST':
        form = PasswordChangeForm(
            user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(reverse('password_change_done'))
        else:
            return render(
                request,
                "registration/accounts-password-change.html",
                {'form': form})


def accounts_user_change(request):
    if request.method == 'GET':
        form = CustomUserChangeForm()
        passed_username = request.user.username
        passed_first_name = request.user.first_name
        passed_last_name = request.user.last_name
        passed_email = request.user.email

        passed_street = request.user.profile.street
        passed_city = request.user.profile.city
        passed_state = request.user.profile.state
        passed_zip = request.user.profile.zip
        passed_country = request.user.profile.country
        passed_cell_phone = request.user.profile.cell_phone
        passed_work_phone = request.user.profile.work_phone
        passed_home_phone = request.user.profile.home_phone


        # form = UserChangeForm(instance=request.user)
        # form = UserProfileForm(instance=request.user)
        return render(request,
                      "registration/accounts-user-change.html",
                      {'form': form,
                       'passed_username': passed_username,
                       'passed_first_name': passed_first_name,
                       'passed_last_name': passed_last_name,
                       'passed_email': passed_email,
                       'passed_street': passed_street,
                       'passed_city': passed_city,
                       'passed_state': passed_state,
                       'passed_zip': passed_zip,
                       'passed_country': passed_country,

                       'passed_cell_phone': passed_cell_phone,
                       'passed_work_phone': passed_work_phone,
                       'passed_home_phone': passed_home_phone,

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
            entered_street = \
                form.cleaned_data['street']
            entered_city = \
                form.cleaned_data['city']
            entered_state = \
                form.cleaned_data['state']
            entered_zip = \
                form.cleaned_data['zip']
            entered_country = \
                form.cleaned_data['country']

            entered_cell_phone = \
                form.cleaned_data['cell_phone']
            entered_home_phone = \
                form.cleaned_data['home_phone']
            entered_work_phone = \
                form.cleaned_data['work_phone']


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

            retrieved_profile = request.user.profile
            retrieved_profile.street = entered_street
            retrieved_profile.city = entered_city
            retrieved_profile.state = entered_state
            retrieved_profile.zip = entered_zip
            retrieved_profile.country = entered_country

            retrieved_profile.cell_phone = entered_cell_phone
            retrieved_profile.work_phone = entered_work_phone
            retrieved_profile.home_phone = entered_home_phone

            retrieved_profile.save()


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


def accounts_password_reset_done(request):
    return render(request,
                  "registration/accounts-password-reset-done.html", {})


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


def accounts_password_reset_complete(request):
    return render(request,
                  "registration/accounts-password-reset-complete.html", {})


# check tangowithdjango.com/book/chapters/login.html
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
                # return HttpResponseRedirect('/')
                return HttpResponseRedirect(reverse('receipts'))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse(
                    "Your ihatepassword.com account is disabled.")
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
        form = AuthenticationForm()
        return render(
            request, "registration/login.html", {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('main'))