"""
Backend Todo list:

# TODO Database Schema Initialization
# - Create 'Patients' table with identity keys and file numbers
# - Create 'Prescriptions' table to handle the list of drugs per patient
# - Create 'Transactions' or 'Pickups' table to track the date of last pickup
# - Set up Foreign Key relationships to link drugs to patients

# TODO Establish Database Connection Manager
# - Load connection strings from .env for security
# - Implement a retry mechanism in case the Docker container is still booting

# TODO Create Patient Management Functions (CRUD)
# - Function to add new patients with a specific location
# - Function to retrieve patient profile and prescription history

# TODO Implement Probation Logic Calculator
# - Query to calculate 'days_overdue' (Current Date - Last Picked Up Date)
# - Logic to assign status: Active, Warning, Probation, Removal

# TODO Create Renewal Task Handler
# - Function to verify eligibility and create new treatment cycles
"""

if __name__ == '__main__':
    pass