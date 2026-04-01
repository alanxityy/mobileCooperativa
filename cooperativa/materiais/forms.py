from django import forms
from .models import Material

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ["nome", "preco_kg", "ativo"]
        widgets = {
            "nome": forms.TextInput(attrs={"placeholder": "Ex.: Papelão"}),
            "preco_kg": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
        }
