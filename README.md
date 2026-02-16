# Sistema de Vacinação de Pets API

Uma API REST para gerenciar registros de vacinação de pets, usando Django.

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/django-4.2-green.svg)
![DRF](https://img.shields.io/badge/DRF-3.14-red.svg)

## Tabela de Conteúdos

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
  - [Local Setup](#local-setup)
  - [Docker Setup](#docker-setup)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Technical Decisions](#technical-decisions)
- [Contributing](#contributing)

---

## Overview

Este sistema permite o acompanhamento do histórico de vacinação, gerenciamento dos registros dos pets e monitoremento dos próximos agendamentos de vacinas.
A API fornece operações completas de CRUD para pets, vacinas e registros de vacinação, com autenticação e autorização.

- **Gerenciamento de Pets**: Cadastre e acompanhe pets com informações detalhadas
- **Base de Dados de Vacinas**: Mantenha um catálogo de vacinas disponíveis
- **Registros de Vacinação**: Registre e acompanhe todas as vacinas administradas
- **Contas de Tutores**: Contas de usuário seguras com controle de acesso baseado em propriedade
- **Agendamento Automático**: Cálculo automático das datas das próximas doses
- **Lembretes**: Acompanhe vacinas a vencer e vencidas

---


## Technologias

### Backend
- **Python 3.10.12**
- **Django 4.2** 
- **Django REST Framework 3.14**
- **SQLite**

### Bibliotecas Adicionais
- **python-decouple** - Gerenciamento de variáveis de ambiente
- **python-dateutil** - Cálculos de datas

## Sugestões
- **curl** para testar os endpoints manualmente
- **jq"** para facilitar o teste  com curl
---

## Instalação

### Prerequisitos
- Python 3.10 ou mais
- pip
- Git

### Setup Local

#### 1. Clone o repositório
```bash
git clone https://github.com/pedrowsxz/django_sistema_vacinacao_api
cd django_sistema_vacinacao_api
```

#### 2. Virtual Environment (venv)
```bash
# Sete o virtual environment
python -m venv venv

# Ative o virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

#### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

#### 4. Configuração do Ambiente

Adicione o arquivo `.env` na raiz do projeto a partir do exemplo no repositório:
```bash
cp .env.example .env
```

Edite `.env` com a sua configuração:
```env
SECRET_KEY=sua-chave
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_ENGINE=django.db.backends.sqlite3
DATABASE_NAME=db.sqlite3
```

#### 5. Setup da Database
```bash
# Run migrations
python manage.py migrate

# Superuser (conta admin)
python manage.py createsuperuser
```

#### 6. Executar o Servidor
```bash
python manage.py runserver
```

A API estará disponível em `http://127.0.0.1:8000/`

- **API Root**: http://127.0.0.1:8000/api/
- **Admin Panel**: http://127.0.0.1:8000/admin/

---

## Documentação da API

###  URL base
```
http://127.0.0.1:8000/api/
```

### Authenticação

Todos os endpoints (exceto cadastro e login) exigem autenticação usando Token Authentication.

**Formato do Header:**
```
Authorization: Token <seu-token>
```

---

### Exemplo de flow com os endpoints de Authenticação
Para isso pode ser usado o curl, ou outra ferramenta de teste de API como Insomnia ou Postman.