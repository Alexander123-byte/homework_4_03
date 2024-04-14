from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView
from django.shortcuts import render
from .models import Products, Version
from .forms import ProductForm


class HomeListView(ListView):
    model = Products
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = context['products']

        for product in products:
            active_version = Version.objects.filter(product=product, is_current=True).first()
            product.current_version = active_version

        return context


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.object
        return context

    def get_initial(self):
        initial = super().get_initial()
        current_version = Version.objects.filter(product=self.object, is_current=True).first()
        if current_version:
            initial['version_number'] = current_version.version_number
            initial['version_name'] = current_version.version_name
        return initial
