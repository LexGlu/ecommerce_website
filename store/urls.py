from django.urls import path
from .views.home import HomeView
from .views.category import CategoryView
from .views.product import ProductView, add_review
from .views.auth import sign_up, log_in, log_out, update_cart_after_logout
from .views.search import search_product, search_elastic
from .views.cart import cart, checkout, update_item, process_order
from .views.customer_views import customer_orders

app_name = 'store'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('category/<slug:category_slug>/', CategoryView.as_view(), name='category'),
    path('product/<int:product_id>/', ProductView.as_view(), name='product'),
    path('signup/', sign_up, name='signup'),
    path('login/', log_in, name='login'),
    path('logout/', log_out, name='logout'),
    path('search/', search_product, name='search'),
    path('search_elastic/', search_elastic, name='search_elastic'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('update_item/', update_item, name='update_item'),
    path('update_cart/', update_cart_after_logout, name='update_cart_after_logout'),
    path('process_order/', process_order, name='process_order'),
    path('cabinet/orders/', customer_orders, name='customer_orders'),
    path('add_review/<int:product_id>/', add_review, name='add_review'),
]
