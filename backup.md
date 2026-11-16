# Resumo e Progresso do Projeto — Ponto de Venda (PDV)

Documento de referência com tudo o que discutimos, configuramos e implementamos até agora para retomar o desenvolvimento.

---

## 1. O que já foi concluído ✅

### A) Estrutura Base e Ambiente
1. **Configuração do `.gitignore`:**
   - Ignorando `venv/`, `.venv/`, `env`, `__pycache__/`, `.vscode/`, `.env` e `media/` (para não enviar fotos de upload de teste para o GitHub).
   - A pasta `templates/` **não** vai para o `.gitignore`, pois faz parte do código do sistema.
2. **Variáveis de Ambiente (`.env`) e Banco de Dados PostgreSQL (`db_pdv`):**
   - Configurado e comentado o arquivo `.env` com `SECRET_KEY`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DEBUG` e `ALLOWED_HOSTS`.
   - Conectado ao `core/settings.py` usando `python-dotenv` (`load_dotenv()`).
3. **Estrutura de Apps Organizada na pasta `app/`:**
   - `app/produto` (`name = 'app.produto'`)
   - `app/venda` (`name = 'app.venda'`)
   - `app/cliente` (`name = 'app.cliente'`)
   - `app/funcionario` (`name = 'app.funcionario'`)
   - `app/utils/forms.py` (funções utilitárias reaproveitáveis, como `formatar_texto`).
   - Todos os 4 apps registrados em `INSTALLED_APPS` no `core/settings.py`.

### B) Personalização do Painel Admin (`django-unfold`) e Templates
1. **Pasta `templates/` na raiz do projeto:**
   - Configurada em `core/settings.py` com `'DIRS': [BASE_DIR / 'templates']`.
   - Sobrescrito o título da tela de login do Unfold em `templates/unfold/helpers/unauthenticated_title.html` (com texto centralizado usando a classe `text-center` do Tailwind CSS).
2. **Dicionário `UNFOLD` no `core/settings.py`:**
   - Configurados `SITE_TITLE`, `SITE_HEADER`, `SITE_SUBHEADER` e `SITE_URL`.

### C) Configuração de Upload de Imagens (`MEDIA`)
1. **No `core/settings.py`:**
   - `MEDIA_URL = '/media/'` (endereço público no navegador).
   - `MEDIA_ROOT = BASE_DIR / 'media'` (pasta física onde os arquivos enviados são salvos).
   - Uso da biblioteca `Pillow` para processar `models.ImageField`.

### D) Módulo de Produto (`app/produto`) e Utilitários (`app/utils`)
1. **Utilitário `formatar_texto` (`app/utils/forms.py`):**
   - Função implementada com `return texto` para retornar o valor original quando vazio/nulo e padronizar textos não vazios com `" ".join(texto.split()).title()`.
2. **Model `Produto` (`app/produto/models.py`):**
   - Import corrigido para `from app.utils.forms import formatar_texto`.
   - Campos criados: `nome`, `preco` (`DecimalField`), `estoque` (`IntegerField`), `marca`, `data_cadastro` (`auto_now_add=True`), `data_atualizacao` (`auto_now=True`), `ativo` (`BooleanField`), `descricao` (`TextField`), `codigo_barras` (`CharField` com `unique=True, null=True, blank=True`) e `imagem` (`ImageField(upload_to='produtos/', blank=True, null=True)`).
   - Método `save()` executando `self.full_clean()` e `super().save(*args, **kwargs)` (garantindo validação no Admin e no ORM).
   - Método `clean()` centralizando a padronização (`formatar_texto()` em `nome` e `marca`, e `codigo_barras.strip() or None` para evitar `IntegrityError` no `unique=True`) e acumulando os erros no dicionário `errors` (`nome` e `marca` não vazios, `preco > 0`, `estoque >= 0`, `codigo_barras` numérico).
   - `class Meta` documentada (`ordering = ['nome']`, `verbose_name = 'Produto'`, `verbose_name_plural = 'Produtos'`), sem `db_table` customizado.
3. **Admin de Produto (`app/produto/admin.py`):**
   - Herda de `unfold.admin.ModelAdmin`.
   - Configurados `list_display`, `search_fields` (`['nome', 'codigo_barras', 'marca']`) e `list_editable`.

---

## 2. Onde você parou (Próximos Passos) ⏳

- Os ajustes imediatos de `app/produto/models.py` e `app/utils/forms.py` foram **concluídos**.
- Próximos passos sugeridos:
  1. Gerar e aplicar as migrações de `produto` (`makemigrations` e `migrate`) e validar no Django Admin.
  2. Implementar os próximos módulos (`app/cliente`, `app/funcionario` e `app/venda`).

---

## 3. Conceitos e Boas Práticas que Revisamos 💡

### A) `BASE_DIR` em `DIRS` vs `MEDIA_ROOT`
- **`'DIRS': [BASE_DIR / 'templates']`**: lista (`[ ]`) de pastas onde ficam os arquivos `.html` criados pelo programador (vai para o GitHub).
- **`MEDIA_ROOT = BASE_DIR / 'media'`**: pasta única (sem colchetes) onde o Django salva arquivos enviados pelos usuários no sistema, como fotos de produtos (fica no `.gitignore`).

### B) Organização de Validações: `models.py` vs `app/utils/forms.py`
- **No `clean()` do `models.py`:** Regras exclusivas daquela tabela (ex.: preço maior que zero e estoque não negativo em `Produto`).
- **Em `app/utils/forms.py`:** Funções genéricas reaproveitáveis em vários apps (ex.: `formatar_texto()`, `validar_apenas_numeros()`, `validar_cpf()`).

### C) Ordem de execução ao clicar em "Salvar"
1. **`clean()`** (em `forms.py` / `models.py`) ➔ Verifica e barra dados inválidos com `raise ValidationError(...)`.
2. **`save_model(self, request, obj, form, change)`** (no `admin.py`) ➔ Roda apenas no painel Admin; útil quando precisa do `request.user`.
3. **`save(self, *args, **kwargs)`** (no `models.py`) ➔ Método nativo do Django que roda sempre que o objeto é salvo em qualquer lugar do sistema; chama `super().save(*args, **kwargs)` para gravar no PostgreSQL.

### D) Opções Prontas do `admin.py` (`ModelAdmin`) e ORM
- `list_display`, `list_editable` *(1º item de `list_display` vira link e não pode estar em `list_editable`)*, `search_fields`, `list_filter`, `ordering`, `list_per_page`, `readonly_fields`, `date_hierarchy`.
- ORM: `.all()`, `.filter()`, `.get()`, `.aggregate(Sum(...))`, `.count()`.

---

## 4. Comandos Úteis de Referência 🛠️

- **Gerar e aplicar migrações no PostgreSQL:**
  ```bash
  python3 manage.py makemigrations
  python3 manage.py migrate
  ```
- **Iniciar o servidor:**
  ```bash
  python3 manage.py runserver
  ```
- **Conectar e enviar para o GitHub:**
  ```bash
  git branch -M main
  git remote add origin https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git
  git push -u origin main
  ```
