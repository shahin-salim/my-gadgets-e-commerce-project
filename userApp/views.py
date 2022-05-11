
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from pymysql import NULL
from accounts.forms import RegistrationForm, add_address, logForm, NumberOnly, OTPField
from django.contrib.auth import authenticate
from .models import CustomUser, address, cart, order, whishlist
from adminApp.models import *
from django.db.models import Q, Sum
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.decorators.cache import never_cache



"""
guest user functionality. using browser session for identify user. return the 
browser session id if dont have create the id
"""
def GetGuestUser(request):
    key = request.session.session_key
    if not key:
        request.session.create()
    return key


"""
after user logged in and if user added products into cart as a guset user
set foreign key into the user_id field and delete browser session id
and if the products alredy in the user id the quantity increse accordingly
"""
def MoveGuestToUser(request):
    cartItems = cart.objects.filter(guest_user=GetGuestUser(request))
    u = CustomUser.objects.get(username=request.session['user'])

    for items in cartItems:
        if cart.objects.filter(Q(user_id=u) & Q(variant_id=items.variant_id)).exists():
            a = cart.objects.get(Q(user_id=u) & Q(variant_id=items.variant_id))
            a.quantity = items.quantity + a.quantity
            a.subtotal = items.subtotal + a.subtotal
            a.save()
            items.delete()

    cartItems.update(user_id=u, guest_user=NULL)


# get all category data for reuse
def GetCategory():
    cat = Category.objects.all()
    return cat


"""
finding the user if user is online or offline or blocked.
if blocked delete the session so user will automatically logout
"""
def foundUser(request):
    if 'user' in request.session:
        u = CustomUser.objects.get(username=request.session['user'])
        if u.block == True:
            del request.session['user']
            return False
        return True
    return False


# def countItems(req): return  if 'user' in req.session else guest_user=req.session['user']).count()
def countItems(request):
    try:
        count = cart.objects.filter(
            user_id__username=request.session['user']).count()
    except:
        count = cart.objects.filter(guest_user=GetGuestUser(request)).count()
    return count


# find subtotal
def FindSubTotal(request):
    try:
        usersProduct = cart.objects.filter(user_id__username=request.session['user']).values(
            'quantity', 'variant_id__quantity', 'subtotal')
    except:
        usersProduct = cart.objects.filter(guest_user=GetGuestUser(request)).values(
            'quantity', 'variant_id__quantity', 'subtotal')

    cart_subtoal = 0
    for i in usersProduct:
        if i['quantity'] <= i['variant_id__quantity']:
            cart_subtoal += i['subtotal']
    return cart_subtoal






# get count of user whishlist if user is in the session
def GetCountWhishlist(request):
    return whishlist.objects.filter(user_id__username=request.session['user']).count() if 'user' in request.session else 0


# home  page with data latest and popular product
@never_cache
def home(request):
    latest = []
    byCategory = []
    avilable_cat = []
    p = products.objects.all().order_by('-date').select_related('product_id__brand_id').select_related('product_id__brand_id__c_id')


    for i in Category.objects.all():
        count = 0

        filterProduct = p.filter(brand_id__c_id=i).order_by('-date').values('id')


        for a in filterProduct:

            count += 1
            variants = VariantAndPrice.objects.filter(product_id__id=a['id']).select_related(
                'product_id').select_related('product_id__brand_id').select_related('product_id__brand_id__c_id')
            
            # ---------------------------------------------------------------------------
            """
            every product have 2 variant it will diaply according which product have least ram.
            is the produt have least ram is out of stock the other varaint is going to display
            """
            temp = variants[0]
            if variants[0].quantity == 0 and variants[1].quantity > 0:
                temp = variants[1]
            # --------------------------------------------------------------------------------
            
            if i not in avilable_cat:
                avilable_cat.append(i)

            byCategory.append(temp)
            latest.append(temp)
            if count == 4:
                break


    context = {
        'latest': latest[:4],
        'session': foundUser(request),
        'category': GetCategory(),
        'banner': Banner.objects.all().select_related('p_id'),
        'cart_count': countItems(request),
        'subcat': SubCategory.objects.values('id', 'c_id__id', 'c_id__id', 'brand_name'),
        'bycategory': byCategory,
        'whishlist_count': GetCountWhishlist(request),
        'avilable_cat': avilable_cat
    }
    return render(request, 'userTempl/sampleHome.html', context)


