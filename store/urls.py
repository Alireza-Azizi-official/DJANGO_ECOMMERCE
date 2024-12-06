from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<slug:category_slug>/', views.home, name='products_by_category'),
    path('<slug:category_slug>/<slug:product_slug>/', views.product_page, name='product_detail'),
    path('cart/add/<int:product_id>', views.add_cart, name='add_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
]
