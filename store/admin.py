from django.contrib import admin
from .models import Product, Category, OrderProduct, Order

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'stock', 'created_at')
    search_fields = ('title', 'category__name')
    list_filter = ('category', 'created_at', 'stock')

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'phone', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user_name', 'phone']
    inlines = [OrderProductInline]
    ordering = ['-created_at']

admin.site.register(Order, OrderAdmin)