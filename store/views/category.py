from django.shortcuts import render
from store.models import Product
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

        sort_param = request.GET.get('sort')
        if sort_param:
            sort_options = {
                'cheap': products.order_by('price'),
                'expensive': products.order_by('-price'),
                'rating': sorted(products, key=lambda p: p.average_rating, reverse=True),
            }
            products = sort_options.get(sort_param, products)

        try:
            category = products.first().category
        except AttributeError:
            category = products[0].category or None

        paginator = Paginator(products, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'page_obj': page_obj, 'category': category, 'sort': sort_param}
        return render(request, 'store/category.html', context)
