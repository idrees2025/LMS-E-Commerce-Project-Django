from django import forms
from Cart.models import ShippingAddress

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['first_name','last_name','company_name'
                  ,'area_code','phone_number','street_address',
                  'zip_code','is_buisness']