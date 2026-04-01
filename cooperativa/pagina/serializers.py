from rest_framework import serializers
from materiais.models import Material
from coletores.models import Coletor
from caixa.models import LancamentoCaixa
from accounts.models import Profile, CalendarioNota

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'
        read_only_fields = ['user']

class ColetorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coletor
        fields = '__all__'
        read_only_fields = ['user']

class LancamentoCaixaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LancamentoCaixa
        fields = '__all__'
        read_only_fields = ['user']

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ['user']

class CalendarioNotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarioNota
        fields = '__all__'
        read_only_fields = ['user']
        extra_kwargs = {
            'texto': {'allow_blank': True, 'required': False}
        }