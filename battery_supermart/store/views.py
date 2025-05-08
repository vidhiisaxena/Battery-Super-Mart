from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Review, CarModel, CarBrand


def home(request):
    brands = Product.objects.values_list('brand', flat=True).distinct()
    car_brands = CarBrand.objects.prefetch_related('models')
    car_models = CarModel.objects.all()
    best_sellers = Product.objects.filter(is_best_seller=True)

    return render(request, 'main.html', {
        'brands': brands,
        'car_brands': car_brands,
        'car_models': car_models,
        'best_sellers': best_sellers,
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

from django.db.models import Q

from .models import Product, CarBrand, CarModel

def products_view(request):
    products = Product.objects.all()

    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(brand__icontains=query) |
            Q(model__icontains=query)
        )

    selected_brand = request.GET.get('brand')
    if selected_brand:
        products = products.filter(brand=selected_brand)

    selected_make = request.GET.get('make')
    selected_model = request.GET.get('model')

    car_models = CarModel.objects.all()  # default initially

    if selected_make:
        selected_car_brand = CarBrand.objects.filter(name=selected_make).first()
        if selected_car_brand:
            car_models = selected_car_brand.models.all()
            products = products.filter(recommended_for__brand=selected_car_brand)

    if selected_model:
        products = products.filter(recommended_for__name=selected_model)

    context = {
        'products': products,
        'brands': Product.objects.values_list('brand', flat=True).distinct(),
        # 'car_brands': CarBrand.objects.all(),
        'car_brands': CarBrand.objects.prefetch_related('models'),
        'query': query,
        'selected_brand': selected_brand,
        'selected_make': selected_make,
        'selected_model': selected_model,
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