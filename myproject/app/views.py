from django.shortcuts import render


def home(request):
    return render(request, 'app/home.html')


def all_product(request):
    ...


def add_product(request):
    ...


def delete_product(request):
    ...


def update_product(request):
    ...
