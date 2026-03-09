# Week 11 — FastAPI + MongoDB + Kubernetes

Introduction to containerized FastAPI apps with MongoDB, deployed to Kubernetes. Three projects at increasing levels of complexity.

---

## Sub-projects

- `fastapi-k8s-mongo/` — Minimal items API on MongoDB with full production K8s manifests and deployment docs
- `week11_k8s_contacts/` — Contacts CRUD API on MongoDB + K8s; contains the most detailed K8s educational docs in the repo (17 K8s concepts explained)
- `week_11_k8_test/` — Single-service experiment: testing a bare Pod and Service in K8s (not a full app)

## Key concepts covered

- FastAPI app containerization with Docker
- PyMongo connection management
- Kubernetes: Pod, Deployment, Service, ConfigMap, PVC, ClusterIP, NodePort, LoadBalancer
- docker-compose for local dev vs K8s manifests for production
- ReadinessProbe, PersistentVolumeClaim for MongoDB storage
