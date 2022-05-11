
from django.urls import path
from .import views
from django.conf.urls import url


urlpatterns = [

    path('addtocart', views.AddToCart, name='Cart'),
    path('mycart', views.myCart, name='myCart'),
    path('changequantity', views.ChangeQuantity, name='changequantity'),
    path('remove_item_cart', views.removeIremFromCart, name='removeItemFromCart'),

]