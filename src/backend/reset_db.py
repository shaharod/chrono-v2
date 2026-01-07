from database import engine
from sqlalchemy import text
import models

print("🔄 Starting Database Reset...")

with engine.connect() as connection:
    # 1. Force drop the Child Table first (Prescriptions)
    print("Dropping Prescriptions table...")
    try:
        connection.execute(text("DROP TABLE IF EXISTS Prescriptions"))
        connection.commit()
    except Exception as e:
        print(f"⚠️ Could not drop Prescriptions (might not exist): {e}")

    # 2. Force drop the Parent Table second (Patients)
    print("Dropping Patients table...")
    try:
        connection.execute(text("DROP TABLE IF EXISTS Patients"))
        connection.commit()
    except Exception as e:
        print(f"⚠️ Could not drop Patients: {e}")

# 3. Rebuild everything fresh
print("✨ Creating new tables...")
models.Base.metadata.create_all(bind=engine)

print("✅ SUCCESS: Database has been fully reset!")