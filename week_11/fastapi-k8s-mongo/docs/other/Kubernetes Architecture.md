# Kubernetes Architecture

## Overview

Kubernetes is a container orchestration system designed to automate deployment, scaling, and management of containerized applications. Its architecture is divided into **Control Plane components**, **Node components**, and **optional supporting services**.

---

## Control Plane Components

The control plane manages the overall state of the cluster and makes global decisions.

### kube-apiserver

* Front-facing REST API for the Kubernetes control plane
* All clients and components communicate **only** through the API server
* Responsibilities:

  * Authentication and authorization
  * Request validation and mutation
  * Admission control
  * Interface to the backing datastore

### etcd

* Distributed key-value datastore for the cluster
* Strong consistency and high availability
* Stores:

  * Cluster state
  * Configuration data
  * Kubernetes objects

### kube-controller-manager

* Runs core control loops
* Continuously monitors cluster state via the API server
* Works to move the cluster toward the desired state

### kube-scheduler

* Assigns workloads (Pods) to nodes
* Evaluates resource and policy requirements such as:

  * CPU / memory
  * Labels
  * Affinity / anti-affinity
  * Custom constraints
* Uses **bin packing** by default

---

## Node Components

Node components run on every worker node and are responsible for running workloads.

### kubelet

* Primary node agent
* Manages the lifecycle of Pods on its node
* Reads Pod manifests from:

  * Local file paths
  * HTTP endpoints
  * etcd watches
  * HTTP server mode (simple API)

### kube-proxy

* Manages network rules on each node
* Provides service-level load balancing and traffic forwarding
* Proxy modes:

  * Userspace
  * iptables
  * ipvs (default if supported)

### Container Runtime Engine

* Executes and manages containers via the CRI (Container Runtime Interface)
* Examples:

  * Docker Engine
  * containerd
  * CRI-O
  * Mirantis Container Runtime

---

## Optional Services

### cloud-controller-manager

* Integrates Kubernetes with cloud provider APIs
* Manages cloud-specific controllers:

  * Node
  * Route
  * Service
  * PersistentVolume labeling

### Cluster DNS

* Provides cluster-wide DNS resolution for services
* Implemented using **CoreDNS**

### Kubernetes Dashboard

* Web-based user interface
* Provides limited, general-purpose cluster visibility and management

---

## Networking

### Container Network Interface (CNI)

* Responsible for Pod networking
* Acts as an interface between the container runtime and networking plugins
* CNCF project
* Uses a simple JSON-based configuration schema

### Fundamental Networking Rules

* Containers within the same Pod can communicate freely
* All Pods can communicate with all other Pods without NAT
* Nodes and Pods communicate bidirectionally without NAT
* A Pod’s IP is the same IP seen by all peers

### Networking Fundamentals Applied

#### Container-to-Container

* Containers in the same Pod share:

  * Network namespace
  * IP address
* Enables communication over `localhost`

#### Pod-to-Pod

* Each Pod receives a cluster-unique IP for its lifetime
* Pods are ephemeral by design

#### Pod-to-Service

* Managed by kube-proxy
* Services receive a persistent, cluster-unique IP
* Services outlive individual Pods

#### External-to-Service

* Handled by kube-proxy
* Often integrated with:

  * Cloud load balancers
  * External traffic managers

---

## Summary

Kubernetes architecture separates concerns between cluster-wide control, node-level execution, and extensible networking and cloud integration, allowing scalable and resilient container orchestration.
