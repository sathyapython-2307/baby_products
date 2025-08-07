from django.urls import path


from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('boys-fashion/', views.boys_fashion_view, name='boys_fashion'),
    path('girls-fashion/', views.girls_fashion_view, name='girls_fashion'),
    path('soap/', views.soap_view, name='soap'),
    path('stroller/', views.stroller_view, name='stroller'),
    path('bottle/', views.bottle_view, name='bottle'),
    path('offers/', views.offers_view, name='offers'),
    path('', views.home_view, name='home'),
    path('pampers/', views.pampers_view, name='pampers'),

    # About page
    path('about/', views.about_view, name='about'),

    # Contact page
    path('contact/', views.contact_view, name='contact'),

    # Cart and checkout
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<str:item_id>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<str:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order-complete/', views.order_complete_view, name='order_complete'),
]
