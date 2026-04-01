from django.contrib import admin
from .models import Coletor

@admin.register(Coletor)
class ColetorAdmin(admin.ModelAdmin):
    list_display = ("nome", "documento", "faz_parte_cooperativa", "email", "telefone")
    list_filter = ("faz_parte_cooperativa",)
    search_fields = ("nome", "documento", "email", "telefone")
