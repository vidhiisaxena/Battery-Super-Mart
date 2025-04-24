from django.contrib import admin
from .models import Product, Review, CarModel, CarBrand

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ('name', 'email', 'content', 'created_at')

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'brand', 'category', 'mrp', 'price_with_old_battery', 'price_without_old_battery']
    search_fields = ['name', 'brand', 'model']
    list_filter = ['category', 'brand', 'is_best_seller']
    inlines = [ReviewInline]
    filter_horizontal = ('recommended_for',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Review)
admin.site.register(CarModel)
admin.site.register(CarBrand)
