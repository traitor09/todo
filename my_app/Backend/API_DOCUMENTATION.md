# API Documentation

## Internship Recommendation System API

Base URL: `http://localhost:5000` (development)

---

## Endpoints

### 1. Health Check

**GET** `/`

Returns basic API information.

**Response:**
```json
{
  "status": "running",
  "message": "Internship Recommendation System API",
  "version": "1.0.0"
}
```

---

### 2. Health Status

**GET** `/health`

Returns detailed health status including database connectivity.

**Response (Healthy):**
```json
{
  "status": "healthy",
  "database": "connected"
}
```

**Response (Unhealthy):**
```json
{
  "status": "unhealthy",
  "database": "disconnected",
  "error": "Connection timeout"
}
```

**Status Codes:**
- `200 OK` - Service is healthy
- `503 Service Unavailable` - Service is unhealthy

---

### 3. Get Recommendations

**POST** `/recommend`

Get personalized internship recommendations based on candidate profile.

**Query Parameters:**
- `top_n` (optional, integer): Number of recommendations to return
  - Default: `10`
  - Min: `1`
  - Max: `100`

**Request Body:**
```json
{
  "Skills": ["Python", "Flask", "MongoDB"],
  "Location": "Remote",
  "Eligibility": "3rd year",
  "Degree": "B.Tech",
  "Sector": "Technology"
}
```

**Required Fields:**
- `Skills` (array of strings): List of candidate skills

**Optional Fields:**
- `Location` (string): Preferred location
- `Eligibility` (string): Current year of study
- `Degree` (string): Degree program
- `Sector` (string): Preferred industry sector

**Success Response:**
```json
{
  "count": 5,
  "recommendations": [
    {
      "_id": "507f1f77bcf86cd799439011",
      "Title": "Python Backend Developer Intern",
      "Description": "Work on backend systems...",
      "Sector": "Technology",
      "Stipend": "15000",
      "Duration": "3 months",
      "Required Skills": ["Python", "Flask", "MongoDB"],
      "Location": "Remote",
      "Skills_matched": ["Python", "Flask", "MongoDB"],
      "Score": 3
    }
  ]
}
```

**Error Responses:**

**400 Bad Request** - Invalid input
```json
{
  "error": "Validation error",
  "message": "Skills field is required"
}
```

**503 Service Unavailable** - Database connection error
```json
{
  "error": "Database connection error",
  "message": "Unable to connect to the database. Please try again later."
}
```

**500 Internal Server Error** - Server error
```json
{
  "error": "Internal server error",
  "message": "An unexpected error occurred. Please try again later."
}
```

---

## Error Handling

All error responses follow this structure:
```json
{
  "error": "Error type",
  "message": "Human-readable error message"
}
```

### Common Error Codes:
- `400` - Bad Request (validation errors, invalid input)
- `404` - Not Found (endpoint doesn't exist)
- `405` - Method Not Allowed (wrong HTTP method)
- `500` - Internal Server Error (unexpected errors)
- `503` - Service Unavailable (database connection issues)

---

## Validation Rules

### Candidate Profile Validation:

1. **Skills** (required)
   - Must be an array of strings
   - At least one skill required
   - Empty strings are removed
   - Whitespace is trimmed

2. **Location** (optional)
   - Must be a string
   - Whitespace is trimmed

3. **Eligibility** (optional)
   - Must be a string
   - Whitespace is trimmed

4. **Degree** (optional)
   - Must be a string
   - Whitespace is trimmed

5. **Sector** (optional)
   - Must be a string
   - Whitespace is trimmed

### Query Parameters:

1. **top_n**
   - Must be an integer
   - Range: 1-100
   - Default: 10

---

## Examples

### Example 1: Basic Request

```bash
curl -X POST http://localhost:5000/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "Skills": ["Python", "Flask"]
  }'
```

### Example 2: Request with All Fields

```bash
curl -X POST http://localhost:5000/recommend?top_n=5 \
  -H "Content-Type: application/json" \
  -d '{
    "Skills": ["Python", "Flask", "MongoDB"],
    "Location": "Remote",
    "Eligibility": "3rd year",
    "Degree": "B.Tech",
    "Sector": "Technology"
  }'
```

### Example 3: Health Check

```bash
curl http://localhost:5000/health
```

---

## Rate Limiting

Currently, there are no rate limits implemented. This may change in future versions.

---

## CORS Configuration

The API supports CORS for the following origins (configurable via environment variables):
- `http://localhost:8080`
- `http://localhost:5173`

To add more origins, update the `ALLOWED_ORIGINS` environment variable in `.env`:
```
ALLOWED_ORIGINS=http://localhost:8080,http://localhost:5173,https://your-domain.com
```

---

## Environment Variables

Required environment variables:
- `MONGO_CONNECTION_STRING` - MongoDB connection URI
- `MONGO_DB_NAME` - MongoDB database name

Optional environment variables:
- `ALLOWED_ORIGINS` - Comma-separated list of allowed CORS origins (default: `http://localhost:8080,http://localhost:5173`)
- `PORT` - Server port (default: `5000`)
- `FLASK_DEBUG` - Enable debug mode (default: `False`)

---

## Recommendation Algorithm

The system uses a rule-based recommendation algorithm that:

1. Matches candidate skills with internship requirements
2. Calculates a match score based on number of matching skills
3. Sorts results by match score (highest first)
4. Returns top N recommendations

Future versions may include ML-based ranking for improved recommendations.

---

## Support

For issues or questions, please open an issue on the GitHub repository.
