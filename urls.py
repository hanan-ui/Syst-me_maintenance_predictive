from django.urls import path
from . import views

app_name = "tempmon"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),                       # Page principale (dashboard)
    path("add/", views.add_reading, name="add_reading"),               # Ajouter un relevé via formulaire
    path("api/readings/", views.api_create_reading, name="api_create_reading"),  # API JSON
    path("graph/", views.graph_page, name="graph_page"),               # Page graphique
]
