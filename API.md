# Referência da API

Referência completa para os endpoints da API com exemplos.

## Exemplos Completos

### Exemplo 1: Fluxo Completo do Usuário
```bash
# 1. Registrar usuário
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "jane_doe",
    "password": "SecurePass123!",
    "name": "Jane Doe",
    "email": "jane@example.com",
    "phone": "+1234567890"
  }'

# Salvar o token da resposta
TOKEN="seu-token-aqui"

# 2. Criar um pet
curl -X POST http://localhost:8000/api/pets/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pessoa":"1",
    "name": "Max",
    "species": "dog",
    "breed": "German Shepherd",
    "birth_date": "2021-03-15",
    "weight": 32.5
  }'

# 3. Listar vacinas
curl -X GET http://localhost:8000/api/vaccines/ \
  -H "Authorization: Token $TOKEN"

# 4. Registrar vacinação
curl -X POST http://localhost:8000/api/vaccinations/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pet": 1,
    "vaccine": 1,
    "administered_date": "2024-01-20",
    "veterinarian_name": "Dr. Wilson"
  }'

# 5. Verificar próximas vacinações
curl -X GET http://localhost:8000/api/vaccinations/due_soon/ \
  -H "Authorization: Token $TOKEN"
