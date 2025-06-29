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
        
class GuestEmailForm(forms.Form):
    email = forms.EmailField(label="Your email", max_length=254)
    full_name = forms.CharField(max_length=100)

    shipping_address = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}))
    shipping_city = forms.CharField(max_length=50)
    shipping_postcode = forms.CharField(max_length=20)

    same_as_shipping = forms.BooleanField(
        required=False,
        initial=False,
        label="Billing address same as shipping"
    )

    billing_address = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), required=False)
    billing_city = forms.CharField(max_length=50, required=False)
    billing_postcode = forms.CharField(max_length=20, required=False)

    def clean(self):
        cleaned_data = super().clean()
        same = cleaned_data.get('same_as_shipping')

        if not same:
            if not all([
                cleaned_data.get('billing_address'),
                cleaned_data.get('billing_city'),
                cleaned_data.get('billing_postcode')
            ]):
                raise forms.ValidationError("Please complete all billing fields or check the box to copy shipping address.")
        return cleaned_data
    
from django import forms

class GuestCheckoutForm(forms.Form):
    email = forms.EmailField(label="Email")
    full_name = forms.CharField(max_length=100)

    shipping_address = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}))
    shipping_city = forms.CharField(max_length=50)
    shipping_postcode = forms.CharField(max_length=20)

    same_as_shipping = forms.BooleanField(
        required=False,
        initial=False,
        label="Billing address same as shipping"
    )

    billing_address = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), required=False)
    billing_city = forms.CharField(max_length=50, required=False)
    billing_postcode = forms.CharField(max_length=20, required=False)

    def clean(self):
        cleaned_data = super().clean()
        same = cleaned_data.get('same_as_shipping')

        if not same:
            if not all([
                cleaned_data.get('billing_address'),
                cleaned_data.get('billing_city'),
                cleaned_data.get('billing_postcode')
            ]):
                raise forms.ValidationError("Please complete all billing fields or check the box to copy shipping address.")
        return cleaned_data
    
