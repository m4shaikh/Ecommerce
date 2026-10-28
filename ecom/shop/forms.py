from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'slug', 'image', 
                 'description', 'price', 'stock', 'available']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Enter product description'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0'
            }),
            'available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'slug': 'A URL-friendly version of the name (letters, numbers, hyphens)'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all().order_by('name')

from django import forms
from django.utils.text import slugify
from .models import Product, Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category name',
                'id': 'id_category_name'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'category-slug',
                'id': 'id_category_slug'
            }),
        }
        help_texts = {
            'slug': 'A URL-friendly version of the name (letters, numbers, hyphens)'
        }

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        name = self.cleaned_data.get('name')
        if not slug and name:
            slug = slugify(name)
        return slug