from django import forms
from Shop.models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating','title','review']
        widgets = {
            'rating':forms.Select(attrs={
                'class':'form-control'
        }),
            'review':forms.Textarea(attrs={
                'form':'form-control',
                'rows':4
        }),
        }