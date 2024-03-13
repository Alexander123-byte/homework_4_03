from django.core.management import BaseCommand
from catalog.models import Products, Category
from django.db import connection


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Удалите все продукты
        # Удалите все категории
        Category.objects.all().delete()
        Products.objects.all().delete()

        # Сбросить счетчики id категорий и продуктов
        with connection.cursor() as cursor:
            cursor.execute("ALTER SEQUENCE catalog_category_id_seq RESTART WITH 1;")
            cursor.execute("ALTER SEQUENCE catalog_products_id_seq RESTART WITH 1;")

        # Создайте списки для хранения объектов
        product_for_create = []
        category_for_create = []

        category_list = [
            {'name_category': 'Фрукты'},
            {'name_category': 'Овощи'},
            {'name_category': 'Техника'}]

        product_list = [
            {"name_product": "Яблоко",
             "category": 1,
             "price": 79,
             },
            {"name_product": "Картофель",
             "category": 2,
             "price": 59,
             },
            {"name_product": "Мандарин",
             "category": 1,
             "price": 119,
             },
            {"name_product": "Робот-пылесос",
             "category": 3,
             "price": 21999,
             }]

        # Обходим все значения категорий из списка для получения информации об одном объекте
        for category_item in category_list:
            category_for_create.append(
                Category(**category_item))
        # Создаем объекты в базе с помощью метода bulk_create()
        Category.objects.bulk_create(category_for_create)

        # Обходим все значения продуктов из списка для получения информации об одном объекте
        for product_item in product_list:
            pk = product_item["category"]
            category = Category.objects.filter(pk=pk).first()
            if category:
                price1 = product_item["price"]
                name1 = product_item["name_product"]
                product_for_create.append(
                    Products(name_product=name1,
                            price=price1,
                            category=category))
        # Создаем объекты в базе с помощью метода bulk_create()
        Products.objects.bulk_create(product_for_create)
