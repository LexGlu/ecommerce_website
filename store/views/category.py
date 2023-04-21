from django.shortcuts import render, get_list_or_404, get_object_or_404
from store.models import Product, Category
from django.views import View
from django.core.paginator import Paginator

class CategoryView(View):
    @staticmethod
    def get(request, category_slug):
        category = get_object_or_404(Category, slug=category_slug)
        products = get_list_or_404(Product, category=category)
        paginator = Paginator(products, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'page_obj': page_obj, 'category': category}
        return render(request, 'store/category.html', context)
