import json
from .models import *

def cookieCart(request):
    try:
        cart = json.loads(request.META['HTTP_COOKIE'][5:].split(';')[0])
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
        cart_items = order['get_cart_items']
        
    
        for i in cart.keys():
            cart_items += cart[i]['quantity']
            product = Product.objects.get(id=i)
            total = product.price * cart[i]['quantity']
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']
            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'image_url': product.image_url
                },
                'quantity': cart[i]['quantity'],
                
                
            }
            items.append(item)
    except:
        cart_items = 0
        order = ''
        items = ''
        
    return {'cart_items':cart_items, 'order':order, 'items':items}

def cookieData(request):
    #print request.HTTP_COOKIE
    if request.user.is_authenticated():
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cart_items = cookieData['cart_items']
        order      = cookieData['order']
        items      = cookieData['items']
        
    return {'cart_items':cart_items, 'order':order, 'items':items}