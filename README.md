# Sistema de Vacinação de Pets API

Uma API REST para gerenciar registros de vacinação de pets, usando Django.

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
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

Este sistema permite que clínicas veterinárias e tutores de animais acompanhem o histórico de vacinação, gerenciem os registros dos pets e monitorem os próximos agendamentos de vacinas.
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

#### Registre Novo Usuário

**POST** `/api/auth/register/`

**Request Body:**
```json
{
  "username": "john_doe",
  "password": "SecurePass123!",
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "address": "123 Main St, City"
}
```

**Response:** `201 Created`
```json
{
  "message": "Registration successful",
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "owner": {
    "id": 1,
    "username": "john_doe",
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890"
  }
}
```

---

#### Login

**POST** `/api/auth/login/`

Autenticação e recebimento do token de acesso.

**Request Body:**
```json
{
  "username": "john_doe",
  "password": "SecurePass123!"
}
```

**Response:** `200 OK`
```json
{
  "message": "Login successful",
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "owner": {
    "id": 1,
    "username": "john_doe",
    "name": "John Doe",
    "email": "john@example.com",
    "total_pets": 2
  }
}
```

---

#### Logout

**POST** `/api/auth/logout/`

Invalidate current token.

**Headers:**
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Response:** `200 OK`
```json
{
  "message": "Successfully logged out"
}
```

---

#### Get Profile

**GET** `/api/auth/profile/`

Get current user's profile.

**Response:** `200 OK`
```json
{
  "id": 1,
  "username": "john_doe",
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "address": "123 Main St",
  "total_pets": 2,
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

#### Change Password

**POST** `/api/auth/change-password/`

Change user password.

**Request Body:**
```json
{
  "old_password": "SecurePass123!",
  "new_password": "NewSecurePass456!"
}
```

**Response:** `200 OK`
```json
{
  "message": "Password changed successfully",
  "token": "new-token-here"
}
```

---

### 🐾 Pet Endpoints

#### List Pets

**GET** `/api/pets/`

Get all pets owned by the authenticated user.

**Query Parameters:**
- `species` - Filter by species (dog, cat, bird, etc.)
- `owner` - Filter by owner ID (staff only)
- `search` - Search by name or breed
- `ordering` - Sort by field (-created_at, name, birth_date)
- `page` - Page number

**Example Request:**
```bash
GET /api/pets/?species=dog&search=lab&page=1
```

**Response:** `200 OK`
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "owner": 1,
      "owner_name": "John Doe",
      "name": "Rex",
      "species": "dog",
      "species_display": "Dog",
      "breed": "Labrador Retriever",
      "birth_date": "2020-05-15",
      "age_years": 3,
      "age_months": 43,
      "color": "Golden",
      "weight": "25.50",
      "notes": "Very friendly",
      "created_at": "2024-01-10T14:30:00Z"
    }
  ]
}
```

---

#### Create Pet

**POST** `/api/pets/`

Register a new pet.

**Request Body:**
```json
{
  "name": "Rex",
  "species": "dog",
  "breed": "Labrador Retriever",
  "birth_date": "2020-05-15",
  "color": "Golden",
  "weight": 25.5,
  "notes": "Very friendly dog"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "owner": 1,
  "owner_name": "John Doe",
  "name": "Rex",
  "species": "dog",
  "species_display": "Dog",
  "breed": "Labrador Retriever",
  "birth_date": "2020-05-15",
  "age_years": 3,
  "age_months": 43,
  "color": "Golden",
  "weight": "25.50",
  "notes": "Very friendly dog",
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

#### Get Pet Details

**GET** `/api/pets/{id}/`

Get detailed information about a specific pet, including vaccination history.

**Response:** `200 OK`
```json
{
  "id": 1,
  "owner": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890"
  },
  "name": "Rex",
  "species": "dog",
  "species_display": "Dog",
  "breed": "Labrador Retriever",
  "birth_date": "2020-05-15",
  "age_years": 3,
  "age_months": 43,
  "color": "Golden",
  "weight": "25.50",
  "notes": "Very friendly dog",
  "vaccination_history": [
    {
      "id": 1,
      "vaccine_name": "Rabies",
      "administered_date": "2024-01-15",
      "next_dose_date": "2025-01-15",
      "veterinarian_name": "Dr. Smith",
      "is_due": false,
      "is_overdue": false
    }
  ],
  "vaccination_count": 1,
  "created_at": "2024-01-10T14:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

