"""
Urban Emergency Response & Resource Allocation System
Database Management Systems Lab (24B15CS213)
JIIT Noida-62 - Department of CSE & IT

Database Access Object & ACID Transaction Engine
"""

import os
import sqlite3
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "urban_emergency.db")
SCHEMA_FILE = os.path.join(BASE_DIR, "schema.sql")
SEED_FILE = os.path.join(BASE_DIR, "seed.sql")


class EmergencySystemError(Exception):
    """Base exception for emergency dispatch system."""
    pass


class ResourceUnavailableError(EmergencySystemError):
    """Raised when an ambulance or hospital bed cannot be allocated."""
    pass


def get_connection(db_path: str = DB_FILE) -> sqlite3.Connection:
    """
    Establish SQLite connection with Foreign Keys enabled and dict-like Row access.
    """
    conn = sqlite3.connect(db_path, timeout=15.0)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn


def init_db(force: bool = False, db_path: str = DB_FILE) -> None:
    """
    Initialize database using schema.sql and seed with seed.sql.
    If force is True, drops existing tables and recreates from scratch.
    Safely handles Windows file locks by relying on schema DROP statements.
    """
    if force and os.path.exists(db_path):
        try:
            os.remove(db_path)
        except (PermissionError, OSError):
            # On Windows, if file is currently accessed by server thread,
            # schema.sql handles clean DROP VIEW and DROP TABLE with foreign_keys = OFF.
            pass

    conn = get_connection(db_path)
    try:
        conn.execute("PRAGMA foreign_keys = OFF;")
        with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
            schema_sql = f.read()
        conn.executescript(schema_sql)

        # Seed data
        with open(SEED_FILE, "r", encoding="utf-8") as f:
            seed_sql = f.read()
        conn.executescript(seed_sql)
        conn.commit()
    finally:
        conn.close()


