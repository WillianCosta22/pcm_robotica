# 🤖 RobotSAP — Sistema de Gestão de Ativos Robóticos

---

## 🚀 Instalação rápida

```bash
# 1. Criar e ativar ambiente virtual
python -m venv venv
source venv/bin/activate      # Linux/Mac
# venv\Scripts\activate       # Windows

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Criar banco de dados
python manage.py makemigrations robots tecnicos manutencoes dashboard usuarios
python manage.py migrate

# 4. Popular com dados de exemplo (inclui robôs do Excel + técnicos com login)
python populate_db.py

# 5. Rodar o servidor
python manage.py runserver
```

**Acesse:** http://127.0.0.1:8000

---

## 🔑 Credenciais de acesso

| Perfil | Usuário | Senha |
|--------|---------|-------|
| Administrador | `admin` | `admin123` |
| Técnico | `carlos.silva` | `tecnico123` |
| Técnico | `ana.santos` | `tecnico123` |
| Técnico | `roberto.ferreira` | `tecnico123` |

---

## 👥 Permissões por perfil

| Ação | Admin | Técnico |
|------|-------|---------|
| Ver robôs | ✅ | ✅ |
| Cadastrar/editar/excluir robôs | ✅ | ❌ |
| Ver todas as manutenções | ✅ | ❌ (só as suas) |
| Abrir nova manutenção | ✅ | ❌ |
| Avançar status (Iniciar/Concluir) | ✅ | ✅ |
| Gerenciar técnicos | ✅ | ❌ |
| Exportar Excel | ✅ | ❌ |

---

## 📦 Dependências

```
Django>=4.2
djangorestframework>=3.14
Pillow>=10.0
openpyxl>=3.1
```
