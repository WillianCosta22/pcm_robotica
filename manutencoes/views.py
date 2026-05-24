from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Q

from .models import Manutencao
from .forms import ManutencaoForm, ManutencaoExecucaoForm, ManutencaoConclusaoForm
from robots.models import Robot


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser


class ManutencaoListView(LoginRequiredMixin, ListView):
    model = Manutencao
    template_name = 'manutencoes/manutencao_list.html'
    context_object_name = 'manutencoes'
    paginate_by = 15

    def get_queryset(self):
        queryset = Manutencao.objects.select_related('robo', 'tecnico')

        # Técnicos comuns só veem as suas manutenções
        user = self.request.user
        if not (user.is_staff or user.is_superuser):
            if hasattr(user, 'tecnico'):
                queryset = queryset.filter(tecnico=user.tecnico)
            else:
                queryset = queryset.none()

        status = self.request.GET.get('status')
        tipo = self.request.GET.get('tipo')
        busca = self.request.GET.get('busca')
        if status:
            queryset = queryset.filter(status=status)
        if tipo:
            queryset = queryset.filter(tipo_manutencao=tipo)
        if busca:
            queryset = queryset.filter(
                Q(robo__nome__icontains=busca) | Q(descricao__icontains=busca)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Manutencao.STATUS_CHOICES
        context['tipo_choices'] = Manutencao.TIPO_CHOICES
        return context


class ManutencaoDetailView(LoginRequiredMixin, DetailView):
    model = Manutencao
    template_name = 'manutencoes/manutencao_detail.html'
    context_object_name = 'manutencao'


class ManutencaoCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Manutencao
    form_class = ManutencaoForm
    template_name = 'manutencoes/manutencao_form.html'
    success_url = reverse_lazy('manutencoes:list')

    def form_valid(self, form):
        manutencao = form.save(commit=False)
        manutencao.robo.status_operacional = 'em_manutencao'
        manutencao.robo.save()
        manutencao.save()
        messages.success(self.request, '✅ Manutenção aberta com sucesso!')
        return redirect('manutencoes:list')

    def get_initial(self):
        initial = super().get_initial()
        robo_id = self.request.GET.get('robo')
        if robo_id:
            initial['robo'] = robo_id
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Abrir Nova Manutenção'
        return context


class ManutencaoIniciarView(LoginRequiredMixin, UpdateView):
    """Técnico pode iniciar execução"""
    model = Manutencao
    form_class = ManutencaoExecucaoForm
    template_name = 'manutencoes/manutencao_execucao.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        user = request.user
        # Admin ou o próprio técnico da manutenção
        if not (user.is_staff or user.is_superuser):
            if not (hasattr(user, 'tecnico') and obj.tecnico == user.tecnico):
                messages.error(request, '⛔ Sem permissão para esta ação.')
                return redirect('manutencoes:list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        manutencao = form.save(commit=False)
        manutencao.status = 'em_execucao'
        if not manutencao.data_execucao:
            manutencao.data_execucao = timezone.now()
        manutencao.save()
        messages.success(self.request, '🔧 Execução iniciada!')
        return redirect('manutencoes:detail', pk=manutencao.pk)


class ManutencaoConcluirView(LoginRequiredMixin, UpdateView):
    """Técnico pode concluir"""
    model = Manutencao
    form_class = ManutencaoConclusaoForm
    template_name = 'manutencoes/manutencao_conclusao.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        user = request.user
        if not (user.is_staff or user.is_superuser):
            if not (hasattr(user, 'tecnico') and obj.tecnico == user.tecnico):
                messages.error(request, '⛔ Sem permissão para esta ação.')
                return redirect('manutencoes:list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        manutencao = form.save(commit=False)
        manutencao.status = 'concluida'
        if not manutencao.data_conclusao:
            manutencao.data_conclusao = timezone.now()
        manutencao.save()
        manutencao.robo.status_operacional = 'operacional'
        manutencao.robo.save()
        messages.success(self.request, '✅ Manutenção concluída!')
        return redirect('manutencoes:detail', pk=manutencao.pk)


def cancelar_manutencao(request, pk):
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, '⛔ Sem permissão.')
        return redirect('manutencoes:list')
    manutencao = get_object_or_404(Manutencao, pk=pk)
    if request.method == 'POST':
        manutencao.status = 'cancelada'
        manutencao.save()
        messages.warning(request, '⚠️ Manutenção cancelada.')
        return redirect('manutencoes:list')
    return redirect('manutencoes:detail', pk=pk)
