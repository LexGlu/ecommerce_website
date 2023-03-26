import decimal

from django.shortcuts import render, redirect
from store.models import Order, Product, OrderItem, ShippingInfo
from django.http import JsonResponse
import json
import datetime


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, status='open')
        items = order.orderitem_set.all().order_by('product__id')
    else:
        try:
            guest_cart = json.loads(request.COOKIES['cart'])
        except KeyError:
            guest_cart = {}
        items = []
        order = {'total_items': 0, 'total_value': 0}

        if guest_cart:
            for product_id in guest_cart:
                product = Product.objects.get(id=product_id)
                product_total = (product.price * guest_cart[product_id]['quantity'])
                product_quantity = guest_cart[product_id]['quantity']
                order['total_value'] += product_total
                order['total_items'] += product_quantity
                item = {
                    'product': product,
                    'quantity': product_quantity,
                    'total_value': product_total,
                }
                items.append(item)

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
        order = {'total_items': 0, 'total_value': 0, 'shipping': False}

        # code to handle guest checkout will be here
        order_data = json.loads(request.COOKIES['cart'])
        # continue here

        if order['total_items'] == 0:
            return redirect('store:home')
    return render(request, 'store/checkout.html', {'order': order})


def update_item(request):
    data = json.loads(request.body)
    product_id = data['productId']
    product = Product.objects.get(id=product_id)
    action = data['action']
    print('Action:', action)
    print('Product:', product_id)

    if request.user.is_authenticated:

        customer = request.user.customer

        order, created = Order.objects.get_or_create(customer=customer, status='open')
        order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

        if action == 'add':
            order_item.quantity = (order_item.quantity + 1)
        elif action == 'remove':
            order_item.quantity = (order_item.quantity - 1)
        elif action == 'delete':
            order_item.quantity = 0

        order_item.save()

        # Get updated cart count and subtotal
        cart_count = order.total_items
        cart_subtotal = order.total_value
        item_count = order_item.quantity
        item_total = order_item.total_value
        # product_id = order_item.product.id

        if order_item.quantity <= 0:
            order_item.delete()

    else:
        try:
            guest_cart = json.loads(request.COOKIES['cart'])
        except Exception as e:
            print(e)
            return {
                'message': 'Cart is empty',
                'cart-count': 0,
                'cart-subtotal': 0,
                'item-count': 0,
                'item-total': 0,
                'product-id': product_id,
            }

        # Get updated cart count and subtotal
        cart_count = 0
        for i in guest_cart:
            cart_count += guest_cart[i]['quantity']

        cart_subtotal = 0
        for i in guest_cart:
            product_in_cart = Product.objects.get(id=i)
            cart_subtotal += product_in_cart.price * guest_cart[i]['quantity']

        try:
            item_count = guest_cart.get(product_id).get('quantity')
            item_total = item_count * product.price
            print(f"Item Count: {item_count} ")
        except Exception as e:
            print(e)
            item_count = 0
            item_total = 0

        # if guest_cart[product_id]['quantity'] <= 0:
        #     del guest_cart[product_id]

    data = {
        'message': 'Item was added',
        'cart-count': cart_count,
        'cart-subtotal': cart_subtotal,
        'item-count': item_count,
        'item-total': item_total,
        'product-id': product_id,
    }

    return JsonResponse(data)


def process_order(request):
    print('Data:', request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, status='open')
        total = decimal.Decimal(data['form']['total'])
        order.transaction_id = transaction_id

        print(f"Total: {total} type {type(total)} | Order Total: {order.total_value} type {type(order.total_value)}")
        print(total == order.total_value)

        if total == order.total_value:
            order.status = 'processing'
        order.save()

        if order.shipping:
            ShippingInfo.objects.create(
                order=order,
                customer=customer,
                city=data['form']['city'],
                np_office=data['form']['np_office'],
            )

    else:
        print('User is not logged in...')

    return JsonResponse('Payment completed', safe=False)
