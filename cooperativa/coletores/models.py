from django.db import models

class Coletor(models.Model):
    # Opções de Documento
    TIPO_DOC = [("CPF", "CPF"), ("RG", "RG"), ("CNH", "CNH")]
    
    # Opções de Conta
    TIPO_CONTA = [("corrente", "Conta Corrente"), ("poupanca", "Poupança")]

    nome = models.CharField(max_length=120)
    tipo_documento = models.CharField(max_length=10, choices=TIPO_DOC, default="CPF")
    documento = models.CharField(max_length=20, unique=True)
    faz_parte_cooperativa = models.BooleanField(default=False)

    email = models.EmailField(blank=True, null=True, verbose_name="E-mail")
    telefone = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.TextField(blank=True, null=True)
    foto = models.ImageField(upload_to="fotos_coletores/", blank=True, null=True)

    banco = models.CharField(max_length=50, blank=True, null=True)
    agencia = models.CharField(max_length=10, blank=True, null=True)
    numero_conta = models.CharField(max_length=20, blank=True, null=True)
    tipo_conta = models.CharField(max_length=10, choices=TIPO_CONTA, blank=True, null=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    @property
    def documento_mascarado(self):
        if not self.documento:
            return ""

        doc = self.documento

        # Lógica específica para CPF
        if self.tipo_documento == "CPF":
            # Formato esperado: 123.456.789-00
            if len(doc) == 14:
                return f"{doc[:3]}.XXX.XXX-{doc[-2:]}"
            # Formato esperado (apenas números): 12345678900
            elif len(doc) == 11:
                return f"{doc[:3]}.XXX.XXX-{doc[-2:]}"

        if len(doc) > 4:
            return f"***{doc[-4:]}"
        
        return doc

    class Meta:
        verbose_name = "Coletor"
        verbose_name_plural = "Coletores"
        ordering = ["nome"]

    def __str__(self):
        return f"{self.nome} ({self.documento_mascarado})"