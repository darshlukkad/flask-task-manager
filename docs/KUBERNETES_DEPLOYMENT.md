# Kubernetes Deployment Guide

This guide provides step-by-step instructions for deploying the Flask Task Manager microservices application on Kubernetes.

## Prerequisites

- **Docker**: For building container images
- **kind**: Kubernetes in Docker (or alternative: minikube, k3s, Docker Desktop)
- **kubectl**: Kubernetes command-line tool

### Install Prerequisites

**macOS**:
```bash
brew install kind kubectl
```

**Linux**:
```bash
# kind
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.30.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind

# kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
```

## Quick Start (Automated)

Use the automated deployment script:

```bash
# Make script executable
chmod +x deploy.sh

# Run deployment
./deploy.sh
```

This script will:
1. Check prerequisites
2. Create kind cluster
3. Build Docker images
4. Load images into kind
5. Apply Kubernetes manifests
6. Verify deployment

**Total time**: ~2-3 minutes

## Manual Deployment Steps

If you prefer manual deployment or need to troubleshoot:

### Step 1: Create kind Cluster

```bash
kind create cluster --name task-manager --config kubernetes/kind-config.yaml
```

### Step 2: Build Docker Images

```bash
# Backend API
docker build -t flask-task-manager-backend:latest ./backend-api

# Frontend
docker build -t flask-task-manager-frontend:latest ./frontend
```

### Step 3: Load Images into kind

```bash
kind load docker-image flask-task-manager-backend:latest --name task-manager
kind load docker-image flask-task-manager-frontend:latest --name task-manager
```

### Step 4: Apply Kubernetes Manifests

```bash
# Namespace and configuration
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/configmap.yaml
kubectl apply -f kubernetes/secret.yaml

# Storage
kubectl apply -f kubernetes/postgres-pvc.yaml

# Database
kubectl apply -f kubernetes/postgres-deployment.yaml
kubectl apply -f kubernetes/postgres-service.yaml

# Wait for database to be ready
kubectl wait --for=condition=ready pod -l app=postgres -n task-manager --timeout=120s

# Backend API
kubectl apply -f kubernetes/backend-deployment.yaml
kubectl apply -f kubernetes/backend-service.yaml

# Wait for backend to be ready
kubectl wait --for=condition=ready pod -l app=backend-api -n task-manager --timeout=120s

# Frontend
kubectl apply -f kubernetes/frontend-deployment.yaml
kubectl apply -f kubernetes/frontend-service.yaml

# Wait for frontend to be ready
kubectl wait --for=condition=ready pod -l app=frontend -n task-manager --timeout=120s
```

### Step 5: Verify Deployment

```bash
# Check all resources
kubectl get all -n task-manager

# Check pods
kubectl get pods -n task-manager

# Check services
kubectl get svc -n task-manager

# Check PVC
kubectl get pvc -n task-manager
```

### Step 6: Access Application

```bash
# Open in browser
open http://localhost:30080

# Or curl
curl http://localhost:30080
```

## Verification

### Check Pod Status

All pods should be in `Running` state:
```bash
kubectl get pods -n task-manager

# Expected output:
# NAME                           READY   STATUS    RESTARTS   AGE
# backend-api-xxx-yyy            1/1     Running   0          5m
# backend-api-xxx-zzz            1/1     Running   0          5m
# frontend-xxx-yyy               1/1     Running   0          5m
# frontend-xxx-zzz               1/1     Running   0          5m
# postgres-xxx-yyy               1/1     Running   0          5m
```

### Check Service Endpoints

```bash
kubectl get endpoints -n task-manager

# All services should have endpoints
```

### Test Backend API

```bash
# Port-forward to backend
kubectl port-forward -n task-manager svc/backend-api 5000:5000 &

# Health check
curl http://localhost:5000/health

# List tasks
curl http://localhost:5000/api/tasks

# Create a task
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Task", "priority": "high"}'
```

### Test Frontend

```bash
# Access via NodePort
open http://localhost:30080

# Or port-forward
kubectl port-forward -n task-manager svc/frontend 8080:8080
open http://localhost:8080
```

### View Logs

```bash
# Backend logs
kubectl logs -n task-manager -l app=backend-api --tail=50

# Frontend logs
kubectl logs -n task-manager -l app=frontend --tail=50

# Database logs
kubectl logs -n task-manager -l app=postgres --tail=50

# Follow logs
kubectl logs -n task-manager -l app=backend-api -f
```

## Troubleshooting

### Pods Not Starting

```bash
# Describe pod for details
kubectl describe pod -n task-manager <pod-name>

# Check events
kubectl get events -n task-manager --sort-by='.lastTimestamp'
```

### Database Connection Issues

