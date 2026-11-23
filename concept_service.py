"""
Urban Emergency Response & Resource Allocation System
Database Management Systems Lab (24B15CS213)
JIIT Noida-62 - Department of CSE & IT

DBMS Concept Visualizer Service:
- Normalization Proofs & Schemas
- ACID Transaction Step-by-Step Simulation Engine
- Trigger Old/New Record Tracing
- Live Integrity Constraint Violation Sandbox
- Relational Algebra and EXPLAIN QUERY PLAN Generators
"""

import sqlite3
from typing import Dict, Any, List, Tuple
import database as db


def get_all_tables_metadata(db_path: str = db.DB_FILE) -> List[Dict[str, Any]]:
    """Fetches metadata for all 12 normalized tables: columns, types, PKs, FKs, and live row counts."""
    conn = db.get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        table_names = [row["name"] for row in cursor.fetchall()]

        tables_meta = []
        for tbl in sorted(table_names):
            cursor.execute(f"PRAGMA table_info({tbl});")
            cols = [
                {
                    "cid": col["cid"],
                    "name": col["name"],
                    "type": col["type"],
                    "notnull": bool(col["notnull"]),
                    "dflt_value": col["dflt_value"],
                    "pk": bool(col["pk"]),
                }
                for col in cursor.fetchall()
            ]

            cursor.execute(f"PRAGMA foreign_key_list({tbl});")
            fks = [
                {
                    "id": fk["id"],
                    "from_col": fk["from"],
                    "to_table": fk["table"],
                    "to_col": fk["to"],
                    "on_update": fk["on_update"],
                    "on_delete": fk["on_delete"],
                }
                for fk in cursor.fetchall()
            ]

            cursor.execute(f"SELECT COUNT(*) AS cnt FROM {tbl};")
            row_count = cursor.fetchone()["cnt"]

            tables_meta.append({
                "name": tbl,
                "columns": cols,
                "foreign_keys": fks,
                "row_count": row_count,
            })

        return tables_meta
    finally:
        conn.close()


def run_constraint_violation_test(test_type: str, db_path: str = db.DB_FILE) -> Dict[str, Any]:
    """
    Executes an intentional constraint violation to prove DBMS enforcement:
    - fk_violation: Invalid Foreign Key
    - check_age: Violate age CHECK (age > 0 AND age <= 125)
    - check_severity: Violate severity CHECK (1 to 5)
    - unique_violation: Duplicate UNIQUE vehicle_no
    """
    conn = db.get_connection(db_path)
    cursor = conn.cursor()

    test_queries = {
        "fk_violation": {
            "name": "Foreign Key Referential Integrity Violation",
            "desc": "Attempting to insert an EMERGENCY with non-existent patient_id = 99999",
            "sql": "INSERT INTO EMERGENCY (patient_id, type_id, location_id, severity, status) VALUES (99999, 1, 1, 5, 'Reported');",
            "expected_rule": "FOREIGN KEY (patient_id) REFERENCES PATIENT(patient_id) ON DELETE RESTRICT",
        },
        "check_age": {
            "name": "Domain Integrity CHECK Constraint (Age Boundary)",
            "desc": "Attempting to insert a PATIENT with negative age = -8",
            "sql": "INSERT INTO PATIENT (name, age, gender, contact_phone, blood_group) VALUES ('Test Invalid Age', -8, 'Male', '+91-9999999999', 'O+');",
            "expected_rule": "CHECK (age > 0 AND age <= 125)",
        },
        "check_severity": {
            "name": "Domain Integrity CHECK Constraint (Clinical Severity)",
            "desc": "Attempting to insert an EMERGENCY with severity = 9 (allowed 1 to 5)",
            "sql": "INSERT INTO EMERGENCY (patient_id, type_id, location_id, severity, status) VALUES (1, 1, 1, 9, 'Reported');",
            "expected_rule": "CHECK (severity BETWEEN 1 AND 5)",
        },
        "unique_violation": {
            "name": "Key Integrity UNIQUE Constraint (Vehicle Registration)",
            "desc": "Attempting to insert duplicate ambulance with vehicle_no = 'UP-16-AM-1001'",
            "sql": "INSERT INTO AMBULANCE (vehicle_no, type, operational_status, base_station) VALUES ('UP-16-AM-1001', 'ALS', 'Available', 'Duplicate Depot');",
            "expected_rule": "vehicle_no TEXT NOT NULL UNIQUE",
        },
    }

    test_info = test_queries.get(test_type)
    if not test_info:
        return {"success": False, "error": f"Unknown constraint test type '{test_type}'."}

    try:
        cursor.execute(test_info["sql"])
        conn.commit()
        # If it didn't fail, constraint enforcement failed!
        return {
            "test_type": test_type,
            "name": test_info["name"],
            "desc": test_info["desc"],
            "sql": test_info["sql"],
            "expected_rule": test_info["expected_rule"],
            "blocked_by_dbms": False,
            "message": "WARNING: The database allowed this statement without error! Constraint not enforced.",
        }
    except sqlite3.IntegrityError as err:
        conn.rollback()
        return {
            "test_type": test_type,
            "name": test_info["name"],
            "desc": test_info["desc"],
            "sql": test_info["sql"],
            "expected_rule": test_info["expected_rule"],
            "blocked_by_dbms": True,
            "dbms_error_type": "sqlite3.IntegrityError",
            "dbms_error_message": str(err),
            "message": f"SUCCESSFULLY BLOCKED BY DBMS ENGINE! Integrity constraint rule was actively enforced.",
        }
    except Exception as e:
        conn.rollback()
        return {
            "test_type": test_type,
            "name": test_info["name"],
            "desc": test_info["desc"],
            "sql": test_info["sql"],
            "expected_rule": test_info["expected_rule"],
            "blocked_by_dbms": True,
            "dbms_error_type": type(e).__name__,
            "dbms_error_message": str(e),
            "message": f"Blocked with database exception: {e}",
        }
    finally:
        conn.close()


