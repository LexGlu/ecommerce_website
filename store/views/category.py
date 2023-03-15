from django.shortcuts import render, get_list_or_404, get_object_or_404
from store.models import Product, Category
from django.views import View


class CategoryView(View):
    @staticmethod
    def get(request, category_slug):
        category = get_object_or_404(Category, slug=category_slug)
        products = get_list_or_404(Product, category=category)
        context = {'products': products, 'category': category}
        return render(request, 'store/category.html', context)
