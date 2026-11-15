from django.core.cache import cache
from .models import Product


def get_products_by_category(category_id):
    # Формируем уникальный ключ кэша для конкретной категории
    cache_key = f'category_{category_id}'

    # Пытаемся достать список товаров из Redis
    products = cache.get(cache_key)

    if products is None:
        # Если в кэше пусто — делаем запрос в базу данных
        products = list(Product.objects.filter(category_id=category_id, is_published=True))
        # Сохраняем результат в Redis на 15 минут (900 секунд)
        cache.set(cache_key, products, 900)

    return products

def get_products_from_cache():
    cache_key = 'products_list'
    products = cache.get(cache_key)

    if products is None:
        # Если в Redis пусто — достаем товары из базы данных и превращаем в список
        products = list(Product.objects.all())
        # Сохраняем в кэш на 15 минут (900 секунд)
        cache.set(cache_key, products, 900)

    return products