---

#### Update Pet

**PATCH** `/api/pets/{id}/`

Update pet information.

**Request Body:**
```json
{
  "weight": 27.0,
  "notes": "Updated notes"
}
```

**Response:** `200 OK` (same format as Get Pet Details)

---

#### Delete Pet

**DELETE** `/api/pets/{id}/`

Delete a pet record.

**Response:** `204 No Content`

---

#### Get Pet Vaccinations

**GET** `/api/pets/{id}/vaccinations/`

Get all vaccination records for a specific pet.

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "pet_name": "Rex",
    "vaccine_name": "Rabies",
    "administered_date": "2024-01-15",
    "next_dose_date": "2025-01-15",
    "veterinarian_name": "Dr. Smith",
    "clinic_name": "Happy Pets Clinic",
    "is_due": false,
    "is_overdue": false,
    "days_until_due": 365
  }
]
```

---

#### Get Upcoming Vaccinations

**GET** `/api/pets/{id}/upcoming_vaccinations/`

Get due and overdue vaccinations for a pet.

**Response:** `200 OK`
```json
{
  "due_soon": [
    {
      "id": 2,
      "vaccine_name": "DHPP",
      "next_dose_date": "2024-02-20",
      "days_until_due": 15
    }
  ],
  "overdue": [
    {
      "id": 3,
      "vaccine_name": "Bordetella",
      "next_dose_date": "2024-01-01",
      "days_until_due": -14
    }
  ]
}
```

---

### 💉 Vaccine Endpoints

#### List Vaccines

**GET** `/api/vaccines/`

Get all available vaccines.

**Query Parameters:**
- `species` - Filter by target species
- `mandatory` - Filter by mandatory status (true/false)
- `search` - Search by name or manufacturer

**Response:** `200 OK`
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "name": "Rabies",
      "manufacturer": "Pfizer",
      "description": "Protects against rabies virus",
      "species_target": "dog",
      "duration_months": 12,
      "is_mandatory": true,
      "total_administrations": 15,
      "created_at": "2024-01-01T10:00:00Z"
    }
  ]
}
```

---

#### Create Vaccine

**POST** `/api/vaccines/`

Add a new vaccine to the system.

**Request Body:**
```json
{
  "name": "Rabies",
  "manufacturer": "Pfizer",
  "description": "Protects against rabies virus",
  "species_target": "dog",
  "duration_months": 12,
  "is_mandatory": true
}
```

**Response:** `201 Created`

---

#### Get Vaccine Details

**GET** `/api/vaccines/{id}/`

Get detailed vaccine information with recent administrations.

**Response:** `200 OK`
```json
{
  "id": 1,
  "name": "Rabies",
  "manufacturer": "Pfizer",
  "description": "Protects against rabies virus",
  "species_target": "dog",
  "duration_months": 12,
  "is_mandatory": true,
  "total_administrations": 15,
  "recent_administrations": [
    {
      "id": 10,
      "pet_name": "Rex",
      "administered_date": "2024-01-15"
    }
  ],
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:00:00Z"
}
```

---

#### Get Vaccine Statistics

**GET** `/api/vaccines/{id}/statistics/`

Get usage statistics for a vaccine.

**Response:** `200 OK`
```json
{
  "vaccine": "Rabies",
  "total_administrations": 15,
  "recent_administrations_30d": 5,
  "by_species": [
    {
      "pet__species": "dog",
      "count": 12
    },
    {
      "pet__species": "cat",
      "count": 3
    }
  ],
  "duration_months": 12,
  "is_mandatory": true
}
```

