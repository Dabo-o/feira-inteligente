from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg
from rest_framework import filters
from .models import (
    Lojista, Cliente, Loja, Produto, Categoria, Avaliacao,
    ProdutoFavorito, LojaFavorita, Setor, TotemPessoal
)
from .serializers import (
    LojistaSerializer, ClienteSerializer, LojaSerializer, ProdutoSerializer,
    CategoriaSerializer, AvaliacaoSerializer, ProdutoFavoritoSerializer,
    LojaFavoritaSerializer, SetorSerializer, TotemPessoalSerializer
)

class LojistaViewSet(viewsets.ModelViewSet):
    queryset = Lojista.objects.all()
    serializer_class = LojistaSerializer
    permission_classes = (permissions.DjangoModelPermissions,)

    def get_queryset(self):
        queryset = super().get_queryset()
        nome = self.request.query_params.get('nome')
        if nome:
            queryset = queryset.filter(nome__icontains=nome)
        return queryset

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = (permissions.DjangoModelPermissions,)

    def get_queryset(self):
        queryset = super().get_queryset()
        nome = self.request.query_params.get('nome')
        if nome:
            queryset = queryset.filter(nome__icontains=nome)
        return queryset

    @action(detail=True, methods=['get'])
    def categorias_desejadas(self, request, pk=None):
        cliente = self.get_object()
        categorias_desejadas = cliente.categorias_desejadas.all()
        serializer = CategoriaSerializer(categorias_desejadas, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def produtos_favoritos(self, request, pk=None):
        cliente = self.get_object()
        produtos = cliente.produtos_favoritos.all()
        serializer = ProdutoSerializer(produtos, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def lojas_favoritas(self, request, pk=None):
        cliente = self.get_object()
        lojas = cliente.lojas_favoritas.all()
        serializer = LojaSerializer(lojas, many=True)
        return Response(serializer.data)

class LojaViewSet(viewsets.ModelViewSet):

    serializer_class = LojaSerializer
    permission_classes = (permissions.DjangoModelPermissions,)


    def get_queryset(self):
        queryset = Loja.objects.annotate(nota_media=Avg('avaliacoes_recebidas__nota'))
        nome = self.request.query_params.get('nome')
        if nome:
            queryset = queryset.filter(nome__icontains=nome)
        return queryset

    # ACTION PARA PAGINAÇÃO
    @action(detail=True, methods=['get'])
    def avaliacoes(self, request, pk=None):
        self.pagination_class.page_size = 1  # Paginação: 1 por página
        avaliacoes = Avaliacao.objects.filter(loja_id=pk)
        page = self.paginate_queryset(avaliacoes)
        if page is not None:
            serializer = AvaliacaoSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = AvaliacaoSerializer(avaliacoes.all(), many=True)
        return Response(serializer.data)
    
    # ACTION PARA ENDPOINT /lojas/1/produtos
    @action(detail=True, methods=['get'])
    def produtos(self, request, pk=None):
        loja = self.get_object()
        produtos = loja.produtos.all()
        serializer = ProdutoSerializer(produtos, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def categorias(self, request, pk=None):
        loja = self.get_object()
        categorias = loja.categorias.all()
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data)
    

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = (permissions.DjangoModelPermissions,)

    # ACTION PARA BUSCAR PELO NOME
    def get_queryset(self):
        queryset = super().get_queryset()
        nome = self.request.query_params.get('nome')
        if nome:
            queryset = queryset.filter(nome__icontains=nome)
        return queryset

    # ACTION PARA CRIAÇÃO DE /produtos/1/lojas
    @action(detail=True, methods=['get'])
    def lojas(self, request, pk=None):
        produto = self.get_object()
        lojas = produto.lojas.all()
        serializer = LojaSerializer(lojas, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def categorias(self, request, pk=None):
        produto = self.get_object()
        categorias = produto.categorias.all()
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data)

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = (permissions.DjangoModelPermissions,)

    def get_queryset(self):
        queryset = super().get_queryset()
        nome = self.request.query_params.get('nome')
        if nome:
            queryset = queryset.filter(nome__icontains=nome)
        return queryset

    @action(detail=True, methods=['get'])
    def lojas(self, request, pk=None):
        categoria = self.get_object()
        serializer = LojaSerializer(categoria.lojas.all(), many=True)
        return Response(serializer.data)
    
    
    @action(detail=True, methods=['get'])
    def setores(self, request, pk=None):
        categoria = self.get_object()
        
        # Pega todas as lojas que têm essa categoria
        lojas = categoria.lojas.all()
        
        # Pega os setores dessas lojas
        setores = set(loja.setor for loja in lojas if loja.setor is not None)
        
        # Serializa os setores
        from .serializers import SetorSerializer  # certifique-se de ter esse serializer criado
        serializer = SetorSerializer(setores, many=True)
        
        return Response(serializer.data)



class AvaliacaoViewSet(viewsets.ModelViewSet):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer
    permission_classes = (permissions.DjangoModelPermissions,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['loja__id']

    def get_queryset(self):
        loja_id = self.request.query_params.get('loja')
        if loja_id:
            return self.queryset.filter(loja_id=loja_id)
        return self.queryset

class ProdutoFavoritoViewSet(viewsets.ModelViewSet):
    queryset = ProdutoFavorito.objects.all()
    serializer_class = ProdutoFavoritoSerializer
    permission_classes = (permissions.DjangoModelPermissions,)

class LojaFavoritaViewSet(viewsets.ModelViewSet):
    queryset = LojaFavorita.objects.all()
    serializer_class = LojaFavoritaSerializer
    permission_classes = (permissions.DjangoModelPermissions,)

class SetorViewSet(viewsets.ModelViewSet):
    queryset = Setor.objects.all()
    serializer_class = SetorSerializer
    permission_classes = (permissions.DjangoModelPermissions,)

    def get_queryset(self):
        queryset = super().get_queryset()
        nome = self.request.query_params.get('nome')
        if nome:
            queryset = queryset.filter(nome__icontains=nome)
        return queryset

    @action(detail=True, methods=['get'])
    def lojas(self, request, pk=None):
        setor = self.get_object()
        lojas = setor.lojas.all()
        serializer = LojaSerializer(lojas, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def categorias(self, request, pk=None):
        setor = self.get_object()

        # Filtra as categorias das lojas que estão nesse setor
        categorias = Categoria.objects.filter(lojas__setor=setor).distinct()
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data)

class TotemPessoalViewSet(viewsets.ModelViewSet):
    queryset = TotemPessoal.objects.all()
    serializer_class = TotemPessoalSerializer
    permission_classes = (permissions.DjangoModelPermissions,)

