from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-wishlist/<int:id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('cart/increase/<int:id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:id>/', views.decrease_quantity, name='decrease_quantity'),
    path('cart/remove/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('place-order/', views.place_order, name='place_order'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('my-orders/', views.my_orders, name='my_orders'),


]
