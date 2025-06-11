from rest_framework import viewsets, status, filters
from rest_framework.views import APIView
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser

from django.db.models import Avg, Q

from .models import (
    Lojista, Cliente, Loja, Produto, Categoria, Avaliacao,
    ProdutoFavorito, LojaFavorita, Setor, TotemPessoal, Mapas, AcaoUsuario
)
from .serializers import (
    LojistaSerializer, ClienteSerializer, LojaSerializer, ProdutoSerializer,
    CategoriaSerializer, AvaliacaoSerializer, ProdutoFavoritoSerializer,
    LojaFavoritaSerializer, SetorSerializer, TotemPessoalSerializer, ClienteRegisterSerializer, 
    MapasSerializer, LojistaRegisterSerializer, AcaoUsuarioSerializer, PesquisaSerializer
)

def registrar_acao(usuario, acao, loja=None, produto=None, detalhes=''):
    AcaoUsuario.objects.create(
        usuario=usuario,
        acao=acao,
        loja=loja,
        produto=produto,
        detalhes=detalhes
    )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"detail": "Logout realizado com sucesso."})
    except Exception as e:
        return Response({"error": "Token inválido ou expirado."}, status=400)

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
    dataid = {"id": user.id}
    data = {"email": user.email}

    try:
        if hasattr(user, 'cliente'):
            data["cliente"] = ClienteSerializer(user.cliente, context={"request": request}).data
            dataid["cliente"] = ClienteSerializer(user.cliente, context={"resquest": request}).dataid
    except Exception as e:
        data["cliente_erro"] = f"Erro ao serializar cliente: {str(e)}"

    try:
        if hasattr(user, 'lojista'):
            data["lojista"] = LojistaSerializer(user.lojista, context={"request": request}).data
    except Exception as e:
        data["lojista_erro"] = f"Erro ao serializar lojista: {str(e)}"

    return Response(data)


class LojasRecomendadasView(APIView):
    permission_classes = [IsAuthenticated]

    
    def get(self, request):
        cliente = request.user.cliente  # ou ajuste conforme sua relação
        categorias = cliente.categorias_desejadas.all()
        lojas = Loja.objects.annotate(
            nota_media=Avg('avaliacoes_recebidas__nota')
        ).filter(categorias__in=categorias).distinct()
        serializer = LojaSerializer(lojas, many=True, context={"request": request})
        return Response(serializer.data)
    
