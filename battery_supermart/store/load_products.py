import csv
from decimal import Decimal
from django.utils.text import slugify
from store.models import Product, CarModel

# Path to your default image (already uploaded to /media/products/default.jpg)
DEFAULT_IMAGE_PATH = 'static/img/default_battery.jpg'

with open('products.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = row['Name'].strip()
        slug = slugify(name)
        model_name = row['Model'].strip()
        brand = row['Brand'].strip()
        category = row['Category'].strip()
        capacity = row['Capacity'].strip()
        warranty = row['Warranty'].strip()
        mrp = Decimal(row['MRP'].strip())
        price_with_old = Decimal(row['Price with Old Battery'].strip())
        price_without_old = Decimal(row['Price without Old Battery'].strip())
        coupon_code = row['Coupon Code'].strip()
        note = row['Note'].strip()
        description = row['Description'].strip()
        recommended_model_names = [m.strip() for m in row['Recommended For'].split(',')]
        is_best_seller = row['Is Best Seller'].strip().lower() in ['true', '1', 'yes']

        # Create or get the product
        product, created = Product.objects.get_or_create(
            name=name,
            slug=slug,
            defaults={
                'image': DEFAULT_IMAGE_PATH,
                'model': model_name,
                'brand': brand,
                'category': category,
                'capacity': capacity,
                'warranty': warranty,
                'mrp': mrp,
                'price_with_old_battery': price_with_old,
                'price_without_old_battery': price_without_old,
                'coupon_code': coupon_code,
                'note': note,
                'description': description,
                'is_best_seller': is_best_seller,
            }
        )

        # Add many-to-many recommended car models
        for model_name in recommended_model_names:
            car_models = CarModel.objects.filter(name=model_name)
            if car_models.exists():
                for car_model in car_models:
                    product.recommended_for.add(car_model)
            else:
                print(f"⚠️ Car model '{model_name}' not found. Skipping...")

        product.save()
