from django.core.cache import cache

from config.settings import CACHE_ENABLED
from catalog.models import Category, Products


def get_category_from_cache():
    if not CACHE_ENABLED:
        return Category.objects.all()
    key = "category_list"
    categories = cache.get(key)
    if categories is not None:
        return categories
    categories = Category.objects.all()
    cache.set(key, categories)
    return categories


def get_products_from_cache():
    if not CACHE_ENABLED:
        return Products.objects.all()
    key = "products_list"
    products = cache.get(key)
    if products is not None:
        return products
    products = Products.objects.all()
    cache.set(key, products)
    return products
