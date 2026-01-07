USE ChronoDB;
GO

-- TODO: Delete these two lines
-- cleaning tables
DROP TABLE IF EXISTS Prescriptions;
DROP TABLE IF EXISTS Patients;
GO


CREATE TABLE Patients (
    patient_id INT PRIMARY KEY IDENTITY(1,1), -- Inner count for db
    national_id NVARCHAR(20),
    private_name NVARCHAR(100),
    last_name NVARCHAR(100),
    email VARCHAR(100),
    location NVARCHAR(50),
    last_picked_up_date DATE,
    is_avtive BIT DEFAULT 1
);


CREATE TABLE Prescriptions (
    prescription_id INT PRIMARY KEY IDENTITY(1,1),  -- Inner count for db
    patient_id INT,
    drug_name NVARCHAR(100),
    arrived_at_clinic DATE,
    dispensed BIT DEFAULT 0,
    notes NVARCHAR(MAX),
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id)
);
GO