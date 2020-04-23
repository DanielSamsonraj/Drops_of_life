from django.shortcuts import render
from django import template

from .models import donarDetails

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


def login(request):
    global loggedin
    val = getVal()
    return render(request, 'files/login.html', val)


def signup(request):
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

        if password == password1:
            obj = donarDetails(
                name=Name,
                email=email,
                password=password,
                blood_group=bloodGroup,
                contact_no=contactNo,
                area=area,
                city=city,
                state=state,
                country=country
            )
            obj.save()
            print("object created successfully ", obj.name)
        else:
            print("password dosent match")
    val = getVal()
    return render(request, 'files/signup.html', val)


def profile(request):
    val = getVal()
    return render(request, 'files/profile.html', val)


def search(request):
    val = getVal()
    val['check'] = False
    if request.method == 'POST':
        bloodGroup = request.POST['bg']
        area = request.POST['area']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        try:
            val['details'].append(
                ["Daniel Samson ", bloodGroup, area, city, state, country, '8309282168'])
        except:
            val['details'] = ["Daniel Samson", bloodGroup, area,
                              city, state, country, '8309282168'], ["Samson", bloodGroup, area,
                                                                    city, state, country, '8309282168']
        val['len'] = range(len(val['details']))
        val['check'] = True
    else:
        if len(val['details']) == 0:
            val['details'] = None
            val['len'] = [0]
    return render(request, 'files/search.html', val)
