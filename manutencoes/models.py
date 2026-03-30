from django.db import models
from robots.models import Robot
from tecnicos.models import Tecnico


class Manutencao(models.Model):
    TIPO_CHOICES = [
        ('preventiva', 'Preventiva'),
        ('corretiva', 'Corretiva'),
        ('preditiva', 'Preditiva'),
    ]
    STATUS_CHOICES = [
        ('aberta', 'Aberta'),
        ('em_execucao', 'Em execução'),
        ('concluida', 'Concluída'),
        ('cancelada', 'Cancelada'),
    ]
    STATUS_COLORS = {
        'aberta': 'primary',
        'em_execucao': 'warning',
        'concluida': 'success',
        'cancelada': 'danger',
    }

    robo = models.ForeignKey(Robot, on_delete=models.CASCADE, verbose_name='Robô')
    tecnico = models.ForeignKey(
        Tecnico, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='Técnico Responsável'
    )
    tipo_manutencao = models.CharField(
        max_length=20, choices=TIPO_CHOICES, verbose_name='Tipo de Manutenção'
    )
    descricao = models.TextField(verbose_name='Descrição do Problema/Serviço')
    data_abertura = models.DateTimeField(auto_now_add=True, verbose_name='Data de Abertura')
    data_execucao = models.DateTimeField(null=True, blank=True, verbose_name='Data de Início da Execução')
    data_conclusao = models.DateTimeField(null=True, blank=True, verbose_name='Data de Conclusão')
    custo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Custo (R$)')
    pecas_substituidas = models.TextField(blank=True, verbose_name='Peças Substituídas')
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='aberta', verbose_name='Status'
    )
    imagem_manutencao = models.ImageField(
        upload_to='manutencoes/imagens/', blank=True, null=True, verbose_name='Foto da Manutenção'
    )
    relatorio = models.FileField(
        upload_to='manutencoes/relatorios/', blank=True, null=True, verbose_name='Relatório'
    )
    observacoes_conclusao = models.TextField(blank=True, verbose_name='Observações de Conclusão')

    class Meta:
        verbose_name = 'Manutenção'
        verbose_name_plural = 'Manutenções'
        ordering = ['-data_abertura']

    def __str__(self):
        return f"Manutenção #{self.pk} - {self.robo.nome} ({self.get_tipo_manutencao_display()})"

    def get_status_color(self):
        return self.STATUS_COLORS.get(self.status, 'secondary')
