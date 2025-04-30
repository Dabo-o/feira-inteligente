from rest_framework import serializers
from .models import (
    Lojista, Cliente, Loja, Produto, Categoria, Avaliacao, 
    ProdutoFavorito, LojaFavorita, Setor, TotemPessoal, TotemPesquisa
)

class LojistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lojista
        fields = (
            'id', 'nome', 'email', 'senha', 'telefone', 'cpf_cnpj', 'foto',
            'criacao', 'atualizacao', 'ativo'
        )
        extra_kwargs = {
            'senha': {'write_only': True},
            'id': {'read_only': True},
            'criacao': {'read_only': True},
            'atualizacao': {'read_only': True},
            'ativo': {'read_only': True},
        }

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = (
            'id', 'nome', 'email', 'senha', 'telefone', 'foto', 'faixa_etaria',
            'genero', 'tipo', 'categoria', 'criacao', 'atualizacao', 'ativo'
        )
        extra_kwargs = {
            'senha': {'write_only': True},
            'id': {'read_only': True},
            'criacao': {'read_only': True},
            'atualizacao': {'read_only': True},
            'ativo': {'read_only': True},
        }


class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = (
            'id', 'nome', 'descricao', 'imagem', 'categoria', 'cor', 
            'composicao', 'url_video', 'criacao', 'atualizacao', 'ativo'
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'criacao': {'read_only': True},
            'atualizacao': {'read_only': True},
            'ativo': {'read_only': True},
        }
class LojaSerializer(serializers.ModelSerializer):
    produtos = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Produto.objects.all()
    )

    class Meta:
        model = Loja
        fields = (
            'id', 'nome', 'banner', 'logo', 'descricao','produtos', 'categoria', 'localizacao',
            'lojista', 'foto_da_loja', 'redes_sociais', 'horario_funcionamento', 
            'avaliacoes', 'nota', 'criacao', 'atualizacao', 'ativo'
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'criacao': {'read_only': True},
            'atualizacao': {'read_only': True},
            'ativo': {'read_only': True},
        }

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = (
            'id', 'nome', 'criacao', 'atualizacao', 'ativo'
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'criacao': {'read_only': True},
            'atualizacao': {'read_only': True},
            'ativo': {'read_only': True},
        }

class AvaliacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avaliacao
        fields = (
            'id', 'cliente', 'loja', 'nota', 'comentario',
            'criacao', 'atualizacao', 'ativo'
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'criacao': {'read_only': True},
            'atualizacao': {'read_only': True},
            'ativo': {'read_only': True},
        }

class ProdutoFavoritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProdutoFavorito
        fields = (
            'id', 'cliente', 'produto', 'criacao', 'atualizacao', 'ativo'
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'criacao': {'read_only': True},
            'atualizacao': {'read_only': True},
            'ativo': {'read_only': True},
        }

class LojaFavoritaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LojaFavorita
        fields = (
            'id', 'cliente', 'loja', 'criacao', 'atualizacao', 'ativo'
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'criacao': {'read_only': True},
            'atualizacao': {'read_only': True},
            'ativo': {'read_only': True},
        }

class SetorSerializer(serializers.ModelSerializer):

    categorias = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Categoria.objects.all()
    )

    class Meta:
        model = Setor
        fields = (
            'id', 'nome', 'categorias', 'lojas', 'criacao', 'atualizacao', 'ativo'
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'criacao': {'read_only': True},
            'atualizacao': {'read_only': True},
            'ativo': {'read_only': True},
        }

class TotemPessoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = TotemPessoal
        fields = (
            'id', 'tipo_usuario', 'faixa_etaria', 'genero', 'criacao', 'atualizacao', 'ativo'
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'criacao': {'read_only': True},
            'atualizacao': {'read_only': True},
            'ativo': {'read_only': True},
        }

class TotemPesquisaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TotemPesquisa
        fields = (
            'id', 'categoria', 'totemid', 'criacao', 'atualizacao', 'ativo'
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'criacao': {'read_only': True},
            'atualizacao': {'read_only': True},
            'ativo': {'read_only': True},
        }
