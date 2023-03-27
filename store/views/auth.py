from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from store.forms.signup_form import CustomerForm
from store.forms.login_form import LoginForm
from django.contrib.auth import login, logout


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

    if request.method == 'POST':
        form = LoginForm(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_user_email(email)
        if not customer:
            error_message = f'Customer with email {email} does not exist'
            return render(request, 'store/login.html', {'form': form, 'error': error_message})
        flag = check_password(password, customer.user.password)
        if not flag:
            error_message = 'Entered password is incorrect'
            return render(request, 'store/login.html', {'form': form, 'error': error_message})
        login(request, customer.user)
        return redirect('store:home')
    else:
        error_user_exists = request.session.get('error_user_exists')
        form = LoginForm()
        return render(request, 'store/login.html', {'form': form, 'error_user_exists': error_user_exists})


def log_out(request):
    logout(request)
    return redirect('store:home')
