from django import forms
from store.models import Product

class ProductForm(forms.ModelForm):

 class Meta:
    model = Product

    fields = [
        'category',
        'subcategory',
        'name',
        'description',
        'price',
        'image'
    ]

from store.models import Categories

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Categories

        fields = [
            'name',
            'description',
            'image'
        ]

from store.models import SubCategory

class SubCategoryForm(forms.ModelForm):

    class Meta:
        model = SubCategory

        fields = [
            'category',
            'name'
        ]       