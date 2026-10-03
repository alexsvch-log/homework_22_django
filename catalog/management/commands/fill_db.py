from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Очищает базу данных и загружает тестовые данные из фикстур"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Шаг 1: Начинаю очистку базы данных..."))

        # Сначала удаляем продукты, затем категории (порядок важен из-за связанных ключей ForeignKey)
        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("База данных полностью очищена."))
        self.stdout.write(self.style.WARNING("Шаг 2: Загружаю данные из фикстур..."))

        try:
            # Вызываем встроенный инструмент Django для работы с фикстурами внутри нашего скрипта
            call_command("loaddata", "categories_data.json", "products_data.json")
            self.stdout.write(self.style.SUCCESS("Тестовые данные успешно загружены из файлов в базу!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка при автоматической загрузке: {e}"))
