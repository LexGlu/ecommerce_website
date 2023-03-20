from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from store.forms.signup_form import CustomerForm
from store.forms.login_form import LoginForm
from django.contrib.auth import login


def sign_up(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            login(request, customer.user)
            return redirect('store:home')
        else:
            return render(request, 'store/signup.html', {'form': form})
    else:
        form = CustomerForm()
        return render(request, 'store/signup.html', {'form': form})


def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
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
    request.session.clear()
    return redirect('store:home')