# showing the product user clicked in the each product page
def eachproduct(request):

    vari = VariantAndPrice.objects.filter(
        product_id=request.GET['p_id']).select_related(
            'product_id'
    ).select_related(
            'product_id__brand_id'
    ).order_by('variant')

    prod = products.objects.filter(id=request.GET['p_id'])

    context = {
        'product': prod,
        'variants': vari,
        'varinat1': vari[0],
        'session': foundUser(request),
        'category': GetCategory(),
        'cart_count': countItems(request),
        'subcat': SubCategory.objects.values('id', 'c_id__id', 'c_id__id', 'brand_name'),
        'whishlist_count': GetCountWhishlist(request)
    }

    return render(request, 'userTempl/eachproduct.html', context)



# covert string into listfor product filtering. data passed  as string from html form. coverting into list for giving in orm
def splitString(request, inp):
    temp = request.GET[inp].split(',')
    for i in range(len(temp)):
        try:
            temp[i] = int(temp[i])
        except:
            temp[i] = temp[i]
    return temp


"""
get product variant according to quantity. if one varaint is out of stock get it will return another variant for lsiting 
product data in the home page and product list page
"""
def ReturnList(prod):
    vari = []
    for i in prod:
        allVari = VariantAndPrice.objects.filter(product_id=i)
        vari += [allVari[0]] if allVari[0].quantity else [allVari[1]]
    return vari


"""
listing all product in this page . also included product sorting  option .
"""
@never_cache
def ProductList(request):
    minBool = False
    sort_by_category = request.GET.get('c_id' or 0)
    sort_by_subcategory = request.GET.get('sub_id' or 0)
    min = request.GET.get('min' or 0)

    vari = []

    if sort_by_category:
        prod = products.objects.filter(
            brand_id__c_id__id=sort_by_category).values_list('id')
        vari = ReturnList(prod)

    elif sort_by_subcategory:
        prod = products.objects.filter(
            brand_id__id=sort_by_subcategory).values_list('id')
        vari = ReturnList(prod)

    elif min:
        minBool = True
        category = splitString(request, 'category')
        brand = splitString(request, 'brand')
        ramIs = splitString(request, 'ram')
        processor = splitString(request, 'processor')

        vari = VariantAndPrice.objects.filter(
            Q(product_id__brand_id__c_id__id__in=category) &
            Q(product_id__brand_id__id__in=brand) &
            Q(variant__in=ramIs) &
            Q(price__gte=request.GET['min']) &
            Q(price__lte=request.GET['max']) &
            Q(product_id__processor__in=processor) 
        ).all()

    else:
        prod = products.objects.values_list('id').all()
        vari = ReturnList(prod)

    paginator = Paginator(vari, 6)
    page = request.GET.get('page')
    pageUrl = request.build_absolute_uri().replace('page='+str(page), '')
    try:
        a = paginator.page(page)
    except PageNotAnInteger:
        a = paginator.page(1)
    except EmptyPage:
        a = paginator.page(paginator.num_pages)

    context = {
        'allProducts': a,
        'category': Category.objects.all(),
        'ram': VariantAndPrice.objects.values("variant").distinct(),
        'processor': VariantAndPrice.objects.values("product_id__processor").distinct(),
        'brand': SubCategory.objects.all(),
        'session': foundUser(request),
        'cart_count': countItems(request),
        'page': page,
        'pageUrl': pageUrl,
        'minBool': minBool,
        'subcat': SubCategory.objects.values('id', 'c_id__id', 'c_id__id', 'brand_name'),
        'whishlist_count': GetCountWhishlist(request)
    }
    return render(request, 'userTempl/product-grids.html', context)



