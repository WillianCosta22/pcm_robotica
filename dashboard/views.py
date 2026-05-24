"""Views do Dashboard"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone
import json

from robots.models import Robot
from manutencoes.models import Manutencao
from tecnicos.models import Tecnico


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # KPIs de robôs (cada um como link para lista filtrada)
        context['total_robots'] = Robot.objects.count()
        context['robots_operacionais'] = Robot.objects.filter(status_operacional='operacional').count()
        context['robots_manutencao'] = Robot.objects.filter(status_operacional='em_manutencao').count()
        context['robots_parados'] = Robot.objects.filter(status_operacional='parado').count()
        context['robots_inativos'] = Robot.objects.filter(status_operacional='inativo').count()

        # Manutenções
        context['manutencoes_abertas'] = Manutencao.objects.filter(status='aberta').count()
        context['manutencoes_em_execucao'] = Manutencao.objects.filter(status='em_execucao').count()
        context['total_tecnicos'] = Tecnico.objects.filter(ativo=True).count()

        # Últimas manutenções
        context['ultimas_manutencoes'] = Manutencao.objects.select_related(
            'robo', 'tecnico'
        ).order_by('-data_abertura')[:8]

        # Gráfico: Manutenções por mês (últimos 6 meses)
        seis_meses = timezone.now() - timezone.timedelta(days=180)
        manut_mes = (
            Manutencao.objects
            .filter(data_abertura__gte=seis_meses)
            .annotate(mes=TruncMonth('data_abertura'))
            .values('mes').annotate(total=Count('id')).order_by('mes')
        )
        context['chart_manutencoes_labels'] = json.dumps([m['mes'].strftime('%b/%Y') for m in manut_mes])
        context['chart_manutencoes_data'] = json.dumps([m['total'] for m in manut_mes])

        # Gráfico: Status dos robôs (pizza)
        status_data = Robot.objects.values('status_operacional').annotate(total=Count('id'))
        status_map = dict(Robot.STATUS_CHOICES)
        context['chart_status_labels'] = json.dumps([status_map.get(s['status_operacional'], s['status_operacional']) for s in status_data])
        context['chart_status_data'] = json.dumps([s['total'] for s in status_data])

        # Gráfico: Custos por mês
        custos = (
            Manutencao.objects
            .filter(data_abertura__gte=seis_meses, custo__isnull=False)
            .annotate(mes=TruncMonth('data_abertura'))
            .values('mes').annotate(total=Sum('custo')).order_by('mes')
        )
        context['chart_custo_labels'] = json.dumps([c['mes'].strftime('%b/%Y') for c in custos])
        context['chart_custo_data'] = json.dumps([float(c['total']) for c in custos])

        return context
