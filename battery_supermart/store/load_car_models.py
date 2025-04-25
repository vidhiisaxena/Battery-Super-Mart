import csv
from store.models import CarModel, CarBrand

with open('car_models.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        brand_name = row['brand'].strip()
        model_name = row['model'].strip()

        brand_obj, _ = CarBrand.objects.get_or_create(name=brand_name)
        CarModel.objects.get_or_create(name=model_name, brand=brand_obj)
