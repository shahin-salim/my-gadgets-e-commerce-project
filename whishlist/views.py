from django.shortcuts import render
from django.views import View
from userApp.models import whishlist, VariantAndPrice, CustomUser
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from userApp.views import foundUser, GetCategory, countItems, SubCategory, GetCountWhishlist

# Create your views here.



# adding product to whishlist
def AddToWhishlist(request):
    status = False
    count = None
    if 'user'  in request.session:
        whishlist.objects.update_or_create(
            product_variant=VariantAndPrice.objects.get(id=request.GET['vari_id']),user_id=CustomUser.objects.get(username=request.session['user'])
        )
        status = True
        count = whishlist.objects.filter(
            user_id__username=request.session['user']).count()
    return JsonResponse({'status': status, 'whishlist_count': count})

# whishlist page view
def Whishlist(request):
    if not 'user' in request.session:
        return redirect('/login')
    items = whishlist.objects.filter(user_id__username=request.session['user'])

    context = {
        'session': foundUser(request),
        'category': GetCategory(),
        'cart_count': countItems(request),
        'subcat': SubCategory.objects.values('id', 'c_id__id', 'c_id__id', 'brand_name'),
        'items': items,
        'whishlist_count': GetCountWhishlist(request),
        'minBool': True,
        'whishlist_count': GetCountWhishlist(request)

    }

    return render(request, 'userTempl/whishlist.html', context)

# remove product from wishlist
def RemoveFromWhishlist(request):
    whishlist.objects.filter(id=request.GET['vari_id']).delete()
    return JsonResponse({'status': True,'whishlist_count':  whishlist.objects.filter(
        user_id__username=request.session['user']).count()})
