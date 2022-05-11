from django.shortcuts import render
from  .verification import SendOTP, check
from django.http.response import JsonResponse
from userApp.views import foundUser, GetCategory, countItems, SubCategory, GetCountWhishlist, GetGuestUser, MoveGuestToUser
from django.shortcuts import redirect, render
from .forms import RegistrationForm, add_address, logForm, NumberOnly, OTPField
from django.views.decorators.cache import never_cache
from userApp.models import CustomUser, cart
from django.contrib.auth import authenticate

# Create your views here.


# resend otp  view
def ResendOtp(request):
    try:
        SendOTP("+91"+request.GET['num'])
    except:
        pass
    return JsonResponse({'status': True,})


# register page view
def register(request):
    if foundUser(request):
        return redirect('/')
    reg_form = RegistrationForm(request.POST or None)

    context1 = {
        'session': foundUser(request),
        'category': GetCategory(),
        'cart_count': countItems(request),
        'subcat': SubCategory.objects.values(
            'id', 'c_id__id', 'c_id__id', 'brand_name'),
    }

    if request.method == "POST":
        if reg_form.is_valid():
            data = reg_form.cleaned_data
            num = "+91" + data['number']
            try:
                SendOTP(num)
                request.session['num'] = data['number']
                f = reg_form.save(commit=False)
                f.is_active = 0
                f.save()
                return redirect('OTP_register')
            except:
                context2 = {'form': reg_form,
                            'url': '/accounts/register',
                            'err': 'enter valid number'}
                context = {**context1, **context2}
                return render(request, 'userTempl/register.html', context)
    context2 = {
        'form': reg_form,
        'url': '/accounts/register',
        'whishlist_count': GetCountWhishlist(request)

    }
    context = {**context1, **context2}
    return render(request, 'userTempl/register.html', context)



# send otp to twilio
@never_cache
def NumberField(request):
    if foundUser(request):
        return redirect('/')

    form = NumberOnly(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            getNum = request.POST['mobile_number']
            num = "+91" + getNum
            SendOTP(num)

            request.session['numberLog'] = getNum
            return redirect('enter_otp')
            
    context = {
        'session': foundUser(request),
        'category': GetCategory(),
        'cart_count': countItems(request),
        'subcat': SubCategory.objects.values('id', 'c_id__id', 'c_id__id', 'brand_name'),
        'form': form,
        'whishlist_count': GetCountWhishlist(request)
    }

    return render(request, "userTempl/enter_num.html", context)



# get otp from  user and check the number for twilio
@never_cache
def EnterOtp(request):
    if foundUser(request):
        return redirect('/')
    err = ''
    
    try:
        current_count = request.POST['current_count']
    except:
        current_count = 30

    form = OTPField(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            otp = request.POST['OTP']
            num = "+91" + request.session['numberLog']
            res = False
            try:
                res = check(otp, num)
            except:
                pass
            if res:
                # user = authenticate(number=num)
                u = CustomUser.objects.get(number=request.session['numberLog'])

                username = u.username
                request.session['user'] = username
                MoveGuestToUser(request)
                request.session['fullName'] = u.first_name +' '+ u.last_name 


                del request.session['numberLog']

                return redirect("home")
            else:
                err = "not a valid otp"

    context = {
        'session': foundUser(request),
        'category': GetCategory(),
        'cart_count': countItems(request),
        'subcat': SubCategory.objects.values('id', 'c_id__id', 'c_id__id', 'brand_name'),
        'form': form,
        'err': err,
        'url': '/accounts/enter_otp',
        'number': request.session['numberLog'],
        'whishlist_count': GetCountWhishlist(request),
        'current_count': current_count
    }
    return render(request, "userTempl/enter_otp.html", context)



# otp register for registration
@never_cache
def OTPRegister(request):
    if foundUser(request):
        return redirect('/')

    err = ''
    form = OTPField(request.POST or None, request.FILES or None)


    try:
        current_count = request.POST['current_count']
    except:
        current_count = 30


    if request.method == "POST":
        if form.is_valid():
            otp = request.POST['OTP']
            n = "+91" + request.session['num']
            if check(otp, n):
                u = CustomUser.objects.get(number=request.session['num'])
                u.is_active = 1
                u.save()
                del request.session['num']
                request.session['user'] = u.username

                request.session['fullName'] = u.first_name +' '+ u.last_name 


                if cart.objects.filter(guest_user=GetGuestUser(request)).exists():
                    MoveGuestToUser(request)

                return redirect("home")
            else:
                err = "not a valid otp"

    context = {
        'number': request.session['num'],
        'form': form,
        'err': err,
        'url': '/accounts/OTP_register',
        'session': foundUser(request),
        'category': GetCategory(),
        'cart_count': countItems(request),
        'subcat': SubCategory.objects.values('id', 'c_id__id', 'c_id__id', 'brand_name'),
        'whishlist_count': GetCountWhishlist(request),
        'current_count': current_count
    }

    return render(request, "userTempl/enter_otp.html", context)



# login page view
@never_cache
def login(request):
    if foundUser(request):
        return redirect('/')

    err = ''

    if request.method == "POST":
        form = logForm(request.POST)
        if form.is_valid():
            u_name = request.POST['username']
            u_pwd = request.POST['password']
            user = authenticate(username=u_name, password=u_pwd)
            if user is not None:
                ck = CustomUser.objects.get(username=u_name)
                if ck.block == 0:
                    request.session['user'] = u_name
                    request.session['fullName'] = ck.first_name +' '+ ck.last_name 

                    if cart.objects.filter(guest_user=GetGuestUser(request)).exists():

                        """
                        if user added product to cart as guset user these items move to user id and delete the session
                        id used in verify the the user
                        """
                        MoveGuestToUser(request)


                    return redirect('/')
                else:
                    err = 'you are blocked'
            else:
                err = 'user not found'
    else:
        form = logForm()

    context = {
        'session': foundUser(request),
        'category': GetCategory(),
        'cart_count': countItems(request),
        'subcat': SubCategory.objects.values(
            'id', 'c_id__id', 'c_id__id', 'brand_name'),
        'form': form,
        'err': err,
        'whishlist_count': GetCountWhishlist(request)
    }
    return render(request, 'userTempl/login.html', context)



# user logout view also delete the user session
def UserLogout(request):
    if foundUser(request):
        del request.session['user']
        del request.session['fullName']
    return redirect('/')




