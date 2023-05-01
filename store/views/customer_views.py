from django.shortcuts import render


def customer_orders(request):
    user = request.user
    orders_not_open = user.customer.order_set.exclude(status='open').order_by('-date_ordered')
    context = {'orders': orders_not_open}
    return render(request, 'store/customer_orders.html', context)
