"""Forms do app Manutenções"""
from django import forms
from .models import Manutencao


class ManutencaoForm(forms.ModelForm):
    """Formulário para abertura de manutenção"""
    class Meta:
        model = Manutencao
        fields = ['robo', 'tecnico', 'tipo_manutencao', 'descricao', 'imagem_manutencao', 'relatorio']
        widgets = {
            'robo': forms.Select(attrs={'class': 'form-select'}),
            'tecnico': forms.Select(attrs={'class': 'form-select'}),
            'tipo_manutencao': forms.Select(attrs={'class': 'form-select'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'imagem_manutencao': forms.FileInput(attrs={'class': 'form-control'}),
            'relatorio': forms.FileInput(attrs={'class': 'form-control'}),
        }


class ManutencaoExecucaoForm(forms.ModelForm):
    """Formulário para registrar início de execução"""
    class Meta:
        model = Manutencao
        fields = ['data_execucao', 'pecas_substituidas']
        widgets = {
            'data_execucao': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'}
            ),
            'pecas_substituidas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ManutencaoConclusaoForm(forms.ModelForm):
    """Formulário para concluir manutenção"""
    class Meta:
        model = Manutencao
        fields = ['data_conclusao', 'custo', 'pecas_substituidas', 'observacoes_conclusao', 'imagem_manutencao']
        widgets = {
            'data_conclusao': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'}
            ),
            'custo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'pecas_substituidas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'observacoes_conclusao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'imagem_manutencao': forms.FileInput(attrs={'class': 'form-control'}),
        }
