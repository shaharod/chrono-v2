"""
CRUD Operations (Create, Read, Update, Delete).

This file contains the core business logic and database interactions.
It acts as the "Worker" that executes queries, such as:
- Fetching patients and prescriptions.
- Handling "Soft Deletes" (marking active/inactive).
- Calculating probation status on-the-fly.
- Filtering renewable prescriptions based on logic rules.
"""


from sqlalchemy.orm import Session
from datetime import date
import models, schemas

from typing import List
from sqlalchemy import or_, and_
from datetime import date, timedelta



# ==========================
#           READ
# ==========================

def get_patient(db: Session, patient_id: int):
    """
    finding patient using internal db id
    """
    return db.query(models.Patient).filter(models.Patient.patient_id == patient_id).first()


def get_patient_by_national_id(db: Session, national_id: str):
    """
    finding patient using national id
    """
    return db.query(models.Patient).filter(models.Patient.national_id == national_id).first()


def get_patients(db: Session, skip: int = 0, limit: int = 100):
    """
    returns a list of all active patients
    """

    return db.query(models.Patient)\
             .filter(models.Patient.is_active == True)\
             .offset(skip).limit(limit).all()



# ==========================
#           CREATE
# ==========================

def create_patient(db: Session, patient: schemas.PatientCreate):
    # 1. Convert the Schema (Pydantic) to a Model (SQLAlchemy)
    db_patient = models.Patient(
        national_id=patient.national_id,
        private_name=patient.private_name,
        last_name=patient.last_name,
        email=patient.email,
        location=patient.location,
        last_picked_up_date=patient.last_picked_up_date
    )


    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


def create_prescription(db: Session, prescription: schemas.PrescriptionCreate, patient_id: int):
    db_prescription = models.Prescription(
        **prescription.model_dump(), # Shortcut to unpack all fields (name, notes, etc.)
        patient_id=patient_id  # Link it to the patient
    )

    db.add(db_prescription)
    db.commit()
    db.refresh(db_prescription)
    return db_prescription



# ==========================
#          UPDATE
# ==========================

def dispense_drug(db: Session, prescription_id: int):
    """
    finds a given prescription and marks it as dispensed
    """
    # Finds the prescription and marks it as dispensed
    db_drug = db.query(models.Prescription).filter(models.Prescription.prescription_id == prescription_id).first()
    if db_drug:
        db_drug.dispensed = True
        db.commit()
        db.refresh(db_drug)
    return db_drug



# ==========================
#           DELETE
# ==========================

def delete_patient(db: Session, patient_id: int):
    """
    performing sfot deletion - marking patient as inactive to ignore
    """

    # find patient by id
    patient = db.query(models.Patient).filter(models.Patient.patient_id == patient_id).first()
    
    # mark as inactive if found (soft delete)
    if patient:
        patient.is_active = False
        db.commit()
        db.refresh(patient)
        
    return patient




# ==========================
#      PROBATION LOGIC
# ==========================

def get_probation_dashboard(db: Session):
    """
    scans all patients and calculates their status based on 'last_picked_up_date'.
    """
    patients: List[models.Patient] = db.query(models.Patient).all()
    results = []
    
    for p in patients:
        days_overdue = 0
        status = "Active"
        
        # Only calculate if they have ever picked up before
        if p.last_picked_up_date:
            delta = date.today() - p.last_picked_up_date
            days_overdue = delta.days

            if days_overdue > 90:
                status = "Removal"
            elif days_overdue > 60:
                status = "Probation"
            elif days_overdue > 30:
                status = "Warning"
        else:
            status = "New"

        # Add to the list
        results.append({
            "patient_id": p.patient_id,
            "national_id": p.national_id,
            "name": f"{p.last_name}, {p.private_name}",
            "last_picked_up_date": p.last_picked_up_date,
            "days_overdue": days_overdue,
            "status": status
        })
        
    return results


def get_renewable_prescriptions(db: Session):
    """
    Returns prescriptions eligible for renewal:
    1. Already dispensed.
    2. NOT dispensed, but arrived within the last 30 days.
    (Excludes undispensed prescriptions older than 30 days).
    Ordered by National ID.
    """
    thirty_days_ago = date.today() - timedelta(days=30)

    return db.query(models.Prescription)\
        .join(models.Patient)\
        .filter(models.Patient.is_active == True)\
        .filter(
            or_(
                models.Prescription.dispensed == True,
                and_(
                    models.Prescription.dispensed == False,
                    models.Prescription.arrived_at_clinic >= thirty_days_ago
                )
            )
        )\
        .order_by(models.Patient.national_id)\
        .all()