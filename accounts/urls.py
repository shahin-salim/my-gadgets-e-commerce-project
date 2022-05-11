
from django.urls import path
from .import views
from django.conf.urls import url


urlpatterns = [

    path('resendotp', views.ResendOtp, name='resendotp'),  
    path('register', views.register, name='register'),
    path('number_field', views.NumberField, name='NumberField'),
    path('enter_otp', views.EnterOtp, name='enter_otp'),
    path('OTP_register', views.OTPRegister, name='OTP_register'),
    path('login', views.login, name='login'),
    path('userlogout', views.UserLogout, name='UserLogout'),

]