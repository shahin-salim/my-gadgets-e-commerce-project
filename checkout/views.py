from userApp.views import countItems, foundUser, FindSubTotal, GetCountWhishlist, isChanged
from django.shortcuts import render


from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from pymysql import NULL
from .forms import add_address
from django.contrib.auth import authenticate
from userApp.models import CustomUser, address, cart, order
from adminApp.models import *
from django.views.decorators.cache import never_cache
from ecom.settings import api_key, api_secret
import razorpay
client = razorpay.Client(auth=(api_key, api_secret))
from django.db.models import Q


# Create your views here.


"""
order placed view. transfer value form products table to order table.
this is only for if the usr buy the products added in cart
"""


def CartCalc(request, address_id, payMethod, coupenId=0):
    limit = 0
    u_id = CustomUser.objects.get(username=request.session['user'])
    cartItems = cart.objects.filter(user_id=u_id)

    coupenData = 0

    if coupenId:
        coupenData = Coupen.objects.get(id=coupenId)
    for i in cartItems:

        # produts are out of tock or the order qty more than orginal produts qty this produts excluding in purchasing
        if i.quantity <= i.variant_id.quantity and not i.variant_id.quantity <= 0:

            addr = address.objects.get(id=address_id)
            addre = 'Full name: ' + str(addr.full_name) + ' address: ' + str(addr.address) + ' city: ' + str(
                addr.city) + ' pincode: ' + str(addr.zipcode) + ' mobile: ' + str(addr.mobile_number)

            if coupenId:
                subtotal = i.subtotal - \
                    (i.subtotal * coupenData.coupen_offer) / 100
                order.objects.create(total_qty=i.quantity,  address=addre, userId=u_id,
                                     variant_id=i.variant_id, payment_method=payMethod,
                                     subtotal=subtotal, coupen_id=coupenData)

            else:
                order.objects.create(total_qty=i.quantity,  address=addre, userId=u_id,
                                     variant_id=i.variant_id, payment_method=payMethod,
                                     subtotal=i.subtotal)

            v = VariantAndPrice.objects.filter(id=i.variant_id_id).update(
                quantity=i.variant_id.quantity - i.quantity)
            i.delete()
            limit += 1
    return limit


# set values into order palced table in the case of buy now.
def BuyNowCalc(request, address_id, payMethod, coupenId=0):
    v = request.POST['variant']
    u_id = CustomUser.objects.get(username=request.session['user'])
    coupenData = 0

    if coupenId:
        coupenData = Coupen.objects.get(id=coupenId)

    i = VariantAndPrice.objects.get(id=v)
    addr = address.objects.get(id=address_id)
    addre = 'Full name: ' + str(addr.full_name) + ' address: ' + str(addr.address) + ' city: ' + str(
        addr.city) + ' pincode: ' + str(addr.zipcode) + ' mobile: ' + str(addr.mobile_number)
    i.quantity = i.quantity - 1
    orders = order()
    orders.total_qty = 1
    orders.address = addre
    orders.userId = u_id
    orders.variant_id = i
    orders.payment_method = payMethod
    if coupenId:
        orders.subtotal = i.final_price - \
            (i.final_price * coupenData.coupen_offer) / 100
        orders.coupen_id = coupenData
    else:
        orders.subtotal = i.final_price
    orders.save()
    i.save()
    return 1

# delte user address. profile side address delete option and delete option in chekout have same view


def DelAddressFromCheckout(request):
    id = request.GET['address_id']
    address.objects.filter(id=id).delete()
    return JsonResponse({'success': True}, safe=False)


