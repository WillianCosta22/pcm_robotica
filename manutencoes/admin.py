from django.contrib import admin
from .models import Manutencao

@admin.register(Manutencao)
class ManutencaoAdmin(admin.ModelAdmin):
    list_display = ['id', 'robo', 'tecnico', 'tipo_manutencao', 'status', 'data_abertura']
    list_filter = ['status', 'tipo_manutencao']
    search_fields = ['robo__nome', 'descricao']
    date_hierarchy = 'data_abertura'