# checks if the product offer changed if changed change price accordingly
def isChanged(request):
    try:
        c = cart.objects.filter(
            user_id__username=request.session['user']).select_related(
                'variant_id'
        )
    except:
        c = cart.objects.filter(
            guest_user=GetGuestUser(request)).select_related(
                'variant_id'
        )
    for a in c:
        # off = 0
        if a.variant_id.final_price != a.subtotal / a.quantity:
            a.subtotal = a.variant_id.final_price * a.quantity
            a.save()



# cancell and return from order deatails page
def CancellOreturn(request):

    val = request.GET['val']
    ord = order.objects.get(id=request.GET['id'])
    if val == "Cancel":
        ord.order_status = "Cancelled" 
    else:
        ord.order_status = "Returned"

    v_id = ord.variant_id
    vari = VariantAndPrice.objects.get(id=v_id.id)
    vari.quantity = vari.quantity + 1
    vari.save()
    ord.save()

    return JsonResponse(
        {'success': True},
        safe=False
    )


# search bar
def Search(request):
    p = products.objects.filter(product_name__icontains=request.GET['input'])
    vari = []
    for i in p:
        vari += [VariantAndPrice.objects.filter(product_id=i)[0]]
    context = {
        'allProducts': vari,
        'brand': SubCategory.objects.all(),
        'ram': VariantAndPrice.objects.values("variant").distinct(),
        'session': foundUser(request),
        'category': Category.objects.all(),
        'brand': SubCategory.objects.all(),
        'session': foundUser(request),
        'cart_count': countItems(request),
        'whishlist_count': GetCountWhishlist(request)
    }
    return render(request, 'userTempl/product-grids.html', context)


# profile page
@never_cache
def Profile(request):
    if 'user' not in request.session:
        return redirect('login')
    form = add_address()
    user = CustomUser.objects.get(username=request.session['user'])
    context = {
        'user': user,
        'address': address.objects.filter(user_id=user).order_by("-id"),
        'session': foundUser(request),
        'form': form,
        'cart_count': countItems(request),
        'category': Category.objects.all(),
        'subcat': SubCategory.objects.values('id', 'c_id__id', 'c_id__id', 'brand_name'),
        'whishlist_count': GetCountWhishlist(request)
    }
    return render(request, 'userTempl/profile.html', context)


# edit profile info 
def EditProfile(request):
    err_username = ''
    err_email = ''
    err_number = ''
    good = 0

    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    number = request.POST['number']

    if request.method == "POST":
        if username != request.session['user'] and CustomUser.objects.filter(username=username).exists():
            err_username = 'username alredy exist'
            good += 1

        if CustomUser.objects.filter(email=email).exclude(username=request.session['user']).exists():
            err_email = 'email exist'
            good += 1

        if CustomUser.objects.filter(number=number).exclude(username=request.session['user']).exists():
            err_number = 'number alredy exist'
            good += 1

        if good == 0:
            u_id = CustomUser.objects.filter(username=request.session['user'])
            u_id.update(
                first_name=first_name, last_name=last_name, username=username, email=email, number=number)
            return JsonResponse(
                {'success': True},
                safe=False
            )
        return JsonResponse(
            {'success': False, 'username': err_username,
                'email': err_number, 'number': err_number},
            safe=False
        )


# change password option in profile 
def ChangePassword(request):

    old_pwd = request.POST['old_pwd']
    new_pwd = request.POST['new_pwd']

    if request.method == "POST":
        user = authenticate(username=request.session['user'], password=old_pwd) # validating the previous password with authenticate method
        if user:
            u = CustomUser.objects.get(username=request.session['user'])
            u.set_password(new_pwd)
            u.save()

            return JsonResponse(
                {'success': True},
                safe=False
            )
        return JsonResponse(
            {'success': False},
            safe=False
        )


# edit address details
def EditAddress(request):
    if request.method == "POST":
        id = request.POST['address_id']
        currentUrl = request.POST['currentUrl']
        form = add_address(request.POST, instance=address.objects.get(id=id))
        if form.is_valid():
            form.save()
            return redirect(currentUrl)
    else:
        id = request.GET['address_id']
        currentUrl = request.GET['currentUrl']
        form = add_address(instance=address.objects.get(id=id))

    context = {
        'url': '/editaddress',
        'form': form,
        'address_id': id,
        'currentUrl': currentUrl,
        'session': foundUser(request),
        'whishlist_count': GetCountWhishlist(request)
    }
    return render(request, 'userTempl/register.html', context)


