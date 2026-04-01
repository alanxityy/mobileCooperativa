from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

class LancamentoCaixa(models.Model):
    TIPO = [("E", "Entrada"), ("S", "Saída")]

    tipo = models.CharField(max_length=1, choices=TIPO)
    categoria = models.CharField(
        max_length=30,
        choices=[
            ("arrecadacao", "Arrecadação"),
            ("repasse", "Repasse"),
            ("despesa", "Despesa"),
            ("ajuste", "Ajuste"),
        ],
        default="arrecadacao",
    )

    # peso referente ao material deste lançamento (quando houver)
    quantidade_kg = models.DecimalField(
        max_digits=12, decimal_places=3,
        null=True, blank=True,
        validators=[MinValueValidator(0)]
    )

    valor = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    descricao = models.CharField(max_length=255, blank=True)

    coletor = models.ForeignKey("coletores.Coletor", on_delete=models.SET_NULL,
                                null=True, blank=True, related_name="lancamentos")
    material = models.ForeignKey("materiais.Material", on_delete=models.SET_NULL,
                                 null=True, blank=True, related_name="lancamentos")

    data = models.DateField(default=timezone.localdate, db_index=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Lançamento de Caixa"
        verbose_name_plural = "Lançamentos de Caixa"
        ordering = ["-data", "-criado_em"]
        indexes = [
            models.Index(fields=["data"]),
            models.Index(fields=["categoria", "data"]),
            models.Index(fields=["material", "data"]),  # útil para somatórios p/ material
        ]

    def clean(self):
        if (
            self.tipo == "E" and
            self.categoria == "arrecadacao" and
            self.material_id and
            self.quantidade_kg is not None
        ):
            preco = self.material.preco_kg or Decimal("0")
            self.valor = (preco * self.quantidade_kg).quantize(Decimal("0.01"))

    def __str__(self):
        sinal = "+" if self.tipo == "E" else "-"
        return f"{sinal} R${self.valor} [{self.categoria}] {self.descricao or ''}".strip()
