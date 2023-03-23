from django.db import models
from .product import Product
from .customer import Customer


class Order(models.Model):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    )
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    transaction_id = models.CharField(max_length=100, null=True)

    def set_transaction_id(self):
        self.transaction_id = f'{self.customer.user.email}#{self.id}'

    def __str__(self):
        return self.transaction_id

    @staticmethod
    def get_orders_by_customer(customer):
        return Order.objects.filter(customer=customer).order_by('-date')

    @property
    def total_value(self):
        return sum(item.total_value for item in self.orderitem_set.all())

    @property
    def total_items(self):
        return sum(item.quantity for item in self.orderitem_set.all())


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name

    @property
    def total_value(self):
        return self.product.price * self.quantity
