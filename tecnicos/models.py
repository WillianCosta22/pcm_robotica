"""Models do app Técnicos"""
from django.db import models
from django.contrib.auth.models import User


class Tecnico(models.Model):
    ESPECIALIDADE_CHOICES = [
        ('mecanica', 'Mecânica'),
        ('eletrica', 'Elétrica'),
        ('eletronica', 'Eletrônica'),
        ('programacao', 'Programação/Software'),
        ('hidraulica', 'Hidráulica'),
        ('pneumatica', 'Pneumática'),
        ('inspecao', 'Inspeção Robótica'),
        ('geral', 'Manutenção Geral'),
    ]

    # Vínculo com usuário Django (permite login no portal)
    usuario = models.OneToOneField(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='tecnico', verbose_name='Usuário de acesso'
    )
    nome = models.CharField(max_length=200, verbose_name='Nome Completo')
    matricula = models.CharField(max_length=50, blank=True, verbose_name='Matrícula')
    email = models.EmailField(blank=True, verbose_name='E-mail')
    telefone = models.CharField(max_length=20, blank=True, verbose_name='Telefone')
    especialidade = models.CharField(
        max_length=50, choices=ESPECIALIDADE_CHOICES, default='geral',
        verbose_name='Especialidade'
    )
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Técnico'
        verbose_name_plural = 'Técnicos'
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome}"
