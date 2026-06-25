from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.dashboard_home,
        name='dashboard_home'
    ),
    path(
        'products/',
        views.admin_products,
        name='admin_products'
    ),
    path(
        'products/add/',
        views.add_product,
        name='add_product'
    ),
    path(
        'products/edit/<int:product_id>/',
        views.edit_product,
        name='edit_product'
    ),
    path(
        'products/delete/<int:product_id>/',
        views.delete_product,
        name='delete_product'
    ),

    path(
    'categories/',
    views.admin_categories,
    name='admin_categories'
),

    path(
    'categories/add/',
    views.add_category,
    name='add_category'
),

    path(
    'categories/edit/<int:category_id>/',
    views.edit_category,
    name='edit_category'
),

    path(
    'categories/delete/<int:category_id>/',
    views.delete_category,
    name='delete_category'
),
    path(
    'subcategories/',
    views.admin_subcategories,
    name='admin_subcategories'
),
    path(
    'subcategories/add/',
    views.add_subcategory,
    name='add_subcategory'
),

    path(
    'subcategories/edit/<int:subcategory_id>/',
    views.edit_subcategory,
    name='edit_subcategory'
),

    path(
    'subcategories/delete/<int:subcategory_id>/',
    views.delete_subcategory,
    name='delete_subcategory'
),


    path(
    'users/',
    views.admin_users,
    name='admin_users'
),

    path(
    'users/delete/<int:user_id>/',
    views.delete_user,
    name='delete_user'
),

    path(
    'users/toggle-staff/<int:user_id>/',
    views.toggle_staff,
    name='toggle_staff'
),

    path(
    'orders/',
    views.admin_orders,
    name='admin_orders'
),

path(
    'orders/status/<int:order_id>/',
    views.update_order_status,
    name='update_order_status'
),

path(
    'orders/delete/<int:order_id>/',
    views.delete_order,
    name='delete_order'
),

  path(
    'orders/<int:order_id>/',
    views.order_details,
    name='order_details'
),


  path(
    'products/<int:product_id>/gallery/add/',
    views.add_product_image,
    name='add_product_image'
),
]