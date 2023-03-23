from django.urls import path
from .views.home import HomeView
from .views.category import CategoryView
from .views.product import ProductView
from .views.auth import sign_up, log_in, log_out
from .views.search import search_product
from .views.cart import cart, checkout, update_item

app_name = 'store'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('category/<slug:category_slug>/', CategoryView.as_view(), name='category'),
    path('product/<int:product_id>/', ProductView.as_view(), name='product'),
    path('signup/', sign_up, name='signup'),
    path('login/', log_in, name='login'),
    path('logout/', log_out, name='logout'),
    path('search/', search_product, name='search'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('update_item/', update_item, name='update_item'),
]
