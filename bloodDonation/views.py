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
        status = "NO"
        if password == password1:
            obj = donarDetails(
                name=Name,
                email=email,
                password=password,
                availiability_status=status,
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
    val['check'] = True
    val['initialCheck'] = False
    if request.method == 'POST':
        bloodGroup = request.POST['bg']
        area = request.POST['area']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']

        # fecthing data

        data = donarDetails.objects.all()
        status_check = donarDetails.objects.filter().values()
        available_donors = []
        temp_list = []
        for values in status_check:
            temp_list.append(list(values.values()))
        for details in temp_list:
            if details[4] == "NO":
                details[4] = None
            available_donors.append(
                [details[1], details[4], details[5], details[6], details[7]])
        val['details'] = available_donors

        # print(val['details'])

        val['table_headers'] = ["Name", "Availiability Status",
                                "Blood Group", "Contact No", "Address"]
        val['initialCheck'] = True
    else:
        val['details'] = None
        val['len'] = []
    return render(request, 'files/search.html', val)
