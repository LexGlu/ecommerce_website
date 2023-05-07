from django.shortcuts import render
from django.views import View
from store.models import Category
from django.core.paginator import Paginator
from django.core.cache import cache


class HomeView(View):

    @staticmethod
    def get(request):
        key = 'categories'
        categories = cache.get(key)

        if not categories:
            categories = Category.objects.all()
            cache.set(key, categories)

        context = {'categories': categories}
        return render(request, 'store/home.html', context)


def custom_handler404(request, exception):
    return render(request, 'store/404.html', {}, status=404)
