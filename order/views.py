from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from store.models import Product
from .models import Wishlist, Order


@login_required
def add_to_cart(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    if product.stock <= 0:

     return redirect(
        'product_detail',
        product.id
    )

    user_cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_item, created = CartItem.objects.get_or_create(
        cart=user_cart,
        product=product
    )

    if not created:

     if cart_item.quantity < product.stock:

        cart_item.quantity += 1

        cart_item.save()

    return redirect('cart')


@login_required
def cart_view(request):

    user_cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_items = CartItem.objects.filter(
        cart=user_cart
    )

    total_price = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    return render(
        request,
        'cart.html',
        {
            'cart_items': cart_items,
            'total_price': total_price
        }
    )


@login_required
def increase_quantity(request, cart_item_id):

    item = get_object_or_404(
        CartItem,
        id=cart_item_id,
        cart__user=request.user
    )

    if item.quantity < item.product.stock:

     item.quantity += 1

    item.save()

    return redirect('cart')


@login_required
def decrease_quantity(request, cart_item_id):

    item = get_object_or_404(
        CartItem,
        id=cart_item_id,
        cart__user=request.user
    )

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('cart')

from django.shortcuts import render
from .models import Cart, CartItem

def checkout(request):

    cart = Cart.objects.get(user=request.user)

    cart_items = CartItem.objects.filter(cart=cart)

    total = 0

    for item in cart_items:
        total += item.product.price * item.quantity

    context = {
        'cart_items': cart_items,
        'total': total,
    }

    return render(request, 'checkout.html', context)

from django.shortcuts import redirect
from .models import Order, OrderItem, Cart, CartItem


def place_order(request):

    if request.method == "POST":

        cart, created = Cart.objects.get_or_create(
            user=request.user
        )

        cart_items = CartItem.objects.filter(
            cart=cart
        )

        total = sum(
            item.product.price * item.quantity
            for item in cart_items
        )

        order = Order.objects.create(
            user=request.user,
            full_name=request.POST['full_name'],
            phone=request.POST['phone'],
            address=request.POST['address'],
            city=request.POST['city'],
            state=request.POST['state'],
            pincode=request.POST['pincode'],
            payment_method='COD',
            total_price=total
        )

        for item in cart_items:

         product = item.product

    if product.stock >= item.quantity:

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=item.quantity,
            price=product.price
        )

        product.stock -= item.quantity

        product.save()
        return redirect('order_success')
def order_success(request):
    return render(
        request,
        'order_success.html'
    )

def add_to_wishlist(request, product_id):

    if not request.user.is_authenticated:
        return redirect('login')

    product = get_object_or_404(
        Product,
        id=product_id
    )

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def wishlist(request):

    wishlist_items = Wishlist.objects.filter(
        user=request.user
    )

    return render(
        request,
        'wishlist.html',
        {
            'wishlist_items': wishlist_items
        }
    )


def remove_from_wishlist(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    Wishlist.objects.filter(
        user=request.user,
        product=product
    ).delete()

    return redirect('wishlist')


@login_required
def order_history(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'order_history.html',
        {
            'orders': orders
        }
    )

@login_required
def remove_from_cart(request, cart_item_id):

    item = get_object_or_404(
        CartItem,
        id=cart_item_id,
        cart__user=request.user
    )

    item.delete()

    return redirect('cart')


@login_required
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'my_orders.html',
        {
            'orders': orders
        }
    )


@login_required
def order_detail_user(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        'order_detail_user.html',
        {
            'order': order
        }
    )