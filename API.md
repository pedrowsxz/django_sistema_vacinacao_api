# API Reference

Complete reference for all API endpoints with detailed examples.

## Complete Examples

### Example 1: Complete User Flow
```bash
# 1. Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "jane_doe",
    "password": "SecurePass123!",
    "name": "Jane Doe",
    "email": "jane@example.com",
    "phone": "+1234567890"
  }'

# Save the token from response
TOKEN="your-token-here"

# 2. Create a pet
curl -X POST http://localhost:8000/api/pets/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Max",
    "species": "dog",
    "breed": "German Shepherd",
    "birth_date": "2021-03-15",
    "weight": 32.5
  }'

# 3. List vaccines
curl -X GET http://localhost:8000/api/vaccines/ \
  -H "Authorization: Token $TOKEN"

# 4. Record vaccination
curl -X POST http://localhost:8000/api/vaccinations/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pet": 1,
    "vaccine": 1,
    "administered_date": "2024-01-20",
    "veterinarian_name": "Dr. Wilson"
  }'

# 5. Check upcoming vaccinations
curl -X GET http://localhost:8000/api/vaccinations/due_soon/ \
  -H "Authorization: Token $TOKEN"
```

---

### Example 2: Filtering and Search
```bash
# Search pets by name
curl -X GET "http://localhost:8000/api/pets/?search=max" \
  -H "Authorization: Token $TOKEN"

# Filter pets by species
curl -X GET "http://localhost:8000/api/pets/?species=dog" \
  -H "Authorization: Token $TOKEN"

# Get vaccinations for specific pet
curl -X GET "http://localhost:8000/api/vaccinations/?pet=1" \
  -H "Authorization: Token $TOKEN"

# Get vaccinations in date range
curl -X GET "http://localhost:8000/api/vaccinations/?date_from=2024-01-01&date_to=2024-12-31" \
  -H "Authorization: Token $TOKEN"
```

---

### Example 3: Update and Delete
```bash
# Update pet weight
curl -X PATCH http://localhost:8000/api/pets/1/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "weight": 33.0
  }'

# Update vaccination notes
curl -X PATCH http://localhost:8000/api/vaccinations/1/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "notes": "Updated: No adverse reactions after 48 hours"
  }'

# Delete a pet
curl -X DELETE http://localhost:8000/api/pets/1/ \
  -H "Authorization: Token $TOKEN"
```