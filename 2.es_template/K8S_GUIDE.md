# ──────────────────────────────────────────────────────────────
# Kubernetes: Converting Docker Compose → K8s YAML
# ──────────────────────────────────────────────────────────────
#
# TOOL: kompose  (official conversion tool by Kubernetes SIG)
# Docs: https://kompose.io/
#
# ── Install kompose ───────────────────────────────────────────
#
# macOS (Homebrew):
#   brew install kompose
#
# Linux:
#   curl -L https://github.com/kubernetes/kompose/releases/download/v1.33.0/kompose-linux-amd64 -o kompose
#   chmod +x kompose
#   sudo mv kompose /usr/local/bin/kompose
#
# Windows (Chocolatey):
#   choco install kubernetes-kompose
#
# ── Convert compose → K8s YAML ────────────────────────────────
#
#   cd pizza-es/
#   kompose convert -f docker-compose.yml -o k8s/
#
# This creates in k8s/ :
#   elasticsearch-deployment.yaml
#   elasticsearch-service.yaml
#   kibana-deployment.yaml
#   kibana-service.yaml
#   fastapi-deployment.yaml
#   fastapi-service.yaml
#   esdata-persistentvolumeclaim.yaml
#
# ── Apply to a cluster ────────────────────────────────────────
#
#   kubectl apply -f k8s/
#
# ── Verify ────────────────────────────────────────────────────
#
#   kubectl get pods
#   kubectl get services
#   kubectl get pvc        # persistent volume claims (esdata)
#
# ── Access services ───────────────────────────────────────────
#
#   # FastAPI (if service type is ClusterIP, use port-forward):
#   kubectl port-forward svc/fastapi 8000:8000
#   # then open http://localhost:8000/docs
#
#   # Kibana:
#   kubectl port-forward svc/kibana 5601:5601
#   # then open http://localhost:5601
#
# ── Important K8s differences vs Docker Compose ───────────────
#
# 1. Image registry:
#    kompose assumes your image is already in a registry.
#    Build and push first:
#      docker build -t your-registry/pizza-fastapi:1.0 .
#      docker push your-registry/pizza-fastapi:1.0
#    Then update fastapi-deployment.yaml:
#      image: your-registry/pizza-fastapi:1.0
#
# 2. Environment variables:
#    kompose converts `environment:` to k8s env vars in the
#    Deployment spec.  For secrets use k8s Secrets instead of
#    plain env vars.
#
# 3. depends_on:
#    K8s has no depends_on — use readinessProbes to wait for
#    ES to be ready before Kibana/FastAPI accept traffic.
#    Add to fastapi-deployment.yaml:
#
#      readinessProbe:
#        httpGet:
#          path: /
#          port: 8000
#        initialDelaySeconds: 15
#        periodSeconds: 5
#
# 4. Persistent volumes:
#    kompose creates a PVC (PersistentVolumeClaim) for the
#    esdata volume.  On cloud providers (GKE, EKS, AKS) a
#    StorageClass will automatically provision the disk.
#    On bare metal / local (minikube) you may need to create
#    a PV (PersistentVolume) manually.
#
# 5. Networking:
#    Services communicate via k8s DNS:
#      http://elasticsearch:9200  (same as Docker Compose — just works)
#
# ── Quick start with minikube (local k8s) ─────────────────────
#
#   minikube start
#   eval $(minikube docker-env)          # use minikube's Docker daemon
#   docker build -t pizza-fastapi:1.0 .  # build into minikube's daemon
#
#   # Edit fastapi-deployment.yaml:
#   #   image: pizza-fastapi:1.0
#   #   imagePullPolicy: Never           # don't try to pull from registry
#
#   kubectl apply -f k8s/
#   minikube service fastapi --url        # get the external URL
