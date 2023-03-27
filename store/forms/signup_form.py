from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from store.models.customer import Customer
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field
from phonenumber_field.formfields import PhoneNumberField


class CustomerForm(UserCreationForm):
    """Form for the user registration."""
    phone = PhoneNumberField()
    phone.error_messages['invalid'] = 'Enter a valid phone number (e.g. +380673332211).'
    email = forms.EmailField()
    address = forms.CharField(max_length=128, required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2', 'phone', 'address')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    Field('first_name'),
                    css_class='col-md-6 mb-0',
                ),
                Column(
                    Field('last_name'),
                    css_class='col-md-6 mb-0',
                ),
            ),
            'email',
            'phone',
            'password1',
            'password2',
            Submit('submit', 'Sign up', css_class='btn-success sign-btn')
        )
        self.fields['first_name'].required = True
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Alex', 'class': 'example-label'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Turner', 'class': 'example-label'})
        self.fields['email'].widget.attrs.update({'placeholder': 'example@mail.com', 'class': 'example-label'})
        self.fields['password1'].widget.attrs.update({'placeholder': '********', 'class': 'example-label'})
        self.fields['password2'].widget.attrs.update({'placeholder': '********', 'class': 'example-label'})
        self.fields['phone'].widget = forms.TextInput(
            attrs={'placeholder': '+380', 'class': 'example-label', 'value': '+380', 'pattern': '\+380[0-9]{9}',
                   'title': 'Enter a valid phone number (e.g. +380673332211)'})

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
