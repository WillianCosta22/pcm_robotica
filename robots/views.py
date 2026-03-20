"""Views do app Robots"""
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.http import HttpResponse
from io import BytesIO

from .models import Robot
from .forms import RobotForm, RobotFilterForm


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser


class RobotListView(LoginRequiredMixin, ListView):
    model = Robot
    template_name = 'robots/robot_list.html'
    context_object_name = 'robots'
    paginate_by = 15

    def get_queryset(self):
        queryset = Robot.objects.all()
        form = RobotFilterForm(self.request.GET)
        if form.is_valid():
            busca = form.cleaned_data.get('busca')
            status = form.cleaned_data.get('status')
            localizacao = form.cleaned_data.get('localizacao')
            if busca:
                queryset = queryset.filter(
                    Q(nome__icontains=busca) | Q(modelo__icontains=busca) |
                    Q(numero_serie__icontains=busca) | Q(patrimonio__icontains=busca) |
                    Q(fabricante__icontains=busca) | Q(alocacao__icontains=busca)
                )
            if status:
                queryset = queryset.filter(status_operacional=status)
            if localizacao:
                queryset = queryset.filter(localizacao__icontains=localizacao)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = RobotFilterForm(self.request.GET)
        context['total'] = Robot.objects.count()
        return context


class RobotDetailView(LoginRequiredMixin, DetailView):
    model = Robot
    template_name = 'robots/robot_detail.html'
    context_object_name = 'robot'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        robot = self.get_object()
        context['manutencoes'] = robot.manutencao_set.order_by('-data_abertura')[:10]
        return context


class RobotCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Robot
    form_class = RobotForm
    template_name = 'robots/robot_form.html'
    success_url = reverse_lazy('robots:list')

    def form_valid(self, form):
        messages.success(self.request, '✅ Robô cadastrado com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Cadastrar Robô'
        context['btn_label'] = 'Cadastrar'
        return context


class RobotUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Robot
    form_class = RobotForm
    template_name = 'robots/robot_form.html'
    success_url = reverse_lazy('robots:list')

    def form_valid(self, form):
        messages.success(self.request, '✅ Robô atualizado com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar Robô: {self.object.nome}'
        context['btn_label'] = 'Salvar Alterações'
        return context


class RobotDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Robot
    template_name = 'robots/robot_confirm_delete.html'
    success_url = reverse_lazy('robots:list')

    def form_valid(self, form):
        messages.success(self.request, '🗑️ Robô excluído com sucesso!')
        return super().form_valid(form)


def exportar_robots_excel(request):
    """Exporta lista de robôs em Excel formatado"""
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter

    wb = Workbook()
    ws = wb.active
    ws.title = 'Gestão de Ativos'

    # Header principal
    ws.merge_cells('A1:L1')
    ws['A1'] = 'Planilha De Gestão de Ativos - Robótica'
    ws['A1'].font = Font(bold=True, size=13, color='FFFFFF')
    ws['A1'].fill = PatternFill('solid', start_color='1F2D40')
    ws['A1'].alignment = Alignment(horizontal='center', vertical='center')
    ws.row_dimensions[1].height = 28

    # Sub-cabeçalho
    headers = ['ATIVO', 'PATRIMÔNIO', 'DENOMINAÇÃO', 'TIPO DE MNT', 'GRUPO',
               'ALOCAÇÃO', 'STATUS', 'MODELO', 'FABRICANTE', 'LOCALIZAÇÃO', 'OBSERVAÇÕES']
    header_row = 2
    header_fill = PatternFill('solid', start_color='2E4057')
    thin = Side(style='thin', color='CCCCCC')
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    for col, h in enumerate(headers, 1):
        cell = ws.cell(row=header_row, column=col, value=h)
        cell.font = Font(bold=True, color='FFFFFF', size=9)
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal='center', vertical='center')
        cell.border = border
    ws.row_dimensions[header_row].height = 22

    # Data rows
    STATUS_LABELS = {
        'operacional': 'Operacional', 'em_manutencao': 'Em manutenção',
        'parado': 'Parado', 'em_inspecao': 'Em inspeção', 'inativo': 'Inativo',
    }
    STATUS_COLORS = {
        'operacional': '198754', 'em_manutencao': 'FFC107',
        'parado': 'DC3545', 'em_inspecao': '0DCAF0', 'inativo': '6C757D',
    }

    row_fills = ['F8F9FA', 'FFFFFF']
    for i, robot in enumerate(Robot.objects.all()):
        row = i + 3
        fill = PatternFill('solid', start_color=row_fills[i % 2])
        vals = [
            robot.numero_serie or '',
            robot.patrimonio,
            robot.nome,
            '',  # tipo mnt — vazio
            robot.grupo,
            robot.alocacao,
            STATUS_LABELS.get(robot.status_operacional, robot.status_operacional),
            robot.modelo,
            robot.fabricante,
            robot.localizacao,
            robot.observacoes,
        ]
        for col, val in enumerate(vals, 1):
            cell = ws.cell(row=row, column=col, value=val)
            cell.fill = fill
            cell.border = border
            cell.font = Font(size=9)
            cell.alignment = Alignment(vertical='center', wrap_text=True)

        # Color status cell
        status_cell = ws.cell(row=row, column=7)
        color = STATUS_COLORS.get(robot.status_operacional, '6C757D')
        status_cell.font = Font(bold=True, color=color, size=9)

    # Column widths
    widths = [14, 12, 40, 12, 12, 14, 14, 20, 18, 20, 30]
    for col, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(col)].width = w

    # Freeze header rows
    ws.freeze_panes = 'A3'

    # Save
    output = BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="gestao_ativos_robotica.xlsx"'
    return response
