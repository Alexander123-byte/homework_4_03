from django import forms
from .models import Products


class ProductForm(forms.ModelForm):
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
