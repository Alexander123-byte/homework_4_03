from django import forms
from django.forms import BooleanField

from .models import Products, Version


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs['class'] = 'form-check-input'
            else:
                fild.widget.attrs['class'] = 'form-control'


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = ['version_number', 'version_name', 'is_current']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_current'].widget.attrs.update({'class': 'form-check-input'})


class ProductForm(forms.ModelForm):
    version_number = forms.CharField(max_length=50, label='Номер версии')
    version_name = forms.CharField(max_length=100, label='Название версии')

    class Meta:
        model = Products
        fields = ['name_product', 'description_product', 'image', 'category', 'price',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name_product'].required = True
        self.fields['description_product'].required = True
        self.fields['image'].required = True
        self.fields['category'].required = True
        self.fields['price'].required = True

    def save(self, commit=True):
        product = super().save(commit=False)
        if commit:
            product.save()
            # Создаем новую версию и связываем ее с этим продуктом
            Version.objects.create(
                product=product,
                version_number=self.cleaned_data['version_number'],
                version_name=self.cleaned_data['version_name'],
                is_current=True
            )
        return product

    def clean_name_product(self):
        name_product = self.cleaned_data.get('name_product')
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']
        for word in forbidden_words:
            if word.lower() in name_product.lower():
                raise forms.ValidationError(f"Слово '{word}' не допускается в названии.")
        return name_product

    def clean_description_product(self):
        description_product = self.cleaned_data.get('description_product')
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']
        for word in forbidden_words:
            if word.lower() in description_product.lower():
                raise forms.ValidationError(f"Слово '{word}' не допускается в описании.")
        return description_product
