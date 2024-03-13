from django.db import models


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

    def __str__(self):
        return f'{self.name_product}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ('name_product',)



