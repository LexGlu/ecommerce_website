from django.http import HttpResponse
from django.shortcuts import render


def homepage(request):
    return HttpResponse('Hi, here will be the homepage of the store.')
