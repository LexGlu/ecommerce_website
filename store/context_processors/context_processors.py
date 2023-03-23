from store.models import Category, Order


def categories(request):
    categories = Category.objects.all()
    return {'categories': categories}


def items_in_cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer)
        items = order.total_items
    else:
        # temporary value for guest user
        items = 0
    return {'items_in_cart': items}
