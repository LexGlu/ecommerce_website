from django.urls import path
from .views import ProductList, ReviewCreate, ProductDetail, sign_up, log_in

app_name = 'api'
urlpatterns = [
    path('products/', ProductList.as_view(), name='api_products'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='api_product_detail'),
    path('products/<int:product_id>/review/', ReviewCreate.as_view(), name='api_reviews'),
    path('signup/', sign_up, name='signup'),
    path('login/', log_in, name='login'),
]