# -----------------------------------------------------------------------------
# Incident Intake & Patient Registration
# -----------------------------------------------------------------------------
def register_emergency(
    patient_name: str,
    age: int,
    gender: str,
    contact_phone: str,
    blood_group: str,
    triage_notes: str,
    address_line: str,
    zone_area: str,
    landmark: str,
    postal_code: str,
    emergency_type_id: int,
    severity: Optional[int] = None,
    city_district: str = "Noida",
    db_path: str = DB_FILE,
) -> int:
    """
    Registers a new incoming emergency call:
    1. Inserts or finds location
    2. Registers patient
    3. Creates EMERGENCY record (database trigger fires to record history)
    Returns emergency_id.
    """
    conn = get_connection(db_path)
    try:
        with conn:
            cursor = conn.cursor()

            # Insert Location
            cursor.execute(
                """
                INSERT INTO LOCATION (address_line, zone_area, landmark, postal_code, city_district)
                VALUES (?, ?, ?, ?, ?)
                """,
                (address_line, zone_area, landmark, postal_code, city_district),
            )
            location_id = cursor.lastrowid

            # Insert Patient
            cursor.execute(
                """
                INSERT INTO PATIENT (name, age, gender, contact_phone, blood_group, triage_medical_notes)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (patient_name, age, gender, contact_phone, blood_group, triage_notes),
            )
            patient_id = cursor.lastrowid

            # Lookup default severity if not explicitly provided
            if severity is None:
                cursor.execute(
                    "SELECT severity_default FROM EMERGENCY_TYPE WHERE type_id = ?",
                    (emergency_type_id,),
                )
                row = cursor.fetchone()
                severity = row["severity_default"] if row else 3

            # Insert Emergency Incident (Fires trg_emergency_status_insert)
            cursor.execute(
                """
                INSERT INTO EMERGENCY (patient_id, type_id, location_id, severity, status)
                VALUES (?, ?, ?, ?, 'Reported')
                """,
                (patient_id, emergency_type_id, location_id, severity),
            )
            emergency_id = cursor.lastrowid

            return emergency_id
    finally:
        conn.close()


# -----------------------------------------------------------------------------
# ACID-Compliant Transactional Resource Allocation Engine
# -----------------------------------------------------------------------------
def allocate_resources_transactional(
    emergency_id: int,
    preferred_ambulance_id: Optional[int] = None,
    preferred_hospital_id: Optional[int] = None,
    preferred_bed_id: Optional[int] = None,
    db_path: str = DB_FILE,
) -> Dict[str, Any]:
    """
    Atomically allocates an ambulance and reserves a hospital bed for an emergency.
    Guarantees ACID properties:
      - Atomicity: Either both ambulance & bed are reserved and emergency is marked dispatched,
                   or all changes roll back.
      - Consistency: Enforces foreign key constraints and prevents double-occupancy.
      - Isolation: Uses SQLite 'BEGIN IMMEDIATE' to block concurrent read-modify-write race conditions.
      - Durability: Changes are committed to disk.
      - Audit Trigger: Updating EMERGENCY status automatically executes the database trigger.
    """
    conn = get_connection(db_path)
    try:
        # BEGIN IMMEDIATE locks for write to avoid race conditions
        conn.execute("BEGIN IMMEDIATE;")
        cursor = conn.cursor()

        # 1. Verify emergency status and fetch severity
        cursor.execute(
            """
            SELECT e.emergency_id, e.severity, e.status, t.type_name, p.name AS patient_name
            FROM EMERGENCY e
            JOIN EMERGENCY_TYPE t ON e.type_id = t.type_id
            JOIN PATIENT p ON e.patient_id = p.patient_id
            WHERE e.emergency_id = ?
            """,
            (emergency_id,),
        )
        emergency = cursor.fetchone()
        if not emergency:
            raise EmergencySystemError(f"Emergency Incident #{emergency_id} not found.")

        if emergency["status"] in ("Dispatched", "In-Transit", "Admitted", "Resolved"):
            raise EmergencySystemError(
                f"Emergency #{emergency_id} is already in state '{emergency['status']}'."
            )

        severity = emergency["severity"]

        # 2. Select Eligible Available Ambulance
        # High severity (>=4) requires ALS with operational equipment
        ambulance_row = None
        if preferred_ambulance_id:
            cursor.execute(
                """
                SELECT ambulance_id, vehicle_no, type, operational_status, base_station
                FROM AMBULANCE
                WHERE ambulance_id = ? AND operational_status = 'Available'
                """,
                (preferred_ambulance_id,),
            )
            ambulance_row = cursor.fetchone()
            if not ambulance_row:
                raise ResourceUnavailableError(
                    f"Selected Ambulance #{preferred_ambulance_id} is currently unavailable."
                )
        else:
            if severity >= 4:
                # Query ALS ambulance with functional equipment
                cursor.execute(
                    """
                    SELECT a.ambulance_id, a.vehicle_no, a.type, a.operational_status, a.base_station
                    FROM AMBULANCE a
                    WHERE a.operational_status = 'Available' AND a.type = 'ALS'
                      AND a.ambulance_id IN (
                          SELECT ambulance_id FROM EQUIPMENT WHERE is_functional = 1
                      )
                    LIMIT 1
                    """
                )
                ambulance_row = cursor.fetchone()

            # Fallback to any available ambulance if ALS search yielded none for lower severity
            if not ambulance_row:
                cursor.execute(
                    """
                    SELECT a.ambulance_id, a.vehicle_no, a.type, a.operational_status, a.base_station
                    FROM AMBULANCE a
                    WHERE a.operational_status = 'Available'
                    ORDER BY CASE WHEN a.type = 'ALS' THEN 1 ELSE 2 END
                    LIMIT 1
                    """
                )
                ambulance_row = cursor.fetchone()

        if not ambulance_row:
            raise ResourceUnavailableError(
                f"Fleet Alert: No available ambulances matching Severity Level {severity}."
            )

        allocated_ambulance_id = ambulance_row["ambulance_id"]

        # 3. Select Eligible Available Hospital Bed
        # High severity (>=4) prioritizes ICU beds in Level 1 Trauma centers
        bed_row = None
        if preferred_bed_id:
            cursor.execute(
                """
                SELECT b.bed_id, b.bed_number, b.bed_type, d.dept_name, h.hospital_id, h.hospital_name
                FROM BED b
                JOIN DEPARTMENT d ON b.dept_id = d.dept_id
                JOIN HOSPITAL h ON d.hospital_id = h.hospital_id
                WHERE b.bed_id = ? AND b.is_occupied = 0
                """,
                (preferred_bed_id,),
            )
            bed_row = cursor.fetchone()
            if not bed_row:
                raise ResourceUnavailableError(
                    f"Selected Bed #{preferred_bed_id} is already occupied or unavailable."
                )
        else:
            required_bed_type = "ICU" if severity >= 4 else "General"
            hospital_filter = ""
            params: List[Any] = [required_bed_type]

            if preferred_hospital_id:
                hospital_filter = "AND h.hospital_id = ?"
                params.append(preferred_hospital_id)

            cursor.execute(
                f"""
                SELECT b.bed_id, b.bed_number, b.bed_type, d.dept_name, h.hospital_id, h.hospital_name
                FROM BED b
                JOIN DEPARTMENT d ON b.dept_id = d.dept_id
                JOIN HOSPITAL h ON d.hospital_id = h.hospital_id
                WHERE b.bed_type = ? AND b.is_occupied = 0 {hospital_filter}
                ORDER BY CASE WHEN h.emergency_level = 'Level 1 Trauma' THEN 1 ELSE 2 END
                LIMIT 1
                """,
                params,
            )
            bed_row = cursor.fetchone()

            # If ICU not available, attempt general trauma emergency bed
            if not bed_row and required_bed_type == "ICU":
                cursor.execute(
                    f"""
                    SELECT b.bed_id, b.bed_number, b.bed_type, d.dept_name, h.hospital_id, h.hospital_name
                    FROM BED b
                    JOIN DEPARTMENT d ON b.dept_id = d.dept_id
                    JOIN HOSPITAL h ON d.hospital_id = h.hospital_id
                    WHERE b.is_occupied = 0 {hospital_filter}
                    LIMIT 1
                    """,
                    params[1:] if preferred_hospital_id else [],
                )
                bed_row = cursor.fetchone()

        if not bed_row:
            raise ResourceUnavailableError(
                f"Hospital Alert: No vacant hospital bed available for patient triage."
            )

        allocated_bed_id = bed_row["bed_id"]
        allocated_hospital_id = bed_row["hospital_id"]

        # 4. Atomic Execution of Updates
        # Update Ambulance Status
        cursor.execute(
            """
            UPDATE AMBULANCE
            SET operational_status = 'Dispatched'
            WHERE ambulance_id = ?
            """,
            (allocated_ambulance_id,),
        )

        # Update Bed Occupancy
        cursor.execute(
            """
            UPDATE BED
            SET is_occupied = 1
            WHERE bed_id = ?
            """,
            (allocated_bed_id,),
        )

        # Insert Resource Allocation Record
        cursor.execute(
            """
            INSERT INTO RESOURCE_ALLOCATION (emergency_id, ambulance_id, hospital_id, bed_id, status)
            VALUES (?, ?, ?, ?, 'Dispatched')
            """,
            (emergency_id, allocated_ambulance_id, allocated_hospital_id, allocated_bed_id),
        )
        allocation_id = cursor.lastrowid

        # Update Emergency Status (Fires trg_emergency_status_update)
        cursor.execute(
            """
            UPDATE EMERGENCY
            SET status = 'Dispatched'
            WHERE emergency_id = ?
            """,
            (emergency_id,),
        )

        # Commit ACID transaction
        conn.commit()

        return {
            "success": True,
            "allocation_id": allocation_id,
            "emergency_id": emergency_id,
            "patient_name": emergency["patient_name"],
            "emergency_type": emergency["type_name"],
            "ambulance": {
                "id": allocated_ambulance_id,
                "vehicle_no": ambulance_row["vehicle_no"],
                "type": ambulance_row["type"],
                "base_station": ambulance_row["base_station"],
            },
            "hospital": {
                "id": allocated_hospital_id,
                "name": bed_row["hospital_name"],
                "department": bed_row["dept_name"],
                "bed_id": allocated_bed_id,
                "bed_number": bed_row["bed_number"],
                "bed_type": bed_row["bed_type"],
            },
            "message": f"Successfully dispatched {ambulance_row['vehicle_no']} and reserved bed {bed_row['bed_number']} at {bed_row['hospital_name']}.",
        }

    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


# -----------------------------------------------------------------------------
# Incident Status Advancement & Unit Release
# -----------------------------------------------------------------------------
def transition_emergency_status(
    emergency_id: int,
    new_status: str,
    remarks: Optional[str] = None,
    db_path: str = DB_FILE,
) -> bool:
    """
    Transitions emergency to: In-Transit, Admitted, Resolved, or Cancelled.
    Triggers automatically record each transition in EMERGENCY_STATUS_HISTORY.
    When Admitted or Resolved:
      - Sets arrival_time in RESOURCE_ALLOCATION
      - Can free ambulance back to 'Available'
    """
    valid_states = ("Pending", "Dispatched", "In-Transit", "Admitted", "Resolved", "Cancelled")
    if new_status not in valid_states:
        raise ValueError(f"Invalid status '{new_status}'. Must be one of {valid_states}.")

    conn = get_connection(db_path)
    try:
        with conn:
            cursor = conn.cursor()

            # Update EMERGENCY (Trigger trg_emergency_status_update fires)
            cursor.execute(
                "UPDATE EMERGENCY SET status = ? WHERE emergency_id = ?",
                (new_status, emergency_id),
            )

            # If custom remarks are provided, append them to the trigger-generated history entry
            if remarks and remarks.strip():
                cursor.execute(
                    """
                    UPDATE EMERGENCY_STATUS_HISTORY
                    SET remarks = remarks || ' | Notes: ' || ?
                    WHERE history_id = (
                        SELECT MAX(history_id) FROM EMERGENCY_STATUS_HISTORY WHERE emergency_id = ?
                    )
                    """,
                    (remarks.strip(), emergency_id),
                )

            # Update Resource Allocation status
            if new_status in ("Admitted", "Resolved"):
                cursor.execute(
                    """
                    UPDATE RESOURCE_ALLOCATION
                    SET arrival_time = CURRENT_TIMESTAMP, status = 'Handover-Complete'
                    WHERE emergency_id = ?
                    """,
                    (emergency_id,),
                )
                # Release ambulance back to Available
                cursor.execute(
                    """
                    UPDATE AMBULANCE
                    SET operational_status = 'Available'
                    WHERE ambulance_id IN (
                        SELECT ambulance_id FROM RESOURCE_ALLOCATION WHERE emergency_id = ?
                    )
                    """,
                    (emergency_id,),
                )

            elif new_status == "Cancelled":
                cursor.execute(
                    """
                    UPDATE RESOURCE_ALLOCATION
                    SET status = 'Cancelled'
                    WHERE emergency_id = ?
                    """,
                    (emergency_id,),
                )
                # Release both ambulance and bed
                cursor.execute(
                    """
                    UPDATE AMBULANCE
                    SET operational_status = 'Available'
                    WHERE ambulance_id IN (
                        SELECT ambulance_id FROM RESOURCE_ALLOCATION WHERE emergency_id = ?
                    )
                    """,
                    (emergency_id,),
                )
                cursor.execute(
                    """
                    UPDATE BED
                    SET is_occupied = 0
                    WHERE bed_id IN (
                        SELECT bed_id FROM RESOURCE_ALLOCATION WHERE emergency_id = ?
                    )
                    """,
                    (emergency_id,),
                )

            return True
    finally:
        conn.close()


# -----------------------------------------------------------------------------
# Read Queries & View Fetchers
# -----------------------------------------------------------------------------
def get_dashboard_metrics(db_path: str = DB_FILE) -> Dict[str, Any]:
    """Summary KPI metrics for the command center dashboard."""
    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) AS count FROM EMERGENCY WHERE status IN ('Reported', 'Pending')")
        pending_emergencies = cursor.fetchone()["count"]

        cursor.execute("SELECT COUNT(*) AS count FROM EMERGENCY WHERE status IN ('Dispatched', 'In-Transit')")
        active_dispatches = cursor.fetchone()["count"]

        cursor.execute("SELECT COUNT(*) AS count FROM AMBULANCE WHERE operational_status = 'Available'")
        available_ambulances = cursor.fetchone()["count"]

        cursor.execute("SELECT COUNT(*) AS count FROM AMBULANCE")
        total_ambulances = cursor.fetchone()["count"]

        cursor.execute("SELECT COUNT(*) AS count FROM BED WHERE is_occupied = 0")
        vacant_beds = cursor.fetchone()["count"]

        cursor.execute("SELECT COUNT(*) AS count FROM BED WHERE bed_type = 'ICU' AND is_occupied = 0")
        vacant_icu_beds = cursor.fetchone()["count"]

        cursor.execute("SELECT COUNT(*) AS count FROM BED")
        total_beds = cursor.fetchone()["count"]

        return {
            "pending_emergencies": pending_emergencies,
            "active_dispatches": active_dispatches,
            "available_ambulances": available_ambulances,
            "total_ambulances": total_ambulances,
            "vacant_beds": vacant_beds,
            "vacant_icu_beds": vacant_icu_beds,
            "total_beds": total_beds,
        }
    finally:
        conn.close()


def get_active_emergencies(db_path: str = DB_FILE) -> List[Dict[str, Any]]:
    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vw_active_emergencies ORDER BY severity DESC, reported_time DESC")
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()


def get_hospital_bed_occupancy(db_path: str = DB_FILE) -> List[Dict[str, Any]]:
    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vw_hospital_bed_occupancy ORDER BY vacant_icu_beds DESC")
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()


def get_ambulance_fleet(db_path: str = DB_FILE) -> List[Dict[str, Any]]:
    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vw_ambulance_fleet_status ORDER BY ambulance_id ASC")
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()


def get_status_history(emergency_id: Optional[int] = None, db_path: str = DB_FILE) -> List[Dict[str, Any]]:
    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        if emergency_id:
            cursor.execute(
                """
                SELECT h.*, p.name AS patient_name, e.severity
                FROM EMERGENCY_STATUS_HISTORY h
                JOIN EMERGENCY e ON h.emergency_id = e.emergency_id
                JOIN PATIENT p ON e.patient_id = p.patient_id
                WHERE h.emergency_id = ?
                ORDER BY h.history_id DESC
                """,
                (emergency_id,),
            )
        else:
            cursor.execute(
                """
                SELECT h.*, p.name AS patient_name, e.severity
                FROM EMERGENCY_STATUS_HISTORY h
                JOIN EMERGENCY e ON h.emergency_id = e.emergency_id
                JOIN PATIENT p ON e.patient_id = p.patient_id
                ORDER BY h.history_id DESC
                LIMIT 50
                """
            )
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()


def get_emergency_types(db_path: str = DB_FILE) -> List[Dict[str, Any]]:
    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM EMERGENCY_TYPE ORDER BY severity_default DESC")
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()


def get_available_resources(db_path: str = DB_FILE) -> Dict[str, Any]:
    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT ambulance_id, vehicle_no, type, base_station 
            FROM AMBULANCE WHERE operational_status = 'Available'
            """
        )
        ambulances = [dict(r) for r in cursor.fetchall()]

        cursor.execute(
            """
            SELECT h.hospital_id, h.hospital_name, l.zone_area
            FROM HOSPITAL h
            JOIN LOCATION l ON h.location_id = l.location_id
            """
        )
        hospitals = [dict(r) for r in cursor.fetchall()]

        cursor.execute(
            """
            SELECT b.bed_id, b.bed_number, b.bed_type, d.dept_name, h.hospital_name
            FROM BED b
            JOIN DEPARTMENT d ON b.dept_id = d.dept_id
            JOIN HOSPITAL h ON d.hospital_id = h.hospital_id
            WHERE b.is_occupied = 0
            """
        )
        beds = [dict(r) for r in cursor.fetchall()]

        return {"ambulances": ambulances, "hospitals": hospitals, "beds": beds}
    finally:
        conn.close()


def execute_arbitrary_query(sql_query: str, db_path: str = DB_FILE) -> Tuple[List[str], List[List[Any]], Optional[str]]:
    """
    Safely executes analytical SQL queries for DBMS lab evaluations.
    Restricted to SELECT/WITH queries to prevent accidental corruption.
    Strips comments before command validation.
    Returns (columns, rows, error_message).
    """
    import re
    # Strip multi-line comments /* ... */ and single line comments -- ...
    cleaned = re.sub(r"/\*.*?\*/", "", sql_query, flags=re.DOTALL)
    cleaned = re.sub(r"--.*$", "", cleaned, flags=re.MULTILINE).strip()

    sql_trimmed = cleaned.upper()
    if not (sql_trimmed.startswith("SELECT") or sql_trimmed.startswith("WITH") or sql_trimmed.startswith("EXPLAIN")):
        return [], [], "Security Restriction: Only read-only queries (SELECT, WITH, EXPLAIN) can be evaluated in this console."

    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute(cleaned)
        columns = [description[0] for description in cursor.description] if cursor.description else []
        rows = cursor.fetchall()
        row_lists = [list(row) for row in rows]
        return columns, row_lists, None
    except Exception as e:
        return [], [], str(e)
    finally:
        conn.close()
