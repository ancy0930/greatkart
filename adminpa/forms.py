from django import forms
from store.models import Product
from category.models import Category
from django.forms import TextInput


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "product_name",

            "description",
            "price",
            "images",
            "stock",
            "is_available",
            "category",
        ]
        widgets = {
            "product_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Product Name",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Product Description",
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Price",
                    "step": "0.01",  # Define step for decimal places
                }
            ),
            "images": forms.FileInput(
                attrs={
                    "class": "form-control-file",
                }
            ),
            "stock": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Stock",
                    "min": "0",  # Ensure stock is non-negative
                }
            ),
            "is_available": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
        }
    def _init_(self, *args, **kwargs):
        super(ProductForm, self)._init_(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            "category_name",
            
            "description",
            "cat_image"
        ]
        widgets = {
        'category_name': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Category Name',
        }),
        'description': forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Description',
        }),
        'cat_image': forms.ClearableFileInput(attrs={
            'class': 'form-control-file',
        }),
    }


    def _init_(self, *args, **kwargs):
        super(CategoryForm, self)._init_(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"
