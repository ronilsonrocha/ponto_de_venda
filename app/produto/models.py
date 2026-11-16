from django.db import models
from app.utils.forms import formatar_texto
from django.core.exceptions import ValidationError

# Create your models here.
class Produto(models.Model):    
    
    # Atributos
    nome = models.CharField("Nome do Produto",max_length=150)
    preco = models.DecimalField("Preço", max_digits=10, decimal_places=2 )
    estoque = models.IntegerField("Estoque", default=0)
    marca = models.CharField("Marca do Produto", max_length=150)
    data_cadastro = models.DateTimeField("Data de Cadastro", auto_now_add=True)
    data_atualizacao = models.DateTimeField("Data de Atualização", auto_now=True)
    ativo = models.BooleanField("Produto Ativo", default=True)
    descricao = models.TextField("Descrição do Produto",blank=True, null=True)
    codigo_barras = models.CharField("Código de Barras",max_length=50, unique=True, null=True, blank=True)
    imagem = models.ImageField("Imagem do Produto", upload_to='produtos/', blank=True, null=True)
    
    # Executa validação/normalização completa antes de gravar no banco
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    # Padroniza os dados de entrada e valida as regras de negócio antes de salvar
    def clean(self):
        self.nome = formatar_texto(self.nome)
        self.marca = formatar_texto(self.marca)
        # Evita IntegrityError no unique=True quando o formulário envia string vazia
        if self.codigo_barras is not None:
            self.codigo_barras = self.codigo_barras.strip() or None
        
        """
        Acumula os erros em um dicionário, para exibir todas as validações 
        inválidas de uma só vez no formulário/Admin
        """
        errors = {}
        if not self.nome:
            errors['nome'] = 'O nome do produto não pode ficar vazio.'
        if not self.marca:
            errors['marca'] = 'A marca do produto não pode ficar vazia.'
        if self.preco is not None and self.preco <= 0:
            errors['preco'] = 'O preço deve ser maior que R$ 0,00.'
        if self.estoque is not None and self.estoque < 0:
            errors['estoque'] = 'O estoque não pode ser negativo.'
        if self.codigo_barras and not self.codigo_barras.isdigit():
            errors['codigo_barras'] = 'O código de barras deve conter apenas números.'

        # Se houver pelo menos um erro, interrompe o salvamento e exibe as mensagens
        if errors:
            raise ValidationError(errors)
        
    # Função de retorno de nome
    def __str__(self):
        return self.nome
    
    # Classe Meta: define metadados (configurações gerais) da tabela/modelo no Django,
    # como os nomes exibidos no painel Admin, ordenação padrão e nome da tabela no banco.
    class Meta:
        ordering = ['nome']               # Ordenar os nomes dos produtos 
        verbose_name = 'Produto'          # Nome do modelo no singular (ex: "Adicionar Produto")
        verbose_name_plural = 'Produtos'  # Nome do modelo no plural no menu do Admin
