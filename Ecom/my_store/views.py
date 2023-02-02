# Create your views here.
from django.shortcuts import render

def store(request):
    context = {}
    return render(request, 'my_store/store.html', context)

def checkout(request):
    context = {}
    return render(request, 'my_store/checkout.html', context)

def cart(request):
    context = {}
    return render(request, 'my_store/cart.html', context)