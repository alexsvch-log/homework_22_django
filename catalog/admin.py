from django.contrib import admin   # noqa: F401
from .models import Category, Product

# Register your models here.

# Регистрация Category с выводом id и name
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


# Регистрация Product с выводом id, name, price, category
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')

    # Настройка фильтрации продуктов по категории
    list_filter = ('category',)

    # Настройка поиска по полям name и description
    search_fields = ('name', 'description')
