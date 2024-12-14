from store.models import Category, Product, Order, OrderItem, Cart, CartItem, Comment
from django.shortcuts import get_object_or_404, redirect, HttpResponse
from .forms import SignUpForm, Contact, SearchBox, CommentForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group, User
from django.contrib.sessions.models import Session
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.conf import settings
import stripe



# Create your views here.
def home(request, category_slug = None ):
    category_page = None
    products = None
    
    if category_slug != None:
        category_page = get_object_or_404(Category, slug = category_slug)
        products = Product.objects.filter(category = category_page, available = True)
    else:
        products = Product.objects.all().filter(available = True)
        
    return render(request, 'store/home.html', {'category': category_page, 'products': products})

def product_page(request, category_slug, product_slug):
    try:
        product  = Product.objects.get(slug = product_slug, category__slug = category_slug)
        
    except Exception as e :
        raise e 
    
    return render(request, 'store/product_detail.html', {'product': product})

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_to_cart(request, product_id):
    try:
        product = Product.objects.get(id=product_id)


        cart, created = Cart.objects.get_or_create(cart_id=request.session.session_key)

  
        if not product or not cart:
            return HttpResponse("Error: Product or Cart not found", status=404)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if created:
            cart_item.quantity = 1
        else:
            cart_item.quantity += 1

        cart_item.save()

        return redirect('cart_detail')

    except Product.DoesNotExist:
        return HttpResponse("Product not found", status=404)

    except IntegrityError as e:
        return HttpResponse(f"Database error: {str(e)}", status=500)

    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)


    
def cart_detail(request, total=0, counter=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass

    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_total = int(total * 100)
    description = 'Store - New Order'
    data_key = settings.STRIPE_PUBLISHABLE_KEY

    if request.method == 'POST':
        try:
            token = request.POST['stripeToken']
            email = request.POST['stripeEmail']
            billingName = request.POST['stripeBillingName']
            billingAddress1 = request.POST['stripeBillingAddressLine1']
            billingCity = request.POST['stripeBillingAddressCity']
            billingPostcode = request.POST['stripeBillingAddressZip']
            billingCountry = request.POST['stripeBillingAddressCountryCode']
            shippingName = request.POST['stripeShippingName']
            shippingAddress1 = request.POST['stripeShippingAddressLine1']
            shippingCity = request.POST['stripeShippingAddressCity']
            shippingPostcode = request.POST['stripeShippingAddressZip']
            shippingCountry = request.POST['stripeShippingAddressCountryCode']
            customer = stripe.Customer.create(
                email=email,
                source=token
            )
            charge = stripe.Charge.create(
                amount=stripe_total,
                currency='usd',
                description=description,
                customer=customer.id
            )

            try:
                order_details = Order.objects.create(
                    token=token,
                    total=total,
                    emailAddress=email,
                    billingName=billingName,
                    billingAddress1=billingAddress1,
                    billingCity=billingCity,
                    billingPostcode=billingPostcode,
                    billingCountry=billingCountry,
                    shippingName=shippingName,
                    shippingAddress1=shippingAddress1,
                    shippingCity=shippingCity,
                    shippingPostcode=shippingPostcode,
                    shippingCountry=shippingCountry
                )
                order_details.save()
                for order_item in cart_items:
                    or_item = OrderItem.objects.create(
                        product=order_item.product.name,
                        quantity=order_item.quantity,
                        price=order_item.product.price,
                        order=order_details
                    )
                    or_item.save()

                    products = Product.objects.get(id=order_item.product.id)
                    products.stock = int(order_item.product.stock - order_item.quantity)
                    products.save()
                    order_item.delete()

                return redirect('thanks_page', order_details.id)
            except ObjectDoesNotExist:
                pass

        except stripe.error.CardError as e:
            return False, e
	
    return render(request, 'store/cart.html', dict(cart_items=cart_items, total=total, counter=counter, data_key=data_key, stripe_total=stripe_total, description=description))

def cart_remove(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id= product_id)
    cart_item = CartItem.objects.get(product = product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_detail')

def cart_remove_product(request, product_id):
    cart = Cart.objects.filter(cart_id=_cart_id(request)).first()
    try:
        product = Product.objects.get(id=product_id)
        cart_item = CartItem.objects.filter(product=product, cart=cart).first() 
        if cart_item:
            cart_item.delete()
    except Product.DoesNotExist:
        pass  
    return redirect('cart_detail')

def thanks_page(request, order_id):
    if order_id:
        customer_order = get_object_or_404(Order, id=order_id)
    return render(request, 'store/thankyou.html', {'customer_order': customer_order})

def signupview(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            signup_user = User.objects.get(username = username)
            customer_group = Group.objects.get(name = 'Customers')
            customer_group.user_set.add(signup_user)
            login(request, signup_user)
    else:
        form = SignUpForm()
    return render(request, 'store/signup.html', {'form': form})

def signinview(request):
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return redirect('signup')
    else:
        form = AuthenticationForm()
    return render(request, 'store/signin.html', {'form': form})

def signoutview(request):
    logout(request)
    return redirect('signin')

def contatct_us(request):
    if request.method == 'POST':
        form = Contact(request.POST)
        if form.is_valid():
            contact = form.save()
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            email_subject = f'New Contact Form Submission from {name}'
            email_body = f'Message:\n{message}\n\nFrom: {email}'
            email = EmailMessage(
                email_subject,
                email_body,
                'alirezaazizi.official.a@gmail.com',  
                ['alirezaz313313@gmail.com'],  
            )
            email.send()        
            return render(request, 'store/contact_success.html')
    else:
        form = Contact()
        
    return render(request, 'store/contact.html', {'form': form})

def about(request):
    return render(request, 'store/about.html')

def search(request):
    form = SearchBox(request.GET)
    
    if form.is_valid():
        query = form.cleaned_data['query']
        products = Product.objects.filter(name__icontains = query)
        
        if products.exists():
            return render(request, 'store/search_result.html', {'products':products, 'query':query,'form':form})
        
        else:
            return render(request, 'store/search_result.html',{'form':form, 'message':'No products found matching your search.'})
        
    return render(request, 'store/search_result.html', {'form':form})

def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(Product, slug = product_slug, category__slug = category_slug)
    return render(request, 'store/product_detail.html', {'product':product})

def order_history(request):
    if request.user.is_authenticated:
        order = Order.objects.filter(emailAddress = request.user.email)
        return render(request, 'store/order_history.html', {'order':order})
    else:
        return redirect('signin')

@login_required
def add_comment(request, category_slug, product_slug):
    product = get_object_or_404(Product, slug=product_slug, category__slug=category_slug)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.user = request.user
            comment.save()
            return redirect('product_detail', category_slug=category_slug, product_slug=product_slug)
    else:
        form = CommentForm()

    return render(request, 'store/product_detail.html', {'product': product, 'form': form})


