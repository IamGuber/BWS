from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products', views.ProductsListView.as_view(), name='products'),
    path('products/<int:product_id>', views.ProductDetailView.as_view(), name='product'),
    path('user_orders/', views.UserOrdersListView.as_view(), name='user_orders'),
    path('register/', views.register, name='register'),
]
