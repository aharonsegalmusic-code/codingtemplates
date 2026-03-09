# Kubernetes Cheat Sheet - Key Terms for FastAPI + MongoDB

---

## 1️⃣ Cluster
- **Definition:** A set of nodes (machines) running Kubernetes, which hosts containerized applications.
- **In this project:** The cluster runs both your **MongoDB pod** and **FastAPI pod**, managing their scheduling and networking.

---

## 2️⃣ Node
- **Definition:** A single machine (virtual or physical) in the cluster.
- **In this project:** Each pod (FastAPI or MongoDB) runs on a node. For local testing, your cluster may be a single-node setup like **Minikube** or **Docker Desktop Kubernetes**.

---

## 3️⃣ Pod
- **Definition:** The smallest deployable unit in Kubernetes, containing one or more containers.
- **In this project:** 
  - **MongoDB pod** runs the MongoDB container.
  - **FastAPI pod** runs your FastAPI container, which connects to the MongoDB pod.

---

## 4️⃣ Deployment
- **Definition:** Manages stateless pods, ensures a desired number of replicas, and handles updates.
- **In this project:** 
  - **MongoDB Deployment** ensures the database pod is running with persistent storage.
  - **FastAPI Deployment** ensures the API pod is running, and can scale replicas if needed.

---

## 5️⃣ Service
- **Definition:** Exposes pods to other pods or external traffic; provides a stable network endpoint.
- **In this project:**  
  - **MongoDB Service** (`ClusterIP`) allows FastAPI pod to connect via hostname `mongo`.  
  - **FastAPI Service** (`NodePort` or `LoadBalancer`) exposes your API to your machine or external clients.

---

## 6️⃣ ConfigMap
- **Definition:** Stores non-sensitive configuration data as key-value pairs.
- **In this project:** Stores `MONGO_URI` and `DB_NAME` for FastAPI. The FastAPI pod reads these values instead of hardcoding them.

---

## 7️⃣ Secret
- **Definition:** Stores sensitive information (like passwords) securely.
- **In this project:** Could store MongoDB credentials if you enable authentication. FastAPI can read them as environment variables.

---

## 8️⃣ PersistentVolume (PV)
- **Definition:** A piece of storage in the cluster that can be used by pods.
- **In this project:** The MongoDB pod mounts a PV to `/data/db` so your database persists even if the pod restarts.

---

## 9️⃣ PersistentVolumeClaim (PVC)
- **Definition:** A request for storage by a pod from available PVs.
- **In this project:** The MongoDB deployment uses a PVC (`mongo-pvc`) to claim storage for the database volume.

---

## 1️⃣0️⃣ Namespace
- **Definition:** A virtual cluster within Kubernetes for organizing resources.
- **In this project:** Could create a namespace like `fastapi-db` to isolate your FastAPI and MongoDB resources from other projects.

---

## 1️⃣1️⃣ ReplicaSet
- **Definition:** Ensures a specified number of pod replicas are running.
- **In this project:** Automatically created by a Deployment. Ensures that if a FastAPI or MongoDB pod dies, a new one starts automatically.

---

## 1️⃣2️⃣ Ingress
- **Definition:** Manages external access to services (usually HTTP/HTTPS) in the cluster.
- **In this project:** Could be used to expose FastAPI externally using a domain name instead of NodePort.

---

## 1️⃣3️⃣ VolumeMount
- **Definition:** Mounts storage inside a pod container.
- **In this project:** MongoDB pod mounts the PVC at `/data/db` to store database files.

---

## 1️⃣4️⃣ Labels and Selectors
- **Definition:** Key-value pairs attached to objects for organization and selection.
- **In this project:**  
  - Pods are labeled `app: fastapi` or `app: mongo`.  
  - Services use selectors to route traffic to the correct pods.

---

## 1️⃣5️⃣ NodePort
- **Definition:** Exposes a service on each node’s IP at a static port.
- **In this project:** The FastAPI Service uses NodePort to allow access from your local machine or outside the cluster.

---

## 1️⃣6️⃣ ClusterIP
- **Definition:** Default service type; exposes service internally in the cluster only.
- **In this project:** The MongoDB Service uses ClusterIP so FastAPI can connect internally via `mongo:27017`.

---

## 1️⃣7️⃣ LoadBalancer
- **Definition:** Exposes a service externally using a cloud provider’s load balancer.
- **In this project:** Optional for FastAPI if you deploy on a cloud cluster and want public access.

---

