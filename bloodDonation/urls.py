from django.urls import path
from . import views

urlpatterns = [
    path('',views.home),
    path('home',views.home),
    path('login',views.login),
    path('signup',views.signup),
    path('profile',views.profile),
    path('search',views.search)
] 
