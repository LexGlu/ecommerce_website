from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.user.username

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except Exception as e:
            print(e)
            return False

    def customer_exists(self):
        if Customer.objects.filter(email=self.email):
            return True
        return False
