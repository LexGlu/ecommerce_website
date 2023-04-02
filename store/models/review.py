from django.db import models
from store.models import Product, Customer
from django.core.validators import MaxValueValidator, MinValueValidator


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5, validators=[MaxValueValidator(5), MinValueValidator(1)])
    comment = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment

    def get_rating_display(self):
        return f'{self.rating}/5'

    @property
    def rating_stars(self):
        stars = ''
        for i in range(1, 6):
            if i <= self.rating:
                stars += '<i class="fa fa-star" aria-hidden="true"></i>'
            else:
                stars += '<i class="fa fa-star-o" aria-hidden="true"></i>'
        return stars
