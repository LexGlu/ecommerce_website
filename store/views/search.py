from django.shortcuts import render
from store.models import Product
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.cache import cache
from django.http import JsonResponse
from functools import reduce
from operator import and_

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


def search_rt(request):
    query = request.GET.get('query', '').lower()
    q_string = f'?{query}'
    
    if not query:
        return JsonResponse([], safe=False)
    
    keywords = query.split()
    
    
    # AJAX request to postgreSQL database
    
    products = cache.get(q_string)
    
    if not products:
        products = cache.get('all_products')
        if not products:
            products = Product.objects.all()
            cache.set('all_products', products)
            
        filters = [
            Q(name__icontains=keyword) |
            Q(description__icontains=keyword) |
            Q(category__name__icontains=keyword)
            for keyword in keywords
        ]
        
        products = products.filter(reduce(and_, filters)).distinct()
        cache.set(q_string, products[:5])

    # Serialize products to a JSON serializable format
    results = []
    for product in products[:5]:
        serialized_product = {
            'id': product.pk,
            'name': product.name,
        }
        results.append(serialized_product)    

    return JsonResponse(results, safe=False)