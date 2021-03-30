from django.shortcuts import render
from django.http import JsonResponse
import json
from .utils import *
from .models import *

def search(request):
    #getting the user status, guest or logged in
    if request.user.is_authenticated:
        #get status info
            buyer = request.user.buyer
            #create or continue with order
            order, created = Order.objects.get_or_create(
                                buyer=buyer, complete=False)
             # total number of cart items already created at the models                   
            cartItems = order.get_cart_items 
    else:
        #using cookies to get the shopping information of guest user
             cookieData= cartCookie(request)
             cartItems = cookieData['cartItems']
            #initiating searching 
    if 'searched' in request.GET:
        searched = request.GET.get('searched')
        products = Product.objects.all().filter(name = searched)
        return render(request, 'search.html', {'searched':searched, 
                                               'products': products,
                                              'cartItems': cartItems })

    
        
def store(request):

    if request.user.is_authenticated:
        buyer = request.user.buyer
        order, created = Order.objects.get_or_create(
            buyer=buyer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        # Create empty cart for now for non-logged in user
        cookieData= cartCookie(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store.html', context)

def cart(request):

    if request.user.is_authenticated:
        buyer = request.user.buyer
        order, created = Order.objects.get_or_create(
            buyer=buyer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData= cartCookie(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
        

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        buyer = request.user.buyer
        order, created = Order.objects.get_or_create(
            buyer=buyer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        # Create empty cart for now for non-logged in user
        cookieData= cartCookie(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'checkout.html', context)


def updateItem(request):
    # Information Of What User Has Done
    data = json.loads(request.body)
    # Product To Buy ID
    productId = data['productId']
    # Action To Add To Cart 
    action = data['action']
    # Print To Make Sure It Workds
    print('Action:', action)
    print('Product:', productId)
   
    buyer = request.user.buyer
    product = Product.objects.get(id=productId)
    #create the order
    order, created = Order.objects.get_or_create(buyer=buyer, complete=False)

    orderedItem, created = orderItem.objects.get_or_create(
        order=order, product=product)
     #add or delete
    if action == 'add':
        orderedItem.quantity = (orderedItem.quantity + 1)
    elif action == 'remove':
        orderedItem.quantity = (orderedItem.quantity - 1)

    orderedItem.save()

    if orderedItem.quantity <= 0:
        orderedItem.delete()

    return JsonResponse('Item was added', safe=False)
