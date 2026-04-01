from django.urls import path
from . import views

app_name = "materiais"

urlpatterns = [
    # Lista / CRUD
    path("", views.MaterialListView.as_view(), name="list"),
    path("novo/", views.MaterialCreateView.as_view(), name="create"),
    path("<int:pk>/editar/", views.MaterialUpdateView.as_view(), name="update"),
    path("<int:pk>/", views.MaterialDetailView.as_view(), name="detail"),
    path("<int:pk>/excluir/", views.MaterialDeleteView.as_view(), name="delete"),

    # JSON: preço por kg
    path("<int:pk>/preco/", views.material_preco, name="preco"),
]
