from django.urls import path
from catalog.views import HomeListView, ContactListView, ProductDetailView

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('contacts/', ContactListView.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]
