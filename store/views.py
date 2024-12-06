from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Category, Product, CartItem, Cart
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def home(request, category_slug = None):
    category_page = None
    products = None
    
    if category_slug:
        category_page = get_object_or_404(Category, slug = category_slug)
        products = Product.objects.filter(category = category_page, available = True)
    else:
        products = Product.objects.filter(available = True)
        
    categories = Category.objects.all()
    return render(request, 'home.html', {
        'category_page': category_page,
        'products':products,
        'links':categories
    })



def product_page(request, category_slug, product_slug):
    try:
        product = Product.objects.get(slug = product_slug, category__slug = category_slug)
    except Exception as e :
        raise e 
    
    return render(request,'product.html', {'product': product})

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    print("Cart ID:", cart) 
    return cart


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
            cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1
        )
        cart.save()
    
    return redirect('cart_detail') 

def cart_detail(request, total=0, counter=0, cart_item=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        cart_items = []  # اطمینان حاصل کنید که در صورت نداشتن سبد خرید، به درستی خالی باشد
    
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
        'counter': counter
    })
