from django.shortcuts import render, redirect, get_object_or_404

from .models import Categories, Product, SubCategory
from django.db.models import Q
from .models import Product, Review
from .forms import ReviewForm

def home(request):
    query = request.GET.get('q', '')

    products = Product.objects.all()
    categories = Categories.objects.all()

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )

        categories = Categories.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    return render(
        request,
        'home.html',
        {
            'products': products,
            'categories': categories,
            'query': query,
        }
    )



def search(request):
    query = request.GET.get('q', '')

    products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query) |
        Q(category__name__icontains=query)
    ) if query else Product.objects.none()

    categories = Categories.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query)
    ) if query else Categories.objects.none()

    return render(
        request,
        'search_results.html',
        {
            'query': query,
            'products': products,
            'categories': categories
        }
    )
def categories(request):
    categories = Categories.objects.all()
    return render(request=request, template_name='categories.html', context={'categories': categories})


def subcategory_products(request, subcategory_id):
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)

    products = Product.objects.filter(
        subcategory=subcategory
    )

    return render(
        request,
        'subcategory_products.html',
        {
            'subcategory': subcategory,
            'products': products
        }
    )

def products(request, category_id):

    category = get_object_or_404(
        Categories,
        id=category_id
    )

    products = Product.objects.filter(
        category=category
    )

    subcategories = SubCategory.objects.filter(
        category=category
    )

    subcategory_id = request.GET.get('subcategory')

    if subcategory_id:
        products = products.filter(
            subcategory_id=subcategory_id
        )

    min_price = request.GET.get('min_price')

    if min_price:
        products = products.filter(
            price__gte=min_price
        )

    max_price = request.GET.get('max_price')

    if max_price:
        products = products.filter(
            price__lte=max_price
        )
        
    sort_by = request.GET.get('sort')

    if sort_by == 'low':
     products = products.order_by('price')

    elif sort_by == 'high':
     products = products.order_by('-price')

    elif sort_by == 'name_asc':
     products = products.order_by('name')

    elif sort_by == 'name_desc':
     products = products.order_by('-name')
        

    return render(
        request,
        'products.html',
        {
            'category': category,
            'products': products,
            'subcategories': subcategories,
        }
    )


def product_detail(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    related_products = Product.objects.filter(
        category=product.category
    ).exclude(
        id=product.id
    )[:4]

    reviews = Review.objects.filter(
        product=product
    ).order_by('-created_at')

    if request.method == "POST":

        if request.user.is_authenticated:

            Review.objects.create(
                product=product,
                user=request.user,
                rating=request.POST['rating'],
                comment=request.POST['comment']
            )

            return redirect(
                'product_detail',
                product_id=product.id
            )

    context = {

        'product': product,

        'related_products': related_products,

        'reviews': reviews

    }

    return render(
        request,
        'product_detail.html',
        context
    )
# Create your views here.
