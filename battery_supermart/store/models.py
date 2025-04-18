from django.db import models

# Create your models here

CATEGORY_CHOICES = [
    ('Car', 'Car'),
    ('Bike', 'Bike'),
    ('Inverter', 'Inverter'),
]

class Product(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='products/')
    model = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    capacity = models.CharField(max_length=50)
    warranty = models.CharField(max_length=100)
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    with_old_price = models.DecimalField(max_digits=10, decimal_places=2)
    without_old_price = models.DecimalField(max_digits=10, decimal_places=2)
    coupon_code = models.CharField(max_length=100, blank=True)
    note = models.TextField(blank=True)
    description = models.TextField()
    recommended_for = models.TextField(blank=True)
    is_best_seller = models.BooleanField(default=False)

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

