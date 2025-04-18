from django.contrib import admin
from .models import Product, Review

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ('name', 'email', 'content', 'created_at')

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'category', 'mrp', 'with_old_price', 'without_old_price']
    search_fields = ['name', 'brand', 'model']
    list_filter = ['category', 'brand', 'is_best_seller']
    inlines = [ReviewInline]

admin.site.register(Product, ProductAdmin)
admin.site.register(Review)

