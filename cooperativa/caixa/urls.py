from django.urls import path
# caixa/urls.py
from django.urls import path
from . import views

app_name = "caixa"

urlpatterns = [
    path("", views.CaixaListView.as_view(), name="list"),
    path("novo/", views.CaixaCreateView.as_view(), name="create"),
    path("<int:pk>/", views.CaixaDetailView.as_view(), name="detail"),
    path("<int:pk>/editar/", views.CaixaUpdateView.as_view(), name="update"),
    path("<int:pk>/excluir/", views.CaixaDeleteView.as_view(), name="delete"),
]
