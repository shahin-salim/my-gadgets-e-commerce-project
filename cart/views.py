from django.shortcuts import render
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from pymysql import NULL
from django.contrib.auth import authenticate
# from use.models import CustomUser, cart
from userApp.models import CustomUser, cart
from adminApp.models import *
from django.db.models import Q, Sum
from django.views.decorators.cache import never_cache
from userApp.views import countItems, foundUser, GetGuestUser, FindSubTotal, GetCategory, GetCountWhishlist, isChanged

# Create your views here.


def AddToCart(request):
    varaintIs = VariantAndPrice.objects.get(id=request.GET['vari_id'])
    if foundUser(request):
        u = CustomUser.objects.get(username=request.session['user'])
        c = cart.objects.filter(Q(user_id=u) & Q(variant_id=varaintIs))
        if not c.exists():
            c.create(
                user_id=u, variant_id=varaintIs,
                subtotal=varaintIs.final_price
            )
        return JsonResponse(
            {'success': True, 'cart_count': countItems(request)},
            safe=False
        )
    else:
        if not cart.objects.filter(Q(guest_user=GetGuestUser(request)) & Q(variant_id=varaintIs)).exists():
            cart.objects.create(
                guest_user=GetGuestUser(request),
                variant_id=varaintIs,
                subtotal=varaintIs.final_price
            )
        return JsonResponse(
            {'success': True, 'cart_count': countItems(request)},
            safe=False
        )

# on click  the cart button go to cart


@never_cache
def myCart(request):
    if foundUser(request):
        isChanged(request)
        items = cart.objects.filter(user_id__username=request.session['user'])
    else:
        items = cart.objects.filter(guest_user=GetGuestUser(request))

    context = {
        'cartItems': items,
        'session': foundUser(request),
        'cart_sub': FindSubTotal(request),
        'category': GetCategory,
        'cart_count': countItems(request),
        'subcat': SubCategory.objects.values('id', 'c_id__id', 'c_id__id', 'brand_name'),
        'whishlist_count': GetCountWhishlist(request)
    }
    return render(request, 'userTempl/cart.html', context)


# change quatity of the product from the cart
def ChangeQuantity(request):
    c_id = request.GET['c_id']
    type = request.GET['type']
    cart_data = cart.objects.get(id=c_id)
    err = 'success'
    sub = 0
    if cart_data.quantity < cart_data.variant_id.quantity and 1 == int(type) or int(type) == -1 and cart_data.quantity > 1:

        cart_data.quantity = cart_data.quantity + int(type)
        q = cart_data.quantity
        cart_data.subtotal = cart_data.variant_id.final_price * cart_data.quantity
        sub = cart_data.subtotal
        cart_data.save()
        return JsonResponse(
            {'success': True, 'quantity': q, 'subtotal': sub,
                'cart_subtotal': FindSubTotal(request), 'err': err},
            safe=False
        )
    return JsonResponse(
        {'success': False, 'err': 'fails'},
        safe=False
    )

# remove items added in cart


def removeIremFromCart(request):
    cart_id = request.GET["c_id"]
    cart.objects.filter(id=cart_id).delete()
    return JsonResponse(
        {'success': True, 'cart_subtotal': FindSubTotal(
            request), 'cartCount': countItems(request)},
        safe=False
    )
