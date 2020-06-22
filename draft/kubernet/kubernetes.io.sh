# Start the cluster, by running the minikube Minikube started a virtual machine
# for you, and a Kubernetes cluster is now running in that VM.
minikube start
# To interact with Kubernetes during this bootcamp we’ll use the command line interface, kubectl.
kubectl version

# Let’s view the cluster details.
kubectl cluster-info

# To view the nodes in the cluster:
kubectl get nodes
