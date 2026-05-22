markdown# 🛰️ Satellite Anomaly Detector

A containerized satellite telemetry monitoring system that simulates satellite data, detects anomalies using a FastAPI backend, stores them in PostgreSQL, and visualizes results in a Streamlit dashboard. Deployed on AWS EC2 with automated CI/CD using Jenkins and GitHub Webhooks.

## 🏗️ Architecture
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

## 🚀 Tech Stack

- **Backend:** FastAPI + SQLAlchemy + PostgreSQL
- **Dashboard:** Streamlit + Plotly
- **Containerization:** Docker + Docker Compose
- **Cloud:** AWS EC2 (Ubuntu 22.04, t2.micro)
- **CI/CD:** Jenkins + GitHub Webhooks

## 📁 Project Structure
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
│-- Dockerfile         # backend Dockerfile
│-- docker-compose.yml
│-- Jenkinsfile
│-- .env

## ⚙️ Setup & Installation

### Prerequisites
- Docker & Docker Compose
- Git

### 1. Clone the repository
```bash
git clone https://github.com/ridhima-2412/satellite-anomaly-detector.git
cd satellite-anomaly-detector
```

### 2. Create `.env` file
DB_URL=postgresql://postgres:postgres@db:5432/telemetry
BACKEND_URL=http://backend:8000

### 3. Run with Docker Compose
```bash
docker compose up --build -d
```

### 4. Access the services
- FastAPI docs: `http://localhost:8000/docs`
- Streamlit dashboard: `http://localhost:8501`

## 🔄 CI/CD Pipeline

Every push to the `Main` branch automatically:
1. Triggers Jenkins via GitHub Webhook
2. SSHes into AWS EC2
3. Pulls latest code
4. Rebuilds and restarts all Docker containers

## 🛰️ Services

| Service | Description | Port |
|---|---|---|
| Backend | FastAPI anomaly detection API | 8000 |
| Dashboard | Streamlit visualization | 8501 |
| Simulator | Satellite telemetry generator | - |
| Database | PostgreSQL storage | 5432 |