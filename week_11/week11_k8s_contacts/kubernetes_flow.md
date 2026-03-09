# FastAPI → Docker → Docker Hub → Kubernetes (Minikube) – Full Command Flow

## 0. Environment & Variables (Recommended)

Set a few variables (for copy–paste convenience):

```bash
# From your project root
PROJECT_ROOT="$HOME/שולחן העבודה/week_11_mongo_k8/week11_k8s_contacts"
IMAGE_NAME="aharonsegal/fastapi"
IMAGE_TAG="v1"          # change version as needed
FULL_IMAGE="$IMAGE_NAME:$IMAGE_TAG"
```

## 1. Local Docker Flow (No Kubernetes Yet)

### 1.1 Clean Start (local)

Stop any previous containers using this image/port:

```bash
# Show running containers
docker ps

# If any container is using port 8000, stop it (replace <id> with actual container id)
docker stop <container-id>
```

Optional: see all containers including stopped:

```bash
docker ps -a
```

---

### 1.2 Build the Docker Image (from your `app/` folder)

Your `Dockerfile` is in `app/`, so:

```bash
cd "$PROJECT_ROOT/app"

# Build image with a version tag AND 'latest'
docker build -t "$IMAGE_NAME:$IMAGE_TAG" -t "$IMAGE_NAME:latest" .
```

Example without variables:

```bash
cd ~/שולחן\ העבודה/week_11_mongo_k8/week11_k8s_contacts/app
docker build -t aharonsegal/fastapi:v1 -t aharonsegal/fastapi:latest .
```

---

### 1.3 Test the Image Locally

Run the container:

```bash
docker run --rm -p 8000:8000 "$FULL_IMAGE"
# or, if you used 'latest':
# docker run --rm -p 8000:8000 aharonsegal/fastapi:latest
```

Now:

- Open in browser: `http://localhost:8000/docs`
- Or test via curl:

```bash
curl http://localhost:8000/
curl http://localhost:8000/docs
```

Stop the container with `Ctrl + C`.

---

### 1.4 Logs for Local Container

If you want to run detached:

```bash
docker run -d -p 8000:8000 --name fastapi_test "$FULL_IMAGE"
```

See logs:

```bash
docker logs fastapi_test         # last logs
docker logs -f fastapi_test      # follow logs
```

Stop & remove:

```bash
docker stop fastapi_test
docker rm fastapi_test
```

---

## 2. Docker Hub Flow (Push, Pull, Test)

### 2.1 Login & Push Image

```bash
docker login   # enter your Docker Hub username/password
docker push "$FULL_IMAGE"
docker push "$IMAGE_NAME:latest"
```

Example:

```bash
docker push aharonsegal/fastapi:v1
docker push aharonsegal/fastapi:latest
```

---

### 2.2 Pull & Test Image on Any Machine

On any machine with Docker:

```bash
docker pull "$FULL_IMAGE"
docker run --rm -p 8000:8000 "$FULL_IMAGE"
```

Check:

```bash
curl http://localhost:8000/
curl http://localhost:8000/docs
```

---

## 3. Kubernetes with Minikube – Full Flow

### 3.1 Clean Slate (Cluster & Namespace)

#### Option A: Soft Clean (just app resources)

From your project root:

```bash
cd "$PROJECT_ROOT"

# Delete all resources defined in k8/ (deployments, services, configmaps, etc.)
kubectl delete -f k8/ || true

# Optional: delete all PVCs if you want to reset Mongo data
kubectl delete pvc --all
```

#### Option B: Hard Reset (delete Minikube cluster)

```bash
# Stop and delete the entire Minikube cluster
minikube delete

# Start fresh
minikube start
```

Pick **one** approach depending on how “clean” you want it.

---

### 3.2 Start / Check Minikube

```bash
# Start cluster (default profile)
minikube start

# OR using your 'test' profile if you used that:
# minikube start -p test

# Verify cluster is up
kubectl get nodes
kubectl config current-context
```

You should see a node like `minikube` in `Ready` status.

---

### 3.3 Apply Your Kubernetes Manifests (Build/Deploy)

From the project root:

```bash
cd "$PROJECT_ROOT"

# Make sure your fastapi-deployment.yaml uses the image you pushed, e.g.:
# image: aharonsegal/fastapi:v1

kubectl apply -f k8/
```

This will create:

- FastAPI Deployment + Service
- Mongo Deployment + Service
- ConfigMap
- (and PVC if you added one)

---

### 3.4 Test if Pods Are Running

```bash
kubectl get pods
```

You want:

- `fastapi-...` → `1/1 Running`
- `mongo-...` → `1/1 Running`

