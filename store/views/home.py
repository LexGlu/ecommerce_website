from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from store.models import Product


class HomeView(View):

    @staticmethod
    def get(request):
        products = Product.objects.all()
        context = {'products': products}
        return render(request, 'store/home.html', context)
