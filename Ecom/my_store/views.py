# Create your views here.
import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .custom_response import JsonResponse
from .models import *

def store(request):
    if request.user.is_authenticated():
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
        cart_items = order['get_cart_items']
    products = Product.objects.all()
    context = {'products':products, 'cart_items':cart_items, 'shipping':False}
    return render(request, 'my_store/store.html', context)

def cart(request):
    if request.user.is_authenticated():
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
        cart_items = order['get_cart_items']
    
    context = {'items':items, 'order':order, 'user':request.user, 'cart_items':cart_items, 'shipping':False}
    return render(request, 'my_store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated():
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
        cart_items = order['get_cart_items']
    
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

