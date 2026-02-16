#!/bin/bash
# cURL Tests for Authentication API
# Replace http://localhost:8000 with your actual API base URL

BASE_URL="http://localhost:8000/api/auth"

echo "=========================================="
echo "Authentication API cURL Tests"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ==========================================
# 1. REGISTER NEW USER
# ==========================================
echo -e "${BLUE}1. Register New User${NC}"
echo "POST ${BASE_URL}/register/"
echo ""

curl -X POST "${BASE_URL}/register/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser1",
    "password": "StrongPass123!",
    "name": "Test User One",
    "email": "testuser1@example.com",
    "phone": "1234567890",
    "address": "123 Test Street"
  }' \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.'

echo ""
echo "Expected: 201 Created, returns token and pessoa data"
echo "=========================================="
echo ""

# ==========================================
# 2. REGISTER WITH WEAK PASSWORD (Should Fail)
# ==========================================
echo -e "${BLUE}2. Register with Weak Password (Should Fail)${NC}"
echo "POST ${BASE_URL}/register/"
echo ""

curl -X POST "${BASE_URL}/register/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser2",
    "password": "123",
    "name": "Test User Two",
    "email": "testuser2@example.com"
  }' \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.'

echo ""
echo "Expected: 400 Bad Request, password validation error"
echo "=========================================="
echo ""

# ==========================================
# 3. LOGIN
# ==========================================
echo -e "${BLUE}3. Login${NC}"
echo "POST ${BASE_URL}/login/"
echo ""

LOGIN_RESPONSE=$(curl -X POST "${BASE_URL}/login/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser1",
    "password": "StrongPass123!"
  }' \
  -w "\nHTTP_STATUS:%{http_code}" \
  -s)

# Extract token for later use
TOKEN=$(echo "$LOGIN_RESPONSE" | sed 's/HTTP_STATUS.*//' | jq -r '.token')

echo "$LOGIN_RESPONSE" | sed 's/HTTP_STATUS.*//' | jq '.'
echo "HTTP Status: $(echo "$LOGIN_RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d: -f2)"
echo ""
echo "Token saved for subsequent requests: $TOKEN"
echo "Expected: 200 OK, returns token and pessoa data"
echo "=========================================="
echo ""

# ==========================================
# 4. LOGIN WITH WRONG PASSWORD (Should Fail)
# ==========================================
echo -e "${BLUE}4. Login with Wrong Password (Should Fail)${NC}"
echo "POST ${BASE_URL}/login/"
echo ""

curl -X POST "${BASE_URL}/login/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser1",
    "password": "WrongPassword123!"
  }' \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.'

echo ""
echo "Expected: 401 Unauthorized, invalid credentials error"
echo "=========================================="
echo ""

# ==========================================
# 5. LOGIN WITH MISSING FIELDS (Should Fail)
# ==========================================
echo -e "${BLUE}5. Login with Missing Fields (Should Fail)${NC}"
echo "POST ${BASE_URL}/login/"
echo ""

curl -X POST "${BASE_URL}/login/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser1"
  }' \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.'

echo ""
echo "Expected: 400 Bad Request"
echo "=========================================="
echo ""

# ==========================================
# 6. GET PROFILE (Authenticated)
# ==========================================
echo -e "${BLUE}6. Get Profile (Authenticated)${NC}"
echo "GET ${BASE_URL}/profile/"
echo "Authorization: Token $TOKEN"
echo ""

curl -X GET "${BASE_URL}/profile/" \
  -H "Authorization: Token $TOKEN" \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.'

echo ""
echo "Expected: 200 OK, returns pessoa profile data"
echo "=========================================="
echo ""

# ==========================================
# 7. GET PROFILE WITHOUT AUTH (Should Fail)
# ==========================================
echo -e "${BLUE}7. Get Profile without Auth (Should Fail)${NC}"
echo "GET ${BASE_URL}/profile/"
echo ""

curl -X GET "${BASE_URL}/profile/" \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.'

echo ""
echo "Expected: 401 Unauthorized"
echo "=========================================="
echo ""

# ==========================================
# 8. UPDATE PROFILE (PUT)
# ==========================================
echo -e "${BLUE}8. Update Profile (PUT)${NC}"
echo "PUT ${BASE_URL}/profile/update/"
echo "Authorization: Token $TOKEN"
echo ""

