from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'cost_price', 'quantity', 'description']

# Sotish uchun forma
from django import forms

class SellForm(forms.Form):
    sold_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label="Sotish narxi",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
