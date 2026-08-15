# 🚀 Performance Testing - Upload App (Locust Branch)

This branch is dedicated to analyzing the system's performance and stability under high load using Locust. The main goal was to identify bottlenecks in the `/users/login` and `/tasks` endpoints and verify the system's behavior with multiple concurrent users.

## 🎯 Objectives

- Stress Testing: Evaluate how the system handles a high volume of concurrent requests.
- Bottleneck Identification: Detect failures in authentication and task retrieval processes.
- Metric Analysis: Measure Response Time, Failures, and Requests Per Second (RPS).

## 🛠️ Setup & Installation

### 1. Prerequisites

- Docker and Docker Compose installed.
- Python 3.x installed (if running Locust locally).

### 2. Running the Tests

To start the application and the Locust load generator, use the following command:

docker-compose up -d

Then, access the Locust web interface at: `http://localhost:8089`

## 🧪 Test Scenario

- User Behavior:
  - Login: Simulating users authenticating via the `/users/login` endpoint.
  - Task Management: Simulating users fetching and managing their tasks via the `/tasks` endpoint.
- Load Configuration:
  - Max Users: 10 (Adjustable via UI)
  - Spawn Rate: 1 user/sec

## 📊 Observations & Results

- Authentication Stress: Observed high failure rates in the `/users/login` endpoint during peak loads, which indicated issues with session/token management or database locking.
- Performance Gap: Identified a significant difference between successful requests and total requests under stress.
- Stability: The system remains stable, but response times increase as the number of concurrent users grows.

## 📝 Key Findings

- The `on_start` method in the Locust file was critical for simulating a real user journey (Login $\rightarrow$ Use API).
- The importance of differentiating between "Virtual Users" and "Total Requests" was highlighted during the analysis.
