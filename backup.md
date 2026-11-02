# Resumo e Progresso do Projeto — Ponto de Venda (PDV)

Documento de referência com tudo o que discutimos e configuramos até agora para retomar o desenvolvimento.

---

## 1. O que já foi feito ✅

1. **Configuração do `.gitignore`:**
   - Configurado para ignorar `venv/`, `.venv/`, `__pycache__/`, `.vscode/` e `.env`.
2. **Pacotes e Dependências:**
   - Django, `django-unfold` (interface administrativa moderna) e driver do PostgreSQL (`pip install "psycopg[binary]"`).
3. **Estrutura de Apps Organizada na pasta `app/`:**
   - Criada a pasta `app/` na raiz do projeto contendo os 4 módulos principais:
     - `app/produto` (`name = 'app.produto'` em `app/produto/apps.py`)
     - `app/venda` (`name = 'app.venda'` em `app/venda/apps.py`)
     - `app/cliente` (`name = 'app.cliente'` em `app/cliente/apps.py`)
     - `app/funcionario` (`name = 'app.funcionario'` em `app/funcionario/apps.py`)
   - Todos os 4 apps já estão registrados no `INSTALLED_APPS` dentro de `core/settings.py`.
   - Idioma (`pt-br`) e fuso horário (`America/Sao_Paulo`) configurados em `core/settings.py`.

---

## 2. Onde paramos (Próximo Passo Imediato) ⏳

Você criou o arquivo `.env` na raiz do projeto e limpou o bloco `DATABASES` em `core/settings.py` para conectar ao PostgreSQL.

### Passo a passo para concluir a configuração do `.env` e Banco de Dados:

#### A) Instalar o leitor de variáveis de ambiente
No terminal (com o `venv` ativo):
```bash
pip install python-dotenv
pip freeze > requirements.txt
```

#### B) Preencher o arquivo `.env` (na raiz do projeto)
```env
SECRET_KEY=django-insecure-fe3ju2)5u47+l^+c6nmqk=6zi3b4u5lh7)-#npdvfr@6r(^qm6
DEBUG=True

DB_NAME=nome_do_seu_banco
DB_USER=postgres
DB_PASSWORD=sua_senha_do_postgres
DB_HOST=localhost
DB_PORT=5432
```

#### C) Atualizar o `core/settings.py`

1. **No topo do arquivo (`core/settings.py`):**
```python
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
```

2. **Na `SECRET_KEY`:**
```python
SECRET_KEY = os.getenv('SECRET_KEY')
```

3. **No `DATABASES`:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

---

## 3. Comandos Úteis de Referência 🛠️

- **Criar um novo app dentro da pasta `app/`:**
  ```bash
  # Estando dentro da pasta app/
  python3 ../manage.py startapp nome_do_app
  ```
  *(Depois, lembrar de mudar `name = 'app.nome_do_app'` no `apps.py` do novo app e adicioná-lo ao `INSTALLED_APPS` no `core/settings.py`).*

- **Rodar migrações do banco de dados:**
  ```bash
  python3 manage.py makemigrations
  python3 manage.py migrate
  ```

- **Criar superusuário (para acessar o painel Admin com Unfold):**
  ```bash
  python3 manage.py createsuperuser
  ```

- **Iniciar o servidor de desenvolvimento:**
  ```bash
  python3 manage.py runserver
  ```

