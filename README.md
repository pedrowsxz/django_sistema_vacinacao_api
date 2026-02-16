# Pet Vaccination Control System API

A REST API for managing pet vaccination records, built with Django and Django REST Framework.

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Django](https://img.shields.io/badge/django-4.2-green.svg)
![DRF](https://img.shields.io/badge/DRF-3.14-red.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
  - [Local Setup](#local-setup)
  - [Docker Setup](#docker-setup)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Technical Decisions](#technical-decisions)
- [Contributing](#contributing)

---

## 🎯 Overview

This system allows veterinary clinics and pet owners to track vaccination history, manage pet records, and monitor upcoming vaccination schedules. The API provides complete CRUD operations for pets, vaccines, and vaccination records, with proper authentication and authorization.

### Key Capabilities

- **Pet Management**: Register and track pets with detailed information
- **Vaccine Database**: Maintain a catalog of available vaccines
- **Vaccination Records**: Record and track all administered vaccinations
- **Owner Accounts**: Secure user accounts with ownership-based access control
- **Automated Scheduling**: Automatic calculation of next dose dates
- **Reminders**: Track due and overdue vaccinations

---

## ✨ Features

### Core Features
- ✅ User registration and authentication (Token-based)
- ✅ Pet registration with species, breed, age tracking
- ✅ Vaccine management with duration and mandatory status
- ✅ Vaccination record keeping with auto-calculated next doses
- ✅ Owner-based access control (users only see their own data)
- ✅ Due/overdue vaccination tracking
- ✅ Comprehensive filtering and search capabilities

### Technical Features
- ✅ RESTful API design
- ✅ Token authentication with throttling
- ✅ Permission-based access control
- ✅ Automated field validation
- ✅ Pagination for list endpoints
- ✅ Comprehensive test coverage (45+ tests)
- ✅ Docker support for easy deployment

---

## 🛠️ Technology Stack

### Backend
- **Python 3.11+**
- **Django 4.2** - Web framework
- **Django REST Framework 3.14** - API toolkit
- **SQLite** - Database (default, easily switchable to PostgreSQL)

### Additional Libraries
- **python-decouple** - Environment variable management
- **python-dateutil** - Date calculations

### Development Tools
- **Coverage** - Test coverage reporting
- **Docker** - Containerization

---

## 📁 Project Structure
```
pet-vaccination-api/
├── pet_vaccination/           # Django project settings
│   ├── __init__.py
│   ├── settings.py           # Project configuration
│   ├── urls.py               # Main URL routing
│   └── wsgi.py
│
├── core/                      # Main application
│   ├── models/               # Data models
│   │   ├── owner.py          # Owner model
│   │   ├── pet.py            # Pet model
│   │   ├── vaccine.py        # Vaccine model
│   │   └── vaccination_record.py
│   │
│   ├── serializers/          # DRF serializers
│   │   ├── owner.py
│   │   ├── pet.py
│   │   ├── vaccine.py
│   │   └── vaccination_record.py
│   │
│   ├── views/                # API views
│   │   ├── owner.py          # Owner viewset
│   │   ├── pet.py            # Pet viewset
│   │   ├── vaccine.py        # Vaccine viewset
│   │   ├── vaccination_record.py
│   │   └── auth.py           # Authentication views
│   │
│   ├── tests/                # Test suite
│   │   ├── test_models.py
│   │   ├── test_api_auth.py
│   │   ├── test_api_pets.py
│   │   ├── test_api_vaccinations.py
│   │   ├── test_permissions.py
│   │   └── test_integration.py
│   │
│   ├── permissions.py        # Custom permissions
│   ├── urls.py              # App URL routing
│   └── admin.py             # Admin interface config
│
├── requirements.txt          # Python dependencies
├── Dockerfile               # Docker image definition
├── docker-compose.yml       # Docker services orchestration
├── .env.example             # Environment variables template
├── .gitignore
└── manage.py
```

---

## 🚀 Installation

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- Git

### Local Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/pet-vaccination-api.git
cd pet-vaccination-api
```

#### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Environment Configuration

Create `.env` file in the project root:
```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```env
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_ENGINE=django.db.backends.sqlite3
DATABASE_NAME=db.sqlite3
```

#### 5. Database Setup
```bash
# Run migrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser

# Load sample data (optional)
python manage.py loaddata sample_data.json
```

#### 6. Run Development Server
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

- **API Root**: http://127.0.0.1:8000/api/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **API Documentation**: http://127.0.0.1:8000/api/docs/ (if enabled)

---

## 🐳 Docker Setup

Docker provides an easy way to run the application without manual setup.

### Prerequisites
- Docker
- Docker Compose

### Quick Start with Docker

#### 1. Clone and Navigate
```bash
git clone https://github.com/yourusername/pet-vaccination-api.git
cd pet-vaccination-api
```

#### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env if needed (default values work for Docker)
```

#### 3. Build and Run
```bash
# Build and start containers
docker-compose up --build

# Or run in detached mode
docker-compose up -d
```

#### 4. Initialize Database
```bash
# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

#### 5. Access the Application

- **API**: http://localhost:8000/api/
- **Admin**: http://localhost:8000/admin/

### Docker Commands
```bash
# View logs
docker-compose logs -f

# Stop containers
docker-compose down

# Stop and remove volumes (database data)
docker-compose down -v

# Run tests in Docker
docker-compose exec web python manage.py test

# Access Django shell
docker-compose exec web python manage.py shell
```

---

## 📚 API Documentation

### Base URL
```
http://127.0.0.1:8000/api/
```

### Authentication

All endpoints (except registration and login) require authentication using Token Authentication.

**Header Format:**
```
Authorization: Token <your-token-here>
```

---

### 🔐 Authentication Endpoints

#### Register New User

**POST** `/api/auth/register/`

Create a new user account with owner profile.

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

Authenticate and receive access token.

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

## 🧪 Testing

The project includes a comprehensive test suite covering models, API endpoints, permissions, and integration workflows.

### Run All Tests
```bash
# Run all tests
python manage.py test

# Run with verbosity
python manage.py test -v 2

# Run specific test file
python manage.py test core.tests.test_models

# Run specific test class
python manage.py test core.tests.test_models.PetModelTest

# Run specific test method
python manage.py test core.tests.test_models.PetModelTest.test_pet_age_calculation
```

### Test Coverage
```bash
# Install coverage
pip install coverage

# Run tests with coverage
coverage run --source='core' manage.py test core

# View coverage report
coverage report

# Generate HTML coverage report
coverage html
# Open htmlcov/index.html in browser
```

### Test Categories

- **Model Tests** (15 tests) - Validation, properties, calculations
- **Authentication Tests** (8 tests) - Register, login, logout, throttling
- **Pet API Tests** (10 tests) - CRUD operations, filtering
- **Vaccination Tests** (8 tests) - Record creation, due dates
- **Permission Tests** (7 tests) - Access control verification
- **Integration Tests** (3 tests) - End-to-end workflows

**Total: 45+ tests with ~94% code coverage**

---

## 🏗️ Technical Decisions

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

### Testing Strategy

#### 1. Comprehensive Coverage
**Decision:** Test models, APIs, permissions, and workflows separately.

**Rationale:**
- Isolates failures
- Clear test organization
- Easy to add new tests
- Documents expected behavior

#### 2. Base Test Classes
**Decision:** Create base classes with common setup.

**Rationale:**
- DRY principle
- Consistent test data
- Faster test writing
- Easier maintenance

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | Required |
| `DEBUG` | Debug mode | `False` |
| `ALLOWED_HOSTS` | Allowed hosts | `localhost` |
| `DATABASE_ENGINE` | Database backend | `django.db.backends.sqlite3` |
| `DATABASE_NAME` | Database name/path | `db.sqlite3` |

### Switching to PostgreSQL

1. Update `.env`:
```env
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=pet_vaccination
DATABASE_USER=postgres
DATABASE_PASSWORD=password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

2. Install psycopg2:
```bash
pip install psycopg2-binary
```

3. Update `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': config('DATABASE_ENGINE'),
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER', default=''),
        'PASSWORD': config('DATABASE_PASSWORD', default=''),
        'HOST': config('DATABASE_HOST', default=''),
        'PORT': config('DATABASE_PORT', default=''),
    }
}
```

---

## 📈 Future Enhancements

Potential features for future versions:

- [ ] Email notifications for due vaccinations
- [ ] PDF report generation
- [ ] Multi-clinic support
- [ ] Appointment scheduling
- [ ] Medical history beyond vaccinations
- [ ] Image uploads for pets
- [ ] QR code generation for pet profiles
- [ ] Integration with veterinary management systems
- [ ] Multi-language support
- [ ] Mobile app (React Native / Flutter)

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style
- Follow PEP 8
- Use meaningful variable names
- Add docstrings to classes and methods
- Write tests for new features

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Your Name** - *Initial work* - [GitHub Profile](https://github.com/yourusername)

---

## 🙏 Acknowledgments

- Django and Django REST Framework communities
- All contributors and testers

---

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Email: your-email@example.com

---

## 📊 Project Status

**Current Version:** 1.0.0  
**Status:** Production Ready  
**Last Updated:** January 2024