# Shop Service

## Overview

Shop Service is a microservice within a cloud-native e-commerce platform. It is responsible for managing shop entities — creating, reading, updating, and deleting shops. The service exposes both a **REST API (HTTP)** via FastAPI and a **gRPC interface** for direct inter-service communication, running both protocols concurrently on separate ports.

The service is built with Python 3.13, uses PostgreSQL as its database, and is containerized for deployment on **AWS EKS** (Elastic Kubernetes Service) using the **AWS ALB Ingress Controller**.

---

## Table of Contents

1. [Tech Stack](#tech-stack)
2. [Inter-Service Communication](#inter-service-communication)
3. [Project Structure](#project-structure)
4. [Environment Variables](#environment-variables)
5. [Local Setup](#local-setup)
6. [Running with Docker](#running-with-docker)
7. [Database Migrations](#database-migrations)
8. [REST API Endpoints](#rest-api-endpoints)
9. [gRPC Interface](#grpc-interface)
10. [AWS Services](#aws-services)
11. [Kubernetes Deployment](#kubernetes-deployment)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| ASGI Server | Uvicorn |
| ORM | SQLAlchemy (async) |
| Database Driver | asyncpg |
| Database | PostgreSQL |
| Migrations | Alembic |
| gRPC | grpcio / grpcio-tools |
| Validation | Pydantic v2 |
| Containerization | Docker (multi-stage, non-root) |
| Orchestration | Kubernetes (AWS EKS) |
| Package Manager | uv |

---

## Inter-Service Communication

The service supports two communication protocols:

- **REST (HTTP)** — External-facing API served on port `5000`. Accessible via the AWS ALB at path prefix `/shops`.
- **gRPC** — Internal service-to-service communication on port `50051`. Other microservices (cart, product, review) use the generated gRPC stubs from the shared `contracts/` directory to call this service directly within the cluster using `ClusterIP` DNS resolution (`shop-service-service:50051`).

The gRPC server starts and stops alongside the FastAPI application via its `lifespan` context manager. Proto definitions are maintained in `contracts/app/generated/shop/shop.proto` and stubs are regenerated using `make proto`.

---

## Project Structure

```
shop-service/
├── app/
│   ├── main.py              # FastAPI app + gRPC lifespan
│   ├── core/
│   │   ├── config.py        # Environment config
│   │   └── database.py      # Async SQLAlchemy engine & session
│   ├── models/              # SQLAlchemy ORM models
│   ├── schemas/             # Pydantic request/response schemas
│   ├── services/            # Business logic layer
│   ├── controllers/         # Route handler logic
│   ├── routes/              # FastAPI router definitions
│   ├── grpc/
│   │   ├── server.py        # gRPC server setup
│   │   └── handlers.py      # gRPC method implementations
│   └── generated/           # Compiled gRPC Python stubs
├── alembic/                 # Database migrations
├── protos/                  # Source .proto files
├── k8s/                     # Kubernetes manifests
├── Dockerfile
├── docker-compose.yaml
└── pyproject.toml
```

---

## Environment Variables

Copy `k8s/secret.example.yaml` as a reference. Create a `.env` file in the `shop-service/` directory for local development:

| Variable | Required | Default | Description |
|---|---|---|---|
| `DB_URL` | Yes | — | PostgreSQL async connection URL (`postgresql+asyncpg://user:pass@host:5432/db`) |
| `PORT` | No | `5000` | HTTP server port |
| `GRPC_SERVER_PORT` | No | `50051` | gRPC server port |

---

## Local Setup

**Prerequisites:** Python 3.13+, `uv`, a running PostgreSQL instance.

```bash
# Clone the repo and navigate to the service
cd shop-service

# Create and activate a virtual environment
uv venv
source .venv/Scripts/activate  # Windows
# source .venv/bin/activate    # Linux/macOS

# Install dependencies
uv sync

# Create a .env file with your DB_URL (see Environment Variables above)

# Run database migrations
alembic upgrade head

# Start the development server
uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
```

**Regenerate gRPC stubs** (after modifying `.proto` files):

```bash
make proto
```

---

## Running with Docker

From the repository root:

```bash
# Build and start the service
docker compose up --build

# Stop the service
docker compose down
```

The service will be available at:
- HTTP: `http://localhost:5000`
- gRPC: `localhost:50051`

---

## Database Migrations

```bash
# Apply all pending migrations
alembic upgrade head

# Create a new migration (auto-detect model changes)
alembic revision --autogenerate -m "description"

# Downgrade one revision
alembic downgrade -1
```

**Migration history:**
1. `01fcf6d82e74` — Create `shops` table
2. `9cfe0466e5b0` — Add `email` and `phone` columns to `shops`

---

## REST API Endpoints

**Base URL:** `http://localhost:5000`

| Method | Path | Description | Request Body |
|---|---|---|---|
| `GET` | `/shops` | Service status | — |
| `GET` | `/shops/health` | Health check | — |
| `GET` | `/shops/` | List all shops | — |
| `GET` | `/shops/{id}` | Get shop by UUID | — |
| `POST` | `/shops/` | Create a shop | `ShopCreate` |
| `PATCH` | `/shops/{id}` | Partially update a shop | `ShopUpdate` |
| `DELETE` | `/shops/{id}` | Delete a shop | — |

### Request / Response Schemas

**`ShopCreate`** (POST body):
```json
{
  "name": "string",
  "description": "string",
  "email": "user@example.com",
  "phone": "string",
  "location": "string",
  "owner_id": "uuid"
}
```

**`ShopUpdate`** (PATCH body — all fields optional):
```json
{
  "name": "string",
  "description": "string",
  "email": "user@example.com",
  "phone": "string",
  "location": "string"
}
```

**`ShopRead`** (response):
```json
{
  "id": "uuid",
  "name": "string",
  "description": "string",
  "email": "user@example.com",
  "phone": "string",
  "location": "string",
  "owner_id": "uuid",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

**Error Responses:** `404 Not Found` (shop not found), `500 Internal Server Error`.

Interactive API docs available at `/docs` (Swagger UI) and `/redoc`.

---

## gRPC Interface

**Proto package:** `app.generated.shop`  
**Default port:** `50051`

```protobuf
service ShopService {
  rpc CreateShop(ShopCreate)   returns (Shop);
  rpc GetShop(ShopID)          returns (Shop);
  rpc GetAllShops(VoidNoParam) returns (Shops);
  rpc UpdateShop(ShopUpdate)   returns (Shop);
  rpc DeleteShop(ShopID)       returns (VoidNoParam);
}
```

| RPC | Input | Output | Error Codes |
|---|---|---|---|
| `CreateShop` | `ShopCreate` | `Shop` | `INTERNAL` |
| `GetShop` | `ShopID` | `Shop` | `NOT_FOUND`, `INTERNAL` |
| `GetAllShops` | `VoidNoParam` | `Shops` | `INTERNAL` |
| `UpdateShop` | `ShopUpdate` | `Shop` | `NOT_FOUND`, `INTERNAL` |
| `DeleteShop` | `ShopID` | `VoidNoParam` | `NOT_FOUND`, `INTERNAL` |

Other services reference the shared `.proto` from the `contracts/` directory at the repository root.

---

## AWS Services

| Service | Usage |
|---|---|
| **Amazon EKS** | Kubernetes cluster hosting all microservices |
| **Amazon ECR** | Container image registry (`323928186636.dkr.ecr.us-east-1.amazonaws.com/shop-service`) |
| **AWS ALB (Elastic Load Balancing)** | Internet-facing Application Load Balancer managed by the AWS Load Balancer Controller; routes `/shops` traffic to the service |
| **Amazon EC2** | Worker nodes (VPCs, subnets, security groups) used by EKS |
| **AWS ACM** | TLS/SSL certificate management for HTTPS on the ALB |
| **AWS IAM** | IAM policy grants the Load Balancer Controller permissions to manage ALB, target groups, security groups, and ACM certificates |

---

## Kubernetes Deployment

Manifests are located in `k8s/`.

| Resource | Details |
|---|---|
| `deployment.yaml` | 2 replicas, image pulled from ECR, ports 5000 & 50051, env from `shop-service-envs` Secret |
| `service.yaml` | `ClusterIP` service exposing ports 5000 (http) and 50051 (grpc) |
| `ingress.yaml` | AWS ALB, internet-facing, routes `prefix /shops` to `shop-service-service:5000` |
| `secret.example.yaml` | Template for the `shop-service-envs` Kubernetes Secret |

**Deploy to EKS:**

```bash
# Authenticate Docker with ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  323928186636.dkr.ecr.us-east-1.amazonaws.com

# Build and push image
docker build -t shop-service ./shop-service
docker tag shop-service:latest \
  323928186636.dkr.ecr.us-east-1.amazonaws.com/shop-service:latest
docker push 323928186636.dkr.ecr.us-east-1.amazonaws.com/shop-service:latest

# Apply Kubernetes manifests
kubectl apply -f shop-service/k8s/
```
