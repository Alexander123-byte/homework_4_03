from django.shortcuts import render
from .models import Products


def home(request):
    products = Products.objects.all()
    return render(request, 'catalog/home.html', {'products': products})


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Пользователь с именем: {name}\nДля связи оставил телефон: {phone}\nОставил сообщение: {message}')
    return render(request, 'catalog/contact.html')


def product_detail(request, pk):
    # Получаем объект товара по его PrimaryKey (id)
    product = Products.objects.get(pk=pk)
    # Формируем контекст для передачи в шаблон
    context = {'product': product}
    # Отображаем страницу с информацией о товаре
    return render(request, 'catalog/product_detail.html', context)
