# Task Management System

A full-stack **Task Management Application** built with **Vue 3 (TypeScript)** for the frontend and a **microservices backend** using **Python (FastAPI)** and **Rust (Axum)**. The app provides task CRUD operations, filtering, pagination, and real-time updates via WebSockets. The project includes containerization, automated deployment, and testing.

---

## 🚀 Features

### ✅ Frontend (Vue 3 + TypeScript + Tailwind CSS)
- **Task List** – table with columns: `ID`, `Title`, `Description`, `Status`, `Created Date`, `Actions`
- **Add Task** – form with client-side validation
- **Edit Task** – inline or modal editing with confirmation
- **Delete Task** – with confirmation dialog
- **Filter Tasks** – by status (`To Do`, `In Progress`, `Done`)
- **Pagination** – when tasks exceed 10 items
- **Responsive Design** – optimized for desktop and mobile

### ✅ Backend
- **Python (FastAPI)** – primary REST API for tasks
- **Rust (Axum)** – microservice handling performance-critical endpoints
- **Endpoints**:
    - `GET /api/tasks` – list tasks with pagination & filtering
    - `POST /api/tasks` – create new task
    - `PUT /api/tasks/{id}` – update existing task
    - `DELETE /api/tasks/{id}` – delete task
- **WebSockets** – real-time task updates
- **Validation** – server-side input validation for all requests

### ✅ Infrastructure
- **Docker** – containerized frontend and backend
- **Docker Compose** – orchestration for multi-service setup
- **AWS-ready** – includes `cloudformation.yml` for S3 + backend deployment
- **Local Development** – LocalStack support for AWS simulation

### ✅ Bonus Features
- **Unit Tests** – for both backend and Rust microservice
- **End-to-End Tests** – Playwright for UI testing
- **CI/CD** – GitHub Actions for automated testing and deployment
- **Real-time updates** – via WebSockets

---

## 🏗 Architecture

Frontend (Vue 3 + TypeScript)
|
| REST + WebSockets
v
Backend API (FastAPI) <-> Rust Microservice (Axum)
|
| Database (optional, in-memory for demo)


---

## 🛠 Tech Stack

**Frontend**:  
- Vue 3, TypeScript, Vite  
- Tailwind CSS  
- Axios (API calls)  
- Playwright (E2E testing)  

**Backend**:  
- Python 3 + FastAPI  
- Rust + Axum  
- Pydantic (validation)  
- SQLAlchemy or in-memory store  
- pytest (unit tests)  

**Infrastructure**:  
- Docker & Docker Compose  
- AWS CloudFormation & LocalStack  
- GitHub Actions (CI/CD)  

---

## ⚡ Installation & Setup

### ✅ Clone the repository
```bash
git clone https://github.com/your-username/task-management-system.git
cd task-management-system
```

**Development Setup (Docker)**
```bash
docker-compose up --build
```

- This will start:
- Frontend at ```http://localhost:5173```
- Backend at ```http://localhost:8000```
- Rust microservice at ```http://localhost:8080```

---

## 📡 API Endpoints ( Python/ FastAPI )

| Method | Endpoint          | Description                     |
| ------ | ----------------- | ------------------------------- |
| GET    | `/api/tasks`      | List tasks (filter, pagination) |
| POST   | `/api/tasks`      | Create a new task               |
| PUT    | `/api/tasks/{id}` | Update a task                   |
| DELETE | `/api/tasks/{id}` | Delete a task                   |

## ⚙️ Microservice Endpoints (Rust / Axum)

- The Rust microservice provides additional functionality, currently for exporting tasks as CSV.

| Method | Endpoint   | Description              |
|--------|------------|--------------------------|
| GET    | `/convert` | Export tasks as CSV file |

---

## ✅ Testing
### Backend (Python + FastAPI)
#### Unit + E2E Tests
```bash
cd backend
pytest -v
```

### Frontend (TypeScript + Vue)
#### Unit + E2E Tests
```bash
cd frontend
npm install   
npx playwright install
npm run test:unit 
npm run test:e2e
```

---

## ☁ Deployment
Local Development with LocalStack
```bash
cd infra
chmod +x cf_deploy.sh
./cf_deploy.sh
```
- AWS Deployment (LocalStack simulation)
- Upload frontend to S3
- Use cloudformation.yml for infrastructure setup

---

## 🔄 CI/CD
### GitHub Actions workflow includes:
- Build & deploy frontend and backend to live-demo

---

## 📸 Screenshots
<img width="1704" height="889" alt="image" src="https://github.com/user-attachments/assets/a126f7da-7fba-4c67-9b74-2806abdbbba0" />

---

## 🔗 Live Demo
- Frontend: ```https://task-management-theta-sable-82.vercel.app```
- Backend API: ```https://task-management-j216.onrender.com```
- Rust Microservice: ```https://task-management-microservice-gbau.onrender.com```
- Note: Due to free hosting limitations, live demos may occasionally be unavailable.

---

## 📘 API Docs
Swagger UI at: ```http://localhost:8000/docs```
