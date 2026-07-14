#  Satellite Anomaly Detector

A containerized satellite telemetry monitoring system that simulates satellite data, detects anomalies using a FastAPI backend, stores them in PostgreSQL, and visualizes results in a Streamlit dashboard. Infrastructure is provisioned and configured automatically using Terraform and Ansible, and deployed on AWS EC2 with automated CI/CD using Jenkins and GitHub Webhooks.

## Architecture

```
┌─────────────────────────┐
│   Terraform (provision)  │
│   → EC2 + SG + Key Pair  │
└──────────────┬────────────┘
               │
               ▼
┌─────────────────────────┐
│   Ansible (configure)    │
│  → Docker + Deploy Stack │
└──────────────┬────────────┘
               │
               ▼
┌─────────────────────────┐
│     Simulator Service    │
│  (Generates Telemetry)   │
└──────────────┬───────────┘
               │  POST /telemetry/
               ▼
┌────────────────────────┐
│     FastAPI Backend    │
│      (port 8000)       │
│ • Receives telemetry   │
│ • Detects anomalies    │
│ • Stores to PostgreSQL │
└──────────────┬─────────┘
               │
               ▼
┌──────────────────────────┐
│     PostgreSQL Database  │
│       (port 5432)        │
└──────────────┬───────────┘
               │  GET /anomalies/latest
               ▼
┌──────────────────────────┐
│     Streamlit Dashboard  │
│        (port 8501)       │
│ • Live anomaly alerts    │
│ • Analytics charts       │
│ • 3D Orbit visualization │
└───────────────────────────┘
```

##  Tech Stack

- **Backend:** FastAPI + SQLAlchemy + PostgreSQL
- **Dashboard:** Streamlit + Plotly
- **Containerization:** Docker + Docker Compose
- **Infrastructure as Code:** Terraform (provisioning) + Ansible (configuration & deployment)
- **Cloud:** AWS EC2 (Ubuntu 22.04, t3.micro)
- **CI/CD:** Jenkins + GitHub Webhooks
- **Secrets Management:** Ansible Vault

## 📁 Project Structure

```
satellite-anomaly-detector/
│-- backend/
│   │-- core/          # database, models, schemas
│   │-- routes/
│   │-- services/
│   │-- main.py
│-- dashboard/
│   │-- streamlit_app.py
│   │-- Dockerfile
│-- simulator/
│   │-- simulator.py
│   │-- Dockerfile
│-- terraform/         # EC2, security group, key pair provisioning
│   │-- main.tf
│   │-- ec2.tf
│   │-- sg.tf
│   │-- output.tf
│   │-- variables.tf
│-- ansible/           # server config, Docker install, app deployment
│   │-- playbook.yaml
│   │-- inventory.ini
│   │-- group_vars/
│       │-- all/vault.yml   # encrypted secrets
│-- Dockerfile         # backend Dockerfile
│-- docker-compose.yml
│-- Jenkinsfile
│-- update_inventory.sh # auto-syncs Ansible inventory from Terraform output
│-- .env
```

##  Setup & Installation

### Prerequisites
- Docker & Docker Compose
- Git

### 1. Clone the repository
```bash
git clone https://github.com/ridhima-2412/satellite-anomaly-detector.git
cd satellite-anomaly-detector
```

### 2. Create `.env` file
```
DB_URL=postgresql://postgres:postgres@db:5432/telemetry
BACKEND_URL=http://backend:8000
```

### 3. Run with Docker Compose
```bash
docker compose up --build -d
```

### 4. Access the services
- FastAPI docs: `http://localhost:8000/docs`
- Streamlit dashboard: `http://localhost:8501`

##  Infrastructure as Code (Terraform + Ansible)

Instead of manually provisioning and configuring the EC2 instance, the entire infrastructure lifecycle is automated:

- **Terraform** provisions the AWS infrastructure — EC2 instance, security group (ports 22, 8000, 8501), and SSH key pair — from scratch, reproducibly.
- **Ansible** then configures the server: installs Docker, clones this repository, generates the `.env` file from encrypted secrets, and runs `docker compose up`.
- **Ansible Vault** encrypts sensitive values (DB URL, backend URL) so no plaintext secrets are committed to the repo.
- A helper script (`update_inventory.sh`) automatically syncs Terraform's output (the instance's public IP) into Ansible's inventory file — no manual copying between provisioning and configuration steps.

### Prerequisites
- Terraform
- Ansible
- AWS CLI configured with valid credentials (`aws configure`)
- An SSH key pair generated locally (`ssh-keygen`), with the public key registered via Terraform

### Deploying from scratch

```bash
# 1. Provision infrastructure
cd terraform
terraform init
terraform apply

# 2. Sync Ansible inventory with the new instance's IP
cd ..
./update_inventory.sh

# 3. Configure server and deploy the app
cd ansible
ansible-playbook -i inventory.ini playbook.yaml --ask-vault-pass
```

### Tearing down

```bash
cd terraform
terraform destroy
```

This makes the entire environment disposable — spin it up for development or demos, tear it down when not in use, with no manual server setup steps required.

##  CI/CD Pipeline

Every push to the `Main` branch automatically:
1. Triggers Jenkins via GitHub Webhook
2. SSHes into the AWS EC2 instance (provisioned via Terraform, configured via Ansible)
3. Pulls latest code
4. Rebuilds and restarts all Docker containers

##  Services

| Service | Description | Port |
|---|---|---|
| Backend | FastAPI anomaly detection API | 8000 |
| Dashboard | Streamlit visualization | 8501 |
| Simulator | Satellite telemetry generator | - |
| Database | PostgreSQL storage | 5432 |