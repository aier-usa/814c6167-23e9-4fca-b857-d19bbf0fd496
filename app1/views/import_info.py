from django.shortcuts import render
from django.http import HttpResponse
from app1.models import (
    Password,
    AccessPoint,
    PasswordAccessPoint)
from app1.forms.ImportUserInfoForm \
    import ImportUserInfoForm
from django.contrib.auth.models import User


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
            "modificationDT,comment,security_questions,email,user_id":
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
        security_questions = parts[7].strip()
        email = parts[8].strip()
        user_id = parts[9].strip()

        obj = None
        try:
            obj = Password.objects.get(pk=password_id)
        except Password.DoesNotExist:  # catch the DoesNotExist error
            obj = None
        if obj is None:
            obj = Password(
                website=website,
                username=username,
                password=password,
                creationDT=creationDT,
                modificationDT=modificationDT,
                comment=comment,
                security_questions=security_questions,
                email=email,
                user_id=user_id
            )
            obj.save()
        else:
            obj.website = website
            obj.username = username
            obj.password = password
            obj.creationDT = creationDT
            obj.modificationDT = modificationDT
            obj.comment = comment
            obj.security_questions = security_questions
            obj.email = email
            obj.user_id = user_id
            obj.save()


def import_one_user_info(request):
    error_message =""
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
                # If the number of commas is 9, it must be Password
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
                elif line2.count(",") == 9:
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

            ## return HttpResponse(
            #    result, content_type='text/plain')

            return render(request,
                "app1/import_processed_successfully.html", {'result': result})


        else:
            pass
    else:
        pass