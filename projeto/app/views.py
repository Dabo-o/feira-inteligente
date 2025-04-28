from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters
from .models import (
    Lojista, Cliente, Loja, Produto, Categoria, Avaliacao,
    ProdutoFavorito, LojaFavorita, Setor, TotemPessoal, TotemPesquisa
)
from .serializers import (
    LojistaSerializer, ClienteSerializer, LojaSerializer, ProdutoSerializer,
    CategoriaSerializer, AvaliacaoSerializer, ProdutoFavoritoSerializer,
    LojaFavoritaSerializer, SetorSerializer, TotemPessoalSerializer, TotemPesquisaSerializer
)

class LojistaViewSet(viewsets.ModelViewSet):
    queryset = Lojista.objects.all()
    serializer_class = LojistaSerializer
    permission_classes = (permissions.DjangoModelPermissions,)

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = (permissions.DjangoModelPermissions,)

class LojaViewSet(viewsets.ModelViewSet):
    queryset = Loja.objects.all()
    serializer_class = LojaSerializer
    permission_classes = (permissions.DjangoModelPermissions,)

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

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = (permissions.DjangoModelPermissions,)

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = (permissions.DjangoModelPermissions,)

    @action(detail=True, methods=['get'])
    def lojas(self, request, pk=None):
        categoria = self.get_object()
        serializer = LojaSerializer(categoria.lojas.all(), many=True)
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

class TotemPessoalViewSet(viewsets.ModelViewSet):
    queryset = TotemPessoal.objects.all()
    serializer_class = TotemPessoalSerializer
    permission_classes = (permissions.DjangoModelPermissions,)

class TotemPesquisaViewSet(viewsets.ModelViewSet):
    queryset = TotemPesquisa.objects.all()
    serializer_class = TotemPesquisaSerializer
    permission_classes = (permissions.DjangoModelPermissions,)
