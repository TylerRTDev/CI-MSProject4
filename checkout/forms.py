from django import forms
from .models import CheckoutOrder

class OrderForm(forms.ModelForm):
    class Meta:
        model = CheckoutOrder
        fields = ['user', 'total_amount'] 
        widgets = {
            'user': forms.HiddenInput(),
            'total_amount': forms.HiddenInput(),
        }
