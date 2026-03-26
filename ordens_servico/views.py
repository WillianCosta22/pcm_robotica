"""Views do app Ordens de Serviço"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Q

from .models import OrdemServico
from .forms import OrdemServicoForm, OrdemServicoConclusaoForm


class OrdemServicoListView(LoginRequiredMixin, ListView):
    model = OrdemServico
    template_name = 'ordens_servico/os_list.html'
    context_object_name = 'ordens'
    paginate_by = 10

    def get_queryset(self):
        queryset = OrdemServico.objects.select_related('robo', 'tecnico')
        status = self.request.GET.get('status')
        prioridade = self.request.GET.get('prioridade')
        busca = self.request.GET.get('busca')

        if status:
            queryset = queryset.filter(status=status)
        if prioridade:
            queryset = queryset.filter(prioridade=prioridade)
        if busca:
            queryset = queryset.filter(
                Q(numero_os__icontains=busca) |
                Q(robo__nome__icontains=busca) |
                Q(descricao_problema__icontains=busca)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = OrdemServico.STATUS_CHOICES
        context['prioridade_choices'] = OrdemServico.PRIORIDADE_CHOICES
        return context


class OrdemServicoDetailView(LoginRequiredMixin, DetailView):
    model = OrdemServico
    template_name = 'ordens_servico/os_detail.html'
    context_object_name = 'ordem'


class OrdemServicoCreateView(LoginRequiredMixin, CreateView):
    model = OrdemServico
    form_class = OrdemServicoForm
    template_name = 'ordens_servico/os_form.html'
    success_url = reverse_lazy('ordens_servico:list')

    def form_valid(self, form):
        messages.success(self.request, '✅ Ordem de Serviço aberta com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Abrir Ordem de Serviço'
        return context


class OrdemServicoUpdateView(LoginRequiredMixin, UpdateView):
    model = OrdemServico
    form_class = OrdemServicoForm
    template_name = 'ordens_servico/os_form.html'
    success_url = reverse_lazy('ordens_servico:list')

    def form_valid(self, form):
        messages.success(self.request, '✅ Ordem de Serviço atualizada!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar OS: {self.object.numero_os}'
        return context


def iniciar_os(request, pk):
    """Inicia o atendimento de uma OS"""
    ordem = get_object_or_404(OrdemServico, pk=pk)
    if request.method == 'POST':
        ordem.status = 'em_andamento'
        ordem.data_inicio = timezone.now()
        ordem.save()
        messages.success(request, '🔧 Ordem de Serviço em andamento!')
    return redirect('ordens_servico:detail', pk=pk)


class OrdemServicoConcluirView(LoginRequiredMixin, UpdateView):
    """Conclui uma OS"""
    model = OrdemServico
    form_class = OrdemServicoConclusaoForm
    template_name = 'ordens_servico/os_conclusao.html'

    def form_valid(self, form):
        ordem = form.save(commit=False)
        ordem.status = 'concluida'
        if not ordem.data_conclusao:
            ordem.data_conclusao = timezone.now()
        ordem.save()
        messages.success(self.request, '✅ Ordem de Serviço concluída!')
        return redirect('ordens_servico:detail', pk=ordem.pk)


def cancelar_os(request, pk):
    """Cancela uma OS"""
    ordem = get_object_or_404(OrdemServico, pk=pk)
    if request.method == 'POST':
        ordem.status = 'cancelada'
        ordem.save()
        messages.warning(request, '⚠️ Ordem de Serviço cancelada.')
        return redirect('ordens_servico:list')
    return redirect('ordens_servico:detail', pk=pk)
