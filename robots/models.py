"""
Models do app Robots - Representa os ativos robóticos do sistema
"""
from django.db import models


class Robot(models.Model):
    STATUS_CHOICES = [
        ('operacional', 'Operacional'),
        ('em_manutencao', 'Em manutenção'),
        ('parado', 'Parado'),
        ('em_inspecao', 'Em inspeção'),
        ('inativo', 'Inativo'),
    ]
    STATUS_COLORS = {
        'operacional': 'success',
        'em_manutencao': 'warning',
        'parado': 'danger',
        'em_inspecao': 'info',
        'inativo': 'secondary',
    }

    nome = models.CharField(max_length=200, verbose_name='Nome do Robô')
    modelo = models.CharField(max_length=200, blank=True, verbose_name='Modelo')
    fabricante = models.CharField(max_length=200, blank=True, verbose_name='Fabricante')
    numero_serie = models.CharField(max_length=100, unique=True, blank=True, null=True, verbose_name='Número de Série (Ativo)')
    patrimonio = models.CharField(max_length=100, blank=True, verbose_name='Patrimônio')
    ano_fabricacao = models.PositiveIntegerField(null=True, blank=True, verbose_name='Ano de Fabricação')
    data_aquisicao = models.DateField(null=True, blank=True, verbose_name='Data de Aquisição')
    localizacao = models.CharField(max_length=300, blank=True, verbose_name='Localização')
    grupo = models.CharField(max_length=100, blank=True, verbose_name='Grupo')
    alocacao = models.CharField(max_length=200, blank=True, verbose_name='Alocação/Cliente')
    status_operacional = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='operacional',
        verbose_name='Status Operacional'
    )
    observacoes = models.TextField(blank=True, verbose_name='Observações')
    imagem = models.ImageField(upload_to='robots/imagens/', blank=True, null=True, verbose_name='Imagem')
    documento_tecnico = models.FileField(upload_to='robots/documentos/', blank=True, null=True, verbose_name='Documento Técnico')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Robô'
        verbose_name_plural = 'Robôs'
        ordering = ['nome']

    def __str__(self):
        pat = f" [{self.patrimonio}]" if self.patrimonio else ""
        return f"{self.nome}{pat}"

    def get_status_color(self):
        return self.STATUS_COLORS.get(self.status_operacional, 'secondary')

    def ultima_manutencao(self):
        return self.manutencao_set.filter(status='concluida').order_by('-data_conclusao').first()
