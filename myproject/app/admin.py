from django.contrib import admin
from .models import Product, Cart, CartItem, Category

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # Показывать дополнительные поля, если нужно
    prepopulated_fields = {'slug': ('name',)}