# invoice page. render this page after payment with the details product purchased
@never_cache
def Invoice(request, limit):
    OrderData = order.objects.filter(
        userId__username=request.session['user']).order_by('-date')[:int(limit)].values(
        'address', 'order_status', 'date', 'order_id',
        'variant_id__product_id__brand_id__brand_name', 'variant_id__product_id__product_name',
        'variant_id__variant', 'subtotal', 'total_qty', 'payment_method')

    data = OrderData[0]
    total = OrderData.aggregate(Sum('subtotal'))
    context = {
        'order': OrderData,
        'oneorder': data,
        'total': total,
        'category': Category.objects.all(),
        'session': foundUser(request),
        'cart_count': countItems(request),
        'subcat': SubCategory.objects.values('id', 'c_id__id', 'c_id__id', 'brand_name'),
        'whishlist_count': GetCountWhishlist(request)
    }
    return render(request, 'userTempl/invoice.html', context)



# sort by popularity, low-to-high and high-to-low in the product list page
@never_cache
def SortBy(request):
    inp = request.GET.get('sortby', None)
    v = []

    if inp == 'popularity':
        o = order.objects.exclude(variant_id=None).values('variant_id').annotate(
            c=Sum('total_qty')).order_by('-c')
        for i in o:
            v += [VariantAndPrice.objects.get(id=i['variant_id'])]
    elif inp == 'low-high':
        v = VariantAndPrice.objects.select_related(
            'product_id').order_by('final_price')
    elif inp == 'high-low':
        v = VariantAndPrice.objects.select_related(
            'product_id').order_by('-final_price')

    paginator = Paginator(v, 6)
    page = request.GET.get('page')
    pageUrl = request.build_absolute_uri().replace('page='+str(page), '')
    try:
        a = paginator.page(page)
    except PageNotAnInteger:
        a = paginator.page(1)
    except EmptyPage:
        a = paginator.page(paginator.num_pages)

    context = {
        'allProducts': a,
        'brand': SubCategory.objects.all(),
        'ram': VariantAndPrice.objects.values("variant").distinct(),
        'category': Category.objects.all(),
        'session': foundUser(request),
        'cart_count': countItems(request),
        'pageUrl': pageUrl,
        'minBool': True,
        'subcat': SubCategory.objects.values('id', 'c_id__id', 'c_id__id', 'brand_name'),
        'whishlist_count': GetCountWhishlist(request)
    }

    return render(request, 'userTempl/product-grids.html', context)


# changing variant price and quantity according to user click on the variant in the each variant
def ChangeVariant(request):
    variantId = request.GET['variantId']
    vId = VariantAndPrice.objects.get(id=variantId)
    return JsonResponse(
        {
            'success': True,
            'pfinalprice': vId.final_price,
            'price': vId.price,
            'currentQuantity': vId.quantity,
            'currentRam': vId.variant
        },
        safe=False
    )


# order deials view
@never_cache
def Ordersdetials(request):
    order_data = order.objects.filter(
        userId__username=request.session['user']
    ).values(
        'userId__username',
        'date',
        'order_status',
        'subtotal',
        'variant_id__variant',
        'variant_id__product_id__product_name',
        'variant_id__product_id__brand_id__brand_name',
        'address',
        'payment_method',
        'total_qty',
        'variant_id__product_id__img1',
        'id'
    ).order_by('-date')

    paginator = Paginator(order_data, 10)
    page = request.GET.get('page')
    try:
        a = paginator.page(page)
    except PageNotAnInteger:
        a = paginator.page(1)
    except EmptyPage:
        a = paginator.page(paginator.num_pages)

    context = {
        'orderdetials': a,
        'ram': VariantAndPrice.objects.values("variant").distinct(),
        'category': Category.objects.all(),
        'brand': SubCategory.objects.all(),
        'session': foundUser(request),
        'cart_count': countItems(request),
        'page': page,
        'whishlist_count': GetCountWhishlist(request)
    }
    return render(request, 'userTempl/orders.html', context)
