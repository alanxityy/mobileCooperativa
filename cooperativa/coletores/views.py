from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Coletor
from accounts.models import Profile
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from .forms import ColetorForm

# operacional teste
class CargoRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        
        # verifica login
        if not user.is_authenticated:
            return False
        
        if user.is_superuser:
            return True
            
        try:
            cargo_usuario = user.profile.cargo
            return cargo_usuario in ['admin', 'gestor']
            
        except Profile.DoesNotExist:
            return False

    def handle_no_permission(self):
        messages.error(self.request, "Acesso negado: Apenas administradores ou gestores podem realizar esta ação.")
        return redirect('coletores:list')

class ColetorListView(LoginRequiredMixin, ListView):
    model = Coletor
    template_name = "coletores/coletores_list.html"
    context_object_name = "coletores"
    paginate_by = 20
    ordering = ["nome"]

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q")
        coop = self.request.GET.get("coop")  # "1" / "0"
        if q:
            qs = qs.filter(
                Q(nome__icontains=q) |
                Q(documento__icontains=q) |
                Q(email__icontains=q) |
                Q(telefone__icontains=q)
            )
        if coop in {"0", "1"}:
            qs = qs.filter(faz_parte_cooperativa=(coop == "1"))
        return qs

class ColetorCreateView(CargoRequiredMixin, CreateView):
    model = Coletor
    form_class = ColetorForm
    template_name = "coletores/coletores_form.html"
    success_url = reverse_lazy("coletores:list")

class ColetorUpdateView(CargoRequiredMixin, UpdateView):
    model = Coletor
    form_class = ColetorForm
    template_name = "coletores/coletores_form.html"
    success_url = reverse_lazy("coletores:list")

class ColetorDeleteView(CargoRequiredMixin, DeleteView):
    model = Coletor
    template_name = "coletores/coletores_confirm_delete.html"
    success_url = reverse_lazy("coletores:list")

class ColetorDetailView(CargoRequiredMixin, DetailView):
    model = Coletor
    template_name = "coletores/coletores_detail.html"
    context_object_name = "obj"
