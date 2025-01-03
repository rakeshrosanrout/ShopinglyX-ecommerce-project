from django.shortcuts import render,redirect
from django.views import View
from .models import *
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.db.models import Q
from django.http import JsonResponse

def custom_logout(request):
    logout(request)
    return redirect('login') 

class ProductView(View):
    def get(self,request):
        topwears=Product.objects.filter(category='TW')
        bottomwears=Product.objects.filter(category='BW')
        mobiles=Product.objects.filter(category='M')
        return render(request,'app/index.html',{'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles})

# def product_detail(request):
#  return render(request, 'app/productdetail.html')

class ProductDetailView(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        return render(request,'app/productdetail.html',{'product':product})

def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('product_id')
    cart(user=user,product=Product.objects.get(id=product_id)).save()
    return redirect('/cart')

def show_cart(request):
    if request.user.is_authenticated:
        user=request.user
        Cart=cart.objects.filter(user=user)
        amount=0.0
        shipping_ammount=70.0
        total_amount=0.0
        cart_product=[p for p in cart.objects.all() if p.user==user]
        # cart_product1=cart.objects.filter(user=user)
        # print(cart_product)
        if cart_product:
            for p in cart_product:
                amount=amount+(p.quantity*p.product.discounted_price)
                total_amount=amount+shipping_ammount
    return render(request,'app/addtocart.html',{'Cart':Cart,'total_amount':total_amount,'amount':amount})

def plus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=cart.objects.get(Q(product=prod_id)& Q(user=request.user))
        c.quantity+=1
        c.save()
        amount=0.0
        shipping_ammount=70.0
        total_amount=0.0
        cart_product=[p for p in cart.objects.all() if p.user==request.user]
        # cart_product1=cart.objects.filter(user=user)
        # print(cart_product)
        if cart_product:
            for p in cart_product:
                amount=amount+(p.quantity*p.product.discounted_price)

            data={
                    'quantity':c.quantity,
                    'amount':amount,
                    'totalamount':amount+shipping_ammount
                }
    return JsonResponse(data) 
def minus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=cart.objects.get(Q(product=prod_id)& Q(user=request.user))
        c.quantity-=1
        c.save()
        amount=0.0
        shipping_ammount=70.0
        total_amount=0.0
        cart_product=[p for p in cart.objects.all() if p.user==request.user]
        # cart_product1=cart.objects.filter(user=user)
        # print(cart_product)
        if cart_product:
            for p in cart_product:
                amount=amount+(p.quantity*p.product.discounted_price)
            data={
                    'quantity':c.quantity,
                    'amount':amount,
                   'totalamount':amount+shipping_ammount
                }
    return JsonResponse(data) 
def remove_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=cart.objects.get(Q(product=prod_id)& Q(user=request.user))
        c.delete()
        amount=0.0
        shipping_ammount=70.0
        total_amount=0.0
        cart_product=[p for p in cart.objects.all() if p.user==request.user]
        # cart_product1=cart.objects.filter(user=user)
        # print(cart_product)
        if cart_product:
            for p in cart_product:
                amount=amount+(p.quantity*p.product.discounted_price)
        data={
                'amount':amount,
                'totalamount':amount+shipping_ammount
                }   
    return JsonResponse(data) 

    
def buy_now(request):
    return redirect()

# def profile(request):
#  return render(request, 'app/profile.html')

class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm()
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            reg=Customer(user=user,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,'Congratulations! Profile Updated Successfully.')
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})

def address(request):
    adrs=Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'address':adrs,'active':'btn-primary'})

def orders(request):
    op=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'order_placed':op})

def change_password(request):
 return render(request, 'app/changepassword.html')

def mobile(request,data=None):
    if data==None:
        mobiles=Product.objects.filter(category="M")
    elif data=='Redmi'  or data=='Realme':
        mobiles=Product.objects.filter(category='M').filter(brand=data)
    elif data=='below':
        mobiles=Product.objects.filter(category='M').filter(discounted_price__lt=10000)
    elif data=='above':
        mobiles=Product.objects.filter(category='M').filter(discounted_price__gt=10000)
    
    return render(request, 'app/mobile.html',{'mobiles':mobiles})

def laptop(request):
    laptops=Product.objects.filter(category='L')
    return render(request,'app/laptop.html',{'laptops':laptops})

def topwear(request,data=None):
    if data==None:
        topwear=Product.objects.filter(category='TW')
    elif data=='below':
        topwear=Product.objects.filter(category='TW').filter(discounted_price__lt=500)
    elif data=='above':
        topwear=Product.objects.filter(category='TW').filter(discounted_price__gt=500)
    return render(request,'app/topwear.html',{'topwear':topwear})
# def login(request):
#  return render(request, 'app/login.html')

class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',{'form':form})
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Congratulations!! Registration Sucessfully')
        return render(request,'app/customerregistration.html',{'form':form})

def checkout(request):
    user=request.user
    add=Customer.objects.filter(user=user)
    cart_items=cart.objects.filter(user=user)
    amount=0.0
    shiping_amount=70.0
    total_amount=0.0
    # cart_product=[p ]
    cart_product=[p for p in cart.objects.all() if p.user==request.user]
        # cart_product1=cart.objects.filter(user=user)
        # print(cart_product)
    if cart_product:
        for p in cart_product:
            amount=amount+(p.quantity*p.product.discounted_price)
            total_amount=amount+shiping_amount
    return render(request, 'app/checkout.html',{'add':add,'total_amount':total_amount,'cart_items':cart_items})

def paymentdone(request):
    user=request.user
    custid=request.GET.get('custid')
    customer=Customer.objects.get(id=custid)
    cart_item=cart.objects.filter(user=user)
    for c in cart_item:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect('orders')
