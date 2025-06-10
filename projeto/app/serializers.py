from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Lojista, Cliente, Loja, Produto, Categoria, Avaliacao, 
    ProdutoFavorito, LojaFavorita, Setor, TotemPessoal, Mapas, AcaoUsuario
)

class AcaoUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcaoUsuario
        fields = '__all__'

class LojistaRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    senha = serializers.CharField(write_only=True)
    nome = serializers.CharField()

    def create(self, validated_data):
        email = validated_data.pop('email')
        senha = validated_data.pop('senha')
        nome = validated_data.pop('nome')

        user = User.objects.create_user(username=email, email=email, password=senha)
        lojista = Lojista.objects.create(user=user, nome=nome, **validated_data)
        return lojista
    
class LojistaSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    class Meta:
        model = Lojista
        fields = (
            'id', 'nome', 'email', 'telefone','genero', 'cnpj', 'foto',
            'criacao', 'atualizacao', 'ativo'
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'criacao': {'read_only': True},
            'atualizacao': {'read_only': True},
            'ativo': {'read_only': True},
        }

        


class ProdutoSerializer(serializers.ModelSerializer):
    favoritado = serializers.SerializerMethodField()
    categorias = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Categoria.objects.all()
    )
    class Meta:
        model = Produto
        fields = (
            'id', 'nome', 'descricao', 'loja', 'imagem', 'categorias', 'cor', 
            'composicao', 'criacao', 'atualizacao', 'ativo', 'favoritado'
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'criacao': {'read_only': True},
            'atualizacao': {'read_only': True},
            'ativo': {'read_only': True},
        }
    
    def get_favoritado(self, obj):
        request = self.context.get('request')
        user = request.user if request and request.user.is_authenticated else None

        if user and hasattr(user, 'cliente'):
            return ProdutoFavorito.objects.filter(produto=obj, cliente=user.cliente).exists()
        return False


class PesquisaSerializer(serializers.ModelSerializer):

    nota_media = serializers.FloatField(read_only=True)
    produtos = ProdutoSerializer(many=True)
    categorias = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Categoria.objects.all()
    )
    avaliacoes = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
        source='avaliacoes_recebidas'  # ou o related_name que você usou no model
    )


    class Meta:
        model = Loja
        fields = (
            'id', 'nome', 'banner', 'logo', 'descricao','produtos','setor', 'categorias', 'localizacao',
            'lojista', 'foto_da_loja', 'Instagram','WhatsApp','Website', 'horario_funcionamento', 
            'avaliacoes', 'nota_media', 'criacao', 'atualizacao', 'ativo'
        )
        extra_kwargs = {
            'nota_media': {'read_only': True},
            'avaliacoes': {'read_only': True},
            'produtos': {'read_only': True},
            'id': {'read_only': True},
            'criacao': {'read_only': True},
            'atualizacao': {'read_only': True},
            'ativo': {'read_only': True},
        }

class LojaSerializer(serializers.ModelSerializer):
    favoritado = serializers.SerializerMethodField()
    nota_media = serializers.FloatField(read_only=True)
    produtos = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )
    categorias = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Categoria.objects.all()
    )
    avaliacoes = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
        source='avaliacoes_recebidas'  # ou o related_name que você usou no model
    )


    class Meta:
        model = Loja
        fields = (
            'id', 'nome', 'banner', 'logo', 'descricao','produtos','setor', 'categorias', 'localizacao',
            'lojista', 'foto_da_loja', 'Instagram','WhatsApp','Website', 'horario_funcionamento', 
            'avaliacoes', 'nota_media', 'criacao', 'atualizacao', 'ativo', 'favoritado'
        )
        
        extra_kwargs = {
            'nota_media': {'read_only': True},
            'avaliacoes': {'read_only': True},
            'produtos': {'read_only': True},
            'id': {'read_only': True},
            'criacao': {'read_only': True},
            'atualizacao': {'read_only': True},
            'ativo': {'read_only': True},
        }

    def get_favoritado(self, obj):
        request = self.context.get('request')
        user = request.user if request and request.user.is_authenticated else None

        if user and hasattr(user, 'cliente'):
            return LojaFavorita.objects.filter(loja=obj, cliente=user.cliente).exists()
        return False



class ClienteRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    senha = serializers.CharField(write_only=True)

    class Meta:
        model = Cliente
        fields = ('nome', 'email', 'senha')

    def create(self, validated_data):
        email = validated_data.pop('email')
        senha = validated_data.pop('senha')
        nome = validated_data.pop('nome')

        user = User.objects.create_user(username=email, email=email, password=senha)
        cliente = Cliente.objects.create(user=user, nome=nome, **validated_data)
        return cliente

class ClienteSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    categorias_desejadas = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Categoria.objects.all()
    )

    produtos_favoritos = ProdutoSerializer(many=True, read_only=True)
    lojas_favoritas = LojaSerializer(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True) 

    def update(self, instance, validated_data):
        validated_data.pop('user', None)  # impede sobrescrita
        return super().update(instance, validated_data)

    class Meta:
        model = Cliente
        fields = (
            'id','user', 'nome','email', 'cpf', 'telefone', 'foto', 'data_nascimento',
            'genero', 'tipo', 'categorias_desejadas','produtos_favoritos', 'lojas_favoritas', 'criacao', 'atualizacao', 'ativo'
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'criacao': {'read_only': True},
            'atualizacao': {'read_only': True},
            'ativo': {'read_only': True},
            'user': {'read_only': True},
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
    nome_cliente = serializers.SerializerMethodField()

    class Meta:
        model = Avaliacao
        fields = (
            'id', 'cliente', 'nome_cliente', 'loja', 'nota', 'comentario',
            'criacao', 'atualizacao', 'ativo'
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'criacao': {'read_only': True},
            'atualizacao': {'read_only': True},
            'ativo': {'read_only': True},
        }

    def get_nome_cliente(self, obj):
        return obj.cliente.nome if obj.cliente else None



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
class MapasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mapas
        fields = (
            'id', 'loja', 'mapa', 'criacao', 'atualizacao', 'ativo'
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
            'id', 'tipo_usuario', 'faixa_etaria', 'genero','categoria', 'criacao', 'atualizacao', 'ativo'
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'criacao': {'read_only': True},
            'atualizacao': {'read_only': True},
            'ativo': {'read_only': True},
        }

