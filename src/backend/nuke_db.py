from database import engine
from sqlalchemy import text
import models

print("☢️  INITIATING NUCLEAR RESET...")

with engine.connect() as connection:
    # 1. KILL ALL FOREIGN KEYS
    # This SQL script finds every connection between tables and deletes it.
    print("...Severing all foreign key constraints")
    kill_fks_sql = """
    DECLARE @sql NVARCHAR(MAX) = N'';
    SELECT @sql += N'ALTER TABLE ' + QUOTENAME(OBJECT_SCHEMA_NAME(parent_object_id))
        + '.' + QUOTENAME(OBJECT_NAME(parent_object_id)) +
        ' DROP CONSTRAINT ' + QUOTENAME(name) + ';'
    FROM sys.foreign_keys;
    EXEC sp_executesql @sql;
    """
    connection.execute(text(kill_fks_sql))
    connection.commit()
    
    # 2. DELETE THE TABLES (Now that nothing is holding them back)
    print("...Dropping Prescriptions table")
    connection.execute(text("DROP TABLE IF EXISTS Prescriptions"))
    connection.commit()

    print("...Dropping Patients table")
    connection.execute(text("DROP TABLE IF EXISTS Patients"))
    connection.commit()

# 3. REBUILD FROM SCRATCH
print("✨ Constructing fresh tables...")
models.Base.metadata.create_all(bind=engine)

print("✅ SUCCESS: Database has been completely wiped and rebuilt.")