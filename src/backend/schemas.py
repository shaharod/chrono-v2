"""
Pydantic Schemas (Data Validation & Contracts).

This file defines the 'Shape' of data moving in and out of the API.
It ensures that:
- Input data (from Frontend) matches expected types (Strings, Dates).
- Output data (to Frontend) is formatted correctly.
- Internal Database IDs are hidden from creation requests but included in responses.
"""


from pydantic import BaseModel
from typing import List, Optional
from datetime import date



# ============================
#    Prescription Schemas
# ============================
class PrescriptionBase(BaseModel):
    drug_name: str
    arrived_at_clinic: Optional[date] = None
    dispensed: bool = False
    notes: Optional[str] = None


class PrescriptionCreate(PrescriptionBase):
    pass


class Prescription(PrescriptionBase):
    prescription_id: int
    patient_id: int

    class Config:
        orm_mode = True



# ============================
#       Patient Schemas
# ============================
class PatientBase(BaseModel):
    national_id: int
    private_name: str
    last_name: str
    email: Optional[str] = None
    location: Optional[str] = None
    last_picked_up_date: Optional[date] = None


class PatientCreate(PatientBase):
    pass


class Patient(PatientBase):

    patient_id: int
    is_active: bool = True
    
    # A patient includes a list of their prescriptions
    prescriptions: List[Prescription] = []

    class Config:
        orm_mode = True


# ============================
#  Probation Dashboard Schema
# ============================
# Calculated on-the-fly (not in DB)
class ProbationStatus(BaseModel):
    patient_id: int
    name: str
    last_picked_up_date: Optional[date]
    days_overdue: int
    status: str  # "Active", "Warning", "Probation", "Removal"