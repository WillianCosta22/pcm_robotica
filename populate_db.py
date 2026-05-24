"""
Script para popular o banco de dados com dados do arquivo Excel de ativos.
Execute: python populate_db.py
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'robot_sap.settings')
django.setup()

from django.contrib.auth.models import User
from robots.models import Robot
from tecnicos.models import Tecnico
from manutencoes.models import Manutencao

print("🤖 Populando banco de dados RobotSAP...")

# ── Superusuário admin ──────────────────────────────────────────────
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@robotsap.com', 'admin123')
    print("✅ Superusuário criado: admin / admin123")
else:
    print("  ℹ️  admin já existe")

# ── Técnicos com logins ─────────────────────────────────────────────
tecnicos_data = [
    {
        'nome': 'Carlos Eduardo Silva',
        'matricula': 'MAT-001',
        'email': 'carlos@robotsap.com',
        'telefone': '(85) 99111-1111',
        'especialidade': 'mecanica',
        'username': 'carlos.silva',
        'password': 'tecnico123',
    },
    {
        'nome': 'Ana Paula Santos',
        'matricula': 'MAT-002',
        'email': 'ana@robotsap.com',
        'telefone': '(85) 99222-2222',
        'especialidade': 'eletronica',
        'username': 'ana.santos',
        'password': 'tecnico123',
    },
    {
        'nome': 'Roberto Ferreira',
        'matricula': 'MAT-003',
        'email': 'roberto@robotsap.com',
        'telefone': '(85) 99333-3333',
        'especialidade': 'inspecao',
        'username': 'roberto.ferreira',
        'password': 'tecnico123',
    },
]

tecnicos = []
for td in tecnicos_data:
    username = td.pop('username')
    password = td.pop('password')

    obj, created = Tecnico.objects.get_or_create(
        matricula=td['matricula'],
        defaults={k: v for k, v in td.items()}
    )
    if created or not obj.usuario:
        user, ucreated = User.objects.get_or_create(username=username)
        if ucreated:
            user.set_password(password)
            user.first_name = td['nome'].split()[0]
            user.last_name = ' '.join(td['nome'].split()[1:])
            user.save()
        obj.usuario = user
        obj.save()
        print(f"  + Técnico: {obj.nome} | login: {username} / {password}")
    else:
        print(f"  ℹ️  Técnico já existe: {obj.nome}")
    tecnicos.append(obj)

# ── Robôs do Excel ──────────────────────────────────────────────────
# Dados extraídos do arquivo: Planilha_de_Gestão_de_Ativos_-_Robótica.xlsx
robots_data = [
    {'numero_serie': 'RIYR301', 'patrimonio': 'RB000', 'nome': 'Robô de Inspeção Yadah Robotics VX-300L',   'grupo': 'GEYR300', 'alocacao': 'BRASKEM', 'status_operacional': 'operacional'},
    {'numero_serie': 'RIYR601', 'patrimonio': 'RB001', 'nome': 'Robô de Inspeção Yadah Robotics VX-600L',   'grupo': 'GEYR600', 'alocacao': '',        'status_operacional': 'inativo'},
    {'numero_serie': 'RIRS002', 'patrimonio': 'RB002', 'nome': 'Robô de Inspeção Transtar II RS Technical Service', 'grupo': 'GERS001', 'alocacao': '', 'status_operacional': 'operacional'},
    {'numero_serie': 'RIES002', 'patrimonio': 'RB004', 'nome': 'Robô de Inspeção Easy Sight Novo',           'grupo': 'GEES005', 'alocacao': 'BRASKEM', 'status_operacional': 'operacional'},
    {'numero_serie': 'RUSL001', 'patrimonio': 'RB005', 'nome': 'Robô de Cura UV SpeedyLight+',               'grupo': 'GEST001', 'alocacao': '',        'status_operacional': 'operacional'},
    {'numero_serie': 'RCCD001', 'patrimonio': 'RB006', 'nome': 'Robô de Corte Cutter Drive',                 'grupo': 'GIMS001', 'alocacao': '',        'status_operacional': 'inativo'},
    {'numero_serie': 'CIYR001', 'patrimonio': 'RB010', 'nome': 'Carretel de Inspeção Yadah Antigo',          'grupo': 'GEYR300', 'alocacao': 'BRASKEM', 'status_operacional': 'operacional'},
    {'numero_serie': 'CIYR002', 'patrimonio': 'RB011', 'nome': 'Carretel de Inspeção Yadah Novo',            'grupo': 'GEYR600', 'alocacao': '',        'status_operacional': 'operacional'},
    {'numero_serie': 'CIRS002', 'patrimonio': 'RB013', 'nome': 'Carretel de Inspeção RS Technical Service Novo', 'grupo': 'GERS001', 'alocacao': '',   'status_operacional': 'operacional'},
    {'numero_serie': 'CIES001', 'patrimonio': 'RB014', 'nome': 'Carretel de Inspeção Easy Sight',            'grupo': 'GEES005', 'alocacao': 'BRASKEM', 'status_operacional': 'operacional'},
    {'numero_serie': 'CRES001', 'patrimonio': 'RB020', 'nome': 'Câmera Robótica Easy Sight',                 'grupo': 'GEES001', 'alocacao': 'BRASKEM', 'status_operacional': 'operacional'},
    {'numero_serie': 'CRQV001', 'patrimonio': 'RB021', 'nome': 'Câmera Robótica Quick View',                 'grupo': 'GEQV001', 'alocacao': 'BRASKEM', 'status_operacional': 'operacional'},
    {'numero_serie': 'CENO002', 'patrimonio': 'RB022', 'nome': 'Câmera Endoscópica Nunes Oliveira',          'grupo': 'GENO001', 'alocacao': 'BRASKEM', 'status_operacional': 'operacional'},
    {'numero_serie': 'CMES002', 'patrimonio': 'RB024', 'nome': 'Câmera de Movimento Easy Sight Nova',        'grupo': 'GEES005', 'alocacao': 'BRASKEM', 'status_operacional': 'operacional'},
    {'numero_serie': 'CLES002', 'patrimonio': 'RB026', 'nome': 'Câmera Lanterna Easy Sight Nova',            'grupo': 'GEES005', 'alocacao': 'BRASKEM', 'status_operacional': 'operacional'},
    {'numero_serie': 'CAES001', 'patrimonio': 'RB027', 'nome': 'Câmera Axial Easy Sight',                    'grupo': 'GEES005', 'alocacao': 'BRASKEM', 'status_operacional': 'operacional'},
    {'numero_serie': 'PEES001', 'patrimonio': 'RB028', 'nome': 'Plataforma Elevatória Easy Sight Antiga',    'grupo': 'GEES005', 'alocacao': 'BRASKEM', 'status_operacional': 'operacional'},
    {'numero_serie': 'PEES002', 'patrimonio': 'RB029', 'nome': 'Plataforma Elevatória Easy Sight Nova',      'grupo': 'GEES005', 'alocacao': 'BRASKEM', 'status_operacional': 'operacional'},
    {'numero_serie': 'CBYR001', 'patrimonio': 'RB040', 'nome': 'Computador de Bordo Yadah Robotics Antiga',  'grupo': 'GEYR600', 'alocacao': 'BRASKEM', 'status_operacional': 'operacional'},
    {'numero_serie': 'CBYR002', 'patrimonio': 'RB041', 'nome': 'Computador de Bordo Yadah Robotics Nova',    'grupo': 'GEYR300', 'alocacao': '',        'status_operacional': 'operacional'},
    {'numero_serie': 'CBRS002', 'patrimonio': 'RB042', 'nome': 'Computador de Bordo RS Technical Service',   'grupo': 'GERS001', 'alocacao': '',        'status_operacional': 'operacional'},
    {'numero_serie': 'CBES001', 'patrimonio': 'RB043', 'nome': 'Computador de Bordo Easy Sight',             'grupo': 'GEES005', 'alocacao': 'BRASKEM', 'status_operacional': 'operacional'},
    {'numero_serie': 'CBNO001', 'patrimonio': 'RB044', 'nome': 'Computador de Bordo Nunes Oliveira',         'grupo': 'GENO001', 'alocacao': 'BRASKEM', 'status_operacional': 'operacional'},
    {'numero_serie': 'TOES001', 'patrimonio': 'RB045', 'nome': 'Tablet de Operação 1 (HONOR)',               'grupo': 'GEES001', 'alocacao': 'BRASKEM', 'status_operacional': 'operacional'},
    {'numero_serie': 'TOQV001', 'patrimonio': 'RB046', 'nome': 'Tablet de Operação 2 (SAMSUNG)',             'grupo': 'GEQV001', 'alocacao': 'BRASKEM', 'status_operacional': 'operacional'},
    {'numero_serie': 'TOQV002', 'patrimonio': 'RB047', 'nome': 'Tablet de Operação 3 (XIAOMI)',              'grupo': 'GEQV001', 'alocacao': 'BRASKEM', 'status_operacional': 'operacional'},
]

robots = []
for rd in robots_data:
    obj, created = Robot.objects.get_or_create(
        numero_serie=rd['numero_serie'],
        defaults=rd
    )
    if created:
        print(f"  + Robô: [{obj.patrimonio}] {obj.nome}")
    else:
        # Update fields if already exists
        for k, v in rd.items():
            setattr(obj, k, v)
        obj.save()
        print(f"  ↻ Atualizado: [{obj.patrimonio}] {obj.nome}")
    robots.append(obj)

# ── Manutenções de exemplo ──────────────────────────────────────────
if Manutencao.objects.count() == 0:
    import random
    from django.utils import timezone
    from datetime import timedelta

    descricoes = [
        'Verificação e limpeza dos sensores de câmera',
        'Substituição do cabo de alimentação danificado',
        'Manutenção preventiva mensal - verificação geral',
        'Problema no motor de tração - análise e substituição',
        'Atualização de firmware do controlador embarcado',
        'Limpeza e lubrificação dos trilhos de deslizamento',
    ]
    tipos = ['preventiva', 'corretiva', 'preditiva']
    for i, robot in enumerate(robots[:8]):
        m = Manutencao.objects.create(
            robo=robot,
            tecnico=tecnicos[i % len(tecnicos)],
            tipo_manutencao=tipos[i % 3],
            descricao=descricoes[i % len(descricoes)],
            status='concluida' if i % 3 != 2 else 'aberta',
        )
        if m.status == 'concluida':
            from django.utils import timezone
            m.data_execucao = timezone.now() - timedelta(days=random.randint(10, 40))
            m.data_conclusao = timezone.now() - timedelta(days=random.randint(1, 9))
            m.custo = round(random.uniform(200, 3000), 2)
            m.save()
        print(f"  + Manutenção: #{m.pk} - {robot.nome} [{m.get_tipo_manutencao_display()}]")

print(f"\n✅ Concluído! {Robot.objects.count()} robôs, {Tecnico.objects.count()} técnicos, {Manutencao.objects.count()} manutenções.")
print("\n🔑 Credenciais:")
print("   Admin:   admin / admin123")
print("   Técnico: carlos.silva / tecnico123")
print("   Técnico: ana.santos / tecnico123")
print("   Técnico: roberto.ferreira / tecnico123")
print("\n🔗 Acesse: http://127.0.0.1:8000")
