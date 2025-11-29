#!/bin/bash
# Deployment script for Flask Task Manager on Kubernetes

set -e  # Exit on error

echo "=================================================="
echo "Flask Task Manager - Kubernetes Deployment Script"
echo "=================================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Check prerequisites
echo -e "${BLUE}Step 1: Checking prerequisites...${NC}"
command -v docker >/dev/null 2>&1 || { echo "Error: docker is not installed"; exit 1; }
command -v kind >/dev/null 2>&1 || { echo "Error: kind is not installed. Install with: brew install kind"; exit 1; }
command -v kubectl >/dev/null 2>&1 || { echo "Error: kubectl is not installed. Install with: brew install kubectl"; exit 1; }
echo -e "${GREEN}✓ All prerequisites installed${NC}"
echo ""

# Step 2: Create kind cluster
echo -e "${BLUE}Step 2: Creating kind cluster...${NC}"
if kind get clusters | grep -q "task-manager"; then
    echo -e "${YELLOW}Cluster 'task-manager' already exists. Deleting and recreating...${NC}"
    kind delete cluster --name task-manager
fi
kind create cluster --name task-manager --config kubernetes/kind-config.yaml
echo -e "${GREEN}✓ Kind cluster created${NC}"
echo ""

# Step 3: Build Docker images
echo -e "${BLUE}Step 3: Building Docker images...${NC}"
echo "Building backend API image..."
docker build -t flask-task-manager-backend:latest ./backend-api
echo "Building frontend image..."
docker build -t flask-task-manager-frontend:latest ./frontend
echo -e "${GREEN}✓ Docker images built${NC}"
echo ""

# Step 4: Load images into kind
echo -e "${BLUE}Step 4: Loading images into kind cluster...${NC}"
kind load docker-image flask-task-manager-backend:latest --name task-manager
kind load docker-image flask-task-manager-frontend:latest --name task-manager
echo -e "${GREEN}✓ Images loaded into kind${NC}"
echo ""

# Step 5: Apply Kubernetes manifests
echo -e "${BLUE}Step 5: Applying Kubernetes manifests...${NC}"
kubectl apply -f kubernetes/namespace.yaml
echo "Waiting for namespace to be ready..."
sleep 2

kubectl apply -f kubernetes/configmap.yaml
kubectl apply -f kubernetes/secret.yaml
kubectl apply -f kubernetes/postgres-pvc.yaml

echo "Deploying PostgreSQL..."
kubectl apply -f kubernetes/postgres-deployment.yaml
kubectl apply -f kubernetes/postgres-service.yaml

echo "Waiting for PostgreSQL to be ready..."
kubectl wait --for=condition=ready pod -l app=postgres -n task-manager --timeout=120s

echo "Deploying Backend API..."
kubectl apply -f kubernetes/backend-deployment.yaml
kubectl apply -f kubernetes/backend-service.yaml

echo "Waiting for Backend API to be ready..."
kubectl wait --for=condition=ready pod -l app=backend-api -n task-manager --timeout=120s

echo "Deploying Frontend..."
kubectl apply -f kubernetes/frontend-deployment.yaml
kubectl apply -f kubernetes/frontend-service.yaml

echo "Waiting for Frontend to be ready..."
kubectl wait --for=condition=ready pod -l app=frontend -n task-manager --timeout=120s

echo -e "${GREEN}✓ All resources deployed${NC}"
echo ""

# Step 6: Display deployment status
echo -e "${BLUE}Step 6: Deployment Status${NC}"
echo ""
echo "Namespaces:"
kubectl get namespaces | grep task-manager
echo ""
echo "Pods:"
kubectl get pods -n task-manager
echo ""
echo "Services:"
kubectl get svc -n task-manager
echo ""
echo "PersistentVolumeClaims:"
kubectl get pvc -n task-manager
echo ""

# Step 7: Access information
echo "=================================================="
echo -e "${GREEN}Deployment Complete!${NC}"
echo "=================================================="
echo ""
echo "Access the application:"
echo "  URL: http://localhost:30080"
echo ""
echo "Useful commands:"
echo "  View pods:     kubectl get pods -n task-manager"
echo "  View services: kubectl get svc -n task-manager"
echo "  View logs:     kubectl logs -n task-manager -l app=frontend"
echo "  Port-forward:  kubectl port-forward -n task-manager svc/frontend 8080:8080"
echo ""
echo "To delete the cluster:"
echo "  kind delete cluster --name task-manager"
echo ""
