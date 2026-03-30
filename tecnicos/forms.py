"""Forms do app Técnicos"""
from django import forms
from django.contrib.auth.models import User
from .models import Tecnico


class TecnicoForm(forms.ModelForm):
    # Campos extras para criar/atualizar o usuário de acesso
    username = forms.CharField(
        label='Nome de usuário (login)', max_length=150, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: joao.silva'})
    )
    password = forms.CharField(
        label='Senha', required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Deixe em branco para não alterar'})
    )
    password2 = forms.CharField(
        label='Confirmar senha', required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repita a senha'})
    )

    class Meta:
        model = Tecnico
        fields = ['nome', 'matricula', 'email', 'telefone', 'especialidade', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'matricula': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: MAT-0042'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(11) 99999-9999'}),
            'especialidade': forms.Select(attrs={'class': 'form-select'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-fill username if tecnico already has a user
        if self.instance and self.instance.pk and self.instance.usuario:
            self.fields['username'].initial = self.instance.usuario.username

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password')
        p2 = cleaned.get('password2')
        if p1 and p1 != p2:
            raise forms.ValidationError('As senhas não coincidem.')
        return cleaned

    def save(self, commit=True):
        tecnico = super().save(commit=False)
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username:
            if tecnico.usuario:
                # Update existing user
                tecnico.usuario.username = username
                if password:
                    tecnico.usuario.set_password(password)
                tecnico.usuario.save()
            else:
                # Create new user
                if not password:
                    password = 'trocar123'  # default
                user = User.objects.create_user(username=username, password=password)
                user.first_name = tecnico.nome.split()[0]
                user.last_name = ' '.join(tecnico.nome.split()[1:])
                user.save()
                tecnico.usuario = user

        if commit:
            tecnico.save()
        return tecnico
