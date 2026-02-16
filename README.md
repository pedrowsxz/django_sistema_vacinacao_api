# Sistema de Vacinação de Pets API

Uma API REST para gerenciar registros de vacinação de pets, usando Django.

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/django-4.2-green.svg)
![DRF](https://img.shields.io/badge/DRF-3.14-red.svg)


## Overview

Este sistema permite o acompanhamento do histórico de vacinação, gerenciamento dos registros dos pets e monitoremento dos próximos agendamentos de vacinas.
A API fornece operações completas de CRUD para pets, vacinas e registros de vacinação, com autenticação e autorização.

- **Gerenciamento de Pets**: Cadastramento e acompanhamento de pets com informações detalhadas
- **Base de Dados de Vacinas**: Catálogo de vacinas disponíveis
- **Registros de Vacinação**: Registro e acompanhamento todas as vacinas administradas
- **Contas de Tutores**: Contas de usuário seguras com controle de acesso baseado em propriedade
- **Agendamento Automático**: Cálculo automático das datas das próximas doses
- **Lembretes**: Acompanhamento de vacinas a vencer e vencidas

---


## Technologias

### Backend
- **Python 3.10.12**
- **Django 4.2** 
- **Django REST Framework 3.14**
- **pip 26.0.1**
- **SQLite**
- **Git 2.53.0**

### Bibliotecas Adicionais
- **python-decouple** - Gerenciamento de variáveis de ambiente
- **python-dateutil** - Cálculos de datas

## Sugestões
- **curl** Ferramenta de linha de comando para fazer requisições HTTP aos endpoints da API, permitindo testar manualmente as rotas, enviar dados e verificar respostas.
- **jq"** Utilitário de linha de comando para processar e formatar JSON, tornando mais fácil a leitura e análise das respostas obtidas com curl.

---

## Instalação

### Prerequisitos
- Python
- pip
- Git

### Setup Local

#### 1. Clone o repositório
```bash
git clone https://github.com/pedrowsxz/django_sistema_vacinacao_api
cd django_sistema_vacinacao_api
```

#### 2. Sete o Virtual Environment (venv)
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

---

## Decisões Técnicas

### Estrutura de App Único
Inicialmente considerei montar um app separado para cada model, mas concluí que múltiplos apps não seriam a forma mais adequada de organizar o projeto. Por isso, optei por manter apenas um app Django (`core`), estruturado com subdiretórios para melhor organização. Colocar tudo em arquivos únicos não escala bem e prejudica a legibilidade. A solução intermediária de um app único com subdiretórios bem organizados mantém o domínio coeso e facilita a manutenção., em que os diretórios foram separados em  models, serializers e views com arquivos individuais para Pessoa, Pet, Vacina e VaccinationRecord.

#### Justificativa:
- Todos os modelos estão fortemente acoplados (Pet depende de Pessoa, VaccinationRecord depende de Pessoa, Pet e Vacina)
- Eles representam um único domínio coeso (gerenciamento de vacinação de pets)
- Apps separados aumenta o risco de dependências circulares
- Nenhum desses modelos seria reutilizável de forma independente em outros projetos
- Mais fácil de manter neste escopo
- Segue o princípio do Django de "apps devem ser reutilizáveis" — este domínio é coeso

### Autenticação por Token
Para autenticação, optei por utilizar o Token Authentication nativo do DRF, a alternativa JWT adicionaria complexidade sem benefício significativo.

**Justificativa:**
- Simples e suficiente para este caso de uso
- Sem dependências externas
- Stateful (tokens armazenados no banco de dados)
- Adequado para clientes mobile e web

### Permissões
Classes de permissão customizadas (`IsPessoa`, `IsPessoaOrReadOnly`, `IsPessoaOrAdmin`), com controle de acesso a recursos, filtragem por pessoa nos querysets, mensagens de erro claras para negação de permissão e acesso total ausuários staff (para administração).

---

### Modelo de Dados

Relação OneToOne entre `Pessoa` e o modelo User do Django.

**Justificativa:**
- Aproveita o sistema de autenticação do Django
- Separa dados de autenticação de dados de negócio
- Permite estender o perfil do usuário sem modificar o modelo User

---

### Estratégia de Validação

Validação em Múltiplas Camadas, modelos, serializers e views.

**Justificativa:**
- **Modelos:** validação de regras de negócio (datas, constraints)
- **Serializer:** validação específica de API (formatos, tipos)
- **View:** validação contextual (permissões, vínculo com pessoa)
- Defesa em profundidade


## Mapeamento das URLs

Como os endpoints se mapeiam para o código:

### Authentication Endpoints (Function-Based Views)
```
POST /api/auth/register/            → core/views/auth.py → register()
POST /api/auth/login/               → core/views/auth.py → login()
POST /api/auth/logout/              → core/views/auth.py → logout()
GET  /api/auth/profile/             → core/views/auth.py → profile()
PUT  /api/auth/profile/update/      → core/views/auth.py → update_profile()
POST /api/auth/change-password/     → core/views/auth.py → change_password()
```

### Pessoa Endpoints (PessoaViewSet)
```
GET    /api/pessoas/                 → core/views/pessoa.py → PessoaViewSet.list()
POST   /api/pessoas/                 → core/views/pessoa.py → PessoaViewSet.create()
GET    /api/pessoas/{id}/            → core/views/pessoa.py → PessoaViewSet.retrieve()
PUT    /api/pessoas/{id}/            → core/views/pessoa.py → PessoaViewSet.update()
PATCH  /api/pessoas/{id}/            → core/views/pessoa.py → PessoaViewSet.partial_update()
DELETE /api/pessoas/{id}/            → core/views/pessoa.py → PessoaViewSet.destroy()
GET    /api/pessoas/{id}/pets/       → core/views/pessoa.py → PessoaViewSet.pets() [@action]
GET    /api/pessoas/{id}/vaccination_summary/ → core/views/pessoa.py → PessoaViewSet.vaccination_summary() [@action]
```

### Pet Endpoints (PetViewSet)
```
GET    /api/pets/                   → core/views/pet.py → PetViewSet.list()
GET    /api/pets/?species=dog       → core/views/pet.py → PetViewSet.get_queryset() (filtering)
GET    /api/pets/?search=lab        → core/views/pet.py → DRF SearchFilter
POST   /api/pets/                   → core/views/pet.py → PetViewSet.create()
GET    /api/pets/{id}/              → core/views/pet.py → PetViewSet.retrieve()
PUT    /api/pets/{id}/              → core/views/pet.py → PetViewSet.update()
PATCH  /api/pets/{id}/              → core/views/pet.py → PetViewSet.partial_update()
DELETE /api/pets/{id}/              → core/views/pet.py → PetViewSet.destroy()
GET    /api/pets/{id}/vaccinations/ → core/views/pet.py → PetViewSet.vaccinations() [@action]
GET    /api/pets/{id}/upcoming_vaccinations/ → core/views/pet.py → PetViewSet.upcoming_vaccinations() [@action]
```

### Vaccine Endpoints (VaccineViewSet)
```
GET    /api/vaccines/               → core/views/vaccine.py → VaccineViewSet.list()
GET    /api/vaccines/?species=dog   → core/views/vaccine.py → VaccineViewSet.get_queryset()
POST   /api/vaccines/               → core/views/vaccine.py → VaccineViewSet.create()
GET    /api/vaccines/{id}/          → core/views/vaccine.py → VaccineViewSet.retrieve()
PUT    /api/vaccines/{id}/          → core/views/vaccine.py → VaccineViewSet.update()
PATCH  /api/vaccines/{id}/          → core/views/vaccine.py → VaccineViewSet.partial_update()
DELETE /api/vaccines/{id}/          → core/views/vaccine.py → VaccineViewSet.destroy()
GET    /api/vaccines/{id}/statistics/ → core/views/vaccine.py → VaccineViewSet.statistics() [@action]
```

### Vaccination Record Endpoints (VaccinationRecordViewSet)
```
GET    /api/vaccinations/           → core/views/vaccination_record.py → VaccinationRecordViewSet.list()
GET    /api/vaccinations/?pet=1     → core/views/vaccination_record.py → VaccinationRecordViewSet.get_queryset()
POST   /api/vaccinations/           → core/views/vaccination_record.py → VaccinationRecordViewSet.create()
GET    /api/vaccinations/{id}/      → core/views/vaccination_record.py → VaccinationRecordViewSet.retrieve()
PUT    /api/vaccinations/{id}/      → core/views/vaccination_record.py → VaccinationRecordViewSet.update()
PATCH  /api/vaccinations/{id}/      → core/views/vaccination_record.py → VaccinationRecordViewSet.partial_update()
DELETE /api/vaccinations/{id}/      → core/views/vaccination_record.py → VaccinationRecordViewSet.destroy()
GET    /api/vaccinations/due_soon/  → core/views/vaccination_record.py → VaccinationRecordViewSet.due_soon() [@action]
GET    /api/vaccinations/overdue/   → core/views/vaccination_record.py → VaccinationRecordViewSet.overdue() [@action]
GET    /api/vaccinations/recent/    → core/views/vaccination_record.py → VaccinationRecordViewSet.recent() [@action]

```

## Modelos e Propriedades

### 1. Pessoa
Representa um dono de pet, vinculado ao modelo `User` do Django.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `user` | OneToOneField → User | Conta de usuário associada. |
| `name` | CharField | Nome completo do dono do pet. |
| `email` | EmailField | Email de contato, único e válido. |
| `phone` | CharField | Telefone de contato, opcional, formato internacional. |
| `address` | TextField | Endereço físico, opcional. |
| `created_at` | DateTimeField | Data de criação do registro (automático). |
| `updated_at` | DateTimeField | Data de atualização do registro (automático). |

**Propriedades:**

- `total_pets`: Retorna o total de pets associados a essa pessoa.

**Meta opções:**

- Ordenado por `name`.
- Singular: "Pessoa", Plural: "Pessoas".

---

### 2. Pet
Representa um pet registrado, vinculado a uma `Pessoa`.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `pessoa` | ForeignKey → Pessoa | Dono do pet. |
| `name` | CharField | Nome do pet. |
| `species` | CharField | Espécie do pet (Dog, Cat, Bird, Rabbit, Hamster, Reptile, Other). |
| `breed` | CharField | Raça do pet (opcional). |
| `birth_date` | DateField | Data de nascimento do pet. |
| `color` | CharField | Cor do pet (opcional). |
| `weight` | DecimalField | Peso em kg, opcional, deve ser positivo. |
| `notes` | TextField | Observações adicionais (opcional). |
| `created_at` | DateTimeField | Data de criação do registro (automático). |
| `updated_at` | DateTimeField | Data de atualização do registro (automático). |

**Propriedades:**

- `age_years`: Calcula a idade em anos.
- `age_months`: Calcula a idade em meses.

**Validações:**

- `birth_date` não pode ser no futuro.
- `weight` deve ser maior que zero.

**Meta opções:**

- Ordenado por data de criação mais recente.
- Índices: `(pessoa, -created_at)` e `(species)`.

---

### 3. Vaccine
Representa um tipo de vacina que pode ser aplicada a pets.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `name` | CharField | Nome da vacina, único. |
| `manufacturer` | CharField | Fabricante da vacina (opcional). |
| `description` | TextField | Proteção oferecida pela vacina (opcional). |
| `species_target` | CharField | Espécies alvo da vacina (opcional). |
| `duration_months` | PositiveIntegerField | Validade em meses, mínimo 1. |
| `is_mandatory` | BooleanField | Indica se a vacina é obrigatória por lei. |
| `created_at` | DateTimeField | Data de criação do registro (automático). |
| `updated_at` | DateTimeField | Data de atualização do registro (automático). |

**Meta opções:**

- Ordenado por `name`.
- Singular: "Vaccine", Plural: "Vaccines".

---

### 4. VaccinationRecord
Representa um evento de vacinação de um pet.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `pet` | ForeignKey → Pet | Pet que recebeu a vacina. |
| `vaccine` | ForeignKey → Vaccine | Vacina aplicada. |
| `administered_date` | DateField | Data em que a vacina foi aplicada. |
| `veterinarian_name` | CharField | Nome do veterinário responsável. |
| `clinic_name` | CharField | Nome da clínica veterinária (opcional). |
| `batch_number` | CharField | Número do lote da vacina (opcional). |
| `next_dose_date` | DateField | Data prevista para próxima dose (opcional). |
| `notes` | TextField | Observações adicionais (opcional). |
| `created_at` | DateTimeField | Data de criação do registro (automático). |
| `updated_at` | DateTimeField | Data de atualização do registro (automático). |

**Propriedades:**

- `is_due`: Retorna True se a próxima dose estiver dentro de 30 dias.
- `is_overdue`: Retorna True se a próxima dose estiver atrasada.
- `days_until_due`: Número de dias até a próxima dose.
- `calculate_next_dose_date()`: Calcula a próxima dose com base na duração da vacina.

**Validações:**

- `administered_date` não pode ser no futuro nem antes do nascimento do pet.
- Evita registros duplicados para o mesmo pet, vacina e data.

**Meta opções:**

- Ordenado por `-administered_date`.
- Unique together: `pet + vaccine + administered_date`.
- Índices: `(pet, -administered_date)`, `(vaccine)`, `(next_dose_date)`.
