from django.urls import path
from . import views

app_name = 'robots'

urlpatterns = [
    path('', views.RobotListView.as_view(), name='list'),
    path('novo/', views.RobotCreateView.as_view(), name='create'),
    path('<int:pk>/', views.RobotDetailView.as_view(), name='detail'),
    path('<int:pk>/editar/', views.RobotUpdateView.as_view(), name='update'),
    path('<int:pk>/excluir/', views.RobotDeleteView.as_view(), name='delete'),
    path('exportar/excel/', views.exportar_robots_excel, name='export_excel'),
    path('importar/preview/', views.preview_importacao_excel, name='import_preview'),
    path('importar/confirmar/', views.confirmar_importacao_excel, name='import_confirm'),
]
