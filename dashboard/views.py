from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from store.models import Product, Categories, SubCategory, ProductImage
from order.models import Order
from django.contrib.auth.models import User
from .forms import CategoryForm, ProductForm, SubCategoryForm, ProductImageForm
from django.db.models import Sum

@login_required
def dashboard_home(request):

    if not request.user.is_staff:
        return redirect('profile')

    total_revenue = Order.objects.filter(
    status='Delivered'
).aggregate(
    Sum('total_price')
)['total_price__sum'] or 0

    pending_orders = Order.objects.filter(
        status='Pending'
    ).count()

    delivered_orders = Order.objects.filter(
        status='Delivered'
    ).count()

    context = {

        'total_products':
            Product.objects.count(),

        'total_categories':
            Categories.objects.count(),

        'total_subcategories':
            SubCategory.objects.count(),

        'total_orders':
            Order.objects.count(),

        'total_users':
            User.objects.count(),

        'total_revenue':
            total_revenue,

        'pending_orders':
            pending_orders,

        'delivered_orders':
            delivered_orders,

        'recent_orders':
            Order.objects.order_by(
                '-created_at'
            )[:5]
    }

    return render(
        request,
        'dashboard_home.html',
        context
    )


@login_required
def admin_products(request):

    if not request.user.is_staff:
        return redirect('profile')

    products = Product.objects.all()

    return render(
        request,
        'admin_products.html',
        {
            'products': products
        }
    )

@login_required
def add_product(request):

    if not request.user.is_staff:
        return redirect('profile')

    if request.method == 'POST':

        form = ProductForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            return redirect('admin_products')

    else:

        form = ProductForm()

    return render(
        request,
        'add_product.html',
        {
            'form': form
        }
    )

@login_required
def edit_product(request, product_id):

    if not request.user.is_staff:
        return redirect('profile')

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if request.method == 'POST':

        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product
        )

        if form.is_valid():

            form.save()

            return redirect('admin_products')

    else:

        form = ProductForm(
            instance=product
        )

    return render(
        request,
        'edit_product.html',
        {
            'form': form
        }
    )


@login_required
def delete_product(request, product_id):

    if not request.user.is_staff:
        return redirect('profile')

    product = get_object_or_404(
        Product,
        id=product_id
    )

    product.delete()

    return redirect('admin_products')


def admin_categories(request):

    if not request.user.is_staff:
        return redirect('profile')

    categories = Categories.objects.all()

    return render(
        request,
        'admin_categories.html',
        {
            'categories': categories
        }
    )

@login_required
def add_category(request):

    if not request.user.is_staff:
        return redirect('profile')

    if request.method == 'POST':

        form = CategoryForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            return redirect('admin_categories')

    else:

        form = CategoryForm()

    return render(
        request,
        'add_category.html',
        {
            'form': form
        }
    )

@login_required
def edit_category(request, category_id):

    if not request.user.is_staff:
        return redirect('profile')

    category = get_object_or_404(
        Categories,
        id=category_id
    )

    if request.method == 'POST':

        form = CategoryForm(
            request.POST,
            request.FILES,
            instance=category
        )

        if form.is_valid():

            form.save()

            return redirect('admin_categories')

    else:

        form = CategoryForm(
            instance=category
        )

    return render(
        request,
        'edit_category.html',
        {
            'form': form
        }
    )

@login_required
def delete_category(request, category_id):

    if not request.user.is_staff:
        return redirect('profile')

    category = get_object_or_404(
        Categories,
        id=category_id
    )

    category.delete()

    return redirect('admin_categories')


def admin_subcategories(request):

    if not request.user.is_staff:
        return redirect('profile')

    subcategories = SubCategory.objects.select_related('category').all()

    return render(
        request,
        'admin_subcategories.html',
        {
            'subcategories': subcategories
        }
    )


@login_required
def add_subcategory(request):

    if not request.user.is_staff:
        return redirect('profile')

    if request.method == 'POST':
        form = SubCategoryForm(
            request.POST,
            request.FILES
        )

        form = SubCategoryForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            return redirect('admin_subcategories')

    else:

        form = SubCategoryForm()

    return render(
        request,
        'add_subcategory.html',
        {
            'form': form
        }
    )

@login_required
def edit_subcategory(request, subcategory_id):

    if not request.user.is_staff:
        return redirect('profile')

    subcategory = get_object_or_404(
        SubCategory,
        id=subcategory_id
    )

    if request.method == 'POST':
        form = SubCategoryForm(
            request.POST,
            request.FILES,
            instance=subcategory
        )

        
        if form.is_valid():

            form.save()

            return redirect('admin_subcategories')

    else:

        form = SubCategoryForm(
            instance=subcategory
        )

    return render(
        request,
        'edit_subcategory.html',
        {
            'form': form
        }
    )

@login_required
def delete_subcategory(request, subcategory_id):

    if not request.user.is_staff:
        return redirect('profile')

    subcategory = get_object_or_404(
        SubCategory,
        id=subcategory_id
    )

    subcategory.delete()

    return redirect('admin_subcategories')



@login_required
def admin_users(request):

    if not request.user.is_staff:
        return redirect('profile')

    users = User.objects.all()

    return render(
        request,
        'admin_users.html',
        {
            'users': users
        }
    )

@login_required
def toggle_staff(request, user_id):

    if not request.user.is_staff:
        return redirect('profile')

    user = get_object_or_404(
        User,
        id=user_id
    )

    user.is_staff = not user.is_staff
    user.save()

    return redirect('admin_users')


@login_required
def delete_user(request, user_id):

    if not request.user.is_staff:
        return redirect('profile')

    user = get_object_or_404(
        User,
        id=user_id
    )

    if user != request.user:
        user.delete()

    return redirect('admin_users')


@login_required
def admin_orders(request):

    if not request.user.is_staff:
        return redirect('profile')

    orders = Order.objects.all().order_by(
        '-created_at'
    )

    return render(
        request,
        'admin_orders.html',
        {
            'orders': orders
        }
    )

@login_required
def update_order_status(request, order_id):

    if not request.user.is_staff:
        return redirect('profile')

    order = get_object_or_404(
        Order,
        id=order_id
    )

    if request.method == "POST":

        order.status = request.POST.get(
            'status'
        )

        order.save()

    return redirect(
        'admin_orders'
    )


@login_required
def delete_order(request, order_id):

    if not request.user.is_staff:
        return redirect('profile')

    order = get_object_or_404(
        Order,
        id=order_id
    )

    order.delete()

    return redirect(
        'admin_orders'
    )


@login_required
def order_details(request, order_id):

    if not request.user.is_staff:
        return redirect('profile')

    order = get_object_or_404(
        Order,
        id=order_id
    )

    return render(
        request,
        'order_details.html',
        {
            'order': order
        }
    )



@login_required
def add_product_image(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if request.method == 'POST':

        form = ProductImageForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            gallery = form.save(
                commit=False
            )

            gallery.product = product

            gallery.save()

            return redirect(
                'admin_products'
            )

    else:

        form = ProductImageForm()

    return render(
        request,
        'add_product_image.html',
        {
            'form': form,
            'product': product
        }
    )