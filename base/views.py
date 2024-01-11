from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail
import math,random
from django.db.models import Q
from django.conf import settings
import datetime
from .models import *
import json
from .utils import cookieCart, cartData, guestOrder
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            redirect_url = request.GET.get('next', 'homepage')
            return redirect(redirect_url)
        else:
            messages.error(request, "Username Or Password is incorrect!!",
                           extra_tags='alert alert-warning alert-dismissible fade show')

    return render(request, 'base/login.html')


def logout_user(request):
    logout(request)
    return redirect('homepage')


def create_user(request):
    if request.method == 'POST':
        check1 = False
        check2 = False
        check3 = False
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            email = form.cleaned_data['email']

            if password1 != password2:
                check1 = True
                messages.error(request, 'Password doesn\'t matched',
                               extra_tags='alert alert-warning alert-dismissible fade show')
            if User.objects.filter(username=username).exists():
                check2 = True
                messages.error(request, 'Username already exists',
                               extra_tags='alert alert-warning alert-dismissible fade show')
            if User.objects.filter(email=email).exists():
                check3 = True
                messages.error(request, 'Email already registered',
                               extra_tags='alert alert-warning alert-dismissible fade show')

            if check1 or check2 or check3:
                messages.error(
                    request, "Registration Failed", extra_tags='alert alert-warning alert-dismissible fade show')
                return redirect('register')
            else:
                user = User.objects.create_user(
                    username=username, password=password1, email=email)
                customer = Customer.objects.create(
                    user=user, name=username, email=email)
                messages.success(
                    request, f'Thanks for registering {user.username}!', extra_tags='alert alert-success alert-dismissible fade show')
                return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'base/register.html', {'form': form})


#OTP
def generateOTP():
    digits = "0123456789"
    OTP = ""
    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

def send_otp(request):
    email=request.POST.get("email")
    print(email)
    o=generateOTP()
    from_email = settings.EMAIL_HOST_USER
    htmlgen = f'<h1> Welcome to Giftos </h1><br><p> Your OTP is <strong>{o}</strong></p>'
    send_mail('OTP request', o, from_email, [email], fail_silently=False, html_message=htmlgen)
    return HttpResponse(o)



def home(request):
    cart_data = cartData(request)

    products = Product.objects.all()
    context = {
        "products": products,
        "cartItems": cart_data['cartItems']
    }
    return render(request, "base/index.html", context)

def shop(request):
    cart_data = cartData(request)

    products = Product.objects.all()
    context = {
        "products": products,
        "cartItems": cart_data['cartItems']
    }
    return render(request, "base/shop.html", context)

def all_products(request):
    cart_data = cartData(request)

    jerseys = Product.objects.filter(type="JERSEY")
    flowers = Product.objects.filter(type="FLOWER")
    rings = Product.objects.filter(type="RING")
    watches = Product.objects.filter(type="WATCH")
    context = {
        "jerseys": jerseys,
        "flowers": flowers,
        "rings": rings,
        "watches": watches,
        "cartItems": cart_data['cartItems']
    }
    return render(request, "base/all_products.html", context)

def product_detail(request, id):
    cart_data = cartData(request)
    product = Product.objects.get(id=id)
    context = {
        "product": product,
        "cartItems": cart_data['cartItems']
    }
    return render(request, "base/product-detail.html", context)

def cart(request):
    cart_data = cartData(request)
    context = {
        "items": cart_data['items'], 
        "order": cart_data['order'],
        "cartItems": cart_data['cartItems']
    }
    return render(request, "base/cart.html", context)

def checkout(request):
    cart_data = cartData(request)
    context = {
        "items": cart_data['items'], 
        "order": cart_data['order'],
        "cartItems": cart_data['cartItems']
    }
    return render(request, "base/checkout.html", context)

def search(request):
    search_product(request)
    return render(request, "base/search.html")

def search_product(request):
    search_product = request.GET.get('search')
    if search_product:
        product = Product.objects.filter(Q(name__icontains=search_product)| Q(type__icontains=search_product))
    else:
        product = Product.objects.all().order_by("-created_at")
    return render(request, "base/search.html", {"products": product})

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse("Item was added",  safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
               
    else:
        customer, order = guestOrder(request, data)
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    print(order)
    if total == float(order.get_cart_total):
        order.complete = True
    order.save() 

    ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            location=data['shipping']['location'],
            region=data['shipping']['region']
        )     
    return JsonResponse('Payment submitted...', safe=False)


def why(request):
    cart_data = cartData(request)
    context = {
        "cartItems": cart_data['cartItems']
    }
    return render(request, "base/why.html", context)

def testimonial(request):
    cart_data = cartData(request)
    testimonials = Testimonial.objects.all()
    context = {
        "cartItems": cart_data['cartItems'],
        "testimonials": testimonials
    }
    return render(request, "base/testimonial.html", context)

def send_testimonial(request):
    from_email=request.POST.get("email")
    name=request.POST.get("name")
    phone=request.POST.get("phonenumber")
    message = request.POST.get("message")
    email = settings.EMAIL_HOST_USER
    htmlgen = f'<h1>{message}</h1><br><span>Name: {name}</span><br><span>Email: {from_email}</span><br><span>Phonenumber: {phone}</span>'
    send_mail('Testimonial for Giftos Managers', message, from_email, [email], fail_silently=False, html_message=htmlgen)
    return redirect('homepage')

def contact(request):
    cart_data = cartData(request)
    context = {
        "cartItems": cart_data['cartItems']
    }
    return render(request, "base/contact.html", context)

def contact_us(request):
    from_email=request.POST.get("email")
    name=request.POST.get("name")
    phone=request.POST.get("phonenumber")
    message = request.POST.get("message")
    email = settings.EMAIL_HOST_USER
    htmlgen = f'<h1>{message}</h1><br><span>Name: {name}</span><br><span>Email: {from_email}</span><br><span>Phonenumber: {phone}</span>'
    send_mail('Message for Giftos Managers', message, from_email, [email], fail_silently=False, html_message=htmlgen)
    return redirect('homepage')