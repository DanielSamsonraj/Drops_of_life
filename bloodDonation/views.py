from django.shortcuts import render, redirect
from django import template
from django.contrib import messages
from .models import DonarDetails
from django.contrib.auth.models import User

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
    return render(request, 'files/login.html', val)


def signup(request):
    val = getVal()
    if request.method == 'POST':
        Name = request.POST['name']
        email = request.POST['email']
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
            return redirect('sigup')
        if password == email:
            messages.info(request, "Password should not be same as email")
            return redirect('signup')
        if password == password1:
            try:
                User.objects.get(username=email)
                messages.info(
                    request, "There's already an account with this email")
                return redirect('signup')
            except User.DoesNotExist:
                user = User.objects.create_user(
                    username=email, password=password)
                extended_user = DonarDetails(
                    name=Name,
                    blood_group=bloodGroup,
                    area=area,
                    city=city,
                    state=state,
                    country=country,
                    user=user
                )
                extended_user.save()
            return
        else:
            messages.info(
                request, "Password and Confirm Password should match")
            return redirect('signup')

    else:
        return render(request, 'files/signup.html', val)


def profile(request):
    val = getVal()
    return render(request, 'files/profile.html', val)


def search(request):
    val = getVal()
    val['check'] = True
    val['initialCheck'] = False
    if request.method == 'POST':
        bloodGroup = request.POST['bg']
        area = request.POST['area']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']

        # fecthing data

        data = DonarDetails.objects.all()
        status_check = DonarDetails.objects.filter().values()
        available_donors = []
        temp_list = []
        for values in status_check:
            temp_list.append(list(values.values()))
        for details in temp_list:
            if details[4] == "NO":
                details[4] = None
            available_donors.append(
                [details[1], details[5], details[6], details[7]])
        val['details'] = available_donors

        # print(val['details'])

        val['table_headers'] = ["Name",
                                "Blood Group", "Contact No", "Address"]
        val['initialCheck'] = True
    else:
        val['details'] = None
        val['len'] = []
    return render(request, 'files/search.html', val)


def changepassword(request):
    val = getVal()
    return render(request, 'files/changepassword.html', val)
