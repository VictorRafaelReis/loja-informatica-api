from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Produto, Cliente, Venda
from logger import logger
from schemas import *
from flask_cors import CORS


info = Info(title = "Minha API - Projeto", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name = "Documentação", description="Seleção de documentação: Swagger, Redoc ou Rapidoc")
produto_tag = Tag(name="Produto", description="Adição, visualização e remoção de produtos à base de dados")
cliente_tag = Tag(name="Cliente", description="Adição, visualização e remoção de clientes à base de dados")
venda_tag = Tag(name="Venda", description="Adição, visualização e remoção de vendas à base de dados")


@app.get('/', tags=[home_tag])
def home():
    """
    Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

"""
---------------------------
PRODUTOS
---------------------------
"""
@app.post('/produto', tags=[produto_tag],
          responses={"200": ProdutoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_produto(form: ProdutoSchema):
    """
    Adiciona um novo produto à base de dados

    Retorna uma representação dos produtos.
    """
    produto = Produto(
        nome = form.nome,
        categoria = form.categoria,
        quantidade = form.quantidade,
        valor = form.valor
    )
    logger.debug(f"Adicionando produto de nome: '{produto.nome}'")
    try:
        # Criando conexão com a base
        session = Session()
        # Adicionando produto
        session.add(produto)
        # Efetivando o comando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionando produto de nome: '{produto.nome}'")
        return apresenta_produto(produto), 200
    
    except IntegrityError as e:
        # Como a duplicidade do nome é a razão do IntegrityError
        error_msg = "Produto de mesmo nome já existe na base"
        logger.warning(f"Erro ao adicionar produto '{produto.nome}', {error_msg}")
        return {"message": error_msg}, 409
    
    except Exception as e:
        # Caso um erro fora do previsto venha a ocorrer
        error_msg = "Não foi possível salvar o novo item"
        logger.warning(f"Erro ao adicionar produto '{produto.nome}', {error_msg}")
        return {"message": error_msg}, 400
    

@app.get('/produtos', tags=[produto_tag],
         responses={"200": ListagemProdutosSchema, "404": ErrorSchema})
def get_produtos():
    """
    Faz a busca por todos os produtos cadastrados

    Retorna uma apresentação da listagem dos produtos.
    """
    logger.debug(f"Coletando Produtos ")
    # Criando conexão com a base
    session = Session()
    # Fazendo a busca
    produtos = session.query(Produto).all()

    if not produtos:
        # Se não há produtos cadastrados
        return {"produtos": []}, 200
    else:
        logger.debug(f"%d produtos encontrados" %len(produtos))
        #retorna a representação de produto
        #print(produtos)
        return apresenta_produtos(produtos), 200
    

@app.get('/produto', tags=[produto_tag],
         responses={"200": ProdutoViewSchema, "404": ErrorSchema})
def get_produto(query: ProdutoBuscaSchema):
    """
    Faz a busca por um produto a partir do seu nome

    Retorna uma representação do produto.
    """
    produto_nome = unquote(unquote(query.nome))
    logger.debug(f"Coletando dados sobre o produto #{produto_nome}")
    # Criando conexão com a base de dados
    session = Session()
    # Fazendo a busca
    produto = session.query(Produto).filter(Produto.nome == produto_nome).first()

    if not produto:
        # Se o produto não foi encontrado
        error_msg = "Produto não econtrado na base"
        logger.warning(f"Erro ao buscar produto '{produto_nome}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Produto encontrado: '{produto.nome}'")
        # Retorna a representação desse produto
        return apresenta_produto(produto), 200
    

@app.get('/produto_por_id', tags=[produto_tag], 
         responses={"200": ProdutoViewSchema, "404": ErrorSchema})
def get_produto_por_id(query: ProdutoBuscaPorIdSchema):
    """
    Faz a busca por um produto a partir do seu id

    Retorna uma representação do produto.
    """
    produto_id = query.id
    logger.debug(f"Coletando dados sobre o produto #{produto_id}")
    # Criando conexão com a base de dados
    session = Session()
    # Fazendo a busca
    produto = session.query(Produto).filter(Produto.id == produto_id).first()
    
    if not produto:
        # Se o produto não for encontrado
        error_msg = "Produto não econtrado na base"
        logger.warning(f"Erro ao buscar produto '{produto_id}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Produto encontrado: '{produto.nome}'")
        # Retorna a representação desse produto
        return apresenta_produto(produto), 200


@app.put('/update_produto', tags=[produto_tag],
         responses= {"200":ProdutoViewSchema, "404": ErrorSchema})
def update_produto(query: ProdutoBuscaSchema, form: ProdutoSchema):
    """
    Atualiza um produto a partir do nome do produto informado

    Retorna uma representação do produto
    """
    produto_nome = unquote(unquote(query.nome))
    logger.debug(f"Coletando dados sobre o produto #{produto_nome} para realizar sua atualização")
    session = Session()

    produto_para_update = session.query(Produto).filter(Produto.nome == produto_nome).first()

    if request.method == 'PUT':
        produto_para_update.nome = form.nome
        produto_para_update.categoria = form.categoria
        produto_para_update.quantidade = form.quantidade
        produto_para_update.valor = form.valor
        
        try:
            logger.debug(f"Alterando produto de nome: '{produto_nome}'")
            session.commit()
            return apresenta_produto(produto_para_update), 200
        
        except IntegrityError as e:
            # Como a duplicidade do nome é a razão do IntegrityError
            error_msg = "Produto de mesmo nome já existe na base"
            logger.warning(f"Erro ao adicionar produto '{produto_para_update.nome}', {error_msg}")
            return {"message": error_msg}, 409
        
        except Exception as e:
            # Caso ocorra algum erro fora do previsto
            error_msg = "Não foi possível alterar o produto"
            logger.warning(f"Erro ao alterar o produto '{produto_nome}', {error_msg}")
            return {"message": error_msg}, 400
    else:
        return apresenta_produto(produto_para_update) 


@app.delete('/produto', tags=[produto_tag],
            responses={"200": ProdutoDelSchema, "404": ErrorSchema})
def del_produto(query: ProdutoBuscaSchema):
    """
    Deleta um produto a partir do nome de produto informado

    Retorna uma mensagem de confirmação da remoção
    """
    produto_nome = unquote(unquote(query.nome))
    logger.debug(f"Deletando dados sobre o produto #{produto_nome}")
    # Criando conexão com a base de dados
    session = Session()
    # Fazendo a remoção
    count = session.query(Produto).filter(Produto.nome == produto_nome).delete()
    session.commit()

    if count:
        # Retorna a representação da mensagem de confirmação
        logger.debug(f"Deletando produto #{produto_nome}")
        return {"message": "Produto Removido", "id": produto_nome}
    else:
        # Se o produto não foi encontrado
        error_msg = "Produto não encontrado na base"
        logger.warning(f"Erro ao deletar produto #'{produto_nome}', {error_msg}")
        return {"message": error_msg}, 404
    

"""
-------------------------
CLIENTE
-------------------------
"""
@app.post('/cliente', tags=[cliente_tag],
          responses={"200": ClienteViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_cliente(form: ClienteSchema):
    """
    Adiciona uma novo cliente à base de dados

    Retorna uma representação dos clientes
    """
    cliente = Cliente(
        nome = form.nome,
        telefone = form.telefone,
        email = form.email,
        cpf = form.cpf
    )
    logger.debug(f"Adicionando cliente de nome: '{cliente.nome}' e cpf: '{cliente.cpf}'")
    try:
        # Criando conexão com a base
        session = Session()
        # Adicionando cliente
        session.add(cliente)
        # Efetivando o comando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionando cliente de nome: '{cliente.nome}' e cpf: '{cliente.cpf}'")
        return apresenta_cliente(cliente), 200
    
    except IntegrityError as e:
        # Duplicidade de email ou CPF
        error_msg = "Cliente com mesmo CPF já existe na base"
        logger.warning(f"Erro ao adicionar cliente '{cliente.nome}', {error_msg}")
        return {"message": error_msg}, 409
    
    except Exception as e:
        # Caso ocorra um erro fora do previsto
        error_msg = "Não foi possível salvar o novo cliente"
        logger.warning(f"Erro ao adicionar cliente '{cliente.nome}', {error_msg}")
        return {"message": error_msg}, 400
    

@app.get('/clientes', tags=[cliente_tag],
         responses={"200": ListagemClientesSchema, "404": ErrorSchema})
def get_clientes():
    """
    Faz a busca por todos os clientes cadastrados

    Retorna uma apresentação da listagem dos clientes.
    """
    logger.debug(f"Coletando Clientes")
    # Criando conexão com a base
    session = Session()
    # Fazendo a busca
    clientes = session.query(Cliente).all()

    if not clientes:
        # Se não há clientes cadastrados
        return {"clientes": []}, 200
    else:
        logger.debug(f"%d clientes encontrados" %len(clientes))
        #retorna a representação de cliente
        #print(clientes)
        return apresenta_clientes(clientes), 200
    

@app.get('/cliente', tags=[cliente_tag],
         responses={"200": ClienteViewSchema, "404": ErrorSchema})
def get_cliente(query: ClienteBuscaSchema):
    """
    Faz a busca por um cliente a partir do seu CPF

    Retorna uma representação do cliente.
    """
    cliente_cpf = unquote(unquote(query.cpf))
    logger.debug(f"Coletando dados sobre o cliente #{cliente_cpf}")
    # Criando conexão com a base de dados
    session = Session()
    # Fazendo a busca
    cliente = session.query(Cliente).filter(Cliente.cpf == cliente_cpf).first()

    if not cliente:
        # Se o cliente não foi encontrado
        error_msg = "Cliente não econtrado na base"
        logger.warning(f"Erro ao buscar cliente '{cliente_cpf}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Cliente encontrado: '{cliente.nome}'")
        # Retorna a representação desse cliente
        return apresenta_cliente(cliente), 200


"""@app.route('/cliente_por_id/<id>', methods=['GET'])
def get_cliente_por_id(id):
    
        Faz a busca por um cliente a partir do seu ID

        Retorna uma representação do cliente.
    
    logger.debug(f"coletando dados sobre o cliente de ID #{id}")
    # Criando conexão com a base de dados
    session = Session()
    # Fazendo a busca
    cliente = session.query(Cliente).filter(Cliente.id == id).first()

    if not cliente:
        # Se o produto não foi encontrado
        error_msg = "Cliente não econtrado na base"
        logger.warning(f"Erro ao buscar cliente '{id}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Cliente encontrado: '{cliente.id}'")
        # Retorna a representação desse cliente
        return apresenta_cliente(cliente), 200
