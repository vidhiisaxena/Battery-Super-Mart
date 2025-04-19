from django.shortcuts import render, get_object_or_404
from .models import Product, Review

def home(request):
    brands = Product.objects.values_list('brand', flat=True).distinct()
    models = Product.objects.values_list('model', flat=True).distinct()
    best_sellers = Product.objects.filter(is_best_seller=True)

    return render(request, 'main.html', {
        'brands': brands,
        'models': models,
        'best_sellers': best_sellers,
    })

from django.db.models import Q

def products_view(request):
    products = Product.objects.all()

    # Get search query
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(brand__icontains=query) |
            Q(model__icontains=query)
        )

    # Get filter values from query parameters
    selected_brands = request.GET.getlist('brand')
    selected_categories = request.GET.getlist('category')

    # Apply filters if selected
    if selected_brands:
        products = products.filter(brand__in=selected_brands)
    if selected_categories:
        products = products.filter(category__in=selected_categories)

    # Get unique brands and categories from DB for filters
    all_brands = Product.objects.values_list('brand', flat=True).distinct()
    all_categories = Product.objects.values_list('category', flat=True).distinct()

    context = {
        'products': products,
        'brands': all_brands,
        'categories': all_categories,
        'selected_brands': selected_brands,
        'selected_categories': selected_categories,
        'query': query,
    }
    return render(request, 'products.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    reviews = Review.objects.filter(product=product)
    return render(request, 'product_detail.html', {
        'product': product,
        'reviews': reviews
    })

def contact(request):
    return render(request, 'contact.html')
