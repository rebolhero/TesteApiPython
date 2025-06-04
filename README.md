# ToDo API
API com funcionalidades de CRUD para gerenciar tarefas.


## Tecnologias
- Python 3.10
- FastAPI
- SQLite
- SQLAlchemy
- Docker

Foi utilizado o banco SQLite pela praticidade de implantacao por se tratar de uma API simples.

## Como executar

Para excutar o projeto e subir a imagem rodar o comando:
    docker-compose up --build

Após executar o projeto, para ter acesso a documentação no swagger e testar os endpoints da api acessar a url:
    http://localhost:8000/docs

Para entrar no conteiner e executar os testes unitarios, rodar o comando no terminal:
    docker exec -it testeapipython-todo-api-1 bash

E depois de entrar no container, colocar o comando a seguir para rodar os testes unitarios:
    pytest --cov=app --cov-report=html tests/

Para ter acesso a porcentagem de coverage do codigo, acessar o arquivo index.html dentro da pasta htmlcov/
