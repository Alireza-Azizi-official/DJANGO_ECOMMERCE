from django.shortcuts import render
from django.http import HttpResponse
from .models import Category, Product
from django.shortcuts import get_object_or_404

# Create your views here.
def home(request, category_slug=None):
    category_page = None
    products = None
    if category_slug != None:
        category_slug = get_object_or_404(Category, slug = category_slug)
        products = Product.objects.filter(category = category_page, available = True)
    else:
        prodcuts = Product.objects.all().filter(available = True)
    return render(request,'home.html',{'category_page': category_page, 'products': products})

def product_page(request):
    return render(request,'product.html')

def cart_detail(request):
    return render(request,'cart.html')
