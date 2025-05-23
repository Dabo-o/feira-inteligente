from rest_framework import viewsets, status, filters
from rest_framework.views import APIView
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.db.models import Avg

from .models import (
    Lojista, Cliente, Loja, Produto, Categoria, Avaliacao,
    ProdutoFavorito, LojaFavorita, Setor, TotemPessoal, Mapas, AcaoUsuario
)
from .serializers import (
    LojistaSerializer, ClienteSerializer, LojaSerializer, ProdutoSerializer,
    CategoriaSerializer, AvaliacaoSerializer, ProdutoFavoritoSerializer,
    LojaFavoritaSerializer, SetorSerializer, TotemPessoalSerializer, ClienteRegisterSerializer, 
    MapasSerializer, LojistaRegisterSerializer
)

def registrar_acao(usuario, acao, loja=None, produto=None, detalhes=''):
    AcaoUsuario.objects.create(
        usuario=usuario,
        acao=acao,
        loja=loja,
        produto=produto,
        detalhes=detalhes
    )

class CriarLojistaView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LojistaRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Lojista criado com sucesso!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def meu_perfil(request):
    user = request.user
    data = {"email": user.email}

    if hasattr(user, 'cliente'):
        data["cliente"] = ClienteSerializer(user.cliente).data

    if hasattr(user, 'lojista'):
        data["lojista"] = LojistaSerializer(user.lojista).data

    return Response(data)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ClienteRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Usuário criado com sucesso!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MapaViewSet(viewsets.ModelViewSet):
    queryset = Mapas.objects.all()
    serializer_class = MapasSerializer
    permission_classes = (IsAuthenticated, )

    @action(detail=True, methods=['get'])
    def loja(self, request, pk=None):
        Mapas = self.get_object()
        lojas = Mapas.loja.all()
        serializer = LojaSerializer(lojas, many=True)
        return Response(serializer.data)

class LojistaViewSet(viewsets.ModelViewSet):
    queryset = Lojista.objects.all()
    serializer_class = LojistaSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        queryset = super().get_queryset()
        nome = self.request.query_params.get('nome')
        if nome:
            queryset = queryset.filter(nome__icontains=nome)
        return queryset

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = (IsAuthenticated, )

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
    permission_classes = (IsAuthenticated, )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Registra a ação automaticamente
        if request.user.is_authenticated:
            registrar_acao(
                usuario=request.user,
                acao='visualizou loja',
                loja=instance
            )

        return super().retrieve(request, *args, **kwargs)


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
    permission_classes = (IsAuthenticated, )

    def retrieve(self, request, *args, **kwargs):
        produto = self.get_object()

        if request.user.is_authenticated:
            registrar_acao(
                usuario=request.user,
                acao='visualizou produto',
                produto=produto
            )

        return super().retrieve(request, *args, **kwargs)

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
    permission_classes = (IsAuthenticated, )

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
    permission_classes = (IsAuthenticated, )
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
    permission_classes = (IsAuthenticated, )

class LojaFavoritaViewSet(viewsets.ModelViewSet):
    queryset = LojaFavorita.objects.all()
    serializer_class = LojaFavoritaSerializer
    permission_classes = (IsAuthenticated, )

class SetorViewSet(viewsets.ModelViewSet):
    queryset = Setor.objects.all()
    serializer_class = SetorSerializer
    permission_classes = (IsAuthenticated, )

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
    permission_classes = (IsAuthenticated, )

