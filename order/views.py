from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from store.models import Product
from .models import Wishlist, Order
from django.http import HttpResponse
from reportlab.pdfgen import canvas


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

        cart_items.delete()

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

@login_required
def download_invoice(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    response = HttpResponse(
        content_type='application/pdf'
    )

    response[
        'Content-Disposition'
    ] = f'attachment; filename="NovaCart_Invoice_{order.id}.pdf"'

    pdf = canvas.Canvas(response)

    # ==========================
    # HEADER
    # ==========================

    pdf.setFillColorRGB(
        0.05,
        0.1,
        0.2
    )

    pdf.rect(
        0,
        770,
        700,
        50,
        fill=1
    )

    pdf.setFillColorRGB(
        1,
        1,
        1
    )

    pdf.setFont(
        "Helvetica-Bold",
        22
    )

    pdf.drawString(
        40,
        790,
        "NovaCart Invoice"
    )

    # ==========================
    # CUSTOMER DETAILS
    # ==========================

    pdf.setFillColorRGB(
        0,
        0,
        0
    )

    pdf.setFont(
        "Helvetica-Bold",
        12
    )

    pdf.drawString(
        40,
        735,
        "Customer Details"
    )

    pdf.rect(
        35,
        620,
        520,
        95
    )

    pdf.setFont(
        "Helvetica",
        11
    )

    pdf.drawString(
        50,
        690,
        f"Name: {order.full_name}"
    )

    pdf.drawString(
        50,
        670,
        f"Phone: {order.phone}"
    )

    pdf.drawString(
        50,
        650,
        f"Order ID: {order.id}"
    )

    pdf.drawString(
        300,
        690,
        f"Status: {order.status}"
    )

    pdf.drawString(
        300,
        670,
        f"Payment: {order.payment_method}"
    )

    pdf.drawString(
        300,
        650,
        f"Date: {order.created_at.strftime('%d-%m-%Y')}"
    )

    # ==========================
    # ADDRESS
    # ==========================

    pdf.setFont(
        "Helvetica-Bold",
        12
    )

    pdf.drawString(
        40,
        590,
        "Delivery Address"
    )

    pdf.setFont(
        "Helvetica",
        11
    )

    pdf.drawString(
        50,
        570,
        order.address[:70]
    )

    pdf.drawString(
        50,
        550,
        f"{order.city}, {order.state} - {order.pincode}"
    )

    # ==========================
    # PRODUCT TABLE HEADER
    # ==========================

    pdf.setFillColorRGB(
        0.05,
        0.1,
        0.2
    )

    pdf.rect(
        35,
        500,
        520,
        30,
        fill=1
    )

    pdf.setFillColorRGB(
        1,
        1,
        1
    )

    pdf.setFont(
        "Helvetica-Bold",
        11
    )

    pdf.drawString(
        50,
        510,
        "Product"
    )

    pdf.drawString(
        320,
        510,
        "Qty"
    )

    pdf.drawString(
        420,
        510,
        "Price"
    )

    # ==========================
    # PRODUCT ROWS
    # ==========================

    y = 470

    pdf.setFillColorRGB(
        0,
        0,
        0
    )

    pdf.setFont(
        "Helvetica",
        11
    )

    for item in order.items.all():

        pdf.drawString(
            50,
            y,
            item.product.name[:35]
        )

        pdf.drawString(
            330,
            y,
            str(item.quantity)
        )

        pdf.drawString(
            420,
            y,
            f"Rs. {item.price}"
        )

        y -= 25

    # ==========================
    # TOTAL BOX
    # ==========================

    pdf.setFillColorRGB(
        0.10,
        0.65,
        0.30
    )

    pdf.rect(
        350,
        y - 20,
        200,
        40,
        fill=1
    )

    pdf.setFillColorRGB(
        1,
        1,
        1
    )

    pdf.setFont(
        "Helvetica-Bold",
        14
    )

    pdf.drawString(
        370,
        y,
        f"Total: Rs. {order.total_price}"
    )

    # ==========================
    # FOOTER
    # ==========================

    pdf.setFillColorRGB(
        0,
        0,
        0
    )

    pdf.setFont(
        "Helvetica-Oblique",
        10
    )

    pdf.drawString(
        40,
        50,
        "Thank you for shopping with NovaCart!"
    )

    pdf.drawString(
        40,
        35,
        "This is a computer generated invoice."
    )

    pdf.save()

    return response