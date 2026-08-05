Task Management API - Initial Base Version

This repository contains the core implementation of the Task Management System. This specific branch (`upload-app`) represents the initial stable version of the application, focused on establishing the project architecture and basic CRUD functionalities.

## 🎯 Project Objective
The goal of this phase was to build a modular and scalable REST API using FastAPI, implementing a clean separation of concerns between the business logic, data models, and routing.

## 🏗️ Current Architecture
- Framework: FastAPI (Asynchronous Python Framework)
- Database: SQLite (Lightweight, file-based storage for rapid development)
- ORM: SQLAlchemy (For object-relational mapping and database abstraction)
- Migrations: Alembic (Version control for database schema)
- Authentication: JWT (JSON Web Tokens) for secure user access

## 🚀 Quick Start Guide

### 1. Environment Setup
Create a `.env` file in the root directory:

SQLALCHEMY_DATABASE_URL=sqlite:///./sql_app.db
SECRET_KEY=your_super_secret_key_here
ALGORITHM=HS256


### 2. Installation
Install the required dependencies:

pip install -r requirements.txt


### 3. Running the Application
Start the server using Uvicorn:

uvicorn app.main:app --reload

The API documentation (Swagger UI) will be available at: `http://127.0.0.1:8000/docs`

## 🛠️ Implemented Features
User Management: Registration, Login, and Profile management.

Task Lifecycle: Create, Read, Update, and Delete tasks.
      
Database Migrations: Basic schema setup using Alembic.
     
Dependency Injection: Implementation of modular database sessions.

## 📌 Developer's Note
This version uses SQLite, which is ideal for local development and prototyping. Future iterations of this project will migrate to PostgreSQL to support high-concurrency environments and advanced data types.

---