curl -X PUT "${BASE_URL}/profile/update/" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Test User",
    "email": "updated@example.com",
    "phone": "9876543210"
  }' \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.'

echo ""
echo "Expected: 200 OK, returns updated profile"
echo "=========================================="
echo ""

# ==========================================
# 9. PARTIAL UPDATE PROFILE (PATCH)
# ==========================================
echo -e "${BLUE}9. Partial Update Profile (PATCH)${NC}"
echo "PATCH ${BASE_URL}/profile/update/"
echo "Authorization: Token $TOKEN"
echo ""

curl -X PATCH "${BASE_URL}/profile/update/" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "5555555555"
  }' \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.'

echo ""
echo "Expected: 200 OK, only phone updated"
echo "=========================================="
echo ""

# ==========================================
# 10. CHANGE PASSWORD
# ==========================================
echo -e "${BLUE}10. Change Password${NC}"
echo "POST ${BASE_URL}/change-password/"
echo "Authorization: Token $TOKEN"
echo ""

CHANGE_PASS_RESPONSE=$(curl -X POST "${BASE_URL}/change-password/" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "old_password": "StrongPass123!",
    "new_password": "NewStrongPass456!"
  }' \
  -w "\nHTTP_STATUS:%{http_code}" \
  -s)

# Extract new token
NEW_TOKEN=$(echo "$CHANGE_PASS_RESPONSE" | sed 's/HTTP_STATUS.*//' | jq -r '.token')

echo "$CHANGE_PASS_RESPONSE" | sed 's/HTTP_STATUS.*//' | jq '.'
echo "HTTP Status: $(echo "$CHANGE_PASS_RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d: -f2)"
echo ""
echo "New Token: $NEW_TOKEN"
echo "Expected: 200 OK, returns new token"
echo "=========================================="
echo ""

# ==========================================
# 11. CHANGE PASSWORD WITH WRONG OLD PASSWORD (Should Fail)
# ==========================================
echo -e "${BLUE}11. Change Password with Wrong Old Password (Should Fail)${NC}"
echo "POST ${BASE_URL}/change-password/"
echo "Authorization: Token $NEW_TOKEN"
echo ""

curl -X POST "${BASE_URL}/change-password/" \
  -H "Authorization: Token $NEW_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "old_password": "WrongOldPassword",
    "new_password": "AnotherNewPass789!"
  }' \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.'

echo ""
echo "Expected: 400 Bad Request, old password incorrect"
echo "=========================================="
echo ""

# ==========================================
# 12. LOGOUT
# ==========================================
echo -e "${BLUE}12. Logout${NC}"
echo "POST ${BASE_URL}/logout/"
echo "Authorization: Token $NEW_TOKEN"
echo ""

curl -X POST "${BASE_URL}/logout/" \
  -H "Authorization: Token $NEW_TOKEN" \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.'

echo ""
echo "Expected: 200 OK, successfully logged out"
echo "=========================================="
echo ""

# ==========================================
# 13. USE OLD TOKEN AFTER LOGOUT (Should Fail)
# ==========================================
echo -e "${BLUE}13. Use Token After Logout (Should Fail)${NC}"
echo "GET ${BASE_URL}/profile/"
echo "Authorization: Token $NEW_TOKEN"
echo ""

curl -X GET "${BASE_URL}/profile/" \
  -H "Authorization: Token $NEW_TOKEN" \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.'

echo ""
echo "Expected: 401 Unauthorized, token deleted"
echo "=========================================="
echo ""

# ==========================================
# 14. RATE LIMITING TEST (5 requests/minute)
# ==========================================
echo -e "${BLUE}14. Rate Limiting Test${NC}"
echo "Making 6 rapid login requests..."
echo ""

for i in {1..6}; do
  echo "Request $i:"
  curl -X POST "${BASE_URL}/login/" \
    -H "Content-Type: application/json" \
    -d '{
      "username": "testuser1",
      "password": "WrongPassword"
    }' \
    -w "\nHTTP Status: %{http_code}\n\n" \
    -s | head -n 1
done

echo ""
echo "Expected: First 5 requests return 401, 6th might return 429 (Too Many Requests)"
echo "=========================================="
echo ""

echo -e "${GREEN}All cURL tests completed!${NC}"
echo ""
echo "Note: Adjust the BASE_URL variable at the top of this script to match your API endpoint"
echo "Make sure jq is installed for JSON formatting: sudo apt-get install jq"
