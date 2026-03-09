# FastAPI + MongoDB on Kubernetes - File Overview

---

## 1️⃣ fastapi-configmap.yaml

**Purpose:** Stores environment variables for FastAPI.

**What it does:**
- Provides FastAPI with `MONGO_URI` and `DB_NAME`.
- Keeps configuration **outside of the container image**, so you can change it without rebuilding the image.
- FastAPI deployment references it using `envFrom: configMapRef`.

---

## 2️⃣ mongo-deployment.yaml

**Purpose:** Deploys MongoDB as a pod in the cluster.

**What it does:**
- Creates a MongoDB pod running the `mongo:latest` image.
- Mounts a **PersistentVolumeClaim (`mongo-pvc`)** at `/data/db` so database data persists even if the pod restarts.
- Labels the pod `app: mongo` so services can find it.

---

## 3️⃣ mongo-service.yaml

**Purpose:** Exposes MongoDB internally to other pods (FastAPI).

**What it does:**
- Creates a **ClusterIP service** named `mongo`.
- Maps port `27017` of the service to port `27017` of the MongoDB pod.
- Allows FastAPI to connect using the hostname `mongo` inside the cluster.

---

## 4️⃣ fastapi-deployment.yaml

**Purpose:** Deploys FastAPI as a pod in the cluster.

**What it does:**
- Creates a FastAPI pod running your image.
- Uses the environment variables from the **ConfigMap**.
- Exposes port `8000` internally in the pod.
- Labels the pod `app: fastapi` so the service can target it.

---

## 5️⃣ fastapi-service.yaml

**Purpose:** Exposes FastAPI to external traffic.

**What it does:**
- Creates a **NodePort or LoadBalancer service**.
- Maps port `8000` of the service to port `8000` of the FastAPI pod.
- Allows you (or other apps) to access FastAPI from outside the Kubernetes cluster.

---

## Summary Table

| File                     | Role       | Key Action                                           |
|---------------------------|------------|----------------------------------------------------|
| fastapi-configmap.yaml    | Config     | Stores env vars for FastAPI                         |
| mongo-deployment.yaml     | Deployment | Creates MongoDB pod with persistent storage        |
| mongo-service.yaml        | Service    | Exposes MongoDB inside the cluster for FastAPI     |
| fastapi-deployment.yaml   | Deployment | Creates FastAPI pod and injects env vars           |
| fastapi-service.yaml      | Service    | Exposes FastAPI outside the cluster (NodePort/LoadBalancer) |

---

## 💡 Key Concepts

- **Deployments** → define pods (actual containers running).  
- **Services** → expose pods internally or externally.  
- **ConfigMaps** → provide configuration data (like environment variables) to pods.  
- **PersistentVolumeClaims** → ensure MongoDB data survives pod restarts.  

