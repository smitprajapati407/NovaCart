from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_view, name='cart'),

    path(
        'add_to_cart/<int:product_id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),

    path(
        'increase_quantity/<int:cart_item_id>/',
        views.increase_quantity,
        name='increase_quantity'
    ),

    path(
        'decrease_quantity/<int:cart_item_id>/',
        views.decrease_quantity,
        name='decrease_quantity'
    ),
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('success/', views.order_success, name='order_success'),
    path(
    'add-to-wishlist/<int:product_id>/',
    views.add_to_wishlist,
    name='add_to_wishlist'
),
    path(
    'wishlist/',
    views.wishlist,
    name='wishlist'
),
    path('remove-from-wishlist/<int:product_id>/',
    views.remove_from_wishlist,
    name='remove_from_wishlist'),

    path(
    'order-history/',
    views.order_history,
    name='order_history'
),
    path(
    'remove-from-cart/<int:cart_item_id>/',
    views.remove_from_cart,
    name='remove_from_cart'
),
    path(
    'my-orders/',
    views.my_orders,
    name='my_orders'
),

path(
    'my-orders/<int:order_id>/',
    views.order_detail_user,
    name='order_detail_user'
),

path(
    'invoice/<int:order_id>/',
    views.download_invoice,
    name='download_invoice'
),

]