---

### 📋 Vaccination Record Endpoints

#### List Vaccination Records

**GET** `/api/vaccinations/`

Get all vaccination records for the authenticated user's pets.

**Query Parameters:**
- `pet` - Filter by pet ID
- `vaccine` - Filter by vaccine ID
- `date_from` - Filter by date range (start)
- `date_to` - Filter by date range (end)
- `search` - Search by pet name, vaccine name, or veterinarian

**Response:** `200 OK`
```json
{
  "count": 10,
  "results": [
    {
      "id": 1,
      "pet": 1,
      "pet_name": "Rex",
      "vaccine": 1,
      "vaccine_name": "Rabies",
      "administered_date": "2024-01-15",
      "veterinarian_name": "Dr. Emily Smith",
      "clinic_name": "Happy Pets Veterinary Clinic",
      "batch_number": "BATCH123456",
      "next_dose_date": "2025-01-15",
      "is_due": false,
      "is_overdue": false,
      "days_until_due": 365,
      "notes": "No adverse reactions",
      "created_at": "2024-01-15T14:30:00Z"
    }
  ]
}
```

---

#### Create Vaccination Record

**POST** `/api/vaccinations/`

Record a new vaccination.

**Request Body:**
```json
{
  "pet": 1,
  "vaccine": 1,
  "administered_date": "2024-01-15",
  "veterinarian_name": "Dr. Emily Smith",
  "clinic_name": "Happy Pets Veterinary Clinic",
  "batch_number": "BATCH123456",
  "notes": "No adverse reactions observed"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "pet": 1,
  "pet_name": "Rex",
  "vaccine": 1,
  "vaccine_name": "Rabies",
  "administered_date": "2024-01-15",
  "veterinarian_name": "Dr. Emily Smith",
  "clinic_name": "Happy Pets Veterinary Clinic",
  "batch_number": "BATCH123456",
  "next_dose_date": "2025-01-15",
  "is_due": false,
  "is_overdue": false,
  "days_until_due": 365,
  "notes": "No adverse reactions observed",
  "created_at": "2024-01-15T14:30:00Z"
}
```

**Note:** `next_dose_date` is automatically calculated based on the vaccine's `duration_months`.

---

#### Get Due Vaccinations

**GET** `/api/vaccinations/due_soon/`

Get all vaccinations due within the next 30 days.

**Response:** `200 OK`
```json
[
  {
    "id": 5,
    "pet_name": "Fluffy",
    "vaccine_name": "FVRCP",
    "next_dose_date": "2024-02-10",
    "days_until_due": 10,
    "is_due": true
  }
]
```

---

#### Get Overdue Vaccinations

**GET** `/api/vaccinations/overdue/`

Get all overdue vaccinations.

**Response:** `200 OK`
```json
[
  {
    "id": 3,
    "pet_name": "Rex",
    "vaccine_name": "Bordetella",
    "next_dose_date": "2024-01-01",
    "days_until_due": -14,
    "is_overdue": true
  }
]
```

---

#### Get Recent Vaccinations

**GET** `/api/vaccinations/recent/`

Get vaccinations administered in the last 30 days.

**Response:** `200 OK`

---

### 👤 Owner Endpoints

#### List Owners

**GET** `/api/owners/`

Get owner information (users see only their own, staff see all).

**Response:** `200 OK`

---

#### Get Owner Details

**GET** `/api/owners/{id}/`

Get detailed owner information including pet list.

**Response:** `200 OK`
```json
{
  "id": 1,
  "username": "john_doe",
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "address": "123 Main St",
  "total_pets": 2,
  "pets": [
    {
      "id": 1,
      "name": "Rex",
      "species": "dog",
      "breed": "Labrador",
      "age_years": 3
    }
  ],
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-15T14:30:00Z"
}
```

---

#### Get Vaccination Summary

**GET** `/api/owners/{id}/vaccination_summary/`

Get comprehensive vaccination summary for all owner's pets.

