from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('home', views.home, name="home"),
    path('login', views.user_login, name="login"),
    path('signup', views.signup, name="signup"),
    path('profile', views.profile, name="profile"),
    path('search', views.search, name="search"),
    path('changepassword', views.changepassword, name="changepassword")
]
