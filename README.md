# Math Operations API

A simple FastAPI application that performs addition and multiplication operations on two numbers via POST requests.

## Features

✅ Addition of two numbers  
✅ Multiplication of two numbers  
✅ Returns JSON response with both results  
✅ FastAPI with automatic API documentation  
✅ Docker support  
✅ Ready for Coolify deployment

## API Endpoints

### POST `/calculate`
Calculate sum and multiplication of two numbers.

**Request Body:**
```json
{
  "x": 10,
  "y": 5
}
```

**Response:**
```json
{
  "sum": 15,
  "mult": 50
}
```

### GET `/`
Root endpoint with API information.

### GET `/health`
Health check endpoint for monitoring.

## Local Development

### Prerequisites
- Python 3.11+
- pip

### Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn main:app --reload
```
The API will be available at http://localhost:8000

### API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Docker Deployment

### Build and run locally
```bash
# Build the image
docker build -t math-api .

# Run the container
docker run -p 8000:8000 math-api
```

Or use docker-compose:
```bash
docker-compose up -d
```

## Coolify Deployment

### Prerequisites
- Coolify installed on your VPS
- Git repository set up

### Steps
1. **Push to Git:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-git-repo-url>
   git push -u origin main
   ```
2. **In Coolify Dashboard:**
   - Click "New Resource" → "Application"
   - Select "Public Repository" or connect your Git account
   - Paste your repository URL
   - Choose the branch (main/master)
   - Coolify will auto-detect the Dockerfile
   - Set the port to 8000
   - Click "Deploy"

3. **Environment Variables (Optional):**
   - In Coolify, you can add environment variables if needed.
   - No required variables for basic operation.

4. **Domain Setup:**
   - In Coolify, configure your domain/subdomain.
   - Coolify will automatically handle SSL with Let's Encrypt.

## Coolify Configuration
The application uses:
- **Port:** 8000
- **Health Check:** `/health` endpoint
- **Build Method:** `Dockerfile`

Coolify will automatically:
- Build the Docker image
- Deploy the container
- Set up reverse proxy
- Configure SSL certificates
- Monitor the application health

## Testing the API

### Using curl:
```bash
# Test calculation
curl -X POST http://localhost:8000/calculate \
  -H "Content-Type: application/json" \
  -d '{"x": 10, "y": 5}'

# Health check
curl http://localhost:8000/health
```

### Using Python:
```python
import requests

response = requests.post(
    "http://localhost:8000/calculate",
    json={"x": 10, "y": 5}
)
print(response.json())
# Output: {'sum': 15.0, 'mult': 50.0}
```

## Project Structure
```
.
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
├── .dockerignore          # Docker ignore file
├── .gitignore            # Git ignore file
└── README.md             # This file
```

## License
MIT
