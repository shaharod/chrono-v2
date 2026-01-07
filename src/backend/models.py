"""
SQLAlchemy Database Models (Table Definitions).

This file maps Python classes to actual SQL Server tables.
It defines:
- The structure of the 'Patients' and 'Prescriptions' tables.
- Columns, Data Types, and Primary/Foreign Keys.
- Relationships (e.g., One Patient -> Many Prescriptions).
"""


from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base

# Patients table
class Patient(Base):
    __tablename__ = "Patients"

    # primary key
    patient_id = Column(Integer, primary_key=True, index=True)

    # rest of the columns
    national_id = Column(String(20), unique=True, index=True)
    private_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100))
    location = Column(String(50))
    last_picked_up_date = Column(Date)
    is_active = Column(Boolean, default=True)

    # Relationship: A patient has many prescriptions
    # 'cascade="all, delete-orphan"' means if you delete a patient, their prescriptions are deleted too.
    prescriptions = relationship("Prescription", back_populates="patient", cascade="all, delete-orphan")


# Prescriptions table
class Prescription(Base):
    __tablename__ = "Prescriptions"

    # primary key
    prescription_id = Column(Integer, primary_key=True, index=True)

    # rest of the columns
    patient_id = Column(Integer, ForeignKey("Patients.patient_id"))
    drug_name = Column(String(100))
    arrived_at_clinic = Column(Date)
    dispensed = Column(Boolean, default=False)
    notes = Column(Text)

    # Relationship: A prescription belongs to one patient
    patient = relationship("Patient", back_populates="prescriptions")