from django.shortcuts import render, get_list_or_404, get_object_or_404
from store.models import Product, Category
from django.views import View
from django.core.paginator import Paginator
from django.core.cache import cache


class CategoryView(View):
    @staticmethod
    def get(request, category_slug):
        key = f'category_{category_slug}'
        products = cache.get(key)

        if not products:
            all_products = cache.get('all_products') or Product.objects.all()
            products = all_products.filter(category__slug=category_slug)
            cache.set(key, products)

        category = products.first().category
        paginator = Paginator(products, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'page_obj': page_obj, 'category': category}
        return render(request, 'store/category.html', context)
