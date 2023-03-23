from django.shortcuts import render, redirect
from store.models import Order, Product, OrderItem
from django.http import JsonResponse
import json


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'total_items': 0, 'total_value': 0}
    context = {'items': items, 'order': order}
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        try:
            order = Order.objects.get(customer=customer, status='open')
            if order.total_items == 0:
                return redirect('store:home')
        except Exception as e:
            print(e)
            return redirect('store:home')
    else:
        order = {'total_items': 0, 'total_value': 0}
        # code to handle guest checkout will be here
        if order['total_items'] == 0:
            return redirect('store:home')
    return render(request, 'store/checkout.html', {'order': order})


def update_item(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', product_id)

    customer = request.user.customer
    product = Product.objects.get(id=product_id)

    order, created = Order.objects.get_or_create(customer=customer)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        order_item.quantity = (order_item.quantity + 1)
    elif action == 'remove':
        order_item.quantity = (order_item.quantity - 1)
    elif action == 'delete':
        order_item.quantity = 0

    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse('Item was added', safe=False)
