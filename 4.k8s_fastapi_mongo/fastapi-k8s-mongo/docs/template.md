# =====================================================
# General Kubernetes YAML Template with Comments
# =====================================================

# --------------------------
# 1️⃣ Deployment (General)
# --------------------------
apiVersion: apps/v1               # Specifies the API version for Deployment
kind: Deployment                  # Object type is Deployment (manages pods)
metadata:
  name: <deployment-name>         # Unique name for this deployment
  labels:                         # Labels are metadata for identification and selection
    app: <app-label>              # Example: "fastapi" or "mongo"
spec:
  replicas: 1                     # Number of pod replicas
  selector:
    matchLabels:
      app: <app-label>            # Selector links Deployment to pods with the same label
  template:                        # Template for pod creation
    metadata:
      labels:
        app: <app-label>          # Pod labels; must match selector
    spec:
      containers:
        - name: <container-name>  # Unique name for this container
          image: <container-image> # Docker image to run
          ports:
            - containerPort: <port-number>  # Port exposed inside the pod
          envFrom:
            - configMapRef:                # Load environment variables from ConfigMap
                name: <configmap-name>    # Shared ConfigMap name
          volumeMounts:
            - name: <volume-name>         # Mount a volume inside the container
              mountPath: <container-path> # Path inside the container

      volumes:                             # Volumes available to this pod
        - name: <volume-name>             # Must match volumeMounts.name
          persistentVolumeClaim:
            claimName: <pvc-name>        # PVC name to claim persistent storage
# -------------------------------------------------
# Notes on uniqueness:
# - deployment-name: unique per deployment (fastapi vs mongo)
# - container-name: unique per pod container
# - app-label: usually shared among related pods (FastAPI pod + service use same label)
# - configmap-name: shared across deployments if multiple pods use same configuration
# - volume-name / pvc-name: can be shared if you want multiple pods to access same persistent data
# -------------------------------------------------

# --------------------------
# 2️⃣ Service (General)
# --------------------------
apiVersion: v1
kind: Service                       # Object type is Service (exposes pods)
metadata:
  name: <service-name>              # Unique service name
spec:
  selector:
    app: <app-label>                # Service selects pods by label
  ports:
    - port: <service-port>          # Port for the service
      targetPort: <pod-port>        # Maps to pod container port
  type: <service-type>              # ClusterIP, NodePort, LoadBalancer

# -------------------------------------------------
# Notes on uniqueness:
# - service-name: unique per service (fastapi vs mongo)
# - app-label: matches deployment pod labels to link service to pods
# - service-type: depends on use case
# -------------------------------------------------

# --------------------------
# 3️⃣ ConfigMap (General)
# --------------------------
apiVersion: v1
kind: ConfigMap
metadata:
  name: <configmap-name>            # Shared configmap name used by multiple deployments
data:
  ENV_VAR_1: <value>
  ENV_VAR_2: <value>

# -------------------------------------------------
# Notes on uniqueness:
# - configmap-name: can be shared by multiple deployments/pods if they use same config
# - individual ENV_VAR keys: unique to your app needs
# -------------------------------------------------

# --------------------------
# 4️⃣ PersistentVolumeClaim (PVC) (General)
# --------------------------
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: <pvc-name>                  # Unique PVC per type of data
spec:
  accessModes:
    - ReadWriteOnce                  # Pod can read/write once
  resources:
    requests:
      storage: <size>               # Storage size requested (e.g., 1Gi)
# -------------------------------------------------
# Notes on uniqueness:
# - pvc-name: usually unique per database or storage type
# - volume-name in deployment must match pvc-name if you want persistence
# - Using the same pvc across multiple pods allows shared persistent data
# -------------------------------------------------

⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘
⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘
⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘
⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘
⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘

# Kubernetes Syntax Reference for FastAPI + MongoDB

| Key / Field                  | Type / Input                     | Mandatory | Example / Project Usage                                      | Notes / Purpose |
|-------------------------------|---------------------------------|-----------|-------------------------------------------------------------|----------------|
| apiVersion                    | string                           | ✅         | `apps/v1`, `v1`                                             | Defines Kubernetes API version for the object type |
| kind                          | string                           | ✅         | `Deployment`, `Service`, `ConfigMap`, `PersistentVolumeClaim` | Type of Kubernetes object |
| metadata                      | object                           | ✅         | `name`, `labels`                                            | Metadata about the object |
| metadata.name                 | string                           | ✅         | `fastapi`, `mongo`, `fastapi-config`                       | Unique identifier for the resource |
| metadata.labels               | key-value map                    | ❌         | `app: fastapi`                                              | Labels for selection and organization |
| spec                          | object                           | ✅         | Depends on object type                                      | Specification of desired state |
| spec.replicas                 | integer                          | ❌         | `1`                                                         | Number of pod replicas (Deployment only) |
| spec.selector.matchLabels     | key-value map                    | ✅         | `app: fastapi`                                              | Used by Deployment/Service to match pods |
| spec.template.metadata.labels | key-value map                    | ✅         | `app: fastapi`                                              | Labels for pods, must match selector |
| spec.template.spec.containers | list of container objects        | ✅         | One container per pod                                        | Define containers to run in the pod |
| containers.name               | string                           | ✅         | `fastapi`, `mongo`                                         | Name of container |
| containers.image              | string                           | ✅         | `your-fastapi-image:latest`, `mongo:latest`               | Docker image to run |
| containers.ports.containerPort | integer                         | ❌         | `8000`, `27017`                                             | Exposed container port |
| containers.envFrom            | list of ConfigMap/Secret refs    | ❌         | `configMapRef: fastapi-config`                              | Inject environment variables |
| containers.volumeMounts       | list of volume objects           | ❌         | `name: mongo-data, mountPath: /data/db`                     | Mount storage into container |
| volumes                       | list of volume objects           | ❌         | `persistentVolumeClaim.claimName: mongo-pvc`               | Define volumes available to pod |
| kind: Service.spec.selector   | key-value map                    | ✅         | `app: fastapi`                                              | Links service to pods |
| Service.spec.ports.port       | integer                          | ✅         | `8000`, `27017`                                             | Port exposed by service |
| Service.spec.ports.targetPort | integer                          | ✅         | `8000`, `27017`                                             | Port on the pod container |
| Service.spec.type              | string                          | ❌         | `ClusterIP`, `NodePort`, `LoadBalancer`                     | How the service is exposed |
| ConfigMap.data                | key-value map                    | ✅         | `MONGO_URI`, `DB_NAME`                                      | Environment/configuration variables |
| PersistentVolumeClaim.spec.accessModes | list of strings          | ✅         | `ReadWriteOnce`                                             | Defines read/write access mode |
| PersistentVolumeClaim.spec.resources.requests.storage | string | ✅ | `1Gi`                                                      | Requested persistent storage size |



⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘
⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘
⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘
⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘
⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘

# FastAPI + MongoDB Kubernetes Variables (Code Style)

## 1️⃣ Deployment / Pod Variables

# Unique per Deployment / Pod
deployment_name_fastapi = "fastapi"
deployment_name_mongo = "mongo"

container_name_fastapi = "fastapi"
container_name_mongo = "mongo"

app_label_fastapi = "fastapi"
app_label_mongo = "mongo"

container_image_fastapi = "your-fastapi-image:latest"
container_image_mongo = "mongo:latest"

port_fastapi = 8000
port_mongo = 27017

---

## 2️⃣ Service Variables

# Unique per Service
service_name_fastapi = "fastapi"
service_name_mongo = "mongo"

service_port_fastapi = 8000
service_port_mongo = 27017

pod_port_fastapi = 8000
pod_port_mongo = 27017

service_type_fastapi = "NodePort"       # exposed externally
service_type_mongo = "ClusterIP"        # internal only

---

## 3️⃣ ConfigMap Variables

configmap_name_fastapi = "fastapi-config"

# Environment variables for FastAPI
MONGO_URI = "mongodb://mongo:27017"
DB_NAME = "fastapi_db_container"

---

## 4️⃣ PersistentVolume / PVC Variables

volume_name_mongo = "mongo-data"
pvc_name_mongo = "mongo-pvc"

container_path_mongo = "/data/db"
pvc_storage_size = "1Gi"   # Example size

---

# Notes:

# - deployment_name, container_name, service_name are unique per resource.
# - app_label and configmap_name can be shared across multiple resources to link them.
# - pvc_name and volume_name provide persistent storage; multiple pods can share a PVC if needed.


⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘
⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘
⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘
⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘
⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘


### **Folder structure**

```
k8/
├── mongo-deployment.yaml
├── fastapi-deployment.yaml
├── mongo-service.yaml
├── fastapi-service.yaml
├── fastapi-configmap.yaml
├── README.md  (optional)
```

---

### **1️⃣ mongo-deployment.yaml**

* **Purpose:** Deploy MongoDB with persistent storage.
* **Contents:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mongo
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mongo
  template:
    metadata:
      labels:
        app: mongo
    spec:
      containers:
        - name: mongo
          image: mongo:latest
          ports:
            - containerPort: 27017
          volumeMounts:
            - name: mongo-data
              mountPath: /data/db
      volumes:
        - name: mongo-data
          persistentVolumeClaim:
            claimName: mongo-pvc
```

---

### **2️⃣ fastapi-deployment.yaml**

* **Purpose:** Deploy FastAPI container.
* **Contents:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi
spec:
  replicas: 1
  selector:
    matchLabels:
      app: fastapi
  template:
    metadata:
      labels:
        app: fastapi
    spec:
      containers:
        - name: fastapi
          image: your-fastapi-image:latest
          ports:
            - containerPort: 8000
          envFrom:
            - configMapRef:
                name: fastapi-config
```

---

### **3️⃣ mongo-service.yaml**

* **Purpose:** Expose MongoDB to FastAPI inside the cluster.
* **Contents:**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mongo
spec:
  selector:
    app: mongo
  ports:
    - protocol: TCP
      port: 27017
      targetPort: 27017
```

---

### **4️⃣ fastapi-service.yaml**

* **Purpose:** Expose FastAPI outside the cluster.
* **Contents:**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: fastapi
spec:
  type: NodePort    # or LoadBalancer if on cloud
  selector:
    app: fastapi
  ports:
    - port: 8000
      targetPort: 8000
```

---

### **5️⃣ fastapi-configmap.yaml**

* **Purpose:** Store environment variables for FastAPI.
* **Contents:**

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fastapi-config
data:
  MONGO_URI: "mongodb://mongo:27017"
  DB_NAME: "fastapi_db_container"
```

