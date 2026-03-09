# week11_k8s_contacts

## Project Overview

contacts manager API built with FastAPI and MongoDB 

Main features:

- CRUD operations for contacts
- Kubernetes manifests for API + MongoDB

Kubernetes Build:

* **Deployment** → runs Pods
* **Service** → network access to Pods
* **ConfigMap** → env vars
* **PVC** → persistent storage

cluster flow:

    Client
        ↓
    FastAPI Service (NodePort)
        ↓
    FastAPI Pod
        ↓ (MONGO_URI = mongo:27017)
    Mongo Service
        ↓
    Mongo Pod
        ↓
    Persistent Volume

## Git Branches

- **dev/api_local_mongo_image**
    - all api endpoints created 
    - FastApi running locally
    - MongoDB running in image

- **dev/compose_api_and_mongo**
  - Docker Compose setup for API + MongoDB together

- **dev/Refine_FastApi_code**
    - refined FastApi code structure
    - 

---

1. **Start Minikube** 

```bash
minikube start
```

2. **Apply Kubernetes manifests**:

```bash
kubectl apply -f k8/
```

3. **Check that pods are running**:

```bash
kubectl get pods
```
expected output-> something both READY:
NAME                      READY   STATUS    RESTARTS   AGE
fastapi-75b68b69d-4kjck   1/1     Running   0          9m8s
mongo-5fdd764968-wtl7x    1/1     Running   0          42m

4. **Open the FastAPI service**:

```bash
minikube service fastapi
```
## API Endpoints

**DB Test**

    GET
    /test/health
    Health

    GET
    /test/db
    Test Db Connection

**Contacts**

    GET
    /contacts/
    List Contacts

    POST
    /contacts/
    Create Contact

    GET
    /contacts/{contact_id}
    Get Contact By Id

    PUT
    /contacts/{contact_id}
    Update Contact By Id

    DELETE
    /contacts/{contact_id}
    Delete Contact

