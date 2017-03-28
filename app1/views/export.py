from django.shortcuts import render
from app1.models import (
    Password,
    AccessPoint,
    PasswordAccessPoint)
from django.contrib.auth.models import User


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
           "comment,security_questions,email,user_id\n"
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

        if obj.security_questions is None:
            security_questions = ""
        else:
            security_questions = obj.security_questions

        if obj.email is None:
            email = ""
        else:
            email = obj.email

        ret += str(obj.id) + "," +\
            website + "," +\
            username + "," +\
            password + "," +\
            creationDT + "," + \
            modificationDT + "," +\
            comment + "," + \
            security_questions + "," + \
            email + "," + \
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
