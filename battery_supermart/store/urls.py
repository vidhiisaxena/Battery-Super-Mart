from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products_view, name='products'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    path('contact/', views.contact, name='contact'),
    path('product/<slug:slug>/add-review/', views.add_review, name='add_review'),
]
