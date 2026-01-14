# Hit Counter API

A simple REST API service to count page visits. Built with Flask, containerized with Docker, and deployed on Kubernetes.

## Features

- ✅ REST API for managing pages and counting hits
- ✅ Prometheus metrics exposure
- ✅ Structured JSON logging
- ✅ Basic request tracing
- ✅ Docker containerization
- ✅ Kubernetes deployment ready
- ✅ CI/CD pipeline with GitHub Actions
- ✅ Security scanning (SAST + DAST)

## Architecture

The application exposes a Flask-based REST API that handles page CRUD
operations and a hit counter. Data is stored in-memory for simplicity.
Metrics are exposed via a `/metrics` endpoint and scraped by Prometheus.

flowchart LR
    Client[Client<br/>(Browser / HTTP User)]

    API[Flask API<br/>• Pages CRUD<br/>• Hit Counter]

    Memory[(In-Memory Data Store<br/>Python dict / cache)]

    Prometheus[Prometheus Server]

    Client -->|HTTP Requests| API
    API --> Memory
    API -->|/metrics| Prometheus


## Requirements

- Python 3.11+
- Docker (optional)
- Kubernetes/Minikube (for production)
- pip

## Installation & Setup

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/devops-hit-counter-api.git
cd devops-hit-counter-api
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
pip install pytest
```

4. Run the API:
```bash
python -m app.main
```

5. Test:
```bash
pytest tests/ -v
```

API will be available at `http://localhost:5000`

### Using Docker

1. Build the image:
```bash
docker build -t hit-counter-api:latest .
```

2. Run the container:
```bash
docker run -p 5000:5000 hit-counter-api:latest
```

3. Using docker-compose:
```bash
docker-compose up -d
docker-compose logs -f
```

### Kubernetes Deployment

1. Start Minikube:
```bash
minikube start
eval $(minikube docker-env)
```

2. Build and deploy:
```bash
docker build -t hit-counter-api:latest .
kubectl apply -f kubernetes/
```

3. Wait for pods to be ready:
```bash
kubectl wait --for=condition=Ready pod -l app=hit-counter-api --timeout=300s
```

4. Get the service URL:
```bash
minikube service hit-counter-api --url
```

## API Endpoints

### Health Check
```bash
GET /health

Response (200):
{
  "status": "healthy"
}
```

### List All Pages
```bash
GET /api/pages

Response (200):
[
  {
    "id": 1,
    "name": "Homepage",
    "hits": 42,
    "created_at": "2024-01-10T15:30:00.123456"
  }
]
```

### Create a Page
```bash
POST /api/pages
Content-Type: application/json

{
  "name": "About Page"
}

Response (201):
{
  "id": 2,
  "name": "About Page",
  "hits": 0,
  "created_at": "2024-01-10T15:31:00.123456"
}
```

### Get Page Hit Count
```bash
GET /api/pages/{id}/hits

Response (200):
{
  "hits": 42
}
```

### Increment Hit Count
```bash
POST /api/pages/{id}/hit

Response (200):
{
  "id": 1,
  "name": "Homepage",
  "hits": 43,
  "created_at": "2024-01-10T15:30:00.123456"
}
```

### Prometheus Metrics
```bash
GET /metrics

Response (200):
# HELP api_requests_total Total API requests
# TYPE api_requests_total counter
api_requests_total{endpoint="pages",method="POST"} 5.0
...
```

## Testing

### Unit Tests
```bash
pytest tests/ -v
```

### Manual API Tests
```bash
# Health check
curl http://localhost:5000/health

# Create page
curl -X POST http://localhost:5000/api/pages \
  -H "Content-Type: application/json" \
  -d '{"name": "Homepage"}'

# Get pages
curl http://localhost:5000/api/pages

# Increment hit
curl -X POST http://localhost:5000/api/pages/1/hit

# Get metrics
curl http://localhost:5000/metrics
```

## Observability

### Metrics
- Prometheus-compatible metrics available at `/metrics`
- Tracks: request count, request duration, page hits

### Logging
- Structured JSON logging for all requests
- Includes: method, path, status, duration, request_id
- Sample log:
```json
{
  "message": "Incoming request",
  "method": "POST",
  "path": "/api/pages/1/hit",
  "request_id": "req-1704878400.123"
}
```

### Tracing
- Each request includes unique `X-Request-ID` header
- Propagated through request lifecycle
- Visible in logs for correlation

## Security

### SAST (Static Application Security Testing)
- Bandit runs on every commit via GitHub Actions
- Scans Python code for security vulnerabilities
- Report available in Actions artifacts

### DAST (Dynamic Application Security Testing)
- Basic runtime security checks
- Input validation testing
- Error handling verification
- Runs after Docker build in CI pipeline

### Best Practices Implemented
- Input validation on POST requests
- Proper error handling (404, 400, 500)
- No sensitive data exposure
- Security headers (basic)

## CI/CD Pipeline

Automated pipeline using GitHub Actions:
1. ✅ Code checkout
2. ✅ Python setup
3. ✅ Dependency installation
4. ✅ Unit tests execution
5. ✅ SAST security scan (Bandit)
6. ✅ Docker image build
7. ✅ Container integration tests
8. ✅ DAST security checks
9. ✅ Artifact uploads

Triggered on: push to main/develop, pull requests

View details: `.github/workflows/ci.yml`

## Project Structure

devops-hit-counter-api/
├── app/
│   ├── main.py                 # Flask application (< 150 lines)
│   └── static/
│       ├── dashboard.html      # Simple monitoring dashboard
│       └── style.css           # Dashboard styles
├── tests/
│   └── test_app.py             # Unit tests
├── kubernetes/
│   ├── deployment.yaml         # Kubernetes Deployment
│   └── service.yaml            # Kubernetes Service
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI pipeline
├── Dockerfile                  # Docker image definition
├── docker-compose.yml          # Docker Compose setup
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
└── .gitignore                  # Git ignore rules

## Lessons Learned

1. **DevOps as a Culture**: DevOps is not just tools; it's about collaboration and continuous improvement.
2. **Infrastructure as Code**: K8s manifests make deployments repeatable and versionable.
3. **Observability Matters**: Metrics, logs, and traces are crucial for production systems.
4. **Security First**: SAST/DAST should be in every pipeline, not an afterthought.
5. **Containerization Benefits**: Docker ensures consistency across environments.
6. **Automation**: CI/CD reduces manual errors and enables rapid iteration.

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make changes and write tests
3. Commit: `git commit -