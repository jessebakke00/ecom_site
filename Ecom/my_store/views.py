# Create your views here.
import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import time
from .custom_response import JsonResponse
from .models import *
from .utils import cookieCart, cookieData

def store(request):
    #print request.META['HTTP_COOKIE']
    print request.user
    data = cookieData(request)
    cart_items = data['cart_items']
    order      = data['order']
    items      = data['items']
        
    products = Product.objects.all()
    context = {'products':products, 'cart_items':cart_items, 'shipping':False, 'user':str(request.user)}
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

def current_orders(request):
    orders = Order.objects.all()
    order_items = OrderItem.objects.all()
    shipping_address = ShippingAddress.objects.all()
    
    context = {'orders':orders, 'order_items':order_items}
    return render(request, 'my_store/current_orders.html', context)

def ship_detail(request, transaction_id):
    transaction_id = float(transaction_id)
    print transaction_id
    order = Order.objects.get(transaction_id=transaction_id)
    shipping_address = ShippingAddress.objects.get(order=order)
    
    
    context = {'order':order, 'shipping_address':shipping_address}
    return render(request, 'my_store/order_detail.html', context)

@csrf_exempt
def processOrder(request):
    # get the post data, since cookies is fucked
    post_data = json.loads(request.POST.keys()[0])
    #print post_data
    # now make a timestamp for later use
    transaction_id = time.time()
    
    if request.user.is_authenticated():
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer)
        # total = float(post_data['form']['total'])
        # order.transaction_id = transaction_id
        # 
        # if total == order.get_cart_total:
        #     order.complete = True
        # order.save()
        
        # if order.shipping == True:
        #     ShippingAddress.objects.create(
        #         customer = customer,
        #         order    = order,
        #         address  = data['shipping']['address'],
        #         city     = data['shipping']['city'],
        #         state    = data['shipping']['state'],
        #         zipcode  = data['shipping']['zipcode']
        #     )
    else:
        print 'User is not logged in!!'
        
        name = post_data['form']['name']
        email = post_data['form']['email']
        
        data = cookieCart(request)
        print data
        items = data['items']
        
        customer, created = Customer.objects.get_or_create(
            email=email
        )
        
        customer.name = name
        customer.save()
        
        order = Order.objects.create(
            customer=customer,
            complete=False
        )
        
        for item in items:
            product = Product.objects.get(id=item['product']['id'])
            orderItem = OrderItem.objects.create(
                product=product,
                order=order,
                quantity=item['quantity']
            )
            
    
    total = float(post_data['form']['total'])
    order.transaction_id = transaction_id
    
    if total == float(order.get_cart_total):
        order.complete = True
    order.save()
    
    
    ShippingAddress.objects.create(
        customer = customer,
        order    = order,
        address  = post_data['shipping']['address'],
        city     = post_data['shipping']['city'],
        state    = post_data['shipping']['state'],
        zipcode  = post_data['shipping']['zipcode']
    )
        
        
    
    
    
    # overwrite thecart file blank
    # f = open('cart', 'w')
    # f.write('')
    # f.close()
    
    return JsonResponse('Order Processed!!', safe=False)

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

# @csrf_exempt
# def updateCookie(request):   
#     data = json.loads(request.POST.keys()[0])
#     f = open('cart', 'w')
#     f.write(request.POST.keys()[0])
#     f.close()
#     return JsonResponse('updated cookie', safe=False)