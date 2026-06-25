from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('categories/', views.categories, name='categories'),
    path('products/<int:category_id>/', views.products, name='products'),
    path('subcategory/<int:subcategory_id>/', views.subcategory_products, name='subcategory_products'),
    path('search/', views.search, name='search'),
    path(
    'product/<int:product_id>/',
    views.product_detail,
    name='product_detail'
),
    
]



