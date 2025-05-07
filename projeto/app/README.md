# 📘 Documentação da API

Bem-vindo à documentação da API!  
Abaixo estão descritos os endpoints disponíveis até o momento.  
O endereço base para todas as rotas é:

http://<seu_ip>:8000/api


> Obs: O `<seu_ip>` foi omitido por fins didáticos.

---

## 🏬 LOJAS

### `GET /lojas`  
Retorna todas as lojas cadastradas.

### `POST /lojas`  
Cadastra uma nova loja.

### `GET /lojas/?nome=<nome_da_loja>`  
Busca lojas por nome (busca parcial permitida).

### `GET /lojas/<id>`  
Retorna os dados de uma loja específica.

### `PUT /lojas/<id>`  
Atualiza os dados de uma loja.

### `DELETE /lojas/<id>`  
Remove uma loja.

### `GET /lojas/<id>/avaliacoes`  
Retorna todas as avaliações da loja.

### `GET /lojas/<id>/produtos`  
Retorna todos os produtos da loja.

### `GET /lojas/<id>/categorias`  
Retorna todas as categorias da loja.

> ℹ️ O campo `nota_media` de uma loja é calculado automaticamente com base nas avaliações.

---

## 🌟 AVALIAÇÕES

### `GET /avaliacoes`  
Retorna todas as avaliações.

### `POST /avaliacoes`  
Cadastra uma nova avaliação.

### `GET /avaliacoes/<id>`  
Retorna uma avaliação específica.

### `PUT /avaliacoes/<id>`  
Atualiza uma avaliação.

### `DELETE /avaliacoes/<id>`  
Remove uma avaliação.

---

## 🗂️ CATEGORIAS

### `GET /categorias`  
Retorna todas as categorias.

### `POST /categorias`  
Cadastra uma nova categoria.

### `GET /categorias/?nome=<nome_da_categoria>`  
Busca categorias por nome (busca parcial permitida).

### `GET /categorias/<id>`  
Retorna uma categoria específica.

### `PUT /categorias/<id>`  
Atualiza uma categoria.

### `DELETE /categorias/<id>`  
Remove uma categoria.

### `GET /categorias/<id>/lojas`  
Retorna as lojas pertencentes à categoria.

### `GET /categorias/<id>/setores`  
Retorna os setores relacionados à categoria.

---

## 📦 PRODUTOS

### `GET /produtos`  
Retorna todos os produtos.

### `POST /produtos`  
Cadastra um novo produto.

### `GET /produtos/?nome=<nome_do_produto>`  
Busca produtos por nome (busca parcial permitida).

### `GET /produtos/<id>`  
Retorna um produto específico.

### `PUT /produtos/<id>`  
Atualiza um produto.

### `DELETE /produtos/<id>`  
Remove um produto.

### `GET /produtos/<id>/lojas`  
Retorna lojas onde o produto está disponível.

### `GET /produtos/<id>/categoria`  
Retorna categorias associadas ao produto.

---

## 👨‍💼 LOJISTAS

### `GET /lojistas`  
Retorna todos os lojistas cadastrados.

### `POST /lojistas`  
Cadastra um novo lojista.

### `GET /lojistas/?nome=<nome_do_lojista>`  
Busca lojistas por nome (busca parcial permitida).

### `GET /lojistas/<id>`  
Retorna um lojista específico.

### `PUT /lojistas/<id>`  
Atualiza um lojista.

### `DELETE /lojistas/<id>`  
Remove um lojista.

---

## 👥 CLIENTES

### `GET /clientes`  
Retorna todos os clientes cadastrados.

### `POST /clientes`  
Cadastra um novo cliente.

### `GET /clientes/?nome=<nome_do_cliente>`  
Busca clientes por nome (busca parcial permitida).

### `GET /clientes/<id>`  
Retorna um cliente específico.

### `PUT /clientes/<id>`  
Atualiza um cliente.

### `DELETE /clientes/<id>`  
Remove um cliente.

### `GET /clientes/<id>/categorias_desejadas`  
Retorna as categorias favoritas do cliente.

### `GET /clientes/<id>/produtos_favoritos`  
Retorna os produtos favoritos do cliente.

### `GET /clientes/<id>/lojas_favoritas`  
Retorna as lojas favoritas do cliente.

---

## ❤️ PRODUTOS FAVORITOS

### `GET /produtos_favoritos`  
Retorna todos os registros de produtos favoritos.

### `POST /produtos_favoritos`  
Adiciona um novo produto favorito.

### `GET /produtos_favoritos/<id>`  
Retorna um registro específico.

### `PUT /produtos_favoritos/<id>`  
Atualiza um registro.

### `DELETE /produtos_favoritos/<id>`  
Remove um registro.

---

## ⭐ LOJAS FAVORITAS

### `GET /lojas_favoritas`  
Retorna todos os registros de lojas favoritas.

### `POST /lojas_favoritas`  
Adiciona uma nova loja favorita.

### `GET /lojas_favoritas/<id>`  
Retorna um registro específico.

### `PUT /lojas_favoritas/<id>`  
Atualiza um registro.

### `DELETE /lojas_favoritas/<id>`  
Remove um registro.

---

## 🏢 SETORES

### `GET /setores`  
Retorna todos os setores.

### `POST /setores`  
Cadastra um novo setor.

### `GET /setores/?nome=<nome_do_setor>`  
Busca setores por nome (busca parcial permitida).

### `GET /setores/<id>`  
Retorna um setor específico.

### `PUT /setores/<id>`  
Atualiza um setor.

### `DELETE /setores/<id>`  
Remove um setor.

### `GET /setores/<id>/lojas`  
Retorna lojas pertencentes ao setor.

### `GET /setores/<id>/categoria`  
Retorna categorias associadas ao setor.

---

## 🖥️ TOTENS

### `GET /totens`  
Retorna todos os registros de totens.

### `POST /totens`  
Cadastra um novo totem.

### `GET /totens/<id>`  
Retorna um totem específico.

### `PUT /totens/<id>`  
Atualiza um totem.

### `DELETE /totens/<id>`  
Remove um totem.

---

## ✅ Observações Finais

- Todos os retornos são em formato JSON.  
- Campos como `nota_media` são calculados automaticamente.  
- A maioria dos endpoints permite apenas operações básicas (GET, POST, PUT, DELETE), sem autenticação documentada neste momento.

---

