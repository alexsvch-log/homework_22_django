from django.db import models  # noqa: F401

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name="Наименование")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    # Поле для изображения. Загружаемые файлы будут падать в папку media/products/
    image = models.ImageField(upload_to="products/", blank=True, null=True, verbose_name="Изображение")
    # Связь с моделью категорий
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", verbose_name="Категория")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за покупку")
    # Записывает дату автоматически только при создании записи
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    # Обновляет дату автоматически при каждом сохранении/изменении записи
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего изменения")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class ContactInfo(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название организации / ФИО")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")
    address = models.TextField(verbose_name="Адрес", blank=True, null=True)

    class Meta:
        verbose_name = "Контактные данные"
        verbose_name_plural = "Контактные данные"

    def __str__(self):
        return self.name
