import json

from django.http import JsonResponse
from django.shortcuts import render, redirect

from store.models import Order, OrderItem, Product
from store.models.customer import Customer
from store.forms.signup_form import CustomerForm
from store.forms.login_form import LoginForm
from django.contrib.auth import login, logout, authenticate


def sign_up(request):

    message = None

    if request.user.is_authenticated:
        return redirect('store:home')

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')

            if Customer.get_customer_by_user_email(email):
                return render(request, 'store/signup.html',
                              {'form': form, 'error': 'Customer with this email already exists'})
            elif Customer.get_customer_by_phone(phone):
                return render(request, 'store/signup.html',
                              {'form': form, 'error': 'Customer with this phone already exists'})

            customer = form.save()
            login(request, customer.user)
            return redirect('store:home')
        else:
            return render(request, 'store/signup.html', {'form': form})
    else:
        customer_data = request.session.get('customer_data')

        if customer_data:
            form = CustomerForm(
                initial={
                    'first_name': customer_data['first_name'],
                    'last_name': customer_data['last_name'],
                    'email': customer_data['email'],
                    'phone': customer_data['phone'],
                }
            )

            message = 'Please fill in the form to complete your registration and view your order details'

            del request.session['customer_data']

        else:
            form = CustomerForm()
        return render(request, 'store/signup.html', {'form': form, 'message': message})


def log_in(request):
    if request.user.is_authenticated:
        return redirect('store:home')
    form = LoginForm(request.POST or None)
    error = None
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        customer = Customer.get_customer_by_user_email(email)
        if not customer:
            error = f'Customer with email {email} does not exist'
        elif not authenticate(request, username=customer.user.username, password=password):
            error = 'Entered password is incorrect'
        else:
            login(request, customer.user)

            # Check if user has a cart cookie
            cart = request.COOKIES.get('cart')
            if cart:
                # add items from cart cookie to user's open order
                cart = json.loads(cart)
                # get customer's open order
                order, created = Order.objects.get_or_create(customer=customer, status='open')
                order_items = order.all_items

                for item in cart:
                    product = Product.objects.get(id=item)

                    try:
                        order_item = order_items.get(product=product)
                        if order_item.quantity < cart[item]['quantity']:
                            order_item.quantity = cart[item]['quantity']
                            order_item.save()
                    except Exception as e:
                        print(e)
                        OrderItem.objects.create(
                            product=product,
                            quantity=cart[item]['quantity'],
                            order=order
                        )
            return redirect('store:home')
    else:
        customer_data = request.session.get('customer_data')
        print(customer_data)
        if customer_data:
            form = LoginForm(initial={'email': customer_data.get('email')})
            error = 'Please login to complete your checkout'
            del request.session['customer_data']
    return render(request, 'store/login.html', {'form': form, 'error': error})


def log_out(request):
    logout(request)
    return redirect('store:home')


def update_cart_after_logout(request):
    if request.user.is_authenticated:
        customer = Customer.get_customer_by_user_email(request.user.email)
        order = Order.objects.get(customer=customer, status='open')
        cart = {}
        if order and order.all_items:
            for item in order.all_items:
                cart[item.product.id] = {"quantity": item.quantity}
        return JsonResponse(cart)
    else:
        return JsonResponse(None)
