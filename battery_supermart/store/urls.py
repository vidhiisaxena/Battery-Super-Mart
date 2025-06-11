from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products_view, name='products'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    path('contact/', views.contact, name='contact'),
    path('product/<slug:slug>/add-review/', views.add_review, name='add_review'),
    path('ajax/get-car-models/', views.get_car_models, name='get_car_models'),
    path('ajax/get-car-data/', views.get_filtered_car_data, name='get_car_data'),
    path('ajax/get-capacities/', views.get_filtered_capacities, name='get_capacities'),
    path('ajax/get-brands/', views.get_filtered_brands, name='get_brands'),
    path('ajax/get-car-brands/', views.get_car_brands_by_category, name='get_car_brands_by_category'),

]
