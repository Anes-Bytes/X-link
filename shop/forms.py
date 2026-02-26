from django import forms

from .models import Product, UserShop


class UserShopForm(forms.ModelForm):
    class Meta:
        model = UserShop
        fields = ["name", "logo", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "نام سایت فروشگاهی"}),
            "logo": forms.FileInput(attrs={"class": "form-control", "accept": "image/*"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "image",
            "short_description",
            "price",
            "discount_percent",
            "buy_link",
            "is_active",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "نام محصول"}),
            "image": forms.FileInput(attrs={"class": "form-control", "accept": "image/*"}),
            "short_description": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "توضیح کوتاه محصول"}
            ),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
            "discount_percent": forms.NumberInput(
                attrs={"class": "form-control", "min": "0", "max": "100", "step": "1"}
            ),
            "buy_link": forms.URLInput(attrs={"class": "form-control", "placeholder": "https://..."}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
