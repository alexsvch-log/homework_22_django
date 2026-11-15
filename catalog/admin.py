from django.contrib import admin  # noqa: F401

from .models import Category, Product
from .models import ContactInfo  # Дописываем импорт новой модели к остальным

# Register your models here.

# Регистрация Category с выводом id и name
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


# Регистрация Product с выводом id, name, price, category
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "category", 'is_published')

    # Настройка фильтрации продуктов по категории и публикации
    list_filter = ("category", 'is_published')

    # Настройка поиска по полям name и description
    search_fields = ("name", "description")

    # Позволит ставить и снимать галочки прямо в таблице, не заходя в товар
    list_editable = ('is_published',)


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "email")
