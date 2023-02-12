# Create your views here.
import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .custom_response import JsonResponse
from .models import *
from .utils import cookieCart, cookieData

def store(request):
    data = cookieData(request)
    cart_items = data['cart_items']
    order      = data['order']
    items      = data['items']
        
    products = Product.objects.all()
    context = {'products':products, 'cart_items':cart_items, 'shipping':False}
    return render(request, 'my_store/store.html', context)

def cart(request):
    data = cookieData(request)
    cart_items = data['cart_items']
    order      = data['order']
    items      = data['items']
    
    context = {'items':items, 'order':order, 'user':request.user, 'cart_items':cart_items, 'shipping':False}
    return render(request, 'my_store/cart.html', context)

def checkout(request):
    data = cookieData(request)
    cart_items = data['cart_items']
    order      = data['order']
    items      = data['items']
        
    context = {'items':items, 'order':order, 'cart_items':cart_items, 'shipping':False}
    return render(request, 'my_store/checkout.html', context)

@csrf_exempt
def updateItem(request):
    # lets get the data posted via ajax 
    data = json.loads(request.POST.keys()[0])
    action = data['action']
    productId = data['productId']
    
    # now, lets fetch info from the database using the posted data
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    # change quantity
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    # save the updated quantity
    orderItem.save()
    
    # delete if quantity is reduced to 0
    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse(data, safe=False)

@csrf_exempt
def updateCookie(request):    
    data = json.loads(request.POST.keys()[0])
    f = open('cart', 'w')
    f.write(request.POST.keys()[0])
    f.close()
    return JsonResponse('updated cookie', safe=False)