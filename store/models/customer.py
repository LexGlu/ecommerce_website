from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    guest_name = models.CharField(max_length=128, blank=True, null=True)
    guest_email = models.EmailField(max_length=128, blank=True, null=True)
    guest_phone = PhoneNumberField(region='UA', blank=True, null=True)
    phone = PhoneNumberField(region='UA', unique=True, blank=True, null=True)
    city = models.CharField(max_length=128, blank=True)
    np_office = models.CharField(max_length=128, blank=True, default='')

    def __str__(self):
        return self.user.email

    @staticmethod
    def get_customer_by_user_email(email):
        try:
            return Customer.objects.get(user__email=email)
        except Customer.DoesNotExist:
            return False

    @staticmethod
    def get_customer_by_guest_email(email):
        try:
            return Customer.objects.get(guest_email=email)
        except Customer.DoesNotExist:
            return False

    @staticmethod
    def get_customer_by_phone(phone):
        try:
            return Customer.objects.get(phone=phone)
        except Customer.DoesNotExist:
            return False

    @staticmethod
    def get_customer_by_guest_phone(phone):
        try:
            return Customer.objects.get(guest_phone=phone)
        except Customer.DoesNotExist:
            return False
