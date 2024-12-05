from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('product/', views.product_page, name = 'product_page'),
    path('cart/', views.cart_detail, name = 'cart_detail'),
]
