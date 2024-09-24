# nao-ai-server

Um servidor simples para auxiliar os Robôs NAO da Linha 3 do CETEC a acessarem funcionalidades de IA.

# Rodando o projeto usando o Docker:

Primeiro, copie as variavéis de ambiente com os comandos abaixo:

```bash
cp backend/default.env .env
```

Eles serão usadas pelo `docker-compose`. Novas variavéis devem ser adicinadas aqui.

Em seguida monte as imagens e rode os containers:

```bash
$ docker-compose build
$ docker-compose up -d
```

A API vai poder ser acessada na porta 8000 por padrão.
http://localhost:8000/

Para auxiliar na documentação da API temos um Swagger:
http://localhost:8000/swagger/

## Backend

Para executar somente o servidor backend siga os comandos abaixo:

```bash
$ docker-compose run --rm --service-ports backend
```

Para rodar os testes:

```bash
$ docker-compose run --rm backend pytest . -s --cov
```

# Contribuições

Para contribuir instalar o pre-commit com as configurações do projeto.

```bash
$ pre-commit install && pre-commit install --hook-type commit-msg
```
