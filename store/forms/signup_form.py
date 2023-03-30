from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from store.models.customer import Customer
from phonenumber_field.formfields import PhoneNumberField

email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
email_msg = 'Enter a valid email address (e.g. example@mail.com}'
pass_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$'
pass_msg = 'Password must contain at least 8 characters, one uppercase letter, one lowercase letter and one number'
phone_pattern = r'^\+380[0-9]{9}$'
phone_msg = 'Enter a valid phone number (e.g. +38 067 333 22 11).'


class CustomerForm(UserCreationForm):
    """Form for the user registration."""
    phone = PhoneNumberField()
    phone.error_messages['invalid'] = 'Enter a valid phone number (e.g. +38 067 333 22 11).'
    email = forms.EmailField()
    address = forms.CharField(max_length=128, required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2', 'phone', 'address')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].required = True
        self.fields['first_name'].widget.attrs.update({'placeholder': 'First name', 'id': 'f_name', 'type': 'text',
                                                       'name': 'f_name'})
        self.fields['last_name'].required = True
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Last name', 'id': 'l_name', 'type': 'text',
                                                      'name': 'l_name'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email', 'id': 'email', 'type': 'email',
                                                  'name': 'email', 'pattern': email_pattern, 'title': email_msg})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password', 'type': 'password', 'name': 'pass',
                                                      'id': 'pass', 'pattern': pass_pattern, 'title': pass_msg})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Repeat your password', 'type': 'password',
                                                      'name': 're_pass', 'id': 're_pass', 'pattern': pass_pattern,
                                                      'title': pass_msg})
        self.fields['phone'].widget = forms.TextInput(
            attrs={'placeholder': 'Phone', 'title': phone_msg,
                   'id': 'phone', 'name': 'phone', 'type': 'tel'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        if commit:
            user.save()

        customer = None
        email = self.cleaned_data['email']
        phone = self.cleaned_data['phone']

        if Customer.get_customer_by_guest_email(email):
            customer = Customer.get_customer_by_guest_email(email)
            customer.user = user
            customer.save()
        if Customer.get_customer_by_guest_phone(phone):
            customer = Customer.get_customer_by_guest_phone(phone)
            if not customer.user:
                customer.user = user
            customer.phone = phone
            customer.save()

        if not customer:
            customer = Customer.objects.create(
                user=user,
                phone=self.cleaned_data['phone'],
            )

        return customer
