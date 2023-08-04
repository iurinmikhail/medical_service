from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    print(request)
    return HttpResponse("Hello, world. You're at the refbooks index.")
