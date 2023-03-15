from django.shortcuts import render, get_object_or_404
from django.views import View
from store.models import Product


class ProductView(View):
    @staticmethod
    def get(request, product_id):
        product = get_object_or_404(Product, id=product_id)
        context = {'product': product}
        return render(request, 'store/product.html', context)
