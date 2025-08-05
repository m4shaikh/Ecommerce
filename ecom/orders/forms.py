from django import forms
from django.core.validators import RegexValidator
from .models import Order

class OrderCreateForm(forms.ModelForm):
    email_confirmation = forms.EmailField(label="Confirm Email")

    class Meta:
        model = Order
        fields = ['full_name', 'email', 'email_confirmation', 'address', 'city', 'phone']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email'
            }),
            'address': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Street address, apartment number'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your city'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+1 234 567 890'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add widget attributes for the non-model field
        self.fields['email_confirmation'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm your email'
        })

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        email_confirmation = cleaned_data.get('email_confirmation')

        if email != email_confirmation:
            self.add_error('email_confirmation', "Emails do not match.")

        return cleaned_data
