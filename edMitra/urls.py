from django.urls import path
from . import views
urlpatterns = [
    path('', views.home,name='home'),
    path('signup/', views.Sign_Up_Page,name='SignUp'),
    path('otp_verification/', views.otp_verification,name='verifyOTP'),
    path('login/', views.Login_page,name='Login'),
    path('logout/', views.logout_page,name='Logout'),
]