**Response:** `200 OK`
```json
{
  "total_pets": 2,
  "total_vaccinations": 5,
  "due_soon": 1,
  "overdue": 1,
  "pets": [
    {
      "id": 1,
      "name": "Rex",
      "species": "dog",
      "total_vaccinations": 3,
      "due_vaccinations": [
        {
          "vaccine": "DHPP",
          "next_dose_date": "2024-02-20",
          "days_until_due": 15
        }
      ],
      "overdue_vaccinations": []
    }
  ]
}
```
---

## Technical Decisions

### Architecture Choices

#### 1. Single App Structure
**Decision:** Use one Django app (`core`) with organized subdirectories.

**Rationale:**
- All models are tightly coupled (Pet depends on Owner, VaccinationRecord depends on both)
- Avoids circular dependencies
- Easier to maintain for this scope
- Follows Django's principle of "apps should be reusable" - this domain is cohesive

#### 2. File Organization
**Decision:** Separate models, serializers, and views into individual files within subdirectories.

**Rationale:**
- Better than single files (easier navigation)
- Better than multiple apps (avoids over-engineering)
- Clear separation of concerns
- Scalable for future growth

#### 3. Token Authentication
**Decision:** Use DRF's built-in Token Authentication.

**Rationale:**
- Simple and sufficient for this use case
- No external dependencies
- Stateful (tokens stored in database)
- Suitable for mobile and web clients
- Alternative (JWT) would add complexity without significant benefit

#### 4. Permission System
**Decision:** Custom permission classes (`IsOwner`, `IsOwnerOrReadOnly`).

**Rationale:**
- Granular control over resource access
- Owner-based filtering in querysets
- Clear error messages for permission denials
- Staff users have full access (for admin purposes)

### Data Model Decisions

#### 1. Owner ↔ User Relationship
**Decision:** OneToOne relationship between Owner and Django's User model.

**Rationale:**
- Leverages Django's authentication system
- Separates authentication data from business data
- Allows extending user profile without modifying User model
- Supports future multi-role systems (e.g., veterinarians)

#### 2. Vaccination Record Design
**Decision:** Junction table (VaccinationRecord) with additional metadata.

**Rationale:**
- Stores more than just relationship (date, veterinarian, batch number)
- Allows multiple vaccinations of same vaccine over time
- Automatic next dose calculation
- Historical tracking

#### 3. Next Dose Calculation
**Decision:** Auto-calculate and store `next_dose_date` on save.

**Rationale:**
- Denormalization for performance (avoids complex queries)
- Enables simple due/overdue checks
- Can be overridden manually if needed
- Uses `python-dateutil` for accurate month arithmetic

### API Design Decisions

#### 1. Nested Serializers
**Decision:** Different serializers for list vs detail views.

**Rationale:**
- List views: Minimal data (performance)
- Detail views: Full nested data (convenience)
- Write operations: Flat structure (simplicity)
- Follows REST best practices

#### 2. Filtering Strategy
**Decision:** Use query parameters for filtering, not nested routes.

**Rationale:**
- More flexible (`/api/pets/?owner=1&species=dog`)
- Standard REST pattern
- Easier to implement and maintain
- Better for complex filters

#### 3. Custom Actions
**Decision:** Use DRF's `@action` decorator for non-CRUD operations.

**Rationale:**
- Clean URL structure (`/api/vaccinations/due_soon/`)
- Semantic HTTP methods
- Discoverable API
- Follows DRF conventions

### Validation Strategy

#### 1. Multi-Layer Validation
**Decision:** Validation at model, serializer, and view levels.

**Rationale:**
- **Model:** Business logic validation (dates, constraints)
- **Serializer:** API-specific validation (format, types)
- **View:** Context-specific validation (permissions, ownership)
- Defense in depth

#### 2. Automatic Calculations
**Decision:** Use model properties for calculated fields (age, status).

**Rationale:**
- Always up-to-date
- No data inconsistency
- Computed on-demand
- Included in serializers as read-only