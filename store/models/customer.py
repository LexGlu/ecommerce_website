from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = PhoneNumberField(region='UA', unique=True)
    city = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.user.email

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(user__email=email)
        except Customer.DoesNotExist:
            return False
