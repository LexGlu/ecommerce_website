from django.db import models
from .category import Category


class Product(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='uploads/products/', blank=True, null=True)

    def __str__(self):
        return self.name

    def is_in_stock(self):
        return self.stock > 0

    def get_image_url(self):
        if self.image:
            return self.image.url
        else:
            return ''

    def get_price_display(self):
        return '${:.2f}'.format(self.price)