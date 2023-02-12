import json
from .models import *

def cookieCart(request):
    f = open('cart', 'rw')
    s = f.read()
    d = json.loads(s)
    cart = d['cart']
    print cart
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
    return {'cart_items':cart_items, 'order':order, 'items':items}

def cookieData(request):
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