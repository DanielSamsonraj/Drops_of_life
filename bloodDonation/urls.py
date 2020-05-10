from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('home', views.home, name="home"),
    path('login', views.user_login, name="login"),
    path('signup', views.signup, name="signup"),
    path('profile', views.profile, name="profile"),
    path('search', views.search, name="search"),
    path('changepassword', views.changepassword, name="changepassword"),
    path('logout', views.logout, name="logout"),
    path('forgotpassword', views.forgotpassword, name="forgotpassword"),
    path('enter_OTP', views.enter_OTP, name="enter_OTP"),
    path('editprofile', views.editprofile, name="editprofile"),
    path('new_password', views.new_password, name="new_password"),
    path('deleteaccount', views.deleteaccount, name="deleteaccount")
]
