# the yaml
kind: Deployment -> This is a deployment resource
name: streamlit  -> the name of the deployment

spec:
    replicas: 1    -> only one pod should be running


# POD
kubectl apply -f pod.yaml

kubectl describe pod streamlit
kubectl get pods 
kubectl logs streamlit-5f64cbccbf-x7xj4 --tail=100