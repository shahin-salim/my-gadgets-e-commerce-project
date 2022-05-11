
from django.urls import path

from accounts.forms import add_address
from .import views
from django.conf.urls import url


urlpatterns = [

    path('addtowhishlist', views.AddToWhishlist, name='addtowhishlist'),  
    path('', views.Whishlist, name='whishlist'),  
    path('removefromwhishlist', views.RemoveFromWhishlist, name='removefromwhishlist'),  

]