class ProdutosRecomendadosView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cliente = request.user.cliente  # ou ajuste conforme sua relação
        categorias = cliente.categorias_desejadas.all()
        produtos = Produto.objects.filter(categorias__in=categorias).distinct()
        serializer = ProdutoSerializer(produtos, many=True, context={"request": request})
        return Response(serializer.data)
    

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
    
    @action(detail=True, methods=['get'])
    def loja(self, request, pk=None):
        lojista = self.get_object()
        lojas = Loja.objects.get(lojista=lojista)  # Aqui usamos filter
        serializer = LojaSerializer(lojas, many=False, context={'request': request})
        return Response(serializer.data)

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
    

    @action(detail=True, methods=['get', 'delete'], url_path='produtos_favoritos(?:/(?P<id_produto>\d+))?')
    def produtos_favoritos(self, request, pk=None, id_produto=None):
        cliente = self.get_object()

        if request.method == 'GET':
            if id_produto:
                try:
                    produto = cliente.produtos_favoritos.get(id=id_produto)
                except Produto.DoesNotExist:
                    return Response({"detail": "Produto não encontrado entre os favoritos."}, status=status.HTTP_404_NOT_FOUND)
                serializer = ProdutoSerializer(produto, context={'request': request})
                return Response(serializer.data)

            produtos = cliente.produtos_favoritos.all()
            serializer = ProdutoSerializer(produtos, many=True, context={'request': request})
            return Response(serializer.data)

        elif request.method == 'DELETE':
            if not id_produto:
                return Response({"detail": "É necessário informar o ID do produto para remover."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                produto = Produto.objects.get(id=id_produto)
            except Produto.DoesNotExist:
                return Response({"detail": "Produto não encontrado."}, status=status.HTTP_404_NOT_FOUND)

            cliente.produtos_favoritos.remove(produto)
            return Response({"detail": "Produto removido dos favoritos."}, status=status.HTTP_204_NO_CONTENT)


    @action(detail=True, methods=['get', 'delete'], url_path='lojas_favoritas(?:/(?P<id_loja>\d+))?')
    def lojas_favoritas(self, request, pk=None, id_loja=None):
        cliente = self.get_object()

        if request.method == 'GET':
            if id_loja:
                try:
                    loja = cliente.lojas_favoritas.get(id=id_loja)
                except Loja.DoesNotExist:
                    return Response({"detail": "Loja não encontrada entre os favoritos."}, status=status.HTTP_404_NOT_FOUND)
                serializer = LojaSerializer(loja, context={'request': request})
                return Response(serializer.data)

            lojas = cliente.lojas_favoritas.all()
            serializer = LojaSerializer(lojas, many=True, context={'request': request})
            return Response(serializer.data)

        elif request.method == 'DELETE':
            if not id_loja:
                return Response({"detail": "É necessário informar o ID da loja para remover."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                loja = Loja.objects.get(id=id_loja)
            except Loja.DoesNotExist:
                return Response({"detail": "Loja não encontrado."}, status=status.HTTP_404_NOT_FOUND)

            cliente.lojas_favoritas.remove(loja)
            return Response({"detail": "Loja removido dos favoritos."}, status=status.HTTP_204_NO_CONTENT)
    
class AcaoUsuarioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AcaoUsuario.objects.all().order_by('-timestamp')
    serializer_class = AcaoUsuarioSerializer
    permission_classes = [IsAuthenticated]  # ou alguma permissão mais específica

    @action(detail=True, methods=['get'])
    def lojas(self, request, pk=None):
        acao = self.get_object()
        lojas = acao.lojas.all()
        serializer = CategoriaSerializer(categorias_desejadas, many=True)
        return Response(serializer.data)

class PesquisaView(APIView):
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
    
    def get(self, request):
        termo = request.query_params.get('nome', '')

        # Lojas que têm no nome OU têm produtos com esse nome
        lojas = Loja.objects.annotate(
            nota_media=Avg('avaliacoes_recebidas__nota')
        ).filter(
            nome__icontains=termo
        ).distinct()

        # Produtos individualmente que batem com o nome
        produtos = Produto.objects.filter(nome__icontains=termo)

        # Serializa tudo
        lojas_serializadas = PesquisaSerializer(lojas, many=True, context={'request': request})
        produtos_serializados = ProdutoSerializer(produtos, many=True, context={'request': request})

        return Response({
            'lojas': lojas_serializadas.data,
            'produtos': produtos_serializados.data
        })

    

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

    @action(detail=True, methods=['get'])
    def avaliacoes(self, request, pk=None):
        avaliacoes = Avaliacao.objects.filter(loja_id=pk)
        serializer = AvaliacaoSerializer(avaliacoes, many=True)
        return Response(serializer.data)

    # # ACTION PARA PAGINAÇÃO
    # @action(detail=True, methods=['get'])
    # def avaliacoes(self, request, pk=None):
    #     self.pagination_class.page_size = 1  # Paginação: 1 por página
    #     avaliacoes = Avaliacao.objects.filter(loja_id=pk)
    #     page = self.paginate_queryset(avaliacoes)
    #     if page is not None:
    #         serializer = AvaliacaoSerializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #     serializer = AvaliacaoSerializer(avaliacoes.all(), many=True)
    #     return Response(serializer.data)
    
    # ACTION PARA ENDPOINT /lojas/1/produtos
    @action(detail=True, methods=['get'])
    def produtos(self, request, pk=None):
        loja = self.get_object()
        serializer = ProdutoSerializer(loja.produtos.all(), many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def categorias(self, request, pk=None):
        loja = self.get_object()
        categorias = loja.categorias.all()
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def acoes(self, request, pk=None):
        acoes = AcaoUsuario.objects.filter(loja_id=pk)
        serializer = AcaoUsuarioSerializer(acoes, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def favoritas(self, request, pk=None):
        favoritos = LojaFavorita.objects.filter(loja_id=pk)
        serializer = LojaFavoritaSerializer(favoritos, many=True)
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
    
    @action(detail=True, methods=['get'])
    def favoritos(self, request, pk=None):
        favoritos = ProdutoFavorito.objects.filter(produto_id=pk)
        serializer = ProdutoFavoritoSerializer(favoritos, many=True)
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

