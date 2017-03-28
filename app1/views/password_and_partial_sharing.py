from django.shortcuts import render
from django.utils import timezone
from app1.models import (
    Password,
    AccessPoint,
    PasswordAccessPoint,
    PasswordTrustedPartner)
from app1.forms.AvailableAccessPointForm import (
    AvailableAccessPointForm)

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist



def get_all_ap_ids(user_id):
    keys = AccessPoint.objects.filter(
        user_id=user_id).values_list('id', flat=True)
    return keys


def unlink_password_access_point(password_id, access_point_id):
    password = Password.objects.get(pk=password_id)
    ap = AccessPoint.objects.get(pk=access_point_id)

    # Find it and delete
    PasswordAccessPoint.objects.filter(
        password_id__exact=password).filter(
        access_point_id__exact=ap).delete()


def link_password_access_point(password_id, access_point_id):
    password = Password.objects.get(pk=password_id)
    ap = AccessPoint.objects.get(pk=access_point_id)

    # establish the linkage between password and access_point
    PasswordAccessPoint.objects.create(
        password=password,
        access_point=ap,
        DT_established=timezone.now())


def get_all_tp_user_ids(password_id):
    keys = PasswordTrustedPartner.objects.filter(
        password_id=password_id).values_list(
        'trusted_partner_id', flat=True)
    return keys


def unlink_password_trusted_partner(password_id, user_id):
    password = Password.objects.get(pk=password_id)
    trusted_partner = User.objects.get(pk=user_id)

    # Find it and delete
    PasswordTrustedPartner.objects.filter(
        password_id__exact=password).filter(
        trusted_partner_id__exact=trusted_partner).delete()


def link_password_trusted_partner(password_id, user_id):
    password = Password.objects.get(pk=password_id)
    trusted_partner = User.objects.get(pk=user_id)

    # establish the linkage between password and access_point
    PasswordTrustedPartner.objects.create(
        password=password,
        trusted_partner=trusted_partner,
        DT_established=timezone.now())

def get_ids_from_usernames(usernames_value, current_user_id):
    set1 = set()
    invalid_usernames = ''
    all_usernames = usernames_value.split(',')
    for single_name in all_usernames:
        trimed_name = single_name.rstrip().lstrip()
        if len(trimed_name) > 0:
            try:
                one_user_id = User.objects.get(
                    username=trimed_name).id
                # make sure that user does NOT
                # add himself/herself.
                if (one_user_id != current_user_id):
                    set1.add(one_user_id)
                else:
                    invalid_usernames += \
                        ' ' + trimed_name + \
                        '[You added yourself. Not valid]'
            except ObjectDoesNotExist:
                invalid_usernames += ' ' + trimed_name


    return {'ids':set1,
            'invalid_usernames':invalid_usernames}

def link_together(request):
    all_ids = ""
    invalid_usernames = ''
    if request.method == 'POST':
        form = AvailableAccessPointForm(request.POST)
        password_id = form.data['password_id']

        username = form.data['username']

        user_id = User.objects.get(username=username).id

        print("inside link_together: password_id is: " + password_id)
        print("inside link_together: user_id is: " + str(user_id))
            # get rid of old linkages
        keys = get_all_ap_ids(user_id)
        for access_point_id in keys:
            unlink_password_access_point(
                password_id, access_point_id)

        # re-establish new linkages
        for key, access_point_id_value in form.data.items():
            if key.startswith('ap_id_'):
                all_ids += ' ' + access_point_id_value
                link_password_access_point(
                    password_id, access_point_id_value)


        ##### get usernames. It is a list of trusted user names
        ##### Max Li 2017-02-14
        # get rid of unchecked "trusted partner username"
        #keys = get_all_ap_ids()
        keys = get_all_tp_user_ids(password_id)
        for tp_user_id in keys:
            unlink_password_trusted_partner(
                password_id, tp_user_id)
        # from the usernames, we need to establish password with
        # a list of trusted users
        tp_user_ids_set = set()
        for key, tp_user_id_value in form.data.items():
            if key.startswith('tp_user_id_'):
                tp_user_ids_set.add(tp_user_id_value)
                link_password_trusted_partner(
                    password_id, tp_user_id_value)

        for key, usernames_value in form.data.items():
            if key.startswith('trusted_partner_usernames'):
                result = get_ids_from_usernames(usernames_value, user_id)

                for one_id in result['ids']:
                    if not (one_id in tp_user_ids_set):
                        link_password_trusted_partner(
                            password_id, one_id)

                invalid_usernames = result['invalid_usernames']

    return render(request, "app1/assign_list_linking_finished.html", {
        'all_ids': all_ids,
        'invalid_usernames': invalid_usernames
    })
