from django.contrib import admin
from .models import Robot

@admin.register(Robot)
class RobotAdmin(admin.ModelAdmin):
    list_display = ['nome', 'modelo', 'fabricante', 'numero_serie', 'localizacao', 'status_operacional']
    list_filter = ['status_operacional', 'fabricante', 'ano_fabricacao']
    search_fields = ['nome', 'modelo', 'numero_serie', 'patrimonio']
    date_hierarchy = 'data_aquisicao'
