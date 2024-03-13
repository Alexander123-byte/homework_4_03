from django.contrib import admin

from catalog.models import Products, Category

# admin.site.register(Catalog)
# admin.site.register(Category)


@admin.register(Products)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_product', 'price', 'category',)
    list_filter = ('category',)
    search_fields = ('name_product', 'description_product',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_category',)
