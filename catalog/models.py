from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    name_category = models.CharField(max_length=100, verbose_name='Наименование')
    description_category = models.TextField(max_length=200, verbose_name='Описание', blank=True, null=True)

    def __str__(self):
        return f'{self.name_category}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('name_category',)


class Products(models.Model):
    name_product = models.CharField(max_length=100, verbose_name='Наименование')
    description_product = models.TextField(max_length=200, verbose_name='Описание', **NULLABLE)
    image = models.ImageField(upload_to='img_catalogs/', verbose_name='Изображение(превью)', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.IntegerField(verbose_name='Цена за покупку')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

    owner = models.ForeignKey(User, verbose_name='Владелец', help_text='Укажите владельца продукта',
                              **NULLABLE, on_delete=models.SET_NULL)

    is_published = models.BooleanField(default=False, verbose_name='Опубликовать')

    def __str__(self):
        return f'{self.name_product}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ['category', 'name_product']
        permissions = [
            ("can_cancel_publication", "Can cancel publication"),
            ("can_edit_category", "Can edit category"),
            ("can_edit_description", "Can edit description")
        ]


class Version(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='продукт')
    version_number = models.CharField(verbose_name='номер версии', max_length=50)
    version_name = models.CharField(verbose_name='название версии', max_length=100)
    is_current = models.BooleanField(verbose_name='признак текущей версии', default=False)

    def __str__(self):
        return f"{self.product.name_product} - {self.version_name}"
