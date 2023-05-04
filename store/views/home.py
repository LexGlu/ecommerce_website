from django.shortcuts import render
from django.views import View
from store.models import Product
from django.core.paginator import Paginator
from django.core.cache import cache


class HomeView(View):

    @staticmethod
    def get(request):
        key = 'all_products'
        products = cache.get(key)

        if not products:
            products = Product.objects.all()
            cache.set(key, products)

        sort_param = request.GET.get('sort')
        if sort_param:
            sort_options = {
                'cheap': products.order_by('price'),
                'expensive': products.order_by('-price'),
                'rating': sorted(products, key=lambda p: p.average_rating, reverse=True),
            }
            products = sort_options.get(sort_param, products)

        paginator = Paginator(products, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'page_obj': page_obj}
        return render(request, 'store/home.html', context)


def custom_handler404(request, exception):
    return render(request, 'store/404.html', {}, status=404)
