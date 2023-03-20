from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from store.models import Category


class HomeView(View):

    @staticmethod
    def get(request):
        return render(request, 'store/home.html')