from django.shortcuts import render, redirect
from django import template
from django.contrib import messages
from .models import DonarDetails
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required

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
    data = DonarDetails.objects.filter(user=request.user)
    val['data'] = data
    print(data)
    return render(request, 'files/profile.html', val)


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
            country=country,
            blood_group=bloodGroup
        ).values()
        statewide_donors = DonarDetails.objects.filter(
            country=country,
            state=state,
            blood_group=bloodGroup
        ).values()
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
    val = getVal()
    return render(request, 'files/changepassword.html', val)