"""

@app.put('/update_cliente', tags=[cliente_tag], 
         responses={"200": ClienteViewSchema, "404": ErrorSchema})
def update_cliente(query: ClienteBuscaSchema, form:ClienteSchema):
    """
    Atualiza um cliente a partir do cpf do cliente informado

    Retorna uma representação do cliente
    """
    cliente_cpf = unquote(unquote(query.cpf))
    logger.debug(f"Coletando dados sobre o cliente #{cliente_cpf} para realizar sua atualização")
    session = Session()

    cliente_para_update = session.query(Cliente).filter(Cliente.cpf == cliente_cpf).first()

    if request.method == "PUT":
        cliente_para_update.nome = form.nome
        cliente_para_update.telefone = form.telefone
        cliente_para_update.email = form.email
        cliente_para_update.cpf = form.cpf

        try:
            logger.debug(f"Alterando cliente de nome: '{cliente_para_update.nome}' e cpf: '{cliente_para_update.cpf}'")
            session.commit()
            return apresenta_cliente(cliente_para_update), 200
        
        except IntegrityError as e:
            # Como a duplicidade do cpf é a razão do IntegrityError
            error_msg = "Cliente de mesmo cpf já existe na base"
            logger.warning(f"Erro ao adicionar cliente '{cliente_para_update.nome}', {error_msg}")
            return {"message": error_msg}, 409
        
        except Exception as e:
            # Caso ocorra um erro fora do previsto
            error_msg = "Não foi possível alterar o cliente"
            logger.warning(f"Erro ao alterar cliente '{cliente_para_update.nome}', {error_msg}")
            return {"message": error_msg}, 400
    else:
        return apresenta_cliente(cliente_para_update)


@app.delete('/delete', tags=[cliente_tag], 
            responses={"200": ClienteDelSchema, "404": ErrorSchema})
def del_cliente(query: ClienteBuscaSchema):
    """
    Deleta um cliente a partir do cpf do cliente informado

    Retorna uma mensagem de confirmação da remoção
    """
    cliente_cpf = unquote(unquote(query.cpf))
    logger.debug(f"Deletando dados sobre o cliente #{cliente_cpf}")
    # Criando conexão com a base de dados
    session = Session()
    # Fazendo a remoção
    cliente_deletado = session.query(Cliente).filter(Cliente.cpf == cliente_cpf).delete()
    session.commit()

    if cliente_deletado:
        # Retorna a representação da mensagem de confirmação
        logger.debug(f"Deletando cliente #{cliente_cpf}")
        return {"message": "Cliente Removido", "cpf": cliente_cpf}, 200
    else:
        # Se o cliente não foi encontrado
        error_msg = "cliente não encontrado na base"
        logger.warning(f"Erro ao deletar cliente #'{cliente_cpf}', {error_msg}")
        return {"message": error_msg}, 404


"""
-------------------------
VENDAS
-------------------------
"""
@app.post('/venda', tags=[venda_tag],
          responses={"200": VendaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_venda(form: VendaSchema):
    """
    Adiciona uma nova venda à base de dados

    Retorna uma representação das vendas
    """
    venda = Venda(
        produto = form.produto_id,
        cliente = form.cliente_id,
        quantidade = form.quantidade,
        valor = form.valor
    )
    logger.debug(f"Adicionando venda de id: '{venda.id}' do produto: '{venda.produto}'")
    try:
        # Criando conexão com a base
        session = Session()
        # Adicionando venda
        session.add(venda)
        # Efetivando o comando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionando venda de id: '{venda.id}' do produto: '{venda.produto}'")
        return apresenta_venda(venda), 200
    
    except Exception as e:
        # Caso ocorra um erro fora do previsto
        error_msg = "Não foi possível salvar a nova venda"
        logger.warning(f"Erro ao adicionar venda '{venda.id}', {error_msg}")
        return {"message": error_msg}, 400


@app.get('/vendas', tags=[venda_tag],
         responses={"200": ListagemVendasSchema, "404": ErrorSchema})
def get_vendas():
    """
    Faz a busca por todas as vendas cadastradas

    Retorna uma apresentação da listagem das vendas.
    """
    logger.debug(f"Coletando Vendas")
    # Criando conexão com a base
    session = Session()
    # Fazendo a busca
    vendas = session.query(Venda).all()

    if not vendas:
        # Se não há vendas cadastradas
        return {"vendas": []}, 200
    else:
        logger.debug(f"%d vendas encontradas" %len(vendas))
        #retorna a representação de venda
        #print(vendas)
        return apresenta_vendas(vendas), 200
    

@app.get('/venda', tags=[venda_tag],
         responses={"200": VendaViewSchema, "404": ErrorSchema})
def get_venda(query: VendaBuscaSchema):
    """
    Faz a busca por uma venda a partir do seu ID

    Retorna uma representação da venda.
    """
    venda_id = query.id
    logger.debug(f"Coletando dados sobre a venda #{venda_id}")
    # Criando conexão com a base de dados
    session = Session()
    # Fazendo a busca
    venda = session.query(Venda).filter(Venda.id == venda_id).first()

    if not venda:
        # Se a venda não foi encontrada
        error_msg = "Venda não econtrada na base"
        logger.warning(f"Erro ao buscar venda '{venda_id}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Venda encontrada: '{venda.id}'")
        # Retorna a representação dessa venda
        return apresenta_venda(venda), 200
    

@app.get('/produto_por_id_venda', tags=[venda_tag], 
         responses={"200": VendaViewSchema, "404": ErrorSchema})
def get_produto_por_id_venda(query: VendaBuscaSchema):
    """
    Faz uma busca no produto a partir do id da venda

    Retorna uma representação do produto
    """
    venda_id = query.id
    logger.debug(f"Coletando dados sobre a venda #{venda_id}")
    # Criando conexão com a base de dados
    session = Session()
    # Fazendo a busca
    venda = session.query(Venda).filter(Venda.id == venda_id).first()
    produto = venda.produto

    if not venda:
        # Se a venda não foi encontrado
        error_msg = "Venda não econtrada na base"
        logger.warning(f"Erro ao buscar venda '{venda_id}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Produto da venda encontrado, id venda: '{venda.id}'")
        # Retorna a representação do produto dessa venda
        return apresenta_produto(produto), 200


@app.get('/cliente_por_id_venda', tags=[venda_tag], 
         responses={"200": VendaViewSchema, "404": ErrorSchema})
def get_cliente_por_id_venda(query: VendaBuscaSchema):
    """
    Faz uma busca no cliente a partir do id da venda

    Retorna uma representação do cliente
    """
    venda_id = query.id
    logger.debug(f"Coletando dados sobre a venda #{venda_id}")
    # Criando conexão com a base de dados
    session = Session()
    # Fazendo a busca
    venda = session.query(Venda).filter(Venda.id == venda_id).first()
    cliente = venda.cliente

    if not venda:
        # Se a venda não foi encontrada
        error_msg = "Venda não econtrada na base"
        logger.warning(f"Erro ao buscar venda '{venda_id}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Produto da venda encontrada, id venda: '{venda.id}'")
        # Retorna a representação do cliente dessa venda
        return apresenta_cliente(cliente), 200


@app.route('/update_quantidade_produto_pela_venda/<id>', methods=['PUT'])
def update_quantidade_produto_pela_venda(id):
    session = Session()

    produto_para_update = session.query(Produto).filter(Produto.id == id).first()

    if request.method == "PUT":
        produto_para_update.quantidade = request.form['quantidade']
        try:
            logger.debug(f"Alterando a quantidade do produto: '{produto_para_update.nome}'")
            session.commit()
            return apresenta_produto(produto_para_update), 200
        except Exception as e:
            # Caso ocorra um erro fora do previsto
            error_msg = "Não foi possível alterar a quantidade do Produto"
            logger.warning(f"Erro ao alterar quantidade do produto '{produto_para_update.nome}', {error_msg}")
            return {"message": error_msg}, 400
    else:
        return apresenta_produto(produto_para_update)
    

"""@app.route('/delete_produto_pela_venda/<id>', methods=['DELETE'])
def del_produto_pela_venda(id):
    session = Session()
    produto_deletado = session.query(Produto).filter(Produto.id == id).delete()
    session.commit()

    if produto_deletado:
        # Retorna a representação da mensagem de confirmação
        logger.debug(f"Deletando produto ID: #{id}")
        return {"message": "Produto Removido", "id": id}, 200
    else:
        # Se o produto não foi encontrado
        error_msg = "produto não encontrado na base"
        logger.warning(f"Erro ao deletar produto #'{id}', {error_msg}")
        return {"message": error_msg}, 404'
"""

@app.delete('/venda', tags=[venda_tag],
            responses={"200": VendaDelSchema, "404": ErrorSchema})
def del_venda(query: VendaBuscaSchema):
    """
    Deleta uma venda a partir do id da venda informada

    Retorna uma mensagem de confirmação da remoção
    """
    venda_id = unquote(unquote(str(query.id)))
    #print(venda_id)
    logger.debug(f"Deletando dados sobre a venda #{venda_id}")
    # Criando conexão com a base de dados
    session = Session()
    # Fazendo a remoção
    count = session.query(Venda).filter(Venda.id == venda_id).delete()
    session.commit()

    if count:
        # Retorna a representação da mensagem de confirmação
        logger.debug(f"Deletando venda #{venda_id}")
        return {"message": "venda Removida", "id": venda_id}
    else:
        # Se a venda não for encontrada
        error_msg = "venda não encontrada na base"
        logger.warning(f"Erro ao deletar venda #'{venda_id}', {error_msg}")
        return {"message": error_msg}, 404
    
