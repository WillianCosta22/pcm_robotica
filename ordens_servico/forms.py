"""Forms do app Ordens de Serviço"""
from django import forms
from .models import OrdemServico


class OrdemServicoForm(forms.ModelForm):
    class Meta:
        model = OrdemServico
        fields = ['robo', 'tecnico', 'prioridade', 'descricao_problema']
        widgets = {
            'robo': forms.Select(attrs={'class': 'form-select'}),
            'tecnico': forms.Select(attrs={'class': 'form-select'}),
            'prioridade': forms.Select(attrs={'class': 'form-select'}),
            'descricao_problema': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class OrdemServicoConclusaoForm(forms.ModelForm):
    class Meta:
        model = OrdemServico
        fields = ['solucao', 'data_conclusao']
        widgets = {
            'solucao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'data_conclusao': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'}
            ),
        }
