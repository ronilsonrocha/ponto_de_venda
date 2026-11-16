from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Produto
# Register your models here.

@admin.register(Produto)
class ProdutoAdmin(ModelAdmin):
    list_display = ('id', 'nome', 'preco', 'estoque', 'marca', 'data_cadastro', 'data_atualizacao', 'ativo', 'imagem')
    search_fields = ['nome', 'codigo_barras', 'marca']
    list_editable = ('nome', 'preco', 'estoque','marca', 'ativo', 'imagem')


