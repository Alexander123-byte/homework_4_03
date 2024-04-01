from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from blog.models import Blog


class BlogCreateView(CreateView):
    model = Blog
    fields = ['title', 'slug', 'content', 'preview', 'is_published']
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        if form.is_valid():
            new_dealer = form.save(commit=False)
            new_dealer.slug = slugify(new_dealer.title)
            new_dealer.save()
        return super().form_valid(form)

    slug_url_kwarg = 'the slug'
    slug_field = 'slug'


class BlogListView(ListView):
    model = Blog

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save()
        return self.object

    slug_url_kwarg = 'the slug'
    slug_field = 'slug'


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ['title', 'content', 'preview', 'is_published']

    def form_valid(self, form):
        if form.is_valid():
            new_dealer = form.save()
            new_dealer.slug = slugify(new_dealer.title)
            new_dealer.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:view', kwargs={'pk': self.object.pk})


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:list')  # Перенаправление на список блогов

    def delete(self, request, *args, **kwargs):
        # Переопределяем метод delete
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()  # Удаляем объект, если пользователь нажал "удалить"
        return HttpResponseRedirect(success_url)  # Перенаправляем на указанный URL
