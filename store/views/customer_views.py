from django.shortcuts import render, redirect


def customer_orders(request):
    if not request.user.is_authenticated:
        return redirect('store:home')
    orders_not_open = request.user.customer.order_set.exclude(status='open').order_by('-date_ordered')
    context = {'orders': orders_not_open}
    return render(request, 'store/customer_orders.html', context)
