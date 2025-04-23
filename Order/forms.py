from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        customclass = "w-full h-full border-2 rounded-sm border-slate-300 focus:outline-none focus:border-slate-700 px-2 text-sm"
        model = Order
        fields = ["client", "contract", "device", "status", "engineer"]
        widgets = {
            "client": forms.Select(attrs={"class": customclass}),
            "contract": forms.Select(attrs={"class": customclass}),
            "device": forms.SelectMultiple(attrs={"class": customclass}),
            "status": forms.Select(attrs={"class": customclass}),
            "engineer": forms.Select(attrs={"class": customclass}),
        }