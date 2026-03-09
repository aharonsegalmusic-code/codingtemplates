# Kubernetes YAML Reference Templates

Standalone K8s manifest templates for a two-service app (web app + MySQL database). Not tied to any specific week — just copy-paste reference.

---

## What's here

- `app-deployment.yaml` — Deployment template for a web application container
- `app-service.yaml` — ClusterIP Service to expose the app internally
- `mysql-deployment.yaml` — MySQL database Deployment
- `mysql-service.yaml` — ClusterIP Service for MySQL (internal access only)

**Covers:** Deployment · Service · ClusterIP · port mapping · environment variables
