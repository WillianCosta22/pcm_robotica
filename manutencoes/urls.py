"""URLs do app Manutenções"""
from django.urls import path
from . import views

app_name = 'manutencoes'

urlpatterns = [
    path('', views.ManutencaoListView.as_view(), name='list'),
    path('nova/', views.ManutencaoCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ManutencaoDetailView.as_view(), name='detail'),
    path('<int:pk>/iniciar/', views.ManutencaoIniciarView.as_view(), name='iniciar'),
    path('<int:pk>/concluir/', views.ManutencaoConcluirView.as_view(), name='concluir'),
    path('<int:pk>/cancelar/', views.cancelar_manutencao, name='cancelar'),
]
