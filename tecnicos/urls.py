"""URLs do app Técnicos"""
from django.urls import path
from . import views

app_name = 'tecnicos'

urlpatterns = [
    path('', views.TecnicoListView.as_view(), name='list'),
    path('novo/', views.TecnicoCreateView.as_view(), name='create'),
    path('<int:pk>/', views.TecnicoDetailView.as_view(), name='detail'),
    path('<int:pk>/editar/', views.TecnicoUpdateView.as_view(), name='update'),
    path('<int:pk>/excluir/', views.TecnicoDeleteView.as_view(), name='delete'),
]
