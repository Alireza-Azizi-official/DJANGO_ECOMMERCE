from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home(request):
    return render(request,'home.html')

def product_page(request):
    return render(request,'product.html')

def cart_detail(request):
    return render(request,'cart.html')
