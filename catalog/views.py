from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView
from django.shortcuts import render
from .models import Products, Version
from .forms import ProductForm, VersionForm, ProductModeratorForm


def is_moderator(user):
    return (user.has_perm('catalog.can_edit_category') and user.has_perm('catalog.can_edit_description') and
            user.has_perm('catalog.can_cancel_publication'))


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

        context['is_moderator'] = is_moderator(self.request.user)

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


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Products
    form_class = ProductForm
    template_name = 'catalog/product_create.html'
    success_url = '/'

    def form_valid(self, form):
        product = form.save(commit=False)
        product.owner = self.request.user
        product.is_published = form.cleaned_data.get('is_published', False)
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
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

    def get_form_class(self):
        user = self.request.user
        if (user.has_perm("catalog.can_edit_category") and user.has_perm("catalog.can_edit_description") and
                user.has_perm("catalog.can_cancel_publication")):
            return ProductModeratorForm
        if user == self.object.owner:
            return ProductForm
        raise PermissionDenied


class VersionCreateView(CreateView):
    model = Version
    form_class = VersionForm
    template_name = 'catalog/version_create.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.product_id = self.kwargs['pk']
        return super().form_valid(form)
