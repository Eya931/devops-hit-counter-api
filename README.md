# 📊 Hit Counter API - DevOps Project

A complete DevOps project: REST API + Docker + Kubernetes + CI/CD + Security scanning + Observability.

## 🚀 Quick Start

### Local Development

```bash
# Setup
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# Run
python -m app.main

# Test
Invoke-WebRequest -Uri http://localhost:5000/health
Invoke-WebRequest -Uri http://localhost:5000/api/pages
Invoke-WebRequest -Uri -X POST http://localhost:5000/api/pages/home/hit
Invoke-WebRequest -Uri http://localhost:5000/metrics
```

### Docker

```bash
docker build -t hit-counter-api:latest .
docker run -d -p 5000:5000 --name api hit-counter-api:latest
Invoke-WebRequest -Uri http://localhost:5000/health
docker stop api
```

### Kubernetes

```bash
minikube start --driver=docker
minikube docker-env | Invoke-Expression

docker build -t hit-counter-api:latest .
kubectl apply -f kubernetes/
kubectl get pods
kubectl port-forward svc/hit-counter-api 5000:80
# http://localhost:5000
```

## 📡 API Endpoints

```bash
GET  /health                     # Health check
GET  /api/pages                  # List pages
POST /api/pages/<page>/hit       # Add hit
GET  /metrics                    # Prometheus metrics
GET  /                           # Dashboard
```

## 🔧 Tech Stack

- **Backend**: Flask (< 150 lines)
- **Container**: Docker
- **Orchestration**: Kubernetes
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus metrics + JSON logs
- **Security**: Bandit (SAST) + DAST checks
- **Dashboard**: Chart.js visualization

## ✨ Features

✅ REST API with hit counter
✅ Docker containerization with health checks
✅ Kubernetes deployment (2 replicas)
✅ GitHub Actions CI/CD pipeline
✅ Prometheus metrics exposure
✅ Structured JSON logging
✅ Request tracing with unique IDs
✅ Interactive web dashboard
✅ SAST security scanning (Bandit)
✅ DAST runtime security checks

## 📊 Observability

**Metrics** - `http://localhost:5000/metrics`
- `api_requests_total` - Total requests
- `api_request_duration_seconds` - Request latency
- `page_hits_total` - Hits per page

**Logs** - Structured JSON format
```json
{"message": "Incoming request", "method": "GET", "path": "/api/pages", "request_id": "req-XXX"}
```

**Tracing** - Each request has unique `request_id` for correlation

## 🔐 Security

- **SAST**: Bandit scans code for vulnerabilities
- **DAST**: Runtime security checks (input validation, error handling, 404 responses)
- Results available in GitHub Actions Artifacts


## Architecture


The application exposes a Flask-based REST API that handles page CRUD
operations and a hit counter. Data is stored in-memory for simplicity.
Metrics are exposed via a `/metrics` endpoint and scraped by Prometheus.


```text
┌──────────────┐
│    Client    │
│ (Browser /   │
│  HTTP User)  │
└───────┬──────┘
        │ HTTP Requests
        ▼
┌──────────────────────────┐
│        Flask API         │
│--------------------------│
│  • Pages CRUD            │
│  • Hit Counter           │
│  • Prometheus Metrics    │
└───────┬───────────┬──────┘
        │           │
        │           │ /metrics
        │           ▼
        │     ┌──────────────┐
        │     │  Prometheus  │
        │     │   Server     │
        │     └──────────────┘
        │
        ▼
┌──────────────────────────┐
│   In-Memory Data Store   │
│ (Python dict / cache)    │
└──────────────────────────┘
```


## 📁 Project Structure

```text
.
├── app/main.py              # Flask API
├── app/static/dashboard.html # Web dashboard
├── tests/test_app.py        # Unit tests
├── kubernetes/              # K8s manifests
├── .github/workflows/ci.yml # CI/CD pipeline
├── Dockerfile               # Docker image
├── requirements.txt         # Dependencies
└── README.md               # This file
```

## 🔄 CI/CD Pipeline

Push to GitHub → Automatic:
1. ✅ Run tests
2. ✅ SAST scan (Bandit)
3. ✅ Build Docker image
4. ✅ DAST checks
5. ✅ Code quality analysis

View results: GitHub → Actions → Latest workflow

## 📊 Dashboard

Open `http://localhost:5000`

Features:
- Real-time statistics
- Chart.js visualization
- Add hits button
- Auto-refresh every 5s

## 🧪 Testing

```bash
pytest tests/ -v
```

## 🐛 Troubleshooting

**Docker connection fails:**
```bash
minikube docker-env | Invoke-Expression
```

**Pods not starting:**
```bash
kubectl logs -f deployment/hit-counter-api
kubectl describe pod hit-counter-api-xxxxx
```

**API returns 500:**
```bash
# Check encoding='utf-8' in app/main.py line ~59
kubectl rollout restart deployment/hit-counter-api
```

## 📚 Files

- `app/main.py` - Flask API (< 150 lines)
- `requirements.txt` - Python dependencies
- `Dockerfile` - Docker image definition
- `kubernetes/` - Deployment & Service manifests
- `.github/workflows/ci.yml` - CI/CD automation
- `tests/` - Unit tests

## ✅ What's Implemented

- ✅ Backend API functionality
- ✅ GitHub workflow (Issues, PRs, Reviews)
- ✅ CI/CD pipeline
- ✅ Docker containerization
- ✅ Kubernetes deployment
- ✅ Observability (metrics, logs, tracing)
- ✅ Security scanning (SAST + DAST)
- ✅ Documentation
- ✅ Interactive dashboard

---
