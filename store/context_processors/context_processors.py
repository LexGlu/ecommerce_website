import json
from store.models import Category, Order


def categories(request):
    catalogue = Category.objects.all()
    return {'catalogue': catalogue}


def items_in_cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, status='open')
        items = order.total_items
    else:
        try:
            guest_cart = json.loads(request.COOKIES['cart'])
            items = sum([guest_cart[product_id]['quantity'] for product_id in guest_cart])
        except KeyError:
            items = 0

    return {'items_in_cart': items}
