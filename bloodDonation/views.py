from django.shortcuts import render, redirect
from django import template
from django.contrib import messages
from .models import DonarDetails
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
import random

loggedin = False


def getVal():
    if loggedin == False:
        navBar = {
            'signup': 'Signup',
            'login': 'Login'
        }
    else:
        navBar = {
            'signup': None,
            'login': None,
            'viewProfile': 'Profile',
            'logout': 'Logout'
        }
    return navBar


def home(request):
    val = getVal()
    return render(request, 'files/home.html', val)


def user_login(request):
    global loggedin
    val = getVal()
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            loggedin = True
            return redirect('home')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'files/login.html', val)


@login_required(login_url='/login/')
def logout(request):
    auth.logout(request)
    global loggedin
    loggedin = False
    return render(request, 'files/home.html', getVal())


def signup(request):
    val = getVal()
    if request.method == 'POST':
        Name = request.POST['name']
        email = request.POST['email'] or None
        password = request.POST['pswd']
        password1 = request.POST['CPswd']
        contactNo = request.POST['CNo']
        area = request.POST['area']
        city = request.POST['city']
        state = request.POST['state']
        bloodGroup = request.POST['bg']
        country = request.POST['country']
        if len(password) < 8:
            messages.info(
                request, "Password should be minimum of 8 charachters")
            return redirect('signup')
        if password == email:
            messages.info(request, "Password should not be same as email")
            return redirect('signup')
        if password == password1:
            try:
                User.objects.get(username=email)
                messages.info(
                    request, "There's already an account with this email")
                return redirect('signup')
            except:
                user = User.objects.create_user(
                    username=email, password=password)
                print(user)
                extended_user = DonarDetails(
                    name=Name.lower(),
                    blood_group=bloodGroup.upper(),
                    contact_no=contactNo,
                    area=area.lower(),
                    city=city.lower(),
                    state=state.lower(),
                    country=country.lower(),
                    user=user
                )
                extended_user.save()
            auth.login(request, user)
            # email sending

            subject = "Thank you for registering for donating blood"
            from_email = settings.EMAIL_HOST_USER
            to_email = [email]
            signup_message = "Hey " + Name + "\n" + "Welcome to Drops of life," + "\n" + \
                "Thank you for registering yourself as a donor hope you help as many people as you can though our platform."
            send_mail(subject=subject, from_email=from_email,
                      recipient_list=to_email, message=signup_message, fail_silently=False)

            global loggedin
            loggedin = True
            return redirect('home')
        else:
            messages.info(
                request, "Password and Confirm Password should match")
            return redirect('signup')

    else:
        return render(request, 'files/signup.html', val)


@login_required(login_url='/login/')
def profile(request):
    val = getVal()
    user = DonarDetails.objects.filter(user=request.user)
    val['data'] = user
    return render(request, 'files/profile.html', val)


@login_required(login_url='/login/')
def editprofile(request):
    val = getVal()
    user = DonarDetails.objects.filter(user=request.user)
    query_set = DonarDetails.objects.filter(name=user[0].name).values()
    pk = list(query_set[0].values())[0]

    if request.method == 'POST':
        data = DonarDetails.objects.get(pk=pk)
        data.name = request.POST['name']
        data.contact_no = request.POST['CNo']
        data.area = request.POST['area']
        data.city = request.POST['city']
        data.state = request.POST['state']
        data.blood_group = request.POST['bg']
        data.country = request.POST['country']

        data.save()
        return render(request, 'files/home.html', val)

    else:
        val['data'] = query_set
        return render(request, 'files/editprofile.html', val)


def convert(person):
    for i in range(len(person)):
        if i != 1 and i != 2:
            person[i] = person[i].capitalize()
    return person


