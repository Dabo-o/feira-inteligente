from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import (
    AvaliacaoViewSet, LojaViewSet, ProdutoViewSet, CategoriaViewSet, AcaoUsuarioViewSet, logout,
    LojistaViewSet, ClienteViewSet, ProdutoFavoritoViewSet, LojaFavoritaViewSet, PesquisaView,
    SetorViewSet, TotemPessoalViewSet, RegisterView, meu_perfil, MapaViewSet, CriarLojistaView,
    LojasRecomendadasView, ProdutosRecomendadosView
)

router = SimpleRouter()
router.register('lojas', LojaViewSet, basename='lojas')
router.register('avaliacoes', AvaliacaoViewSet)
router.register('categorias', CategoriaViewSet) 
router.register('produtos', ProdutoViewSet)
router.register('lojistas', LojistaViewSet)
router.register('clientes', ClienteViewSet)
router.register('produtos_favoritos', ProdutoFavoritoViewSet)
router.register('lojas_favoritas', LojaFavoritaViewSet)
router.register('setores', SetorViewSet)
router.register('totens', TotemPessoalViewSet)
router.register('mapa', MapaViewSet)
router.register(r'acoes', AcaoUsuarioViewSet, basename='acao')



urlpatterns = [
    path("logout/", logout, name="logout"),
    path('register/', RegisterView.as_view(), name='register'),
    path('lojas-recomendadas/', LojasRecomendadasView.as_view(), name='recomendadas'),
    path('produtos-recomendados/', ProdutosRecomendadosView.as_view(), name='recomendados'),
    path('pesquisa/', PesquisaView.as_view(), name='pesquisa'),
    path('criar-lojista/', CriarLojistaView.as_view(), name='criar-lojista'),
    path('meu-perfil/', meu_perfil),

    path('', include(router.urls)),
]
