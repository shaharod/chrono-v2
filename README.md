# Chrono v2 - Clinic Management System

## Project Overview
This version replaces the PostgreSQL architecture with **MSSQL (SQL Server)** running on **OrbStack**. The goal is a professional, scalable medical system.

**Version:** 2.1.0 (Backend Complete)
**Status:** 🟢 Backend Active | 🟡 Frontend Pending

Chrono is a specialized management system for tracking chronic prescriptions, patient eligibility, and probation status. It automates the calculation of "overdue" patients and identifies prescriptions eligible for renewal based on strict logic rules.

---

## 🛠 Tech Stack

### Backend (Completed)
* **Language:** Python 3.10+
* **Framework:** FastAPI
* **Database:** Microsoft SQL Server (ODBC Driver 18)
* **ORM:** SQLAlchemy
* **Validation:** Pydantic v2

### Frontend (Upcoming)
* **Framework:** React.js
* **Styling:** Material UI (MUI)

---

## 🚀 Features

### 1. Patient Management
* **CRUD Operations:** Create, Read, and "Soft Delete" patients.
* **Duplicate Prevention:** Prevents creating patients with existing National IDs.

### 2. Probation Dashboard (The "Chrono Logic")
Automatically calculates patient status based on their last pickup date:
* **Active:** < 30 days.
* **Warning:** 30 - 60 days.
* **Probation:** 60 - 90 days.
* **Removal:** > 90 days.

### 3. Smart Prescriptions
* **Renewal Window:** Filters prescriptions that are either fully dispensed OR arrived within the last 30 days (but not dispensed).
* **Dispensing:** Tracks specific drug pickups.

---

## ⚡️ How to Run the Backend

**Prerequisite:** Ensure your SQL Server container/service is running.

1.  **Navigate to the backend folder:**
    ```bash
    cd src/backend
    ```

2.  **Start the Server:**
    ```bash
    python -m uvicorn main:app --reload
    ```

3.  **Access the API Docs:**
    * Open your browser to: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
    * Use the **Swagger UI** to test endpoints manually.

---

## 📂 Project Structure

```text
chrono-v2/
├── .env                  # Configuration & Secrets
├── README.md             # Project Documentation
├── TODO.md               # Task Tracking
├── docs/                 # Documentation & Architecture
│   ├── architecture/     # Diagrams & Drafts
│   ├── sql/              # SQL Schemas
│   ├── actions_flow.md
│   ├── system_design.md
│   └── version_history.md
└── src/
    ├── backend/          # Python FastAPI Application
    │   ├── main.py       # API Entry Point
    │   ├── models.py     # Database Models
    │   ├── schemas.py    # Pydantic Schemas
    │   ├── crud.py       # Business Logic
    │   ├── database.py   # Database Connection
    │   ├── reset_db.py   # Utility: Reset Tables
    │   └── nuke_db.py    # Utility: Force Clean DB
    └── frontend/         # React Application (Phase 2)