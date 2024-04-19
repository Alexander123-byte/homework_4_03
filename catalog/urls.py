from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import (HomeListView, ContactListView, ProductDetailView, ProductCreateView, ProductUpdateView,
                           VersionCreateView)

app_name = CatalogConfig.name

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('contacts/', ContactListView.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/version/create/', VersionCreateView.as_view(), name='version_create'),
]
