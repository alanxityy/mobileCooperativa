from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import Profile

@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        # garante que existe e salva
        if not hasattr(instance, "profile"):
            Profile.objects.create(user=instance)
        else:
            instance.profile.save()

# Opcional: vincular grupo ao cargo automaticamente
@receiver(post_save, sender=Profile)
def sync_groups_with_role(sender, instance, **kwargs):
    role_to_group = {
        "admin": "Administrador",
        "gestor": "Gestor",
        "operacional": "Operador",
    }
    group_name = role_to_group.get(instance.cargo)
    if not group_name:
        return
    # remove grupos do “conjunto”
    user = instance.user
    user.groups.remove(*Group.objects.filter(name__in=role_to_group.values()))
    # adiciona o grupo do cargo (crie os grupos antes, veja Seção 2)
    g, _ = Group.objects.get_or_create(name=group_name)
    user.groups.add(g)
