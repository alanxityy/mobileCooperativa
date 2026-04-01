# app/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf.urls.static import static
from . import views

from pagina.views import MaterialViewSet, ColetorViewSet, LancamentoCaixaViewSet, ProfileViewSet, CalendarioNotaViewSet

router = DefaultRouter() # rotas da api
router.register(r'notas', CalendarioNotaViewSet, basename='calendarionota')
router.register(r'materiais', MaterialViewSet, basename='material')
router.register(r'coletores', ColetorViewSet, basename='coletor')
router.register(r'caixa', LancamentoCaixaViewSet, basename='lancamentocaixa')
router.register(r'perfis', ProfileViewSet, basename='profile')

urlpatterns = [
    path("admin/logout/", views.admin_logout_view, name="admin_logout"),
    path('admin/', admin.site.urls),

    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/', include(router.urls)),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path("login/", views.custom_login, name="login"),
    path("logout/", views.logout_get, name="logout"),  # <-- GET OK

    path("", views.dashboard, name="dashboard"),

    path("coletores/", include(("coletores.urls", "coletores"), namespace="coletores")),
    path("materiais/", include(("materiais.urls", "materiais"), namespace="materiais")),
    path("caixa/", include(("caixa.urls", "caixa"), namespace="caixa")),

    path("materiais-reciclaveis/", views.materiais_reciclaveis, name="materiais_reciclaveis"),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
