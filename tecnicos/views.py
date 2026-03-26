"""Views do app Técnicos"""
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from .models import Tecnico
from .forms import TecnicoForm


class AdminRequiredMixin(UserPassesTestMixin):
    """Só admins/staff podem criar/editar técnicos"""
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser


class TecnicoListView(LoginRequiredMixin, ListView):
    model = Tecnico
    template_name = 'tecnicos/tecnico_list.html'
    context_object_name = 'tecnicos'
    paginate_by = 12

    def get_queryset(self):
        queryset = Tecnico.objects.all()
        busca = self.request.GET.get('busca')
        if busca:
            queryset = queryset.filter(
                Q(nome__icontains=busca) | Q(especialidade__icontains=busca) | Q(matricula__icontains=busca)
            )
        ativo = self.request.GET.get('ativo')
        if ativo in ['true', 'false']:
            queryset = queryset.filter(ativo=(ativo == 'true'))
        return queryset


class TecnicoDetailView(LoginRequiredMixin, DetailView):
    model = Tecnico
    template_name = 'tecnicos/tecnico_detail.html'
    context_object_name = 'tecnico'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tecnico = self.get_object()
        context['manutencoes'] = tecnico.manutencao_set.order_by('-data_abertura')[:10]
        return context


class TecnicoCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Tecnico
    form_class = TecnicoForm
    template_name = 'tecnicos/tecnico_form.html'
    success_url = reverse_lazy('tecnicos:list')

    def form_valid(self, form):
        messages.success(self.request, '✅ Técnico cadastrado com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Cadastrar Técnico'
        return context


class TecnicoUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Tecnico
    form_class = TecnicoForm
    template_name = 'tecnicos/tecnico_form.html'
    success_url = reverse_lazy('tecnicos:list')

    def form_valid(self, form):
        messages.success(self.request, '✅ Técnico atualizado com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar Técnico: {self.object.nome}'
        return context


class TecnicoDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Tecnico
    template_name = 'tecnicos/tecnico_confirm_delete.html'
    success_url = reverse_lazy('tecnicos:list')

    def form_valid(self, form):
        messages.success(self.request, '🗑️ Técnico excluído com sucesso!')
        return super().form_valid(form)
