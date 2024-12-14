from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.home , name="home"),
    path('category/<slug:category_slug>', views.home , name="products_by_category"),
    path('category/<slug:category_slug>/<slug:product_slug>', views.product_page , name="product_detail"),
    path('cart/add/<int:product_id>', views.add_to_cart, name='add_cart'),
    path('cart/remove/<int:product_id>', views.cart_remove, name='cart_remove'),
    path('cart/remove_product/<int:product_id>', views.cart_remove_product, name='cart_remove_product'),
    path('cart/', views.cart_detail , name="cart_detail"),
    path('thankyou/<int:order_id>', views.thanks_page, name='thanks_page'),
    path('account/create/', views.signupview, name='signup'),
    path('account/signin/', views.signinview, name='signin'),
    path('account/signout/', views.signoutview, name='signout'),
    path('contact/', views.contatct_us, name = 'contact'),
    path('about/', views.about, name = 'about'),
    path('search/', views.search, name = 'search'),
    path('order-history/', views.order_history, name='orderhistory'), 
    path('product/<slug:category_slug>/<slug:product_slug>/comment/', views.add_comment, name = 'addcomment'),
    path('product/<slug:category_slug>/<slug:product_slug>/', views.product_page, name='product_detail'),
    path('product/<slug:category_slug>/<slug:product_slug>/comment/', views.add_comment, name='add_comment'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
