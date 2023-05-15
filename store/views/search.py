from django.shortcuts import render
from store.models import Product
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.cache import cache
from store.documents import ProductDocument
from django.http import JsonResponse
from elasticsearch_dsl import Q as DSLQ

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


def search_elastic(request):
    query = request.GET.get('query', '').lower()
    
    if not query:
        return JsonResponse([], safe=False)

    # Split the query string into individual words
    words = query.split()

    # Construct a list of wildcard queries for each word in the query
    wildcard_queries = [
        DSLQ('wildcard', name='*' + word + '*') |
        DSLQ('wildcard', description='*' + word + '*') |
        DSLQ('wildcard', brand='*' + word + '*')
        for word in words
    ]

    # Perform a search query on the Elasticsearch index where name, description, or brand fields contain all of the words
    products = ProductDocument.search().query(
        DSLQ('bool', must=wildcard_queries)
    )

    results = [product.to_dict() for product in products[0:5]]

    return JsonResponse(results, safe=False)