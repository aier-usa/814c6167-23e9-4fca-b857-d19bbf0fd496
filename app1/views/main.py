from app1.utils.generate import (
    create_max_receipt,
    gen_daily_all_data,
    get_selected_users)
from django.shortcuts import (
    render)
from django.contrib.auth import (
    login)
from django.contrib.auth import (
    authenticate)


from app1.forms.UserCreationWithMoreForm import (
    UserCreationWithMoreForm)


from app1.forms.ProfileForm import ProfileForm


def testing(request):
    return render(request, 'app1/testing.html', {})


def main(request):
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
            #return HttpResponseRedirect("/")
            return render(request, 'app1/register-latest-spending.html', {})

    else:
        form = UserCreationWithMoreForm()
        profile_form = ProfileForm()
    return render(request, 'app1/main.html', {
        'form': form,
        'profile_form': profile_form
    })


def how_to_use(request):
    return render(request, 'app1/how_to_use.html', {})


def gen_max_receipt(request):
    create_max_receipt()
    return render(request, 'app1/gen_max_receipt.html', {})

def eyecare_q_and_a(request):
    return render(request, 'app1/eyecare_q_and_a.html', {})

def daily_all_data(request):
    data = gen_daily_all_data()
    return render(request, 'app1/daily_all_data.html', {'data': data})





def users_joined_in_a_date(request, **kwargs):
    a_date = kwargs['date_joined']
    data = get_selected_users(a_date)
    return render(request, 'app1/selected_users.html', {'data': data})
