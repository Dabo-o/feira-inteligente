from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import (
    AvaliacaoViewSet, LojaViewSet, ProdutoViewSet, CategoriaViewSet,
    LojistaViewSet, ClienteViewSet, ProdutoFavoritoViewSet, LojaFavoritaViewSet,
    SetorViewSet, TotemPessoalViewSet, TotemPesquisaViewSet
)

router = SimpleRouter()
router.register('lojas', LojaViewSet)
router.register('avaliacoes', AvaliacaoViewSet)
router.register('categorias', CategoriaViewSet)
router.register('produtos', ProdutoViewSet)
router.register('lojistas', LojistaViewSet)
router.register('clientes', ClienteViewSet)
router.register('produtos-favoritos', ProdutoFavoritoViewSet)
router.register('lojas-favoritas', LojaFavoritaViewSet)
router.register('setores', SetorViewSet)
router.register('totens-pessoais', TotemPessoalViewSet)
router.register('totens-pesquisa', TotemPesquisaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
