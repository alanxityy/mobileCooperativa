from django.contrib import admin
from .models import LancamentoCaixa

@admin.register(LancamentoCaixa)
class LancamentoCaixaAdmin(admin.ModelAdmin):
    list_display = ("data", "tipo", "categoria", "valor", "coletor", "material", "descricao")
    list_filter = ("tipo", "categoria", "data")
    search_fields = ("descricao",)
    autocomplete_fields = ("coletor", "material")
    date_hierarchy = "data"
