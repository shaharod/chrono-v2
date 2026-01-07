from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from fastapi.middleware.cors import CORSMiddleware

import models, schemas, crud
from database import SessionLocal, engine

# 1. Create the Database Tables (if they don't exist yet)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 2. CORS Configuration (Allow React to talk to Python)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # The address of your React App
    allow_credentials=True,
    allow_methods=["*"], # Allow all types (GET, POST, PUT, DELETE)
    allow_headers=["*"],
)

# 3. Dependency (The Database Session Manager)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# ==========================
# PATIENT ROUTES
# ==========================

@app.post("/patients/", response_model=schemas.Patient)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    # Check if national_id already exists
    db_patient = crud.get_patient_by_national_id(db, national_id=patient.national_id)
    if db_patient:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists")
    return crud.create_patient(db=db, patient=patient)


@app.get("/patients/", response_model=List[schemas.Patient])
def read_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_patients(db, skip=skip, limit=limit)

@app.get("/patients/{patient_id}", response_model=schemas.Patient)
def read_patient(patient_id: int, db: Session = Depends(get_db)):
    db_patient = crud.get_patient(db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient


@app.delete("/patients/{patient_id}", response_model=schemas.Patient)
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    db_patient = crud.delete_patient(db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient



# ==========================
# PRESCRIPTION ROUTES
# ==========================

@app.post("/patients/{patient_id}/prescriptions/", response_model=schemas.Prescription)
def create_prescription_for_patient(
    patient_id: int, prescription: schemas.PrescriptionCreate, db: Session = Depends(get_db)
):
    return crud.create_prescription(db=db, prescription=prescription, patient_id=patient_id)

@app.put("/prescriptions/{prescription_id}/dispense", response_model=schemas.Prescription)
def dispense_drug(prescription_id: int, db: Session = Depends(get_db)):
    # Marks a drug as 'picked up'
    db_drug = crud.dispense_drug(db, prescription_id=prescription_id)
    if db_drug is None:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return db_drug

@app.get("/prescriptions/renewable", response_model=List[schemas.Prescription])
def read_renewable_prescriptions(db: Session = Depends(get_db)):
    # Returns the filtered list based on your 30-day logic
    return crud.get_renewable_prescriptions(db)

# ==========================
# DASHBOARD ROUTES
# ==========================

@app.get("/probation/", response_model=List[schemas.ProbationStatus])
def read_probation_dashboard(db: Session = Depends(get_db)):
    # Calculates status on-the-fly
    return crud.get_probation_dashboard(db)
