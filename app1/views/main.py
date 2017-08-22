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


def About_us(request):
    return render(request, 'app1/About_us.html', {})


def Contact_us(request):
    return render(request, 'app1/Contact_us.html', {})


def Q_and_A(request):
    return render(request, 'app1/Q_and_A.html', {})


def Contacts_glasses(request):
    return render(request,
                  'app1/Contacts_glasses.html', {})

def Cell_phone_computer_Eye_Syndrome(request):
    return render(request,
                  'app1/Cell_phone_computer_Eye_Syndrome.html',
                  {})

def D3_SMILE(request):
    return render(request,
                  'app1/D3_SMILE.html', {})

def D3_LASIK(request):
    return render(request,
                  'app1/D3_LASIK.html', {})

def D3_Kamra(request):
    return render(request,
                  'app1/D3_Kamra.html', {})

def D3_Raindrop(request):
    return render(request,
                  'app1/D3_Raindrop.html', {})

def D3_Forever_Young_Lens(request):
    return render(request,
                  'app1/D3_Forever_Young_Lens.html', {})

def D3_Laser_Cataract(request):
    return render(request,
                  'app1/D3_Laser_Cataract.html', {})


def users_joined_in_a_date(request, **kwargs):
    a_date = kwargs['date_joined']
    data = get_selected_users(a_date)
    return render(request, 'app1/selected_users.html', {'data': data})
