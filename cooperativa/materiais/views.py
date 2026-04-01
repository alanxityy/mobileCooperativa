from django.db.models import Q, Sum  # ✅ adicionar Sum
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_GET
from rest_framework import permissions
from accounts.models import Profile
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from .models import Material
from .forms import MaterialForm


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
            
            print(f"DEBUG: Usuário {user.username} tem cargo: {cargo_usuario}")
            
            return cargo_usuario in ['admin', 'gestor']
            
        except Profile.DoesNotExist:
            print(f"DEBUG: Usuário {user.username} não possui um Profile cadastrado!")
            return False

    def handle_no_permission(self):
        messages.error(self.request, "Acesso negado: Apenas administradores ou gestores podem realizar esta ação.")
        return redirect('materiais:list')
    

class MaterialListView(LoginRequiredMixin, ListView):
    model = Material
    template_name = "materiais/materiais_list.html"
    context_object_name = "materiais"
    paginate_by = 20
    ordering = ["nome"]

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q")
        ativo = self.request.GET.get("ativo")  # "1" / "0"
        if q:
            qs = qs.filter(nome__icontains=q)
        if ativo in {"0", "1"}:
            qs = qs.filter(ativo=(ativo == "1"))

        # ✅ Anotar totais por material considerando ENTRADA de ARRECADAÇÃO
        qs = qs.annotate(
            total_kg=Sum(
                "lancamentos__quantidade_kg",
                filter=Q(lancamentos__tipo="E", lancamentos__categoria="arrecadacao"),
                default=0,
            ),
            total_rs=Sum(
                "lancamentos__valor",
                filter=Q(lancamentos__tipo="E", lancamentos__categoria="arrecadacao"),
                default=0,
            ),
        )
        return qs


class MaterialCreateView(CargoRequiredMixin, CreateView):
    model = Material
    form_class = MaterialForm
    template_name = "materiais/materiais_form.html"
    success_url = reverse_lazy("materiais:list")


class MaterialUpdateView(CargoRequiredMixin, UpdateView):
    model = Material
    form_class = MaterialForm
    template_name = "materiais/materiais_form.html"
    success_url = reverse_lazy("materiais:list")

    # ✅ Mostrar totais e últimos lançamentos no formulário (edição)
    def get_context_data(self, **kwargs):
        from caixa.models import LancamentoCaixa  # import local para evitar ciclos
        ctx = super().get_context_data(**kwargs)
        base = LancamentoCaixa.objects.filter(
            material=self.object, tipo="E", categoria="arrecadacao"
        )
        aggs = base.aggregate(
            total_kg=Sum("quantidade_kg", default=0),
            total_rs=Sum("valor", default=0),
        )
        ctx.update(aggs)
        ctx["ultimos"] = base.order_by("-data", "-criado_em")[:10]
        return ctx


class MaterialDeleteView(CargoRequiredMixin, DeleteView):
    model = Material
    template_name = "materiais/materiais_confirm_delete.html"
    success_url = reverse_lazy("materiais:list")


class MaterialDetailView(LoginRequiredMixin, DetailView):
    model = Material
    template_name = "materiais/materiais_detail.html"
    context_object_name = "obj"

    # ✅ Detalhe também mostra totais e últimos lançamentos
    def get_context_data(self, **kwargs):
        from caixa.models import LancamentoCaixa
        ctx = super().get_context_data(**kwargs)
        base = LancamentoCaixa.objects.filter(
            material=self.object, tipo="E", categoria="arrecadacao"
        )
        aggs = base.aggregate(
            total_kg=Sum("quantidade_kg", default=0),
            total_rs=Sum("valor", default=0),
        )
        ctx.update(aggs)
        ctx["ultimos"] = base.order_by("-data", "-criado_em")[:10]
        return ctx


@require_GET
@login_required
def material_preco(request, pk: int):
    try:
        m = Material.objects.get(pk=pk)
    except Material.DoesNotExist:
        raise Http404("Material não encontrado")
    # str() evita problemas de serialização Decimal
    return JsonResponse({"preco_kg": str(m.preco_kg), "ativo": m.ativo})