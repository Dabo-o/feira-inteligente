from django.contrib import admin
from .models import (
    Lojista, TotemPessoal, Categoria, Setor, Cliente, Loja,
    Produto, Avaliacao, ProdutoFavorito, LojaFavorita, TotemPesquisa
)

@admin.register(Lojista)
class LojistaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'cpf_cnpj', 'ativo', 'criacao', 'atualizacao')
    search_fields = ('nome', 'email', 'cpf_cnpj')
    list_filter = ('ativo',)

@admin.register(TotemPessoal)
class TotemPessoalAdmin(admin.ModelAdmin):
    list_display = ('tipo_usuario', 'faixa_etaria', 'genero', 'ativo', 'criacao', 'atualizacao')
    list_filter = ('tipo_usuario', 'faixa_etaria', 'ativo')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'setor', 'ativo', 'criacao', 'atualizacao')
    search_fields = ('nome',)
    list_filter = ('ativo',)

@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'lojas', 'ativo', 'criacao', 'atualizacao')
    search_fields = ('nome',)
    list_filter = ('ativo',)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'tipo', 'categoria', 'ativo', 'criacao', 'atualizacao')
    search_fields = ('nome', 'email', 'telefone')
    list_filter = ('tipo', 'ativo')

@admin.register(Loja)
class LojaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'localizacao', 'lojista', 'nota', 'ativo', 'criacao', 'atualizacao')
    search_fields = ('nome', 'localizacao', 'lojista__nome')
    list_filter = ('ativo',)

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'loja', 'categoria', 'cor', 'ativo', 'criacao', 'atualizacao')
    search_fields = ('nome', 'cor')
    list_filter = ('ativo',)

@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'loja', 'nota','ativo', 'criacao', 'atualizacao')
    search_fields = ('cliente__nome', 'loja__nome')
    list_filter = ('nota', 'ativo')

@admin.register(ProdutoFavorito)
class ProdutoFavoritoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'produto', 'ativo', 'criacao', 'atualizacao')
    search_fields = ('cliente__nome', 'produto__nome')
    list_filter = ('ativo',)

@admin.register(LojaFavorita)
class LojaFavoritaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'loja','ativo', 'criacao', 'atualizacao')
    search_fields = ('cliente__nome', 'loja__nome')
    list_filter = ('ativo',)

@admin.register(TotemPesquisa)
class TotemPesquisaAdmin(admin.ModelAdmin):
    list_display = ('categoria','totemid', 'ativo', 'criacao', 'atualizacao')
    search_fields = ('categoria__nome',)
    list_filter = ('ativo',)
