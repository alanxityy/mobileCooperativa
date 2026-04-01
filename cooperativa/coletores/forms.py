from django import forms
from .models import Coletor

class ColetorForm(forms.ModelForm):
    class Meta:
        model = Coletor
        fields = [
            "nome", "tipo_documento", "documento", "faz_parte_cooperativa",
            "email", "telefone", "endereco",
            "foto",
            "banco", "agencia", "numero_conta", "tipo_conta",
        ]
        widgets = {
            "endereco": forms.Textarea(attrs={"rows": 3}),
        }
