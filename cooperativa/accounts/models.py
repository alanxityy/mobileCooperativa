from django.db import models
from django.contrib.auth.models import User

class CalendarioNota(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data_br = models.CharField(max_length=10)
    texto = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em'] 

    def __str__(self):
        return f"{self.user.username} - {self.data_iso}: {self.texto[:20]}",

class Profile(models.Model):
    CARGOS = [
        ("admin", "Administrador"),
        ("gestor", "Gestor"),
        ("operacional", "Operacional"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    foto = models.ImageField(upload_to="profiles/", blank=True, null=True)
    cargo = models.CharField(max_length=20, choices=CARGOS, default="operacional")

    def __str__(self):
        return f"Perfil de {self.user.username}"
