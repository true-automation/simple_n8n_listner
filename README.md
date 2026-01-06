# Math & Chat API

A FastAPI application that performs math operations and provides AI-powered chat responses using the Bytez GLM-4.6V-Flash model.

## Features

- ✅ Addition and multiplication of two numbers
- ✅ AI-powered chat responses using GLM-4.6V-Flash
- ✅ Returns JSON responses
- ✅ FastAPI with automatic API documentation
- ✅ Docker support
- ✅ Ready for Coolify deployment

## API Endpoints

### POST /calculate
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

### POST /chat
Send a question to the AI chat model and get a response.

**Request Body:**
```json
{
  "question": "What is the capital of France?"
}
```

**Response:**
```json
{
  "answer": "The capital of France is Paris.",
  "error": null
}
```

### GET /
Root endpoint with API information.

### GET /health
Health check endpoint for monitoring.

## Local Development

### Prerequisites
- Python 3.11+
- pip
- Bytez API key (default included, or get yours from https://bytez.com)

### Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# (Optional) Set your Bytez API key
export BYTEZ_API_KEY=your_api_key_here

# Run the application
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Docker Deployment

### Build and run locally
```bash
# Build the image
docker build -t math-chat-api .

# Run the container
docker run -p 8000:8000 -e BYTEZ_API_KEY=your_key_here math-chat-api
```

Or use docker-compose:
```bash
# (Optional) Create .env file with your API key
cp .env.example .env
# Edit .env and set your BYTEZ_API_KEY

# Start the service
docker-compose up -d
```

## Dokploy / Coolify Deployment

### Prerequisites
- Dokploy or Coolify installed on your VPS
- Git repository set up

### Quick Steps

1. **Push to Git:**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-git-repo-url>
git push -u origin main
```

2. **In Dokploy/Coolify Dashboard:**
   - Click "New Resource" or "+ Add Service" → "Application"
   - Select "Public Repository" or connect your Git account
   - Paste your repository URL
   - Choose the branch (main/master)
   - Auto-detect Dockerfile
   - Set the port to **8000**
   - Add environment variable: `BYTEZ_API_KEY` (optional, default provided)
   - Click "Deploy"

3. **Domain Setup:**
   - Configure your domain/subdomain
   - SSL will be automatically configured

### Detailed Guides

- **For Dokploy:** See [DOKPLOY_DEPLOYMENT.md](DOKPLOY_DEPLOYMENT.md)
- **For Coolify:** See [COOLIFY_DEPLOYMENT.md](COOLIFY_DEPLOYMENT.md)

### Configuration

The application uses:
- **Port:** 8000
- **Health Check:** `/health` endpoint
- **Build Method:** Dockerfile

Both platforms will automatically:
- Build the Docker image
- Deploy the container
- Set up reverse proxy
- Configure SSL certificates
- Monitor the application health

## Testing the API

### Using curl:
```bash
# Test math calculation
curl -X POST http://localhost:8000/calculate \
  -H "Content-Type: application/json" \
  -d '{"x": 10, "y": 5}'

# Test chat
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Hello, how are you?"}'

# Health check
curl http://localhost:8000/health
```

### Using Python:
```python
import requests

# Test calculation
response = requests.post(
    "http://localhost:8000/calculate",
    json={"x": 10, "y": 5}
)
print(response.json())
# Output: {'sum': 15.0, 'mult': 50.0}

# Test chat
response = requests.post(
    "http://localhost:8000/chat",
    json={"question": "What is Python?"}
)
print(response.json())
# Output: {'answer': '...', 'error': None}
```

### Using the test script:
```bash
python test_api.py
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `BYTEZ_API_KEY` | API key for Bytez chat model | Included default key |
| `ENVIRONMENT` | Application environment | `production` |

## Project Structure

```
.
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
├── .dockerignore          # Docker ignore file
├── .gitignore            # Git ignore file
├── .env.example          # Environment variables example
├── test_api.py           # API test suite
├── setup.sh              # Setup script
├── README.md             # This file
└── COOLIFY_DEPLOYMENT.md # Coolify deployment guide
```

## API Models

### ChatRequest
```python
{
    "question": str  # The question to ask the AI
}
```

### ChatResponse
```python
{
    "answer": Optional[str],  # AI's response
    "error": Optional[str]    # Error message if any
}
```

### Numbers
```python
{
    "x": float,  # First number
    "y": float   # Second number
}
```

### Result
```python
{
    "sum": float,   # Sum of x and y
    "mult": float   # Product of x and y
}
```

## Troubleshooting

### Chat endpoint returns errors
- Verify your `BYTEZ_API_KEY` is valid
- Check your internet connection (API requires external access)
- Check the API logs for detailed error messages

### Port already in use
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>
```

## License

MIT