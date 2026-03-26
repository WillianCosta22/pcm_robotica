from django.contrib import admin
from .models import OrdemServico

@admin.register(OrdemServico)
class OrdemServicoAdmin(admin.ModelAdmin):
    list_display = ['numero_os', 'robo', 'tecnico', 'prioridade', 'status', 'data_abertura']
    list_filter = ['status', 'prioridade']
    search_fields = ['numero_os', 'robo__nome', 'descricao_problema']
