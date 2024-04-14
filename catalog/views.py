from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView
from django.shortcuts import render
from .models import Products
from .forms import ProductForm
from django.urls import reverse_lazy


class HomeListView(ListView):
    model = Products
    template_name = 'catalog/home.html'
    context_object_name = 'products'


class ContactListView(TemplateView):
    template_name = 'catalog/contact.html'

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Пользователь с именем: {name}\nДля связи оставил телефон: {phone}\nОставил сообщение: {message}')
        return render(request, self.template_name)


class ProductDetailView(DetailView):
    model = Products
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'pk'


class ProductCreateView(CreateView):
    model = Products
    form_class = ProductForm
    template_name = 'catalog/product_create.html'
    success_url = '/'


class ProductUpdateView(UpdateView):
    model = Products
    form_class = ProductForm
    template_name = 'catalog/product_update.html'
    success_url = '/'
