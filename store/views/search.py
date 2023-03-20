from django.shortcuts import render
from store.models import Product
from django.db.models import Q


def search_product(request):
    products = Product.objects.all()
    query = request.GET.get('query')
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()
    context = {'products': products, 'query': query}
    return render(request, 'store/search.html', context)


