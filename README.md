# Project Chrono (v2.0.0)
Managing medical care cycles with a robust SQL Server foundation.

## Project Overview
This version replaces the PostgreSQL architecture with **MSSQL (SQL Server)** running on **OrbStack**. The goal is a professional, scalable medical system.

## Directory Structure
- **`/docs`**: Contains Excel drafts, architecture diagrams, and versioning logs.
- **`/src`**:
    - **`/backend`**: FastAPI wrapper and database management logic.
    - **`/frontend`**: (Future) React/Vite interface.

## Tech Stack
- **Database**: SQL Server (MSSQL) via OrbStack.
- **Backend**: Python 3.x / FastAPI.
- **Drivers**: `pyodbc` for SQL Server connectivity.
- **Version Control**: Git (Major Version 2.x).

## How to Run
1. Start OrbStack and ensure the SQL Server container is running.
2. Navigate to `src/backend`.
3. (Future) `uvicorn main:app --reload`.