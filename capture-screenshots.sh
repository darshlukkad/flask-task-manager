#!/bin/bash
# Script to capture Kubernetes state for assignment documentation

set -e

echo "=================================================="
echo "Kubernetes Screenshot Capture Script"
echo "=================================================="
echo ""

# Create screenshots directory
mkdir -p screenshots
cd screenshots

echo "📸 Capturing Kubernetes state..."
echo ""

# 1. All resources
echo "1. Capturing all resources..."
kubectl get all -n task-manager -o wide > 01-all-resources.txt

# 2. Pods
echo "2. Capturing pods..."
kubectl get pods -n task-manager -o wide > 02-pods.txt

# 3. Services
echo "3. Capturing services..."
kubectl get svc -n task-manager -o wide > 03-services.txt

# 4. Deployments
echo "4. Capturing deployments..."
kubectl get deployments -n task-manager -o wide > 04-deployments.txt

# 5. PVC
echo "5. Capturing PersistentVolumeClaims..."
kubectl get pvc -n task-manager > 05-pvc.txt

# 6. ConfigMaps and Secrets
echo "6. Capturing ConfigMaps and Secrets..."
kubectl get configmap,secret -n task-manager > 06-config-secrets.txt

# 7. Pod details
echo "7. Capturing pod details..."
BACKEND_POD=$(kubectl get pod -n task-manager -l app=backend-api -o jsonpath='{.items[0].metadata.name}')
kubectl describe pod -n task-manager $BACKEND_POD > 07-backend-pod-details.txt

FRONTEND_POD=$(kubectl get pod -n task-manager -l app=frontend -o jsonpath='{.items[0].metadata.name}')
kubectl describe pod -n task-manager $FRONTEND_POD > 08-frontend-pod-details.txt

# 8. Logs
echo "8. Capturing logs..."
kubectl logs -n task-manager -l app=backend-api --tail=50 > 09-backend-logs.txt
kubectl logs -n task-manager -l app=frontend --tail=50 > 10-frontend-logs.txt

# 9. Cluster info
echo "9. Capturing cluster info..."
kubectl cluster-info > 11-cluster-info.txt
kind get clusters > 12-kind-clusters.txt

echo ""
echo "=================================================="
echo "✅ Screenshots captured!"
echo "=================================================="
echo ""
echo "Text outputs saved to: screenshots/"
echo ""
echo "📋 Next Steps:"
echo "1. Take terminal screenshots of these commands:"
echo "   - kubectl get all -n task-manager"
echo "   - kubectl get pods -n task-manager"
echo "   - kubectl get svc -n task-manager"
echo ""
echo "2. Take browser screenshots:"
echo "   - Open http://localhost:30080"
echo "   - Screenshot the application homepage"
echo "   - Screenshot tasks with different priorities"
echo ""
echo "3. Methods to capture terminal output as images:"
echo "   a) Use Cmd+Shift+4 on macOS (then select area)"
echo "   b) Use your terminal's export to PDF feature"
echo "   c) Use 'script' command to save session"
echo ""

# Create a combined report
cat > 00-DEPLOYMENT-SUMMARY.txt << 'EOF'
# KUBERNETES DEPLOYMENT VERIFICATION

## Cluster Information
EOF

kind get clusters >> 00-DEPLOYMENT-SUMMARY.txt
echo "" >> 00-DEPLOYMENT-SUMMARY.txt

cat >> 00-DEPLOYMENT-SUMMARY.txt << 'EOF'

## All Resources in task-manager Namespace
EOF

kubectl get all -n task-manager >> 00-DEPLOYMENT-SUMMARY.txt
echo "" >> 00-DEPLOYMENT-SUMMARY.txt

cat >> 00-DEPLOYMENT-SUMMARY.txt << 'EOF'

## Services
EOF

kubectl get svc -n task-manager -o wide >> 00-DEPLOYMENT-SUMMARY.txt
echo "" >> 00-DEPLOYMENT-SUMMARY.txt

cat >> 00-DEPLOYMENT-SUMMARY.txt << 'EOF'

## Persistent Storage
EOF

kubectl get pvc -n task-manager >> 00-DEPLOYMENT-SUMMARY.txt

echo ""
echo "📄 Combined report: screenshots/00-DEPLOYMENT-SUMMARY.txt"
echo ""
