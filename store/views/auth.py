from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from store.forms.signup_form import CustomerForm
from store.forms.login_form import LoginForm
from django.contrib.auth import login, logout


def sign_up(request):
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
        form = CustomerForm()
        return render(request, 'store/signup.html', {'form': form})


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
        form = LoginForm()
        return render(request, 'store/login.html', {'form': form})


def log_out(request):
    logout(request)
    return redirect('store:home')

