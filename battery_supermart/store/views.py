from django.shortcuts import render, get_object_or_404
from .models import Product, Review

def home(request):
    return render(request, 'home.html')

def products_view(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    reviews = Review.objects.filter(product=product)
    return render(request, 'product_detail.html', {
        'product': product,
        'reviews': reviews
    })

def contact(request):
    return render(request, 'contact.html')
