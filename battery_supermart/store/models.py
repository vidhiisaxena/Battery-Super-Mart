from django.db import models
from django.utils.text import slugify

CATEGORY_CHOICES = [
    ('2_wheeler', '2 Wheeler Batteries'),
    ('Car', 'Car'),
    # ('4_wheeler', '4 Wheeler Batteries'),
    ('computer_ups', 'Computer UPS'),
    ('inverter_combo', 'Inverter and Battery Combo'),
    ('inverter_ups', 'Inverter and UPS Systems'),
    ('inverter_batteries', 'Inverter Batteries'),
    ('smf_vrla', 'SMF/VRLA Batteries'),
    ('truck', 'Truck Batteries'),
    ('lithium_ion', 'Lithium Ion Batteries'),
    ('inverter_lithium', 'Inverter + Lithium Ion Batteries'),
]

# models.py

class CarBrand(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Car')

    def __str__(self):
        return self.name

from django.utils.text import slugify

class CarModel(models.Model):
    name = models.CharField(max_length=100)
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE, related_name='models', default=1)
    slug = models.SlugField(null=True, blank=True, unique=True)
  # No unique yet!
  # NEW FIELD

    def __str__(self):
        return f"{self.brand.name} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug_candidate = base_slug
            counter = 1
            while CarModel.objects.filter(slug=slug_candidate).exists():
                slug_candidate = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug_candidate
        super().save(*args, **kwargs)



class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)  # 👈 Add this line
    # image = models.ImageField(upload_to='products/')
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    model = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    capacity = models.CharField(max_length=50)
    warranty = models.CharField(max_length=100)
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    price_with_old_battery = models.DecimalField(max_digits=10, decimal_places=2)
    price_without_old_battery = models.DecimalField(max_digits=10, decimal_places=2)
    coupon_code = models.CharField(max_length=100, blank=True)
    note = models.TextField(blank=True)
    description = models.TextField()
    recommended_for = models.ManyToManyField(CarModel)
    is_best_seller = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.name} on {self.product.name}"
