
## 3️⃣ Option 2 — Build and push to Docker Hub (or other registry)

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

4. Apply your deployment to the cluster:

```bash
kubectl apply -f k8s/fastapi-deployment.yaml
```

---

## 4️⃣ Notes

* **Minikube local build** avoids the need to push images and is ideal for rapid testing.
* **ImagePullPolicy**:

  * `IfNotPresent` → use local image if available
  * `Always` → always pull from registry
* If you see `ImagePullBackOff`, check that:

```bash
kubectl describe pod <pod-name>
```

* Make sure your Dockerfile is in the same directory as your build context.

```