# checkout page. check the user wants to buy the products form the cart or the buy now
@never_cache
def Checkout(request, id=0):
    if 'user' not in request.session:
        return redirect('login')
    isChanged(request)

    context = {}
    context2 = {}
    form = add_address()
    addresses = address.objects.filter(
        user_id__username=request.session['user']
    ).order_by(
        "-id"
    ).values('full_name', 'city', 'mobile_number', 'zipcode', 'address', 'id'
             )
    context1 = {
        'form': form,
        'url': '/checkout/addressForm',
        'addresses': addresses,
        'session': foundUser(request),
        'category': Category.objects.all(),
        'cart_count': countItems(request),
        'subcat': SubCategory.objects.values('id', 'c_id__id', 'c_id__id', 'brand_name'),
        'whishlist_count': GetCountWhishlist(request)

    }

    # if the received id is 0 it will assumed as user clicked the cart checkout button
    if int(id) == 0:
        context2 = {
            'cartItems': cart.objects.filter(
                user_id__username=request.session['user']).values(
                    'variant_id__price',
                    'variant_id__final_price',
                    'variant_id__product_id__offer',
                    'variant_id__product_id__brand_id__c_id__offer',
                    'variant_id__product_id__product_name',
                    'variant_id__product_id__brand_id__brand_name',
                    'quantity',
                    'variant_id__quantity',
                    'subtotal'
            ),
            'cart_subtotal': FindSubTotal(request),
            'from': id
        }
        context2['raz_amt'] = context2['cart_subtotal'] * 100

    elif int(id) > 0:
        # ..................................................................................................
        """
        # if user clicked the buy now option the varaint id will be pass. definately the value is greater than 0.
        # so programm asume that user is cliked buy now
        """
        v = VariantAndPrice.objects.get(id=id)
        context2 = {
            'items': v,
            'buynow': True,
            'from': id,
            'whishlist_count': GetCountWhishlist(request)
        }
        context2['raz_amt'] = v.final_price * 100
        # ..................................................................................................

    context = {**context1, **context2}

    r = int(context['raz_amt'])
    request.session['raz_amt'] = r
    return render(request, 'userTempl/checkout.html', context)


# validating address form placed in checkout page
def addressForm(request):
    form = add_address(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            f = form.save(commit=False)
            f.user_id = CustomUser.objects.get(
                username=request.session['user'])
            f.save()
            return JsonResponse(
                {'success': True},
                safe=False
            )
    return JsonResponse(
        {'success': False},
        safe=False
    )


# passing order details set data in order table. finding which option user choosen and redirect to corrent function
def MakePayment(request):
    payMethod = request.POST['paymentMethod']
    address_id = request.POST['addressId']
    buyOrCart = request.POST['from']
    coupenId = request.POST.get('coupenId' or 0)

    if buyOrCart == "cart":
        # funtion for products buyed from cart
        limit = CartCalc(request, address_id, payMethod, coupenId)
    else:
        # funtion if user buyed using buy now option
        limit = BuyNowCalc(request, address_id, payMethod, coupenId)

    return redirect('/invoice/'+str(limit))


# amount for product is pas to razorpay when using click checkout option
def RazorpaySetAmt(request):
    raz_amt = request.session['raz_amt']
    try:
        DATA = {
            "amount": raz_amt,
            "currency": "INR",
            "receipt": "receipt#1",
            "notes": {
                "key1": "value3",
                "key2": "value2"
            }
        }
        orders = client.order.create(data=DATA)
        ordersid = orders['id']
        return JsonResponse({'status': 'success', 'ordersid': ordersid, 'payable_amt': raz_amt})
    except:
        return JsonResponse({'status': 'fails'})



# checking coupen is exist and if the user is used the coupen.
def AddCoupen(request):
    choosen = request.POST.get('choosen' or None)
    code = request.POST['coupen-code']
    err = 'fails'

    if Coupen.objects.filter(coupen_code=code).exists(): #check coupen exist in coupen table
        err = 'success'
        coupen = Coupen.objects.get(coupen_code=code)

        # checking if user already used this coupen . if user used coupen id is presented in order table  
        if not order.objects.filter(Q(coupen_id=coupen) & Q(userId=CustomUser.objects.get(username=request.session['user']))).exists():

            if VariantAndPrice.objects.filter(id=choosen).exists(): # if user id found in variant user selected buy now option

                v = VariantAndPrice.objects.get(id=choosen)
                finalPrice = v.final_price - \
                    (v.final_price * coupen.coupen_offer) / 100

            else: # user going buy product from cart

                val = FindSubTotal(request)
                finalPrice = val - (val * coupen.coupen_offer) / 100

            request.session['raz_amt'] = finalPrice * 100 # save the amt for razorpay payment

            return JsonResponse(
                {
                    'success': True,
                    'err': err,
                    'finalprice': finalPrice,
                    'offerIs': coupen.coupen_offer,
                    'coupenId': coupen.id,
                    # 'data-order_id': ordersid

                }, safe=False)

    return JsonResponse({'success': False, 'err': 'coupen code not found'},
                        safe=False)