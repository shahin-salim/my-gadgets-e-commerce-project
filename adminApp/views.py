
from datetime import datetime
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from userApp.models import CustomUser, order
from .forms import *
from .models import *
from django.db.models import Count, Q, Sum
from accounts.forms import logForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from userApp.models import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import xlwt
from django.views.decorators.cache import never_cache


# add offer for products according to category
def addoff(v):
    for i in v:
    
        CategoryOffer = i['product_id__brand_id__c_id__offer']
        ProductOffer = i['product_id__offer']
        VariantPrice = i['price']
        if CategoryOffer > ProductOffer:
            value = VariantPrice - (VariantPrice * CategoryOffer) / 100

        else:
            VariantPrice = i['price']
            value = VariantPrice - (VariantPrice * ProductOffer) / 100

        if i['final_price'] != value:
            if not value:
                value = i['price']
            VariantAndPrice.objects.filter(
                id=i['id']).update(final_price=value)


# admin login page and validations
@never_cache
def AdminLogin(request):
    if request.user.is_authenticated:
        return redirect('/admin_side')

    form = logForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            admin = authenticate(
                username=request.POST['username'], password=request.POST['password'])
            
            if admin:
                login(request, admin)
                return redirect("/admin_side")
    return render(request, 'adminTempl/adminLogin.html', {'form': form})


# admin logout view
@never_cache
@login_required(login_url='/admin_side/admin_login')
def AdminLogout(request):
    logout(request)
    return redirect('/admin_side/admin_login')


# admin dashboard . collecting all the data the admin dashboard
@never_cache
@login_required(login_url='/admin_side/admin_login')
def Dashboard(request):
    context = {}
    try:
        # mothly earning
        delivered = order.objects.filter(order_status="Delivered").count()
        pending = order.objects.filter(Q(order_status="Delivered") | Q(
            order_status="shipped") | Q(order_status="Order Placed")).count()

        # daily sales
        dialy_sales = order.objects.values('date__day', 'date__month', 'date__year').filter(
            order_status="Delivered").annotate(Sum('subtotal')).order_by('-date__date')[:7]
        
        # current user count
        user_count = CustomUser.objects.filter(is_superuser=0).count()

        # montly sales data
        monthly_sales = order.objects.values('date__month').filter(
            order_status="Delivered").annotate(Sum('subtotal'))[:4]

        # payment method most choosen
        method = order.objects.values('payment_method').filter(
            order_status="Delivered").annotate(Count('payment_method'))

        # all order status date
        status = order.objects.values(
            'order_status').annotate(Count('order_status'))

        # sales based on month
        sales_this_month = order.objects.values('date__month').filter(
            order_status="Delivered").annotate(Sum('subtotal')).order_by('-date__month')[0]

        # money earned current month
        sales_month = sales_this_month['subtotal__sum']

        # pending orders
        pending = order.objects.filter(
            Q(order_status='shipped') | Q(order_status='Order Placed')).count()

        context = {
            'daily_sales': dialy_sales,
            'method': method,
            'monthly_sales': monthly_sales,
            'status': status,
            'sales_this_month': sales_month,
            'pending': pending,
            'user_count':user_count,
            'today_earning': dialy_sales[0]['subtotal__sum']
            }
    except:
        pass

    return render(request, 'adminTempl/charts.html', context)

# user details view
@never_cache
@login_required(login_url='/admin_side/admin_login')
def UserManagement(request):
    UserData = CustomUser.objects.filter(is_superuser=0)
    return render(request, 'adminTempl/usertable.html', {'user': UserData})


# block and unblock user
@never_cache
@login_required(login_url='/admin_side/admin_login')
def BlockAndUnblock(request):
    u = CustomUser.objects.get(id=request.GET.get('id'))
    u.block = not(u.block)
    u.save()
    return redirect('/admin_side/user')


# add  product category (os)
@never_cache
@login_required(login_url='/admin_side/admin_login')
def AddCategory(request):

    form = CategoriesForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('/admin_side/category')
    # form = CategoriesForm(initial={'id': 0})
    return render(request, 'adminTempl/admin_form.html', {'form': form, 'url': '/admin_side/addcategory/'})


# update product category(os)
@never_cache
@login_required(login_url='/admin_side/admin_login')
def UpdateCategory(request):

    if request.method == 'POST':
        id = request.POST.get('product_id')
        cate = Category.objects.get(id=id)
        form = CategoriesForm(request.POST, instance=cate , initial={'id': id})
        if form.is_valid():
            form.save()
            return redirect('/admin_side/category')
    else:
        id = request.GET['id']
        cate = Category.objects.get(id=id)

        form = CategoriesForm(instance=cate, initial={'id': id})

    return render(request, 'adminTempl/admin_form.html', {'form': form, 'url': '/admin_side/updatecategory/', 'product_id': id})


