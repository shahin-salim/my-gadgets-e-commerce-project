
from django.urls import path

from accounts.forms import add_address
from .import views
from django.conf.urls import url


urlpatterns = [

    path('<id>/', views.Checkout, name='checkout'),
    path('addressForm', views.addressForm, name='addressForm'),
    path('makepayment', views.MakePayment, name='makepayment'),
    path('DelAddressFromCheckout', views.DelAddressFromCheckout, name='DelAddressFromCheckout'), 
    path('razorpaysetamt', views.RazorpaySetAmt, name='razorpaysetamt'),   
    path('addcoupen', views.AddCoupen, name='AddCoupen'),   

]