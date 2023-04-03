from django.db import models
from .category import Category


class Product(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    digital = models.BooleanField(default=False, null=True, blank=True)
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

    @property
    def all_reviews(self):
        return self.review_set.all()

    @property
    def total_reviews(self):
        return self.review_set.count()

    @property
    def average_rating(self):
        reviews = self.all_reviews
        if reviews:
            total = 0
            for review in reviews:
                total += review.rating
            return round(total / reviews.count(), 1)
        else:
            return 0

    @property
    def rating_stars(self):
        return f'<i data-star="{self.average_rating}"></i>'
