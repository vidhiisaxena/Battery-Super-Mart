from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Review, CarModel, CarBrand


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

    # Search query
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(brand__icontains=query) |
            Q(model__icontains=query)
        )

    # Brand & category filters
    selected_brands = request.GET.getlist('brand')
    selected_categories = request.GET.getlist('category')

    if selected_brands:
        products = products.filter(brand__in=selected_brands)
    if selected_categories:
        products = products.filter(category__in=selected_categories)
    

    # Filter by car model (using slugs now!)
    selected_car_model_slugs = [slug for slug in request.GET.getlist('car_model') if slug.strip()]
    if selected_car_model_slugs:
        products = products.filter(recommended_for__slug__in=selected_car_model_slugs).distinct()

    # Get all available filter options
    all_brands = Product.objects.values_list('brand', flat=True).distinct()
    all_categories = Product.objects.values_list('category', flat=True).distinct()

    # Fetch car brands with related models
    car_brands = CarBrand.objects.prefetch_related('models').all()

    context = {
        'products': products,
        'brands': all_brands,
        'categories': all_categories,
        'car_brands': car_brands,
        'selected_brands': selected_brands,
        'selected_categories': selected_categories,
        'selected_car_models': selected_car_model_slugs,
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

def add_review(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        content = request.POST.get('review')

        Review.objects.create(
            product=product,
            name=name,
            email=email,
            content=content
        )
    return redirect('product_detail', slug=slug)