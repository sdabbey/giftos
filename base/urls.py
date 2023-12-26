from django.urls import path
from .views import *
urlpatterns = [
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', create_user, name='register'),
    path('register/send_otp', send_otp, name="send_otp"),
    path('', home, name="homepage" ),
    path('shop/', shop, name="shop"),
    path('shop/all-products', all_products, name="all-products"),
    path('shop/product-detail/<int:id>', product_detail, name="product-detail"),
    path('cart/', cart, name="cart"),
    path('checkout/', checkout, name="checkout"),
    path('update_item/', updateItem, name="update-item"),
    path('process_order/', processOrder, name="process_order"),
    path('why/', why, name="why"),
    path('testimonial/', testimonial, name="testimonial"),
    path('contact/', contact, name="contact")
]
