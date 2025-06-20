from django.db import models
from django.contrib.auth.models import User

class Base(models.Model):
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        abstract = True

class AcaoUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    acao = models.CharField(max_length=100)  # ex: "entrou na loja", "visualizou produto"
    timestamp = models.DateTimeField(auto_now_add=True)
    loja = models.ForeignKey('Loja', null=True, blank=True, on_delete=models.SET_NULL)
    produto = models.ForeignKey('Produto', null=True, blank=True, on_delete=models.SET_NULL)
    detalhes = models.TextField(blank=True)  # opcional, para info adicional (ex: navegador, IP)

    def __str__(self):
        return f'{self.usuario} fez {self.acao} em {self.timestamp}'

class Lojista(Base):
    nome = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20)
    cnpj = models.CharField(max_length=20)
    foto = models.ImageField(upload_to='lojistas/', blank=True, null=True)
    genero = models.CharField(max_length=50, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
       return self.user.username

class TotemPessoal(Base):
    TIPO_USUARIO_CHOICES = [
        ('Turista', 'Turista'),
        ('Local', 'Local'),
        ('Comerciante', 'Comerciante'),
    ]
    FAIXA_ETARIA_CHOICES = [
        ('18-', '18-'),
        ('18-25', '18-25'),
        ('26-35', '26-35'),
        ('36-45', '36-45'),
        ('46-55', '46-55'),
        ('56-65', '56-65'),
        ('65+', '65+'),
    ]
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_CHOICES)
    faixa_etaria = models.CharField(max_length=10, choices=FAIXA_ETARIA_CHOICES)
    genero = models.CharField(max_length=50)
    categoria = models.ForeignKey('Categoria', on_delete=models.SET_NULL, null=True, related_name='pesquisas_totem')

    def __str__(self):
        return f'{self.tipo_usuario} - {self.faixa_etaria}'

class Categoria(Base):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

class Setor(Base):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

class Cliente(Base):
    TIPO_CHOICES = [
        ('Turista', 'Turista'),
        ('Local', 'Local'),
        ('Comerciante', 'Comerciante'),
    ]
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=15)
    telefone = models.CharField(max_length=20)
    foto = models.ImageField(upload_to='clientes/', blank=True, null=True)
    data_nascimento = models.CharField(max_length=20, blank=True, null=True)
    genero = models.CharField(max_length=50)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)    
    categorias_desejadas = models.ManyToManyField(Categoria, related_name='clientes', blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cliente')
    
    produtos_favoritos = models.ManyToManyField(
        'Produto',
        through='ProdutoFavorito',
        related_name='clientes_que_favoritaram',
        related_query_name='cliente_que_favoritou'
    )
    lojas_favoritas = models.ManyToManyField(
        'Loja',
        through='LojaFavorita',
        related_name='clientes_que_favoritaram',
        related_query_name='cliente_que_favoritou'
    )

    def __str__(self):
        return self.nome
    
class Mapas(Base):
    loja = models.ForeignKey('Loja', on_delete=models.SET_NULL, null=True, related_name='mapas_lojas')
    mapa = models.ImageField(upload_to='produtos/', blank=True, null=True)

    
class Produto(Base):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)
    loja = models.ForeignKey('Loja', on_delete=models.CASCADE, related_name='produtos')
    categorias = models.ManyToManyField(Categoria, related_name="produtos")
    cor = models.CharField(max_length=50)
    composicao = models.TextField()

    def __str__(self):
        return self.nome

class Loja(Base):
    nome = models.CharField(max_length=255,blank=True, null=True)
    banner = models.ImageField(upload_to='lojas/banners/', blank=True, null=True)
    logo = models.ImageField(upload_to='lojas/logos/', blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE,null = True, related_name="lojas")
    categorias = models.ManyToManyField(Categoria, related_name="lojas")
    localizacao = models.CharField(max_length=255, blank=True, null=True)
    lojista = models.ForeignKey(Lojista, on_delete=models.CASCADE, related_name='lojas')
    foto_da_loja = models.ImageField(upload_to='lojas/fotos/', blank=True, null=True)
    Instagram = models.TextField(blank=True, null=True)
    WhatsApp = models.TextField(blank=True, null=True)
    Website = models.TextField(blank=True, null=True)
    horario_funcionamento = models.CharField(max_length=255,blank=True, null=True)
    avaliacoes = models.ManyToManyField('Avaliacao', related_name='lojas', blank=True)
    nota = models.FloatField(default=0)

    def __str__(self):
        return self.nome

class Avaliacao(Base):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='avaliacoes')
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE, related_name='avaliacoes_recebidas')
    nota = models.FloatField()
    comentario = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.cliente.nome} avaliou {self.loja.nome}'

class ProdutoFavorito(Base):
    cliente = models.ForeignKey(
        'Cliente',
        on_delete=models.CASCADE,
        related_name='produto_favorito_rel',
        related_query_name='produto_favorito'
    )
    produto = models.ForeignKey(
        'Produto',
        on_delete=models.CASCADE,
        related_name='cliente_favorito_rel',
        related_query_name='cliente_favorito'
    )

    def __str__(self):
        return f'{self.cliente.nome} favoritou {self.produto.nome}'

class LojaFavorita(Base):
    cliente = models.ForeignKey(
        'Cliente',
        on_delete=models.CASCADE,
        related_name='loja_favorita_rel',
        related_query_name='loja_favorita'
    )
    loja = models.ForeignKey(
        'Loja',
        on_delete=models.CASCADE,
        related_name='cliente_favorita_rel',
        related_query_name='cliente_favorita'
    )

    def __str__(self):
        return f'{self.cliente.nome} favoritou {self.loja.nome}'

