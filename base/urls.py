from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *
urlpatterns = [
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', create_user, name='register'),
    path('register/send_otp', send_otp, name="send_otp"),
    #Password Reset Urls
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('', home, name="homepage" ),
    path('shop/', shop, name="shop"),
    path('shop/all-products', all_products, name="all-products"),
    path('shop/product-detail/<int:id>', product_detail, name="product-detail"),
    path('cart/', cart, name="cart"),
    path('checkout/', checkout, name="checkout"),
    path('search/', search, name="search"),
    path('search/product/', search_product, name="search-product"),
    path('update_item/', updateItem, name="update-item"),
    path('process_order/', processOrder, name="process_order"),
    path('why/', why, name="why"),
    path('testimonial/', testimonial, name="testimonial"),
    path('contact/', contact, name="contact"),
    path('contact_us/', contact_us, name="contact_us"),
]
