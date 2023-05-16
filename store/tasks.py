from ecom_website.celery import app
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
from store.models import Order


@app.task
def send_welcome_email(user_id):
    user = User.objects.get(id=user_id)
    subject = "Welcome to Pineapple Store!"
    message = f"Hi {user.first_name} {user.last_name}!\n" \
              "Thank you for registering in our store!\n" \
              "Best regards,\n" \
              "Pineapple Team\n" \

    sender = settings.EMAIL_HOST_USER
    recipient = user.email
    send_mail(subject, message, sender, [recipient], fail_silently=False)


@app.task
def send_order_detail_email(order_id):
    order = Order.objects.get(id=order_id)
    subject = f"Your order {order.transaction_id} is confirmed!"
    products = order.all_items
    cabinet_link = f'https://lexglu.online/cabinet/orders/'
    message = f'Hi {order.customer.full_name}!\n' \
              f'Your order {order.transaction_id} has been accepted.\n' \
              f'Products:\n'
    for index, product in enumerate(products):
        message += f'{index + 1}) {product.product.name}. Price: {product.product.price} UAH. Quantity: {product.quantity}.\n'

    if order.shipping:
        message += f'Shipping to {order.shipping_city} in Nova Poshta office #{order.shipping_np_office()}.\n'

    message += f'Total: {order.total_value} UAH.\n' \
               f'You can track your order status in your cabinet: {cabinet_link}\n' \
               'Best regards,\n' \
               'Pineapple Team'

    sender = settings.EMAIL_HOST_USER
    
    if order.customer.user:
        recipient = order.customer.user.email
    else:
        recipient = order.customer.guest_email
    
    send_mail(subject, message, sender, [recipient], fail_silently=False)
