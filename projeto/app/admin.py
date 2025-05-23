from django.contrib import admin
from .models import (
    Lojista, TotemPessoal, Categoria, Setor, Cliente, Loja,
    Produto, Avaliacao, ProdutoFavorito, LojaFavorita
)

@admin.register(Lojista)
class LojistaAdmin(admin.ModelAdmin):
    list_display = ('telefone', 'cpf_cnpj', 'ativo', 'criacao', 'atualizacao')
    search_fields = ('nome', 'email', 'cpf_cnpj')
    list_filter = ('ativo',)

@admin.register(TotemPessoal)
class TotemPessoalAdmin(admin.ModelAdmin):
    list_display = ('tipo_usuario', 'faixa_etaria', 'genero','categoria', 'ativo', 'criacao', 'atualizacao')
    list_filter = ('tipo_usuario', 'faixa_etaria', 'ativo')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome','ativo', 'criacao', 'atualizacao')
    search_fields = ('nome',)
    list_filter = ('ativo',)

@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ativo', 'criacao', 'atualizacao')
    search_fields = ('nome',)
    list_filter = ('ativo',)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'get_email', 'telefone', 'tipo', 'ativo', 'criacao', 'atualizacao')
    search_fields = ('nome', 'get_email', 'telefone')
    filter_horizontal = ['categorias_desejadas']
    list_filter = ('tipo', 'ativo')

    def get_email(self, obj):
        return obj.user.email
    
    get_email.short_description = 'Email'  # título da coluna no admin
    get_email.admin_order_field = 'user__email'  # permite ordenação pelo email

@admin.register(Loja)
class LojaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'localizacao', 'lojista', 'nota', 'ativo', 'criacao', 'atualizacao')
    search_fields = ('nome', 'localizacao', 'lojista__nome')
    filter_horizontal = ['categorias']
    filter_horizontal = ['avaliacoes']
    filter_horizontal = ['produtos']
    list_filter = ('ativo',)

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cor', 'ativo', 'criacao', 'atualizacao')
    filter_horizontal = ['categorias']
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
