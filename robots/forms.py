"""Forms do app Robots"""
from django import forms
from .models import Robot


class RobotForm(forms.ModelForm):
    class Meta:
        model = Robot
        fields = [
            'nome', 'modelo', 'fabricante', 'numero_serie', 'patrimonio',
            'ano_fabricacao', 'data_aquisicao', 'localizacao', 'grupo', 'alocacao',
            'status_operacional', 'observacoes', 'imagem', 'documento_tecnico'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'fabricante': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_serie': forms.TextInput(attrs={'class': 'form-control'}),
            'patrimonio': forms.TextInput(attrs={'class': 'form-control'}),
            'ano_fabricacao': forms.NumberInput(attrs={'class': 'form-control', 'min': 1990, 'max': 2030}),
            'data_aquisicao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'localizacao': forms.TextInput(attrs={'class': 'form-control'}),
            'grupo': forms.TextInput(attrs={'class': 'form-control'}),
            'alocacao': forms.TextInput(attrs={'class': 'form-control'}),
            'status_operacional': forms.Select(attrs={'class': 'form-select'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'imagem': forms.FileInput(attrs={'class': 'form-control'}),
            'documento_tecnico': forms.FileInput(attrs={'class': 'form-control'}),
        }


class RobotFilterForm(forms.Form):
    busca = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar robô...'})
    )
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'Todos os status')] + Robot.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    localizacao = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Filtrar por localização...'})
    )
