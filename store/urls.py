from django.urls import path
from .views.home import HomeView
from .views.category import CategoryView
from .views.product import ProductView

app_name = 'store'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('category/<slug:category_slug>/', CategoryView.as_view(), name='category'),
    path('product/<int:product_id>/', ProductView.as_view(), name='product'),
]
