# the yaml
kind: Service            -> This is a service resource
name: streamlit-service  -> the name of the service

app: streamlit           -> service for this deployment   
  ports:
    - port: 8080         -> pod port
      targetPort: 8080   -> client port

# SERVICE
kubectl apply -f service.yaml

kubectl describe service streamlit-service
kubectl get svc        
kubectl get deploy    

# RUN
minikube service streamlit-service