# coletores/urls.py
from django.urls import path
from . import views

app_name = "coletores"

urlpatterns = [
    path("", views.ColetorListView.as_view(), name="list"),
    path("novo/", views.ColetorCreateView.as_view(), name="create"),
    path("<int:pk>/", views.ColetorDetailView.as_view(), name="detail"),
    path("<int:pk>/editar/", views.ColetorUpdateView.as_view(), name="update"),
    path("<int:pk>/excluir/", views.ColetorDeleteView.as_view(), name="delete"),
]
