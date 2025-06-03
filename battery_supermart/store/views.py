from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Review, CarModel, CarBrand
from store.models import CarBrand, CarModel

from .models import CATEGORY_CHOICES

def home(request):
    brands = Product.objects.values_list('brand', flat=True).distinct()
    car_brands = CarBrand.objects.prefetch_related('models')
    car_models = CarModel.objects.all()
    best_sellers = Product.objects.filter(is_best_seller=True)
    selected_capacity = request.GET.get('capacity')

    # Dynamically fetch unique non-empty capacities
    capacities = (
        Product.objects.exclude(capacity__isnull=True)
                      .exclude(capacity__exact="")
                      .values_list('capacity', flat=True)
                      .distinct()
    )

    return render(request, 'main.html', {
        'brands': brands,
        'car_brands': car_brands,
        'car_models': car_models,
        'best_sellers': best_sellers,
        'category_choices': CATEGORY_CHOICES,
        'selected_capacity': selected_capacity,
        'capacities': capacities,  # <-- ✅ Now added
    })



from django.http import JsonResponse

def get_car_models(request):
    make = request.GET.get('make')
    models = []

    if make:
        car_brand = CarBrand.objects.filter(name=make).first()
        if car_brand:
            models = list(car_brand.models.values('name', 'slug'))

    return JsonResponse({'models': models})

from django.shortcuts import render
from django.db.models import Q
from .models import Product, CarBrand, CarModel, CATEGORY_CHOICES

def products_view(request):
    products = Product.objects.all()

    # GET filter values
    query = request.GET.get("q")
    selected_brands = request.GET.getlist("brand")
    selected_categories = request.GET.getlist("category")
    selected_car_models = request.GET.getlist("car_model")

    selected_category = request.GET.get('category')
    selected_brand = request.GET.get('brand')
    selected_make = request.GET.get('make')
    selected_model = request.GET.get('model')
    selected_capacity = request.GET.get('capacity')

    # Apply category-based filtering
    if selected_category:
        products = products.filter(category=selected_category)

        if selected_brand:
            products = products.filter(brand=selected_brand)

        if selected_category in ['2_wheeler', 'Car', 'truck']:
            if selected_make:
                products = products.filter(recommended_for__brand__name=selected_make)
            if selected_model:
                products = products.filter(recommended_for__name=selected_model)

        elif selected_category in [
            'computer_ups', 'inverter_combo', 'inverter_ups', 'inverter_batteries',
            'smf_vrla', 'lithium_ion', 'inverter_lithium'
        ]:
            if selected_capacity:
                products = products.filter(capacity=selected_capacity)

    # Apply search query
    if query:
        matched_brand = CarBrand.objects.filter(name__icontains=query).first()
        if matched_brand and matched_brand.name not in selected_brands:
            selected_brands.append(matched_brand.name)

        matched_models = CarModel.objects.filter(name__icontains=query)
        for model in matched_models:
            if model.slug not in selected_car_models:
                selected_car_models.append(model.slug)

        products = products.filter(
            Q(name__icontains=query) |
            Q(brand__icontains=query) |
            Q(model__icontains=query) |
            Q(recommended_for__brand__name__icontains=query) |
            Q(recommended_for__name__icontains=query)
        ).distinct()

    # Filter values to be displayed in UI
    brands = Product.objects.values_list('brand', flat=True).distinct()
    capacities = Product.objects.values_list('capacity', flat=True).distinct()
    car_brands = CarBrand.objects.prefetch_related('models').all()

    # Handle car models shown based on selected make
    car_models = CarModel.objects.all()
    if selected_make:
        selected_car_brand = CarBrand.objects.filter(name=selected_make).first()
        if selected_car_brand:
            car_models = selected_car_brand.models.all()

    context = {
        'products': products,
        'brands': brands,
        'capacities': capacities,
        'car_brands': car_brands,
        'car_models': car_models,
        'category_choices': CATEGORY_CHOICES,

        # For form selection persistence
        'selected_brands': selected_brands,
        'selected_categories': selected_categories,
        'selected_category': selected_category,
        'selected_make': selected_make,
        'selected_model': selected_model,
        'selected_capacity': selected_capacity,
        'selected_car_models': selected_car_models,
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