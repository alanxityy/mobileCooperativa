from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from .models import Profile

class MyAdminSite(admin.AdminSite):
    def has_permission(self, request):
        user = request.user
        
        if not user.is_authenticated:
            return False
            
        if user.is_superuser:
            return True
            
        try:
            cargo_usuario = user.profile.cargo
            if cargo_usuario in ['admin', 'gestor']:
                return True
        except Profile.DoesNotExist:
            pass

        is_allowed = user.is_staff or user.groups.filter(name='admin').exists() or user.groups.filter(name='gestor').exists()
        
        return is_allowed

admin.site = MyAdminSite()


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    fk_name = "user"
    extra = 0
    fields = ("foto", "cargo", "preview")
    readonly_fields = ("preview",)

    def preview(self, obj):
        if obj and obj.foto:
            return mark_safe(f'<img src="{obj.foto.url}" style="width:96px;height:96px;border-radius:50%;object-fit:cover;">')
        return "—"
    preview.short_description = "Pré-visualização"

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = UserAdmin.list_display + ("get_cargo", "get_foto")

    def get_cargo(self, obj):
        return getattr(getattr(obj, "profile", None), "cargo", "—")
    get_cargo.short_description = "Cargo"

    def get_foto(self, obj):
        p = getattr(obj, "profile", None)
        if p and p.foto:
            return mark_safe(f'<img src="{p.foto.url}" style="width:32px;height:32px;border-radius:50%;object-fit:cover;">')
        return "—"
    get_foto.short_description = "Foto"

admin.site.register(User, CustomUserAdmin)

@admin.register(Profile, site=admin.site) 
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "cargo")