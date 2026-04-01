from django.db import models
from django.core.validators import MinValueValidator

class Material(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    preco_kg = models.DecimalField(max_digits=9, decimal_places=2,
                                   validators=[MinValueValidator(0)])

    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materiais"
        ordering = ["nome"]

    def __str__(self):
        return self.nome