If a pod is `CrashLoopBackOff` or `Pending`, describe it:

```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name> --tail=100
```

---

### 3.5 See Services, Pods, and More

Basic views:

```bash
kubectl get pods
kubectl get svc        # services
kubectl get deploy     # deployments
kubectl get pvc        # persistent volume claims
kubectl get all        # all common resources in the current namespace
```

Detailed views:

```bash
kubectl describe pod <pod-name>
kubectl describe svc fastapi
kubectl describe deploy fastapi
```

---

### 3.6 Logs from Pods (Kubernetes)

Get logs from FastAPI pod(s):

```bash
# Show logs from all pods with label app=fastapi
kubectl logs -l app=fastapi --tail=100

# Follow logs in real time:
kubectl logs -l app=fastapi -f
```

Specific pod:

```bash
kubectl get pods      # get exact pod name, e.g. fastapi-75b68b69d-xxxx
kubectl logs fastapi-75b68b69d-xxxx --tail=100
```

For Mongo:

```bash
kubectl logs -l app=mongo --tail=100
```

---

### 3.7 Communicate with the FastAPI Service (Kubernetes)

Your `fastapi-service.yaml` is a `NodePort` service on port `8000`.

#### Option A: Minikube Service (Easiest)

```bash
# default profile
minikube service fastapi

# or with profile 'test'
# minikube service fastapi -p test
```

This will:

- Open a browser, or
- Print a URL like `http://192.168.49.2:30689`

Test endpoints:

```bash
# Replace HOST:PORT with the printed service URL
curl http://HOST:PORT/
curl http://HOST:PORT/docs
```

#### Option B: Port-Forward

```bash
# Forward local port 8000 to the fastapi service
kubectl port-forward svc/fastapi 8000:8000
```

Then:

```bash
curl http://localhost:8000/
curl http://localhost:8000/docs
```

Stop forwarding with `Ctrl + C`.

---

### 3.8 Updating the Image in Kubernetes

When you change code:

1. Rebuild & push new image (e.g., `v2`):

   ```bash
   cd "$PROJECT_ROOT/app"
   docker build -t "$IMAGE_NAME:v2" -t "$IMAGE_NAME:latest" .
   docker push "$IMAGE_NAME:v2"
   docker push "$IMAGE_NAME:latest"
   ```

2. Update deployment to use the new tag:

   In `k8/fastapi-deployment.yaml`:

   ```yaml
   containers:
     - name: fastapi
       image: aharonsegal/fastapi:v2
       imagePullPolicy: Always
   ```

3. Apply & restart:

   ```bash
   cd "$PROJECT_ROOT"
   kubectl apply -f k8/fastapi-deployment.yaml
   kubectl rollout restart deployment fastapi
   kubectl get pods
   ```

4. Check logs and test via `minikube service fastapi` or `kubectl port-forward`.

---

## 4. Full Step-by-Step Flow (Cheat Sheet)

### A. Clean Start

```bash
cd "$PROJECT_ROOT"

# Soft clean cluster resources
kubectl delete -f k8/ || true
kubectl delete pvc --all || true

# (Optional) Hard reset:
# minikube delete
# minikube start
```

---

### B. Build (Docker)

```bash
cd "$PROJECT_ROOT/app"
docker build -t "$IMAGE_NAME:v1" -t "$IMAGE_NAME:latest" .
```

---

### C. Test Image Locally

```bash
docker run --rm -p 8000:8000 "$IMAGE_NAME:v1"
# Visit http://localhost:8000/docs
```

---

### D. Logs (Local Docker)

```bash
docker run -d -p 8000:8000 --name fastapi_test "$IMAGE_NAME:v1"
docker logs -f fastapi_test
docker stop fastapi_test
docker rm fastapi_test
```

---

### E. Push to Docker Hub

```bash
docker login
docker push "$IMAGE_NAME:v1"
docker push "$IMAGE_NAME:latest"
```

---

### F. Start Kubernetes & Deploy

```bash
# Start / ensure Minikube running
minikube start

cd "$PROJECT_ROOT"
kubectl apply -f k8/
kubectl get pods
kubectl get svc
```

---

### G. Test if Running (Kubernetes)

```bash
kubectl get pods
kubectl get svc
kubectl logs -l app=fastapi --tail=100
```

---

### H. Communicate with the App (Kubernetes)

```bash
# Option A:
minikube service fastapi

# Option B:
kubectl port-forward svc/fastapi 8000:8000
curl http://localhost:8000/
curl http://localhost:8000/docs
```

---

### I. See Everything in the Cluster

```bash
kubectl get all
kubectl get pods
kubectl get svc
kubectl get deploy
kubectl get pvc
```