def get_query_execution_plan(sql_query: str, db_path: str = db.DB_FILE) -> Tuple[List[str], List[List[Any]], Optional[str]]:
    """Runs EXPLAIN QUERY PLAN on an arbitrary query to show query optimizer operations."""
    conn = db.get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute(f"EXPLAIN QUERY PLAN {sql_query}")
        cols = [d[0] for d in cursor.description]
        rows = [list(r) for r in cursor.fetchall()]
        return cols, rows, None
    except Exception as e:
        return [], [], str(e)
    finally:
        conn.close()


def get_emergency_live_state(emergency_id: int, db_path: str = db.DB_FILE) -> Dict[str, Any]:
    """
    Fetches the exact raw row states across all 5 affected tables for an emergency.
    Used for before-and-after visual data diff inspection.
    """
    conn = db.get_connection(db_path)
    try:
        cursor = conn.cursor()

        # 1. EMERGENCY row
        cursor.execute("SELECT * FROM EMERGENCY WHERE emergency_id = ?", (emergency_id,))
        em_row = cursor.fetchone()
        em = dict(em_row) if em_row else None

        # 2. PATIENT row
        patient = None
        if em:
            cursor.execute("SELECT * FROM PATIENT WHERE patient_id = ?", (em["patient_id"],))
            p_row = cursor.fetchone()
            patient = dict(p_row) if p_row else None

        # 3. RESOURCE_ALLOCATION row
        cursor.execute(
            """
            SELECT ra.*, a.vehicle_no, a.type AS amb_type, a.operational_status AS amb_status,
                   h.hospital_name, b.bed_number, b.bed_type, b.is_occupied AS bed_occupied
            FROM RESOURCE_ALLOCATION ra
            JOIN AMBULANCE a ON ra.ambulance_id = a.ambulance_id
            JOIN HOSPITAL h ON ra.hospital_id = h.hospital_id
            JOIN BED b ON ra.bed_id = b.bed_id
            WHERE ra.emergency_id = ?
            ORDER BY ra.allocation_id DESC LIMIT 1
            """,
            (emergency_id,),
        )
        alloc_row = cursor.fetchone()
        allocation = dict(alloc_row) if alloc_row else None

        # 4. If not allocated, get first available candidate ambulance and bed
        candidate_ambulance = None
        candidate_bed = None
        if not allocation and em:
            if em["severity"] >= 4:
                cursor.execute("SELECT * FROM AMBULANCE WHERE operational_status = 'Available' AND type = 'ALS' LIMIT 1")
            else:
                cursor.execute("SELECT * FROM AMBULANCE WHERE operational_status = 'Available' LIMIT 1")
            ca_row = cursor.fetchone()
            candidate_ambulance = dict(ca_row) if ca_row else None

            bed_type = "ICU" if em["severity"] >= 4 else "General"
            cursor.execute(
                """
                SELECT b.*, h.hospital_name, d.dept_name
                FROM BED b
                JOIN DEPARTMENT d ON b.dept_id = d.dept_id
                JOIN HOSPITAL h ON d.hospital_id = h.hospital_id
                WHERE b.bed_type = ? AND b.is_occupied = 0
                LIMIT 1
                """,
                (bed_type,),
            )
            cb_row = cursor.fetchone()
            candidate_bed = dict(cb_row) if cb_row else None

        # 5. History rows for this emergency
        cursor.execute(
            """
            SELECT * FROM EMERGENCY_STATUS_HISTORY 
            WHERE emergency_id = ? 
            ORDER BY history_id DESC
            """,
            (emergency_id,),
        )
        history = [dict(r) for r in cursor.fetchall()]

        return {
            "emergency": em,
            "patient": patient,
            "allocation": allocation,
            "candidate_ambulance": candidate_ambulance,
            "candidate_bed": candidate_bed,
            "history": history,
        }
    finally:
        conn.close()

