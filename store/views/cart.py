import decimal

from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse
from store.models import Order, Product, OrderItem, ShippingInfo, Customer
from django.http import JsonResponse
import json
import datetime
from store.tasks import send_order_detail_email
from django.views.decorators.csrf import csrf_exempt


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
            else:
                redirect_url = reverse('store:checkout')
        except Exception as e:
            print(e)
            return redirect('store:home')
    else:

        redirect_url = reverse('store:signup')

        all_items = []
        order = {
            'total_items': 0,
            'total_value': 0,
            'all_items': all_items,
            'shipping': False,
        }

        order_data = json.loads(request.COOKIES['cart'])

        for product_id in order_data:
            product = Product.objects.get(id=product_id)

            product_total = (product.price * order_data[product_id]['quantity'])
            product_quantity = order_data[product_id]['quantity']
            order['total_value'] += product_total
            order['total_items'] += product_quantity
            item = {
                'product': product,
                'quantity': product_quantity,
                'total_value': product_total,
            }
            all_items.append(item)

        if any(not item['product'].digital for item in all_items):
            order['shipping'] = True

        if order['total_items'] == 0:
            return redirect('store:home')

    return render(request, 'store/checkout.html', {'order': order, 'redirect_url': redirect_url})

@csrf_exempt
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
            if product.is_in_stock() and order_item.quantity < product.stock:
                order_item.quantity = (order_item.quantity + 1)
            else:
                return JsonResponse({
                    'message': 'Out of stock',
                    'cart-count': order.total_items,
                    'cart-subtotal': order.total_value,
                    'item-count': order_item.quantity,
                    'item-total': order_item.total_value,
                    'product-id': product_id,
                }, status=400)
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
        else:
            order.status = 'canceled'
        order.save()

        if order.shipping:
            ShippingInfo.objects.create(
                order=order,
                customer=customer,
                city=data['form']['city'],
                np_office=data['form']['np_office'],
            )

        for item in order.all_items:
            item.product.stock -= item.quantity
            item.product.save()

        if order.status == 'processing':
            send_order_detail_email(order.id)

    else:
        guest_email = data['form']['email']
        guest_phone = data['form']['phone']

        # Check if guest email or phone already exists in user database

        user_exists_mail = User.objects.filter(email=guest_email).exists()
        user_exists_phone = Customer.objects.filter(phone=guest_phone).exists()

        error_user_exists = None
        if user_exists_mail and user_exists_phone:
            error_user_exists = f'User with email {guest_email} and phone {guest_phone} is already registered. ' \
                                f'Please login to continue or check entered information. Do you want to login?'
            customer_data = {
                'email': guest_email,
            }
            request.session['customer_data'] = customer_data
        elif user_exists_mail:
            error_user_exists = f'User with email {guest_email} is already registered. ' \
                                f'Please login to continue or check entered email. Do you want to login?'
            customer_data = {
                'email': guest_email,
            }
            request.session['customer_data'] = customer_data
        elif user_exists_phone:
            error_user_exists = f'User with phone {guest_phone} is already registered. Please login to continue or' \
                                f'check entered information. Do you want to login?'

        if error_user_exists:
            return JsonResponse({'error_user_exists': error_user_exists})

        guest_name = f"{data['form']['first_name']} {data['form']['last_name']}"

        shipping = data['form']['shipping']
        items = json.loads(request.COOKIES['cart'])
        print('Items:', items)

        customer, created = Customer.objects.get_or_create(guest_email=guest_email)
        customer.guest_name = guest_name
        customer.guest_phone = guest_phone
        customer.save()

        order = Order.objects.create(
            customer=customer,
            status='processing',
            transaction_id=transaction_id,
        )

        if shipping:
            ShippingInfo.objects.create(
                order=order,
                customer=customer,
                city=data['form']['city'],
                np_office=data['form']['np_office'],
            )

        # create order items
        for item in items:
            product = Product.objects.get(id=item)
            quantity = items[item]['quantity']
            item_value = product.price * quantity
            if item_value:
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                )

        guest_phone_validated = str(guest_phone[:3]+' '+guest_phone[3:6]+' '+guest_phone[6:9]+' '+guest_phone[9:11]+' '
                                    + guest_phone[11:])
        # added for new customer registration after guest checkout
        customer_data = {
            'email': guest_email,
            'first_name': data['form']['first_name'],
            'last_name': data['form']['last_name'],
            'phone': guest_phone_validated,
        }

        request.session['customer_data'] = customer_data
        send_order_detail_email(order.id)

    return JsonResponse('Payment submitted..', safe=False)

