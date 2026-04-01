from django.contrib import admin
from .models import Material

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("nome", "preco_kg", "ativo")
    list_filter = ("ativo",)
    search_fields = ("nome",)
