from django.contrib import admin
from .models import Tecnico

@admin.register(Tecnico)
class TecnicoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'telefone', 'especialidade', 'ativo']
    list_filter = ['especialidade', 'ativo']
    search_fields = ['nome', 'email']