```bash
# Check if database is ready
kubectl get pod -n task-manager -l app=postgres

# Test database connection
kubectl exec -n task-manager deployment/postgres -- \
  psql -U taskuser -d taskmanager -c "SELECT 1"

# Check database logs
kubectl logs -n task-manager -l app=postgres --tail=100
```

### Image Pull Errors

If using kind, ensure images are loaded:
```bash
kind load docker-image flask-task-manager-backend:latest --name task-manager
kind load docker-image flask-task-manager-frontend:latest --name task-manager
```

### Port Already in Use

If port 30080 is already in use:
```bash
# Change port in frontend-service.yaml
# Or use port-forward instead
kubectl port-forward -n task-manager svc/frontend 8080:8080
```

## Scaling

### Scale Deployments

```bash
# Scale frontend to 3 replicas
kubectl scale deployment/frontend -n task-manager --replicas=3

# Scale backend to 4 replicas
kubectl scale deployment/backend-api -n task-manager --replicas=4

# Verify scaling
kubectl get pods -n task-manager
```

### Auto-scaling (HPA)

```bash
# Create HPA for backend
kubectl autoscale deployment backend-api -n task-manager \
  --cpu-percent=70 --min=2 --max=10

# Check HPA status
kubectl get hpa -n task-manager
```

## Updates

### Update Application

After code changes:

```bash
# Rebuild images
docker build -t flask-task-manager-backend:latest ./backend-api
docker build -t flask-task-manager-frontend:latest ./frontend

# Load into kind
kind load docker-image flask-task-manager-backend:latest --name task-manager
kind load docker-image flask-task-manager-frontend:latest --name task-manager

# Restart deployments
kubectl rollout restart deployment/backend-api -n task-manager
kubectl rollout restart deployment/frontend -n task-manager

# Check rollout status
kubectl rollout status deployment/backend-api -n task-manager
kubectl rollout status deployment/frontend -n task-manager
```

## Cleanup

### Delete Application

```bash
# Delete namespace (removes all resources)
kubectl delete namespace task-manager
```

### Delete Cluster

```bash
# Delete kind cluster
kind delete cluster --name task-manager
```

## Deploying to Cloud

### Google Kubernetes Engine (GKE)

```bash
# Create cluster
gcloud container clusters create task-manager --num-nodes=3

# Build and push images
docker tag flask-task-manager-backend:latest gcr.io/PROJECT_ID/backend:latest
docker tag flask-task-manager-frontend:latest gcr.io/PROJECT_ID/frontend:latest
docker push gcr.io/PROJECT_ID/backend:latest
docker push gcr.io/PROJECT_ID/frontend:latest

# Update image names in deployments
# Apply manifests
kubectl apply -f kubernetes/
```

### Amazon EKS

```bash
# Create cluster
eksctl create cluster --name task-manager --nodes 3

# Push to ECR
aws ecr create-repository --repository-name flask-task-manager-backend
aws ecr create-repository --repository-name flask-task-manager-frontend

# Tag and push
docker tag flask-task-manager-backend:latest ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/flask-task-manager-backend:latest
docker push ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/flask-task-manager-backend:latest

# Update image names and apply
kubectl apply -f kubernetes/
```

### Azure AKS

```bash
# Create cluster
az aks create --resource-group myResourceGroup --name task-manager --node-count 3

# Create ACR
az acr create --resource-group myResourceGroup --name myregistry --sku Basic

# Push images
docker tag flask-task-manager-backend:latest myregistry.azurecr.io/backend:latest
docker push myregistry.azurecr.io/backend:latest

# Apply manifests
kubectl apply -f kubernetes/
```

## Monitoring

### Install Prometheus & Grafana

```bash
# Add Helm repository
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install Prometheus
helm install prometheus prometheus-community/kube-prometheus-stack -n task-manager

# Access Grafana
kubectl port-forward -n task-manager svc/prometheus-grafana 3000:80
```

### View Metrics

```bash
# Install metrics-server (if not present)
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# View pod metrics
kubectl top pods -n task-manager

# View node metrics
kubectl top nodes
```

## Security Best Practices

1. **Use External Secret Manager** (Vault, AWS Secrets Manager)
2. **Enable Network Policies** to restrict traffic
3. **Use RBAC** for access control
4. **Scan images** for vulnerabilities
5. **Enable Pod Security Standards**
6. **Use TLS** for all communications
7. **Regular updates** of base images and dependencies

## Next Steps

- Set up CI/CD pipeline
- Add Ingress controller
- Configure backups for PostgreSQL
- Implement monitoring and alerting
- Add authentication and authorization
- Configure horizontal pod autoscaling

## Support

For issues or questions:
- Check [Architecture Documentation](docs/ARCHITECTURE.md)
- View [Walkthrough](../walkthrough.md)
- Open an issue on GitHub

---

**Last Updated**: 2025-11-29
