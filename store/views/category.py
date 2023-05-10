from django.shortcuts import render
from store.models import Product, Category
from django.views import View
from django.core.paginator import Paginator
from django.core.cache import cache


class CategoryView(View):
    @staticmethod
    def get(request, category_slug):
        key = f'category_{category_slug}'
        products = cache.get(key)

        params = []

        if not products:
            products = Product.objects.filter(category__slug=category_slug)
            cache.set(key, products)

        # Filtering by brand
        brand_param = request.GET.get('brand')
        if brand_param:
            brands = brand_param.split(',')
            products = products.filter(brand__in=brands)
            params.append(f'brand={brand_param}')

        # Filtering by price range
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')

        if min_price:
            products = products.filter(price__gte=min_price)
            params.append(f'min_price={min_price}')
        if max_price:
            products = products.filter(price__lte=max_price)
            params.append(f'max_price={max_price}')

        # Sorting
        sort_param = request.GET.get('sort')
        if sort_param:
            sort_options = {
                'cheap': products.order_by('price'),
                'expensive': products.order_by('-price'),
                'rating': sorted(products, key=lambda p: p.average_rating, reverse=True),
            }
            products = sort_options.get(sort_param, products)
            params.append(f'sort={sort_param}')

        category = Category.objects.get(slug=category_slug)

        params_str = '&'.join(params)
        
        paginator = Paginator(products, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'page_obj': page_obj, 'category': category, 'params': params_str}
        return render(request, 'store/category.html', context)
