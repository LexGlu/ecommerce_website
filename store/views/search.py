from django.shortcuts import render
from store.models import Product
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.cache import cache
from store.documents import ProductDocument


def search_product(request):
    query = request.GET.get('query')
    q = f'?{query.lower()}'

    products = cache.get(q)

    if not products:
        all_products = cache.get('all_products') or Product.objects.all()

        products = all_products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()
        cache.set(q, products)

    products_count = products.count()
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'query': query, 'products_count': products_count}
    return render(request, 'store/search.html', context)
