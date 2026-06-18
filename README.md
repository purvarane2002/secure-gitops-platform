# Secure GitOps Deployment Platform

An automated cloud deployment platform that builds, security-scans, and deploys 
a containerised Python application to Kubernetes, with self-healing infrastructure 
and live monitoring.

Built to solve a real problem: catching security vulnerabilities before they reach 
production, not after.

## The Problem This Solves

Most deployment pipelines ship code without checking what is inside the container 
image. Vulnerabilities hide in standard packages and go undetected until they are 
already in production, by which point it is an emergency.

This platform catches that at the pipeline stage, before anything reaches the cluster.

**On the first real test, the scanner flagged 2 critical CVEs hiding in a standard 
Python base image. Both were blocked before a single deployment took place.**

![Architecture Diagram](https://github.com/user-attachments/assets/06944bc3-84f7-4bea-aedf-7660db899d31)

The full pipeline runs automatically on every code push:
Code Push → GitHub Actions (CI)

→ pytest (automated tests)

→ Docker build

→ Trivy (security scan — blocks on CRITICAL CVEs)

→ ArgoCD (GitOps auto-deploy to Kubernetes)

→ Kubernetes (self-healing, 2 replicas)

→ Prometheus + Grafana (live monitoring)


## Key Outcomes

**Security scanning caught 2 critical CVEs before deployment**

![Trivy CVE Output](https://github.com/user-attachments/assets/f06577f3-e6c1-4d7a-95da-3f7280254fb0)

Trivy detected CVE-2026-42496 and CVE-2026-8376 in the `python:3.11-slim` base 
image — both critical vulnerabilities in `perl-base`. Fixed by switching to 
`python:3.11-alpine`, which strips unnecessary packages and eliminated both risks.


**CI pipeline went from red to green after the fix**

![Green Pipeline](https://github.com/user-attachments/assets/beed1680-4d2d-437b-b22d-abfc26abf2f0)


After switching the base image, all 3 checks passed — tests, Docker build, and 
Trivy scan — in 51 seconds.


**Self-healing infrastructure**

Deleted a live pod during testing. Kubernetes detected the failure and had a 
replacement running in under 35 seconds with zero downtime, because the second 
replica kept serving traffic throughout.


**GitOps auto-deployment**

![ArgoCD Dashboard](https://github.com/user-attachments/assets/beed1680-4d2d-437b-b22d-abfc26abf2f0)

ArgoCD watches the GitHub repo and automatically syncs any change pushed to the 
`kubernetes/` folder to the running cluster. No manual `kubectl` steps required.


## Tech Stack

| Category | Tools |
|---|---|
| Application | Python, Flask |
| Containerisation | Docker |
| CI/CD | GitHub Actions |
| Security Scanning | Trivy |
| Orchestration | Kubernetes, Minikube |
| GitOps | ArgoCD |
| Monitoring | Prometheus, Grafana, Helm |
| Infrastructure as Code | Terraform |



## Project Structure
secure-gitops-platform/

├── app/

│   ├── app.py              # Flask application with health and metrics endpoints

│   ├── Dockerfile          # Container image — uses python:3.11-alpine

│   ├── requirements.txt    # Python dependencies

│   └── test_app.py         # pytest tests for all 3 endpoints

├── kubernetes/

│   ├── deployment.yaml     # 2 replicas with liveness probe on /health

│   └── service.yaml        # NodePort service

├── monitoring/             # Prometheus and Grafana configurations

└── .github/workflows/

└── ci.yaml             # Full CI pipeline with tests, Docker build, Trivy scan



## How to Run Locally

You will need Docker, Minikube, kubectl, and Helm installed on your machine.

**Step 1 — Clone the project**
```bash
git clone https://github.com/purvarane2002/secure-gitops-platform
cd secure-gitops-platform
```

**Step 2 — Start your local Kubernetes cluster**
```bash
minikube start
```

**Step 3 — Build the Docker image and load it into the cluster**
```bash
docker build -t secure-gitops-platform:v1 app/
minikube image load secure-gitops-platform:v1
```

**Step 4 — Deploy the app to Kubernetes**
```bash
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
```

**Step 5 — Get the URL to access the app**
```bash
minikube service gitops-app-service --url
```

**Step 6 — Install Prometheus and Grafana**
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace
```

**Step 7 — Open the Grafana dashboard**
```bash
kubectl --namespace monitoring port-forward svc/monitoring-grafana 3000:80
```
Go to `http://localhost:3000` — username is `admin`.


## What I Learned

Automation does not just save time. It catches the things you would have missed
doing it manually. A security scanner running on every push is not overhead, it
is the thing that stops a 3am incident.


## Author

**Purva Rane** — Cloud and DevOps Engineer
[LinkedIn](https://www.linkedin.com/in/purva-rane-) |
[GitHub](https://github.com/purvarane2002)
