from django.contrib import admin
from .models import Categories, SubCategory, Product


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'subcategory', 'price']
    list_filter = ['category', 'subcategory']
    search_fields = ['name']