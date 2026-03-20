"""Models do app Ordens de Serviço"""
from django.db import models
from django.utils import timezone
from robots.models import Robot
from tecnicos.models import Tecnico


class OrdemServico(models.Model):
    """Modelo representando uma Ordem de Serviço"""

    PRIORIDADE_CHOICES = [
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta'),
        ('critica', 'Crítica'),
    ]

    STATUS_CHOICES = [
        ('aberta', 'Aberta'),
        ('em_andamento', 'Em andamento'),
        ('concluida', 'Concluída'),
        ('cancelada', 'Cancelada'),
    ]

    PRIORIDADE_COLORS = {
        'baixa': 'success',
        'media': 'info',
        'alta': 'warning',
        'critica': 'danger',
    }

    STATUS_COLORS = {
        'aberta': 'primary',
        'em_andamento': 'warning',
        'concluida': 'success',
        'cancelada': 'secondary',
    }

    numero_os = models.CharField(max_length=20, unique=True, verbose_name='Número OS', blank=True)
    robo = models.ForeignKey(Robot, on_delete=models.CASCADE, verbose_name='Robô')
    tecnico = models.ForeignKey(
        Tecnico, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Técnico Responsável'
    )
    prioridade = models.CharField(
        max_length=10, choices=PRIORIDADE_CHOICES, default='media', verbose_name='Prioridade'
    )
    descricao_problema = models.TextField(verbose_name='Descrição do Problema')
    data_abertura = models.DateTimeField(auto_now_add=True, verbose_name='Data de Abertura')
    data_inicio = models.DateTimeField(null=True, blank=True, verbose_name='Data de Início')
    data_conclusao = models.DateTimeField(null=True, blank=True, verbose_name='Data de Conclusão')
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='aberta', verbose_name='Status'
    )
    solucao = models.TextField(blank=True, verbose_name='Solução Aplicada')

    class Meta:
        verbose_name = 'Ordem de Serviço'
        verbose_name_plural = 'Ordens de Serviço'
        ordering = ['-data_abertura']

    def __str__(self):
        return f"OS {self.numero_os} - {self.robo.nome}"

    def save(self, *args, **kwargs):
        """Gera número de OS automaticamente se não informado"""
        if not self.numero_os:
            year = timezone.now().year
            last = OrdemServico.objects.filter(
                data_abertura__year=year
            ).order_by('-numero_os').first()
            if last and last.numero_os:
                try:
                    num = int(last.numero_os.split('-')[-1]) + 1
                except (ValueError, IndexError):
                    num = 1
            else:
                num = 1
            self.numero_os = f"OS-{year}-{num:04d}"
        super().save(*args, **kwargs)

    def get_prioridade_color(self):
        return self.PRIORIDADE_COLORS.get(self.prioridade, 'secondary')

    def get_status_color(self):
        return self.STATUS_COLORS.get(self.status, 'secondary')
