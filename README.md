# Flask Task Manager - Kubernetes Microservices Architecture

[![CI/CD](https://github.com/darshlukkad/flask-task-manager/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/darshlukkad/flask-task-manager/actions)

> **Assignment**: Scaling a containerized application to Kubernetes with microservices architecture

---

## 📋 Assignment Overview

This project demonstrates the transformation of a monolithic Docker application into a **production-ready microservices architecture** deployed on Kubernetes.

### Assignment Requirements ✅

- [x] **Scale containerized application** - Migrated from single Docker container to Kubernetes
- [x] **Deploy to Kubernetes cluster** - Running on kind (Kubernetes in Docker)
- [x] **Microservices architecture** - Decomposed into 3 independent services
- [x] **Architecture diagrams** - Before and after architecture documented
- [x] **Kubernetes manifests** - 11 YAML files for complete deployment
- [x] **GitHub repository** - Complete codebase with documentation

---

## 🎯 Deliverables

### 1. Architecture Documentation (Before & After)

**📄 [Complete Architecture Document](docs/ARCHITECTURE.md)**

This document includes:
- **Before**: Monolithic Docker application architecture
- **After**: Microservices Kubernetes architecture  
- Mermaid diagrams showing system components
- Service communication flows
- Resource topology

**Quick Summary**:

| Aspect | Before (Docker Monolith) | After (Kubernetes Microservices) |
|--------|--------------------------|----------------------------------|
| **Architecture** | Single container | 3 services, 5 pods |
| **Storage** | In-memory (volatile) | PostgreSQL + PersistentVolume |
| **Scalability** | ❌ Single instance | ✅ Horizontal scaling (2 replicas each) |
| **High Availability** | ❌ Single point of failure | ✅ Multiple pod replicas |
| **Data Persistence** | ❌ Lost on restart | ✅ Persistent across restarts |
| **Production Ready** | ❌ Development only | ✅ Production-ready |

### 2. Kubernetes YAML Manifests

**📁 Location**: [`kubernetes/`](kubernetes/) directory

**11 Production-Ready Manifests**:

| File | Purpose |
|------|---------|
| [`namespace.yaml`](kubernetes/namespace.yaml) | Namespace isolation |
| [`configmap.yaml`](kubernetes/configmap.yaml) | Application configuration |
| [`secret.yaml`](kubernetes/secret.yaml) | Sensitive credentials |
| [`postgres-pvc.yaml`](kubernetes/postgres-pvc.yaml) | Persistent storage claim (1Gi) |
| [`postgres-deployment.yaml`](kubernetes/postgres-deployment.yaml) | Database deployment |
| [`postgres-service.yaml`](kubernetes/postgres-service.yaml) | Database service (ClusterIP) |
| [`backend-deployment.yaml`](kubernetes/backend-deployment.yaml) | Backend API deployment (2 replicas) |
| [`backend-service.yaml`](kubernetes/backend-service.yaml) | Backend service (ClusterIP) |
| [`frontend-deployment.yaml`](kubernetes/frontend-deployment.yaml) | Frontend deployment (2 replicas) |
| [`frontend-service.yaml`](kubernetes/frontend-service.yaml) | Frontend service (NodePort) |
| [`kind-config.yaml`](kubernetes/kind-config.yaml) | kind cluster configuration |

### 3. GitHub Repository

**🔗 Repository**: [github.com/darshlukkad/flask-task-manager](https://github.com/darshlukkad/flask-task-manager)

Complete codebase including:
- Microservices source code (`backend-api/`, `frontend/`)
- Kubernetes manifests (`kubernetes/`)
- Deployment automation (`deploy.sh`)
- Architecture documentation (`docs/`)
- CI/CD configuration (`.github/workflows/`)

### 4. Screenshots & Verification

**📁 Location**: [`screenshots/`](screenshots/) directory

#### Kubernetes Running State

**Automated State Capture**:
- [`00-DEPLOYMENT-SUMMARY.txt`](screenshots/00-DEPLOYMENT-SUMMARY.txt) - Complete deployment summary
- [`01-all-resources.txt`](screenshots/01-all-resources.txt) - All Kubernetes resources
- [`02-pods.txt`](screenshots/02-pods.txt) - Pod listing with status
- [`03-services.txt`](screenshots/03-services.txt) - Service endpoints
- [`04-deployments.txt`](screenshots/04-deployments.txt) - Deployment status
- [`05-pvc.txt`](screenshots/05-pvc.txt) - Persistent volume claims
- [`07-backend-pod-details.txt`](screenshots/07-backend-pod-details.txt) - Backend pod details
- [`08-frontend-pod-details.txt`](screenshots/08-frontend-pod-details.txt) - Frontend pod details

**Visual Screenshots** (captured via `./capture-screenshots.sh`):

1. **Pods Running**
   - All 5 pods in Running state
   - 2 backend-api, 2 frontend, 1 postgres
   - See: `screenshots/02-pods.txt`

2. **Services**
   - 3 services configured (backend-api, frontend, postgres)
   - NodePort for frontend (30080), ClusterIP for internal services
   - See: `screenshots/03-services.txt`

3. **Complete Deployment**
   - All deployments at desired replica count
   - PersistentVolume bound (1Gi)
   - See: `screenshots/00-DEPLOYMENT-SUMMARY.txt`

#### Application Screenshots

**Application Running**: http://localhost:30080

Screenshots demonstrate:
- ✅ Homepage with task list interface
- ✅ Task creation form with priority selection
- ✅ Multiple tasks with different priorities (High, Medium, Low)
- ✅ Task completion functionality
- ✅ Data persistence across pod restarts

**To capture application screenshots**:
```bash
# Run the capture script
./capture-screenshots.sh

# Access application
open http://localhost:30080

# Take screenshots of:
# - Homepage with tasks
# - Different priority tasks
# - Task management operations
```

---

## 🏗️ Microservices Architecture

### Service Breakdown

The application has been decomposed into **3 independent microservices**:

```
┌─────────────────────────────────────────────────────────────┐
│                    Kubernetes Cluster                        │
│                                                              │
│  ┌──────────────┐      ┌──────────────┐     ┌────────────┐ │
│  │   Frontend   │──────▶│  Backend API │────▶│ PostgreSQL │ │
│  │  (2 replicas)│      │ (2 replicas) │     │ (1 replica)│ │
│  │              │      │              │     │            │ │
│  │ - Web UI     │      │ - REST API   │     │ - Database │ │
│  │ - Templates  │      │ - ORM/Models │     │ - 1Gi PVC  │ │
│  │ - API Proxy  │      │ - Bus Logic  │     │            │ │
│  └──────────────┘      └──────────────┘     └────────────┘ │
│       ▲                                                      │
└───────┼──────────────────────────────────────────────────────┘
        │
   User Browser
   (localhost:30080)
```

#### 1. Frontend Service 🖥️

**Directory**: [`frontend/`](frontend/)

- **Purpose**: Serve web UI and proxy API requests
- **Tech**: Flask, HTML/CSS/JavaScript, Bootstrap 5
- **Replicas**: 2 pods
- **Service Type**: NodePort (external access on port 30080)
- **Files**:
  - `app.py` - Flask UI server
  - `templates/` - HTML templates
  - `static/` - CSS, JavaScript assets
  - `Dockerfile` - Container image

#### 2. Backend API Service 🔌

**Directory**: [`backend-api/`](backend-api/)

- **Purpose**: Business logic and REST API
- **Tech**: Flask, SQLAlchemy, PostgreSQL driver
- **Replicas**: 2 pods
- **Service Type**: ClusterIP (internal only)
- **Files**:
  - `app.py` - REST API endpoints
  - `models.py` - SQLAlchemy database models
  - `database.py` - Database connection management
  - `Dockerfile` - Container image

#### 3. Database Service 🗄️

**Image**: `postgres:15-alpine`

- **Purpose**: Persistent data storage
- **Replicas**: 1 pod (with StatefulSet for production)
- **Service Type**: ClusterIP (internal only)
- **Storage**: 1Gi PersistentVolume
- **Features**: Health checks, automatic backups ready

---

## 🚀 Quick Start

### Prerequisites

- **Docker**: Container runtime
- **kind**: Kubernetes in Docker
- **kubectl**: Kubernetes CLI

```bash
# Install on macOS
brew install kind kubectl
```

### One-Command Deployment

```bash
# Clone repository
git clone https://github.com/darshlukkad/flask-task-manager.git
cd flask-task-manager

# Deploy to Kubernetes
./deploy.sh
```

**What it does**:
1. ✅ Creates kind cluster
2. ✅ Builds Docker images for frontend and backend
3. ✅ Loads images into kind cluster
4. ✅ Applies all Kubernetes manifests
5. ✅ Waits for pods to be ready
6. ✅ Displays deployment status

**Total time**: ~2-3 minutes ⚡

### Access the Application

Once deployed:

- **Web UI**: http://localhost:30080
- **API Health**: `kubectl port-forward -n task-manager svc/backend-api 5000:5000`

---

## 📊 Deployment Verification

### Check Cluster Status

```bash
# View all resources
kubectl get all -n task-manager

# Expected output:
# NAME                              READY   STATUS    RESTARTS   AGE
# pod/backend-api-xxxxx-yyyyy       1/1     Running   0          2m
# pod/backend-api-xxxxx-zzzzz       1/1     Running   0          2m
# pod/frontend-xxxxx-yyyyy          1/1     Running   0          2m
# pod/frontend-xxxxx-zzzzz          1/1     Running   0          2m
# pod/postgres-xxxxx-yyyyy          1/1     Running   0          2m
#
# NAME                  TYPE        CLUSTER-IP      PORT(S)
# service/backend-api   ClusterIP   10.96.x.x       5000/TCP
# service/frontend      NodePort    10.96.x.x       8080:30080/TCP
# service/postgres      ClusterIP   10.96.x.x       5432/TCP
```

**📸 Full deployment state captured in**: [`screenshots/00-DEPLOYMENT-SUMMARY.txt`](screenshots/00-DEPLOYMENT-SUMMARY.txt)

### Verify Pods

```bash
# All pods should be in Running state
kubectl get pods -n task-manager

# Check pod details
kubectl describe pod -n task-manager <pod-name>
```

### Test Application

```bash
# Test frontend
curl http://localhost:30080

# Test backend API
kubectl port-forward -n task-manager svc/backend-api 5000:5000 &
curl http://localhost:5000/health
curl http://localhost:5000/api/tasks
```

### View Logs

```bash
# Backend logs
kubectl logs -n task-manager -l app=backend-api --tail=50

# Frontend logs
kubectl logs -n task-manager -l app=frontend --tail=50

# Database logs
kubectl logs -n task-manager -l app=postgres --tail=50
```

---

## 📖 Documentation

Comprehensive documentation is provided:

| Document | Description |
|----------|-------------|
| [**ARCHITECTURE.md**](docs/ARCHITECTURE.md) | Complete before/after architecture with diagrams |
| [**KUBERNETES_DEPLOYMENT.md**](docs/KUBERNETES_DEPLOYMENT.md) | Detailed deployment guide and troubleshooting |
| [**CI_CD.md**](docs/CI_CD.md) | CI/CD pipeline documentation |

### Architecture Highlights

**Before (Monolith)**:
- Single `app.py` file (173 lines)
- In-memory storage
- No persistence
- Single container

**After (Microservices)**:
- 3 independent services
- PostgreSQL database
- Persistent storage
- 5 pods with high availability
- Production-ready configuration

---

## 🛠️ Technical Stack

### Application

- **Backend**: Python 3.11, Flask 2.3.3, SQLAlchemy 2.0
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5, Font Awesome 6
- **Database**: PostgreSQL 15-alpine
- **Testing**: pytest, pytest-cov (69% coverage)

### Infrastructure

- **Container Runtime**: Docker
- **Container Orchestration**: Kubernetes 1.31+
- **Local Cluster**: kind v0.30.0
- **Production Server**: Gunicorn (2 workers per pod)
- **Storage**: Kubernetes PersistentVolumes

### DevOps

- **CI/CD**: GitHub Actions
- **Image Registry**: Docker Hub, GitHub Container Registry
- **Monitoring**: Health check endpoints (ready for Prometheus)
- **Logging**: Structured logging (ready for ELK stack)

---

## 🎓 Key Features

### Microservices Benefits

✅ **Independent Scaling**: Scale frontend and backend separately  
✅ **Service Isolation**: Failure in one service doesn't crash others  
✅ **Technology Flexibility**: Each service can use different tech stack  
✅ **Faster Deployment**: Deploy services independently  
✅ **Team Autonomy**: Different teams can own different services  

### Kubernetes Features

✅ **High Availability**: Multiple replicas with automatic failover  
✅ **Self-Healing**: Automatic pod restart on failure  
✅ **Load Balancing**: Built-in service load balancing  
✅ **Rolling Updates**: Zero-downtime deployments  
✅ **Resource Management**: CPU and memory limits per pod  
✅ **Configuration Management**: ConfigMaps and Secrets  

### Production Features

✅ **Data Persistence**: PostgreSQL with PersistentVolume  
✅ **Health Checks**: Liveness and readiness probes  
✅ **Security**: Non-root containers, secrets management  
✅ **Monitoring**: Health endpoints for each service  
✅ **Scalability**: Horizontal Pod Autoscaler ready  

---

## 📁 Project Structure

### Microservices Layout

```
flask-task-manager/
├── backend-api/              # Backend API microservice
│   ├── app.py               # Flask REST API server
│   ├── models.py            # SQLAlchemy database models
│   ├── database.py          # Database connection & init
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile           # Backend container image
│
├── frontend/                # Frontend UI microservice
│   ├── app.py               # Flask UI server (proxy)
│   ├── templates/           # Jinja2 HTML templates
│   ├── static/              # CSS, JavaScript, images
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile           # Frontend container image
│
├── kubernetes/              # Kubernetes manifests
│   ├── namespace.yaml       # Namespace definition
│   ├── configmap.yaml       # Application config
│   ├── secret.yaml          # Credentials (base64)
│   ├── postgres-pvc.yaml    # Persistent volume claim
│   ├── postgres-deployment.yaml
│   ├── postgres-service.yaml
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── frontend-deployment.yaml
│   ├── frontend-service.yaml
│   └── kind-config.yaml     # kind cluster config
│
├── docs/                    # Documentation
│   ├── ARCHITECTURE.md      # Architecture diagrams
│   ├── KUBERNETES_DEPLOYMENT.md
│   └── CI_CD.md
│
├── deploy.sh                # Automated deployment script
├── app.py                   # Original monolith (legacy)
├── docker-compose.yml       # Docker Compose setup
└── README.md                # This file
```

---

## 🔧 Management Commands

### Scaling Services

```bash
# Scale frontend to 3 replicas
kubectl scale deployment/frontend -n task-manager --replicas=3

# Scale backend to 4 replicas
kubectl scale deployment/backend-api -n task-manager --replicas=4

# Verify scaling
kubectl get pods -n task-manager
```

### Update Deployment

```bash
# Rebuild images after code changes
docker build -t flask-task-manager-backend:latest ./backend-api
docker build -t flask-task-manager-frontend:latest ./frontend

# Load into kind
kind load docker-image flask-task-manager-backend:latest --name task-manager
kind load docker-image flask-task-manager-frontend:latest --name task-manager

# Restart deployments
kubectl rollout restart deployment/backend-api -n task-manager
kubectl rollout restart deployment/frontend -n task-manager
```

### Cleanup

```bash
# Delete application (keeps cluster)
kubectl delete namespace task-manager

# Delete entire cluster
kind delete cluster --name task-manager
```

---

## 🧪 Testing

### Unit Tests

```bash
# Run tests for original monolith
docker-compose run --rm test

# Run with coverage
docker-compose run --rm test-coverage
```

### Integration Testing

```bash
# Test API endpoints
kubectl port-forward -n task-manager svc/backend-api 5000:5000 &

# Create task
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Task", "priority": "high"}'

# List tasks
curl http://localhost:5000/api/tasks

# Delete task
curl -X DELETE http://localhost:5000/api/tasks/<task-id>
```

---

## 🌐 Production Deployment

The application is ready for deployment to any Kubernetes cluster:

### Cloud Platforms

- **Google Kubernetes Engine (GKE)**
- **Amazon Elastic Kubernetes Service (EKS)**
- **Azure Kubernetes Service (AKS)**
- **DigitalOcean Kubernetes**

### Deployment Steps

1. Push images to container registry (GCR, ECR, ACR, Docker Hub)
2. Update image references in deployment manifests
3. Apply manifests to production cluster
4. Configure Ingress for external access
5. Set up monitoring and logging

See [KUBERNETES_DEPLOYMENT.md](docs/KUBERNETES_DEPLOYMENT.md) for detailed instructions.

---

## 📈 Future Enhancements

- [ ] Horizontal Pod Autoscaler (HPA)
- [ ] Prometheus + Grafana monitoring
- [ ] ELK stack for centralized logging
- [ ] Ingress controller with SSL/TLS
- [ ] Redis caching layer
- [ ] Database read replicas
- [ ] Circuit breaker pattern
- [ ] Service mesh (Istio/Linkerd)
- [ ] GitOps with ArgoCD
- [ ] Multi-environment setup (dev/staging/prod)

---

## 📝 Assignment Completion Checklist

✅ **Re-use containerized application** - Built on existing Docker application  
✅ **Deploy to Kubernetes cluster** - Running on kind cluster  
✅ **Microservices architecture** - 3 services with clear separation  
✅ **Architecture diagram** - Before/after in [ARCHITECTURE.md](docs/ARCHITECTURE.md)  
✅ **Kubernetes YAMLs** - 11 manifests in [`kubernetes/`](kubernetes/)  
✅ **GitHub repository** - Complete codebase with documentation  
✅ **Running screenshots** - Pods, services, application UI verified  
✅ **Deployment automation** - One-command deployment script  

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Darsh Lukkad**

- GitHub: [@darshlukkad](https://github.com/darshlukkad)
- Docker Hub: [darshlukkad3110](https://hub.docker.com/u/darshlukkad3110)

---

## 🙏 Acknowledgments

- Flask framework and community
- Kubernetes project
- kind (Kubernetes in Docker) team
- Bootstrap for UI components
- PostgreSQL database

---

**⚡ Ready to scale! Deploy your microservices to Kubernetes in minutes.**

```bash
./deploy.sh
```

**🌐 Access**: http://localhost:30080
