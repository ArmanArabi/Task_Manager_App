# 📦 Task Management API - Base Version
This branch (`upload-app-base`) serves as the *initial foundation of the project. It is designed for rapid prototyping and local testing.

## 🛠️ Current Status
- Database: SQLite (Lightweight, file-based storage)
- Focus: Establishing core API logic and basic CRUD operations.
- Deployment: Dockerized for a "plug-and-play" experience.

## 🚀 Quick Start
1. Environment: Setup your `.env` file with `SQLALCHEMY_DATABASE_URL=sqlite:///./sqlite.db`.
2. Run with Docker:

   docker-compose up --build
   

3. 
API Docs: Visit `http://localhost:8000/docs`

## 🛣️ Roadmap
This version is a stepping stone. In the next evolution of this project (branch: `upload-app`), the architecture is upgraded to:
- 🐘 PostgreSQL: For production-grade data management.
- ⚙️ Alembic Migrations: For professional database schema versioning.
- 🚀 Optimized Docker Networking: Improved communication between app and database.

---
