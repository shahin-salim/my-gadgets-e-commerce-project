
from django.urls import path

from accounts.forms import add_address
from .import views
from django.conf.urls import url


urlpatterns = [
    path('', views.home, name='home'),

    path('eachproduct', views.eachproduct, name='eachproduct'),
    path('productlist', views.ProductList, name='ProductList'),
 

    path('cancell_order', views.CancellOreturn, name='cancell_order'),   

    path('editprofile', views.EditProfile, name='editprofile'),   
    path('profile', views.Profile, name='profile'),   
    path('changepassword', views.ChangePassword, name='changepassword'), 
    path('editaddress', views.EditAddress, name='editaddress'), 

    path('invoice/<limit>/', views.Invoice, name='invoice'), 

    # all  url related to sorting
    path('sortby/', views.SortBy, name='sortby'), 
    path('search', views.Search, name='search'),   
    
    path('changevariant', views.ChangeVariant, name='changevariant'),   
    path('orderdetails', views.Ordersdetials, name='orderdetails'),



]