def search(request):
    val = getVal()
    val['check'] = False
    val['check1'] = False
    val['req_method'] = False
    if request.method == 'POST':
        val['req_method'] = True
        bloodGroup = request.POST['bg'].upper()
        area = request.POST['area'].lower()
        city = request.POST['city'].lower()
        state = request.POST['state'].lower()
        country = request.POST['country'].lower()

        val['table_headers'] = ["Name", "Blood Group", "Contact No", "Address"]

        worldwide_donors = DonarDetails.objects.filter(
            blood_group=bloodGroup).values()
        if len(worldwide_donors) > 0:
            val['check1'] = True
        countrywide_donors = DonarDetails.objects.filter(
            country=country, blood_group=bloodGroup).values()
        statewide_donors = DonarDetails.objects.filter(
            country=country, state=state, blood_group=bloodGroup).values()
        citywide_donors = DonarDetails.objects.filter(
            country=country,
            state=state,
            city=city,
            blood_group=bloodGroup
        ).values()
        areawide_donors = DonarDetails.objects.filter(
            country=country,
            state=state,
            city=city,
            area=area,
            blood_group=bloodGroup
        ).values()

        check_dup = {}

        # print(countrywide_donors)

        filter1 = []
        for value in areawide_donors:
            person = list(value.values())[1:-1]
            if person[2] not in check_dup:
                finalList = convert(person)
                check_dup[person[2]] = True
                finalList1 = finalList[:3]
                finalList1.append(",".join(finalList[3:]))
                filter1.append(finalList1)
                # print("filter1 ", filter1)

        filter2 = []
        for value in citywide_donors:
            person = list(value.values())[1: -1]
            if person[2] not in check_dup:
                check_dup[person[2]] = True
                finalList = convert(person)
                finalList1 = finalList[:3]
                finalList1.append(",".join(finalList[3:]))
                filter2.append(finalList1)
                # print("filter2 ", filter2)

        filter3 = []
        for value in statewide_donors:
            person = list(value.values())[1: -1]
            if person[2] not in check_dup:
                check_dup[person[2]] = True
                finalList = convert(person)
                finalList1 = finalList[:3]
                finalList1.append(",".join(finalList[3:]))
                filter3.append(finalList1)
                # print("filter3 ", filter3)

        filter4 = []
        for value in countrywide_donors:
            person = list(value.values())[1: -1]
            if person[2] not in check_dup:
                check_dup[person[2]] = True
                finalList = convert(person)
                finalList1 = finalList[:3]
                finalList1.append(",".join(finalList[3:]))
                filter4.append(finalList1)
                # print("filter4 ", filter4)
        filter5 = []
        for value in worldwide_donors:
            person = list(value.values())[1: -1]
            if person[2] not in check_dup:
                check_dup[person[2]] = True
                finalList = convert(person)
                finalList1 = finalList[:3]
                finalList1.append(",".join(finalList[3:]))
                filter5.append(finalList1)

        val['details'] = [filter1, filter2, filter3, filter4, filter5]
        val['check'] = True
        return render(request, 'files/search.html', val)
    else:
        val['details'] = None
        return render(request, 'files/search.html', val)


@login_required(login_url='/login/')
def changepassword(request):
    if request.method=="POST":
        cur_pwd=request.POST['currentpassword']
        new_pwd=request.POST['newpassword']
        conf_pwd=request.POST['conformpassword']
        #print(request.user)
        u=User.objects.get(username=request.user)
        if(u.check_password(cur_pwd)):
            if new_pwd == conf_pwd:
                if len(new_pwd)<8:
                    messages.info(request,"Password should be minimum of 8 characters")
                else:
                    u.set_password(new_pwd)
                    u.save()
                    global loggedin
                    loggedin=False
                    return render(request,'files/login.html',getVal())
            else:
                messages.info(request,"new password and conform password should match")
                return redirect('changepassword')
        else:
            messages.info(request,"Please Enter Valid Password")
            return redirect('changepassword')     
    else:
        return render(request, 'files/changepassword.html', getVal())


def generate_OTP():
    otp = [str(random.randrange(10)) for i in range(4)]
    return "".join(otp)


def enter_OTP(request):
    global OTP
    if request.method == 'POST':
        entered_otp = request.POST['otp']
        if entered_otp == OTP:
            return render(request, 'files/new_password.html',getVal())
        else:
            messages.error(request, "OTP didn't match")
            return redirect('enter_OTP')
    else:
        return render(request, 'files/enter_OTP.html', getVal())


def new_password(request):
    if request.method == "POST":
        pwd = request.POST['password']
        conf_pwd = request.POST['confirm-password']
        if new_pwd == conf_pwd:
            if len(new_pwd)<8:
                messages.info(request,"Password should be minimum of 8 characters")
            else:
                u=User.objects.get(username=email)
                u.set_password(new_pwd)
                u.save()
                global loggedin
                loggedin=False
                return render(request,'files/login.html',getVal())
        else:
            messages.info(request,"new password and conform password should match")
            return redirect('new_password')
    else:
        return render(request, 'files/new_password', getVal())


OTP = ""
email=''

def forgotpassword(request):
    if request.method == 'POST':
        global email
        email = request.POST['email']
        global OTP
        OTP = generate_OTP()
        subject = "Drops Of Life Resetting Password"
        from_email = settings.EMAIL_HOST_USER
        to_email = [email]
        signup_message = "Hey user," + '\n' + OTP + " \n This is your OTP for your request" + \
            '\n' + "If its not working please repeat this process again."
        send_mail(subject=subject, from_email=from_email,
                  recipient_list=to_email, message=signup_message, fail_silently=False)
        return redirect('enter_OTP')
    else:
        return render(request, 'files/forgotpassword.html', getVal())