# category and subcatogory data .  2 of them set in the same page (os and brand)
@never_cache
@login_required(login_url='/admin_side/admin_login')
def CategoryAndSubCategory(request):
    return render(request, 'adminTempl/category.html', {'category': Category.objects.all(), 'subcategory': SubCategory.objects.all()})


# delete product category(os)
@never_cache
@login_required(login_url='/admin_side/admin_login')
def DeleteCategory(request):
    Category.objects.filter(id=request.GET['id']).delete()
    return redirect("/admin_side/category")


# add subcategory(brand) view
@never_cache
@login_required(login_url='/admin_side/admin_login')
def AddSubCategory(request):
    form = SubCategoriesForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('/admin_side/category')
    else:
        form = SubCategoriesForm(initial={'id': 0})
    return render(request, 'adminTempl/admin_form.html', {'form': form, 'url': '/admin_side/addsubcategory/'})


# update subcategory(brand) of product
@never_cache
@login_required(login_url='/admin_side/admin_login')
def UpdateSubCategory(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        cate = SubCategory.objects.get(id=id)
        form = SubCategoriesForm(request.POST, instance=cate)
        if form.is_valid():
            form.save()
            return redirect('/admin_side/category')
    else:
        id = request.GET['id']
        cate = SubCategory.objects.get(id=id)
        form = SubCategoriesForm(instance=cate)

    return render(request, 'adminTempl/admin_form.html', {'form': form, 'url': '/admin_side/updatesubcategory/', 'id': id})


# delete subcategory view (brand)
@never_cache
@login_required(login_url='/admin_side/admin_login')
def DeleteSubCategory(request):
    SubCategory.objects.filter(id=request.GET['id']).delete()
    return redirect("/admin_side/category")


# listing all products data on product.html
@never_cache
@login_required(login_url='/admin_side/admin_login')
def AllProducts(request):

    pro = products.objects.all()

    final = []
    for i in pro:
        temp = []
        var = VariantAndPrice.objects.filter(product_id=i)
        a = [i.product_name, i.back_camera, i.battery,
             i.brand_id.brand_name, i.date, i.front_camera, i.rom]

        for j in var:
            # temp[j.variant] = j.price
            a.append(j.variant)
            a.append(j.price)
            a.append(j.quantity)

        a.append(i.id)
        final.append(a)

    return render(request, 'adminTempl/products.html', {'products': final})


# add product form its contain 3 form which are product form and 2 variant forn
@never_cache
@login_required(login_url='/admin_side/admin_login')
def AddProducts(request):
    product = ProductForm(request.POST or None, request.FILES or None)
    variant_1 = VariantForm(request.POST or None, request.FILES or None)
    variant_2 = VariantForm2(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if product.is_valid() and variant_1.is_valid() and variant_2.is_valid():
            product.save()

            a = products.objects.all().last()
            v1 = variant_1.save(commit=False)
            v1.product_id = a
            v1.save()
            v2_data = variant_2.cleaned_data
            second = VariantAndPrice(
                variant=v2_data['nameOfVariant'], price=v2_data['priceOfVariant'], product_id=a, quantity=v2_data['quantity_2'])
            second.save()

            v = VariantAndPrice.objects.filter(
                product_id__id=a.id).values('price', 'final_price', 'product_id__offer', 'product_id__brand_id__c_id__offer', 'id')

            addoff(v)

            return redirect("/admin_side/allproducts")

    context = {
        "form": product,
        'url': '/admin_side/addproducts/',
        'variant_1': variant_1,
        'variant_2': variant_2,
        'title': 'Add Products',
    }

    return render(request, 'adminTempl/productForm.html', context)


# delete product listed in the prodcuct page
@never_cache
@login_required(login_url='/admin_side/admin_login')
def DelProduct(request):
    products.objects.filter(id=request.GET['id']).delete()
    return redirect("/admin_side/allproducts")


# update all product details. these are product data from product table variant data from variant table
@never_cache
@login_required(login_url='/admin_side/admin_login')
def UpdateProduct(request):

    if request.method == "POST":

        product_id = request.POST['product_id']
        prod = products.objects.get(id=product_id)
        v1 = VariantAndPrice.objects.filter(product_id=prod)
        id = v1[1].id
        product_fm = ProductForm(request.POST, request.FILES, instance=prod)
        variant_1 = VariantForm(request.POST, instance=v1[0])
        variant_2 = VariantForm2(request.POST)

        if product_fm.is_valid() and variant_1.is_valid() and variant_2.is_valid():
            product_fm.save()
            v1 = variant_1.save()
            v2_data = variant_2.cleaned_data
            VariantAndPrice.objects.filter(id=id).update(
                variant=v2_data['nameOfVariant'], price=v2_data['priceOfVariant'], quantity=v2_data['quantity_2'])

            v = VariantAndPrice.objects.filter(
                product_id__id=product_id).values('price', 'final_price', 'product_id__offer', 'product_id__brand_id__c_id__offer', 'id')

            # funtion for adding offer for the product
            addoff(v)

            return redirect("/admin_side/allproducts")

    else:

        product_id = request.GET.get('id')
        prod = products.objects.get(id=product_id)
        product_fm = ProductForm(instance=prod)
        v1 = VariantAndPrice.objects.filter(product_id=prod)
        variant_1 = VariantForm(instance=v1[0])
        a = v1[1].variant
        b = v1[1].price
        c = v1[1].quantity

        variant_2 = VariantForm2(
            initial={'nameOfVariant': a, 'priceOfVariant': b, 'quantity_2': c})

    context = {
        "form": product_fm,
        'url': '/admin_side/updateproduct/',
        'variant_1': variant_1,
        'variant_2': variant_2,
        'title': 'Update Products',
        'product_id': product_id,
        'prod': prod
    }

    return render(request, 'adminTempl/productForm.html', context)


# view all the order details user made
@never_cache
@login_required(login_url='/admin_side/admin_login')
def ViewOrder(request):
    orders = order.objects.values(
        'total_qty','order_status','userId_id__username','variant_id__product_id__product_name',
        'variant_id__product_id__brand_id__brand_name','variant_id__variant','address','subtotal','date','id'
    )
    return render(request, 'adminTempl/orderTable.html', {'order': orders})


# change order status like (ordered, shipped, delivered and cancell)
@never_cache
@login_required(login_url='/admin_side/admin_login')
def OrderStatus(request):

    if "Admin cancell" == request.GET['val']:
        ord = order.objects.get(id=request.GET['id'])
        ord.order_status = "Admin cancell"

        v_id = ord.variant_id
        vari = VariantAndPrice.objects.get(id=v_id.id)
        vari.quantity = vari.quantity + 1
        vari.save()
        ord.save()

        return JsonResponse(
            {'success': True},
            safe=False
        )
    else:
        ord = order.objects.get(id=request.GET['id'])
        ord.order_status = request.GET['val']
        ord.save()

        return JsonResponse(
            {'success': True},
            safe=False
        )


# set banner image for product
@never_cache
@login_required(login_url='/admin_side/admin_login')
def Setbanner(request):
    banner = BannerForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if banner.is_valid():
            banner.save()
            return redirect("/admin_side/bannertable")
    return render(request, 'adminTempl/admin_form.html', {"form": banner, 'url': "/admin_side/setbanner/"})


# banner image of the product
@never_cache
@login_required(login_url='/admin_side/admin_login')
def BannerTable(request):
    banner = Banner.objects.all()
    return render(request, 'adminTempl/banner.html', {'banner': banner})


# delete banner image of the product
@never_cache
@login_required(login_url='/admin_side/admin_login')
def DelBanner(request):
    id = request.GET['b_id']
    Banner.objects.filter(id=id).delete()
    return redirect("/admin_side/bannertable")


# product offer page . listing the product name and offer if the product have any. also the search and paginations is done here
@never_cache
@login_required(login_url='/admin_side/admin_login')
def ProductOffer(request):
    val = request.GET.get('search' or None)
    if val:
        inp = products.objects.filter(product_name__icontains=val).values(
            'product_name', 'id', 'offer')
    else:
        inp = products.objects.values('product_name', 'id', 'offer')

    paginator = Paginator(inp, 10)
    page = request.GET.get('page')
    try:
        a = paginator.page(page)
    except PageNotAnInteger:
        a = paginator.page(1)
    except EmptyPage:
        a = paginator.page(paginator.num_pages)
    return render(request, 'adminTempl/productoffer.html', {'prod': a, 'page': page})


# category offer page with offer details. also searching according to input
@never_cache
@login_required(login_url='/admin_side/admin_login')
def CategoryOffer(request):
    val = request.GET.get('search' or None)
    if val:
        inp = Category.objects.filter(category__icontains=val)
    else:
        inp = Category.objects.all()

    return render(request, 'adminTempl/categoryoffer.html', {'category': inp})


# set product offer and calculate the amt after offer and save into product variant table
@never_cache
@login_required(login_url='/admin_side/admin_login')
def AddProductOffer(request):
    id = request.GET['id']
    offer = request.GET.get('offer', 0)
    p = products.objects.get(id=id)
    p.offer = offer
    p.save()
    v = VariantAndPrice.objects.filter(
        product_id__id=id).values(
        'price', 'final_price', 'product_id__offer',
        'product_id__brand_id__c_id__offer', 'id')

    addoff(v)
    return redirect('/admin_side/productoffer')


# set offer for category and calculate amt after deduct offer from price and set amt in the product table according to category
@never_cache
@login_required(login_url='/admin_side/admin_login')
def AddCategoryOffer(request):
    id = request.GET['id']
    offer = request.GET.get('offer', 0)
    c = Category.objects.get(id=id)
    c.offer = offer
    c.save()
    v = VariantAndPrice.objects.filter(
        product_id__brand_id__c_id__id=id).values(
        'price', 'final_price', 'product_id__offer',
        'product_id__brand_id__c_id__offer', 'id')
    addoff(v)
    return redirect('/admin_side/categoryoffer')


# coupen management view.list all the coupen. search and pgination is done here
@never_cache
@login_required(login_url='/admin_side/admin_login')
def CoupenManagement(request):
    val = request.GET.get('search' or None)
    if val:
        inp = Coupen.objects.filter(coupen_code__icontains=val)
    else:
        inp = Coupen.objects.all()

    paginator = Paginator(inp, 10)
    page = request.GET.get('page')
    try:
        a = paginator.page(page)
    except PageNotAnInteger:
        a = paginator.page(1)
    except EmptyPage:
        a = paginator.page(paginator.num_pages)
    return render(request, 'adminTempl/coupen.html', {'coupen': a, 'page': page})


# add, update and delete coupen view
@never_cache
@login_required(login_url='/admin_side/admin_login')
def AddCoupen(request):
    id = request.GET.get('id' or 0)
    remove = request.GET.get('remove' or 0)
    if id and not remove:
        form = CoupenForm(request.POST or None,
                          instance=Coupen.objects.get(id=id))
        if request.method == "POST":
            if form.is_valid():
                form.save()
                return redirect('/admin_side/coupenmanagement')

    elif not remove:
        form = CoupenForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                return redirect('/admin_side/coupenmanagement')
    else:
        Coupen.objects.filter(id=id).delete()
        return redirect('/admin_side/coupenmanagement')
    return render(request, 'adminTempl/admin_form.html', {'form': form})


"""
sales report view. finding which option user choosen ex: motnth or specific date. if nothing work return all the data.
reused this funtion for download as excell option. finding which data user needs
"""
def FindOutWhichIsWIch(request):
    dateFrom = request.GET.get('from' or 0)
    dateTo = request.GET.get('to' or 0)
    monthly = request.GET.get('monthly', 0)
    year = request.GET.get('year', 0)

    val = request.GET.get('search', 0)
    a = order.objects.values_list('variant_id__product_id__product_name').annotate(
        Count('total_qty'), Sum('subtotal'))

    if dateFrom and dateTo:
        a = order.objects.filter(Q(date__gte=dateFrom) & Q(date__lte=dateTo)).values_list(
            'variant_id__product_id__product_name').annotate(Count('total_qty'), Sum('subtotal'))
    elif dateFrom:
        a = order.objects.filter(date__gte=dateFrom).values_list(
            'variant_id__product_id__product_name').annotate(Count('total_qty'), Sum('subtotal'))
    elif dateTo:
        a = order.objects.filter(date__lte=dateTo).values_list(
            'variant_id__product_id__product_name').annotate(Count('total_qty'), Sum('subtotal'))
    elif monthly:
        m = monthly.split('-')
        a = order.objects.filter(date__month=m[1], date__year=m[0]).values_list(
            'variant_id__product_id__product_name').annotate(Count('total_qty'), Sum('subtotal'))
    elif year and not None:
        a = order.objects.filter(date__year=year).values_list(
            'variant_id__product_id__product_name').annotate(Count('total_qty'), Sum('subtotal'))
    elif val:
        a = order.objects.filter(variant_id__product_id__product_name__icontains=val).values_list(
            'variant_id__product_id__product_name').annotate(Count('total_qty'), Sum('subtotal'))
    return a


# sales report page view
@never_cache
@login_required(login_url='/admin_side/admin_login')
def SalesReport(request):
    a = FindOutWhichIsWIch(request)
    context = {
        'dateFrom': request.GET.get('from' or 0),
        'dateTo': request.GET.get('to' or 0),
        'monthly': request.GET.get('monthly', 0),
        'report': a,
        'year': request.GET.get('year' or 0),
    }
    return render(request, 'adminTempl/salesReport.html', context)


# print sales report as excell
def Excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + \
        str(datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('report')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['name', 'quantity', 'revenue']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    rows = FindOutWhichIsWIch(request)
    
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)
    return response
