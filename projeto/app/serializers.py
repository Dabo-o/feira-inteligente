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


class ProdutoSerializer(serializers.ModelSerializer):
    categorias = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Categoria.objects.all()
    )
    class Meta:
        model = Produto
        fields = (
            'id', 'nome', 'descricao', 'imagem', 'categorias', 'cor', 
            'composicao', 'criacao', 'atualizacao', 'ativo'
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'criacao': {'read_only': True},
            'atualizacao': {'read_only': True},
            'ativo': {'read_only': True},
        }
class LojaSerializer(serializers.ModelSerializer):
    nota_media = serializers.FloatField(read_only=True)
    produtos = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Produto.objects.all()
    )
    categorias = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Categoria.objects.all()
    )

    class Meta:
        model = Loja
        fields = (
            'id', 'nome', 'banner', 'logo', 'descricao','produtos','setor', 'categorias', 'localizacao',
            'lojista', 'foto_da_loja', 'redes_sociais', 'horario_funcionamento', 
            'avaliacoes', 'nota_media', 'criacao', 'atualizacao', 'ativo'
        )
        extra_kwargs = {
            'nota_media': {'read_only': True},
            'avaliacoes': {'read_only': True},
            'id': {'read_only': True},
            'criacao': {'read_only': True},
            'atualizacao': {'read_only': True},
            'ativo': {'read_only': True},
        }

class ClienteSerializer(serializers.ModelSerializer):
    categorias_desejadas = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Categoria.objects.all()
    )

    produtos_favoritos = ProdutoSerializer(many=True, read_only=True)
    lojas_favoritas = LojaSerializer(many=True, read_only=True)

    class Meta:
        model = Cliente
        fields = (
            'id', 'nome', 'email', 'senha', 'telefone', 'foto', 'faixa_etaria',
            'genero', 'tipo', 'categorias_desejadas','produtos_favoritos', 'lojas_favoritas', 'criacao', 'atualizacao', 'ativo'
        )
        extra_kwargs = {
            'senha': {'write_only': True},
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

    class Meta:
        model = Setor
        fields = (
            'id', 'nome', 'criacao', 'atualizacao', 'ativo'
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
