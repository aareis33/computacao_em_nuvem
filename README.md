# Mural de Recados

Aplicação web simples em **Python (Flask)** com banco **PostgreSQL**, totalmente containerizada com Docker Compose.
Um formulário grava recados no banco e a página lista todos os recados enviados.

## Pré-requisitos

- Docker
- Docker Compose (plugin `docker compose`)
- Git

## Como subir o ambiente

```bash
git clone <url-do-repositorio>
cd <pasta-do-repositorio>
cp .env.example .env
docker compose up -d --build
```

## Como acessar

Abra no navegador: http://localhost:8000

(a porta pode ser alterada em `APP_PORT` no arquivo `.env`)

## Comandos úteis

```bash
docker compose ps            # situação dos serviços
docker compose logs -f app   # logs da aplicação
docker compose down          # encerra e MANTÉM os dados (volume)
docker compose down -v       # encerra e APAGA os dados
```

## Estrutura

```
app/                 código Flask, Dockerfile e .dockerignore
docker-compose.yml   serviços: app e db (volume nomeado + healthcheck)
.env.example         modelo das variáveis de ambiente
```

## Autores

- Alexandre 
- guilherme
