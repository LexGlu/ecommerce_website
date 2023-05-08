from django.db import models
from autoslug import AutoSlugField
from django.core.cache import cache


class Category(models.Model):
    name = models.CharField(max_length=128)
    slug = AutoSlugField(populate_from='name', unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='uploads/categories/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    @property
    def brands(self):
        """Returns a list of unique brands for products in this category sorted (a-z)."""
        key = f'category_{self.slug}_brands'
        brands = cache.get(key)
        if not brands:
            brands = sorted(set(product.brand for product in self.product_set.all() if product.brand))
            cache.set(key, brands)
        return brands
