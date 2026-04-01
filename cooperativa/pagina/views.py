from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from materiais.models import Material
from coletores.models import Coletor
from caixa.models import LancamentoCaixa
from accounts.models import Profile, CalendarioNota

from .serializers import (
    MaterialSerializer, ColetorSerializer, 
    LancamentoCaixaSerializer, ProfileSerializer, 
    CalendarioNotaSerializer
)

class MaterialViewSet(viewsets.ModelViewSet):
    serializer_class = MaterialSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Material.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ColetorViewSet(viewsets.ModelViewSet):
    serializer_class = ColetorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Coletor.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LancamentoCaixaViewSet(viewsets.ModelViewSet):
    serializer_class = LancamentoCaixaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return LancamentoCaixa.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

class CalendarioNotaViewSet(viewsets.ModelViewSet):
    serializer_class = CalendarioNotaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CalendarioNota.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        data_br = request.data.get('data_br')
        texto = str(request.data.get('texto', '')).strip()

        if not data_br:
            return Response({"error": "Data não informada"}, status=status.HTTP_400_BAD_REQUEST)

        if not texto:
            CalendarioNota.objects.filter(user=request.user, data_br=data_br).delete()
            return Response({"status": "removido"}, status=status.HTTP_204_NO_CONTENT)

        nota, created = CalendarioNota.objects.update_or_create(
            user=request.user, 
            data_br=data_br,
            defaults={'texto': texto}
        )
        
        serializer = self.get_serializer(nota)
        return Response(serializer.data, status=status.HTTP_201_CREATED)