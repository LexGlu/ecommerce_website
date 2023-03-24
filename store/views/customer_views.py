from django.shortcuts import render


def customer_orders(request):
    orders_not_open = request.user.customer.order_set.exclude(status='open')
    context = {'orders': orders_not_open}
    return render(request, 'store/customer_orders.html', context)
