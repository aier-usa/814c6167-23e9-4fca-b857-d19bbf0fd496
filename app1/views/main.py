from django.shortcuts import render
from app1.utils.generate import (
    create_max_pwd_ap
)
from app1.models import (
    Password,
    PasswordTrustedPartner
)


def testing(request):
    return render(request, 'app1/testing.html', {})

def main(request):
    return render(request, 'app1/main.html', {})


def how_to_use(request):
    return render(request, 'app1/how_to_use.html', {})

def demo(request):
    return render(request, 'app1/demo.html', {})

def encryption(request):
    return render(request,
                  'app1/encryption.html', {})


def benefits(request):
    return render(request,
                  'app1/benefits.html', {})


def security_and_convenience(request):
    return render(request,
                  'app1/security_and_convenience.html', {})


def two_factor_authentication(request):
    return render(request,
                  'app1/two_factor_authentication.html', {})


def our_story(request):
    return render(request,
                  'app1/our_story.html', {})


def partial_sharing(request):
    uid = request.user.id

    # compute to_others list. It is a list of dictionary
    to_others = []
    passwords = Password.objects.filter(
        user_id = uid
    )
    for password in passwords:
        pid = password.id

        partners = PasswordTrustedPartner.objects.filter(
            password_id=pid
        )

        for one_partner in partners:
            one_dict = {}
            one_dict['website'] = password.website
            one_dict['username'] = password.username
            one_dict['password'] = password.password
            one_dict['trusted_partner'] = \
                one_partner.trusted_partner.username
            to_others.append(one_dict)

    # compute from_other list. It is a list of dictionary
    from_others = []
    partners = PasswordTrustedPartner.objects.filter(
        trusted_partner_id=uid
    )

    for one_partner in partners:
        different_dict = {}

        password = one_partner.password
        owner_name = password.user.username
        different_dict['owner_name'] = owner_name
        different_dict['website'] = password.website
        different_dict['username'] = password.username
        different_dict['password'] = password.password
        from_others.append(different_dict)



    return render(
        request,
        'app1/partial_sharing.html', {
            'to_others': to_others,
            'from_others': from_others}
    )


def gen_max_pwd_ap(request):
    create_max_pwd_ap()
    return render(request, 'app1/gen_max_pwd_ap.html', {})