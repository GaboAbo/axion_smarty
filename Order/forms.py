"""
Forms for the Order app.

Includes ModelForm definitions for creating and updating Order instances.
"""

from django import forms
from .models import Order

# Custom Tailwind CSS class used across all form fields
CUSTOM_CLASS = (
    "w-full h-full border-2 rounded-sm border-slate-300 "
    "focus:outline-none focus:border-slate-700 px-2 text-sm"
)


class OrderForm(forms.ModelForm):
    """
    Form for creating and updating Order instances.
    Applies consistent styling to each field using Tailwind CSS classes.
    """

    class Meta:
        model = Order
        fields = ["client", "contract", "device", "status", "engineer"]
        widgets = {
            "client": forms.Select(attrs={"class": CUSTOM_CLASS}),
            "contract": forms.Select(attrs={"class": CUSTOM_CLASS}),
            "device": forms.SelectMultiple(attrs={"class": CUSTOM_CLASS}),
            "status": forms.Select(attrs={"class": CUSTOM_CLASS}),
            "engineer": forms.Select(attrs={"class": CUSTOM_CLASS}),
        }
