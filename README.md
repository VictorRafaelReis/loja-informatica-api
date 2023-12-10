# Projeto Loja de Informática - API:
  Este projeto foi desenvolvido com o intuito de ser um dos métodos de avaliação para a disciplina de desenvolvimento full-stack básico da pós graduação da PUC-Rio.
  Ele consiste em um sistema de gerenciamento de uma loja que venda produtos de informática e afins. Assim, permitindo a gestão de clientes, produtos e vendas.

# Instalação e Configuração:
  Para que esta API funcione será necessário a realização dos seguintes procedimentos.

  1 - será necessário clonar este repositório, para que tenha acesso aos seus arquivos e pastas.
  
    1.1 - git clone https://github.com/VictorRafaelReis/loja-informatica-api.git

  2 - uma vez clonado o repositório, execute os seguintes comandos no terminal para conseguir rodar o projeto.
      
      2.1 - Criar um ambiente virtual na raiz do projeto com o comando "python -m venv venv"
      
      2.2 - entrar no ambiente virtual com o comando "venv\Scripts\Activate"

      2.3 - instalar os requirements.txt do projetos dentro do ambiente virtual, utilizar o comando "pip install -r requirements.txt"

      2.4 - uma vez concluidas as etapas acima o projeto já está pronto para ser executado com o comando "flask run --host 0.0.0.0 --port 5000"

# Funcionalidades e Execução do Projeto:
  O projeto dispõe de 3 áreas diferentes. A área de Clientes, Produtos e Vendas.

  # Clientes:
    Ao entrar na área de Clientes, que pode ser acessada clicando no item "Clientes", no menu localizado a baixo do título 
    da página em azul.
    Caso exista algum cliente cadastrado no banco de dados, e que esteja sendo recebido via API, ele será exibido em forma 
    de tabela ao centro da tela,
    contendo seus dados: nome, telefone, email e cpf.

    Nessa mesma tabela contendo os clientes, existe o campo opções, contendo os botões "Editar" e "Excluir". Caso o botão
    "Editar" seja pressionado, será aberta a tela de edição contendo os dados do seu respectivo cliente, nessa área de 
    edição, o usuário pode optar por todos ou qual campo deseja modificar deste cliente, após realizadas as modificações 
    é necessário o clique no botão "Salvar", localizado no canto inferior direito desta mesma área de edição.
    Caso não deseje modificar nenhum campo do cliente, basta apenas pressionar o botão "Fechar", localizado ao lado 
    do botão salvar, ou no "X", localizado no canto superior direito da tela de edição.

    Caso o botão "Excluir" seja pressionado, será exibido um alerta pedindo a confirmação de exclusão do cliente que,
    caso confirmado, será deletado do banco de dados, e não será mais exibido na lista.

    Por fim, existe também o botão "Adicionar Cliente", localizado no canto direito abaixo do menu. Ao ser pressionado,
    será exibida a área de adição de cliente, contendo os campos nome, que espera receber valores de texto, o campo de
    telefone, que espera receber valores numéricos, o campo email, que espera receber valores de texto e por fim,
    o campo cpf, que espera receber valores numéricos. Após preenchidos os campos o usuário deverá clicar no botão 
    "Salvar", localizado no canto inferior direito da área de adição. Após adicionado o cliente, o novo cliente será 
    exibido na lista de clientes.

  # Produtos:
    A área de Produtos possue a mesma lógica de funcionamento que a de cliente. A única diferença são nos campos exibidos
    na tabela e nos formulários de adição de novo produto ou atualização de um produto já existente. Que são os seguintes:
    nome, categoria, quantidade e valor unitário. Nos campos de adição de novo produto, ou atualização de produto os 
    campos nome, categoria, quantidade e valor, esperam receber, respectivamente, valores de texto e numéricos. 
    Com ressalva no campo categoria da adição de um novo produto, onde o usuário deverá selecionar dentre alguma das 
    categorias já existentes.

  # Vendas:
    A área de vendas, assim como as áreas de clientes e produtos, também possue uma lista contendo todas as vendas realizadas,
    com os campos: ID da venda, produto, cliente, quantidade e valor. Porém nas opções da lista só existe o botão "Excluir".

    Quanto a adição de uma nova venda. A mesma só poderá ser realizada caso exista algum produto ou cliente, previamente 
    cadastrado no sistema. Ao clicar no botão "Adicionar Venda", o usuário deverá selecionar o produto a que a venda se refere,
    o cliente que estará realizando a compra e a quantidade de itens comprados nesta venda. Ao clicar em "Salvar", será
    exibida uma mensagem informando o valor total da venda, e se deseja realizar a mesma. Caso confirmada a venda será realizada
    e exibida na lista de vendas. E o produto relacionado aquela venda tera a sua quantidade em estoque reduzida pelo valor da 
    quantidade da venda. Caso algum produto esteja com quantidade 0 em estoque, ele não será exibido no select produto na área 
    de adição de uma nova venda.

# Estrutura:
  
  # app.py:
    Nesse arquivo são definidas as rotas da aplicação, levando até seus end points.

  # model:
    na pasta model são definidas as configurações do banco de dados, e a criação das classes que serão mapeadas para tabelas no banco

  # schemas:
    na pasta esquema são definidos as formas padrões para adição, busca, apresentação e delete que serão utilizadas pelos modelos
      
# Utilizações da API:
  Após configurada e compreendida, a API pode ser utilizada acessando diretamente a url que será gerada pelo comando
  "flask run --host 0.0.0.0 --port 5000", nesse caso a url "http://127.0.0.1:5000".
  E nessa url, pode ser acessado o swagger que gera a documentação do sistema e permite a execução dos end-points da API.

  Ou ainda, com a API executando, pode ser feita a integração com o front-end desse sistema, como demonstrado no seguinte link:
  https://github.com/VictorRafaelReis/loja-informatica-front
