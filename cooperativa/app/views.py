# app/views.py
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt

@login_required
def dashboard(request):
    return render(request, "dashboard.html")

@require_GET
def logout_get(request):
    """
    Logout via GET para funcionar no link do menu.
    Redireciona SEMPRE para a tela de login.
    """
    logout(request)
    return redirect("login")  # ou: return redirect(settings.LOGIN_URL)

@csrf_exempt
def admin_logout_view(request):
    """
    Logout chamado a partir do Admin/Jazzmin (GET/POST).
    Redireciona para a tela de login do ADMIN.
    """
    logout(request)
    return redirect("/admin/login/")

def materiais_reciclaveis(request):
    return render(request, "materiais_reciclaveis.html")

def custom_login(request):
    # se você já usa LoginView no urls.py, pode remover esta função.
    # Deixei aqui só para não quebrar importes antigos caso existam.
    from django.contrib.auth.views import LoginView
    return LoginView.as_view(template_name="pagina/login.html")(request)
