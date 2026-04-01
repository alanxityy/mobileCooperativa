from django import forms
from .models import LancamentoCaixa
from django.contrib.auth.models import User
from coletores.models import Coletor

class LancamentoCaixaForm(forms.ModelForm):
    class Meta:
        model = LancamentoCaixa
        fields = ["tipo", "categoria", "material", "quantidade_kg",
                  "valor", "descricao", "coletor", "data"]
        widgets = {
            "quantidade_kg": forms.NumberInput(attrs={"step": "0.001", "min": "0"}),
            "valor": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "data": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        # usuario enviado pelo formulario
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user:
            is_admin = self.user.is_staff or self.user.groups.filter(name__in=['admin', 'gestor']).exists()
            if not is_admin:
                if 'coletor' in self.fields:
                    self.fields['coletor'].widget = forms.HiddenInput()
                    self.fields['coletor'].required = False

    def clean(self):
        cleaned = super().clean()
        instance = self.instance

        # Coletor Automático
        if self.user:
            is_admin = self.user.is_staff or self.user.groups.filter(name__in=['admin', 'gestor']).exists()
            
            if not is_admin:
                try:
                    # Condição do usuário logado existir como coletor
                    coletor_obj = Coletor.objects.get(nome__icontains=self.user.username)
                    cleaned['coletor'] = coletor_obj
                    instance.coletor = coletor_obj
                except Coletor.DoesNotExist:
                    raise forms.ValidationError(f"Não existe um Coletor cadastrado com o nome {self.user.username}.")

        # Cálculo Automático do Valor
        instance.tipo = cleaned.get("tipo")
        instance.categoria = cleaned.get("categoria")
        instance.material = cleaned.get("material")
        instance.quantidade_kg = cleaned.get("quantidade_kg")
        instance.valor = cleaned.get("valor")
        
        # calcular Preço * Qtd
        instance.clean() 
        cleaned["valor"] = instance.valor
        
        return cleaned