"""URLs do app Ordens de Serviço"""
from django.urls import path
from . import views

app_name = 'ordens_servico'

urlpatterns = [
    path('', views.OrdemServicoListView.as_view(), name='list'),
    path('nova/', views.OrdemServicoCreateView.as_view(), name='create'),
    path('<int:pk>/', views.OrdemServicoDetailView.as_view(), name='detail'),
    path('<int:pk>/editar/', views.OrdemServicoUpdateView.as_view(), name='update'),
    path('<int:pk>/iniciar/', views.iniciar_os, name='iniciar'),
    path('<int:pk>/concluir/', views.OrdemServicoConcluirView.as_view(), name='concluir'),
    path('<int:pk>/cancelar/', views.cancelar_os, name='cancelar'),
]
