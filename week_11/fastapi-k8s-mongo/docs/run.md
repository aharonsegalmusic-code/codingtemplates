# FastAPI + MongoDB Setup Cheat Sheet

## 1. Local FastAPI + Local MongoDB

###  Environment variables
MONGO_URI="mongodb://localhost:27017"
DB_NAME="fastapi_db"
cat .env

### MongoDB service (Administrator PowerShell)

```powershell
# Start MongoDB service
Start-Service MongoDB
Stop-Service MongoDB
Get-Service -Name MongoDB

# Run FastAPI
uvicorn app.main:app --reload
```

⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘
⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘

## 2. Local FastAPI + MongoDB in Docker container (no port conflict)

### Run MongoDB container on a different host port
```bash
# Expose container port 27017 as host port 27018
docker run -d --name mongodb_container -p 27018:27017 mongo:latest
````
### Environment variables for FastAPI

# Connect FastAPI to the container on port 27018
MONGO_URI="mongodb://localhost:27018"
DB_NAME="fastapi_db_container"
cat .env


### Run FastAPI locally

```bash
uvicorn app.main:app --reload
```

### Stop and remove MongoDB container when done

```bash
docker stop mongodb_container
docker rm mongodb_container
```
View and inspect MongoDB container
# Check running containers
docker ps

# View container logs
docker logs mongodb_container

# Open Mongo shell inside the container
docker exec -it mongodb_container mongosh

# Show databases in the container
show dbs

# Switch to your FastAPI database
use fastapi_db_container

# Show collections in that database
show collections
db.items.find().pretty()

⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘
⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘

## 3. FastAPI + MongoDB via Docker Compose

# .env
MONGO_URI="mongodb://mongo:27017"
DB_NAME="fastapi_db_container"

# Start FastAPI + MongoDB in containers
docker-compose up --build

# Run in background
docker-compose up -d --build

# Stop and remove containers
docker-compose down

# View logs
docker-compose logs fastapi
docker-compose logs mongo

# Check running containers
docker ps


⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘
⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘

---

# **Kubernetes Commands for FastAPI + MongoDB**

---


1. Build the Docker image locally:

```bash
docker build -t aharonsegal/fastapi:latest .
```

2. Push the image to Docker Hub:

```bash
docker push aharonsegal/fastapi:latest
```

3. Reference the image in your deployment YAML:

```yaml
image: aharonsegal/fastapi:latest
```


## **1️⃣ Apply / Create Resources**

```bash
# Apply a ConfigMap
kubectl apply -f k8/fastapi-configmap.yaml

# Apply MongoDB deployment and service
kubectl apply -f k8/mongo-deployment.yaml
kubectl apply -f k8/mongo-service.yaml

# Apply FastAPI deployment and service
kubectl apply -f k8/fastapi-deployment.yaml
kubectl apply -f k8/fastapi-service.yaml
```

💡 **Tip:** You can combine all YAMLs into one folder and run:

```bash
kubectl apply -f k8s/

# opens communication to the specified service
 minikube service fastapi
```


---

## **2️⃣ View Cluster Resources**

```bash
# List all pods
kubectl get pods

# List all deployments
kubectl get deployments

# List all services
kubectl get services

# Get detailed info about a pod
kubectl describe pod <pod-name>

# Get detailed info about a deployment
kubectl describe deployment <deployment-name>

# List ConfigMaps
kubectl get configmaps

# List P
```

---

## **3️⃣ View Logs**

```bash
# View logs of a pod
kubectl logs <pod-name>

# Follow logs in real-time
kubectl logs -f <pod-name>

# If pod has multiple containers
kubectl logs <pod-name> -c <container-name>
```

---

## **4️⃣ Connect to a Pod**

```bash
# Start an interactive shell in a pod
kubectl exec -it <pod-name> -- /bin/bash

# Example: Connect to MongoDB pod and run mongosh
kubectl exec -it mongo-<id> -- mongosh
```

---

## **5️⃣ Delete / Shutdown Resources**

```bash
# Delete a specific deployment
kubectl delete deployment <deployment-name>

# Delete a specific service
kubectl delete service <service-name>

# Delete a specific ConfigMap
kubectl delete configmap <configmap-name>

# Delete all resources in a namespace or folder
kubectl delete -f k8/

# Optional: Delete namespace (removes all resources inside)
kubectl delete namespace <namespace-name>
```

---

## **6️⃣ Scaling Pods**

```bash
# Scale FastAPI deployment to 3 replicas
kubectl scale deployment fastapi --replicas=3
```

---

## **7️⃣ Checking Connectivity**

```bash
# Exec into FastAPI pod and check MongoDB connection
kubectl exec -it <fastapi-pod-name> -- /bin/bash
# Inside pod
ping mongo
```

---

## **8️⃣ Useful Shortcuts**

```bash
# Get pods with labels
kubectl get pods -l app=fastapi
kubectl get pods -l app=mongo

# Delete all pods (they will be recreated by deployment)
kubectl delete pod -l app=fastapi
```

---

💡 **Notes / Tips**

* Pods are ephemeral; deleting them won’t lose data if you use **PVC for MongoDB**.
* Services provide stable network endpoints, so FastAPI can always reach MongoDB via `mongo:27017`.
* Use `kubectl logs -f` to follow FastAPI logs while testing endpoints.
* Combine with `kubectl describe` to troubleshoot issues like image pull errors or port conflicts.

---







test data
[
  {
    "name": "Sunset Landscape",
    "description": "A vivid painting of a sunset over rolling hills."
  },
  {
    "name": "Ocean Breeze",
    "description": "A calming scene with waves gently hitting the shore."
  },
  {
    "name": "Mountain Trek",
    "description": "An adventurous trail through rugged mountain terrain."
  },
  {
    "name": "City Lights",
    "description": "A night cityscape with illuminated skyscrapers."
  },
  {
    "name": "Forest Whisper",
    "description": "A serene forest path with sunlight streaming through the trees."
  }
]
