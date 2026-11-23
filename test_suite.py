"""
Urban Emergency Response & Resource Allocation System
Database Management Systems Lab (24B15CS213)
JIIT Noida-62 - Department of CSE & IT

Comprehensive Automated Test Suite:
- Schema & Normalization Checks
- Foreign Key Referential Integrity
- Database Triggers Verification (trg_emergency_status_*)
- ACID Transaction Resource Allocation & Rollback Tests
- SQL Views & Complex Joins Validation
- Flask Web Route Verification
"""

import os
import unittest
import sqlite3
import database as db
from app import app

TEST_DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_urban_emergency.db")


class TestUrbanEmergencySystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up clean test database once for the test suite."""
        db.init_db(force=True, db_path=TEST_DB)

    @classmethod
    def tearDownClass(cls):
        """Remove test database after all tests complete."""
        if os.path.exists(TEST_DB):
            try:
                os.remove(TEST_DB)
            except Exception:
                pass

    def setUp(self):
        self.conn = db.get_connection(TEST_DB)

    def tearDown(self):
        self.conn.close()

    # -------------------------------------------------------------------------
    # 1. Schema & Relational Table Integrity
    # -------------------------------------------------------------------------
    def test_01_all_tables_created(self):
        """Verify all 12 normalized relational tables exist."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row["name"] for row in cursor.fetchall()]

        expected_tables = [
            "LOCATION",
            "PATIENT",
            "EMERGENCY_TYPE",
            "EMERGENCY",
            "AMBULANCE",
            "EQUIPMENT",
            "HOSPITAL",
            "DEPARTMENT",
            "BED",
            "STAFF",
            "RESOURCE_ALLOCATION",
            "EMERGENCY_STATUS_HISTORY",
        ]
        for tbl in expected_tables:
            self.assertIn(tbl, tables, f"Table '{tbl}' is missing from schema!")

    def test_02_all_views_created(self):
        """Verify all 4 analytical SQL views exist."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='view';")
        views = [row["name"] for row in cursor.fetchall()]

        expected_views = [
            "vw_hospital_bed_occupancy",
            "vw_ambulance_fleet_status",
            "vw_active_emergencies",
            "vw_response_latency_analytics",
        ]
        for v in expected_views:
            self.assertIn(v, views, f"View '{v}' is missing from schema!")

    def test_03_foreign_key_enforcement(self):
        """Verify Foreign Key constraints reject orphaned child records."""
        cursor = self.conn.cursor()
        # Attempt to insert an emergency with a non-existent patient_id = 99999
        with self.assertRaises(sqlite3.IntegrityError):
            cursor.execute(
                """
                INSERT INTO EMERGENCY (patient_id, type_id, location_id, severity, status)
                VALUES (99999, 1, 1, 5, 'Reported')
                """
            )
            self.conn.commit()

    # -------------------------------------------------------------------------
    # 2. Database Trigger Verification
    # -------------------------------------------------------------------------
    def test_04_trigger_insert_audit(self):
        """Verify AFTER INSERT trigger on EMERGENCY populates EMERGENCY_STATUS_HISTORY."""
        eid = db.register_emergency(
            patient_name="Unit Test Patient A",
            age=32,
            gender="Male",
            contact_phone="+91-9999900001",
            blood_group="A+",
            triage_notes="Suspected severe concussion.",
            address_line="Sector 62 Gate 1",
            zone_area="Sector 62",
            landmark="Near Library",
            postal_code="201309",
            emergency_type_id=2,  # Severe Road Trauma
            severity=5,
            db_path=TEST_DB,
        )

        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT * FROM EMERGENCY_STATUS_HISTORY
            WHERE emergency_id = ? AND status_state = 'Reported'
            """,
            (eid,),
        )
        history_entry = cursor.fetchone()
        self.assertIsNotNone(history_entry, "Trigger failed: No audit entry created for initial emergency insert!")
        self.assertIn("Severity Level 5", history_entry["remarks"])
        self.assertEqual(history_entry["updated_by"], "SYSTEM_TRIGGER")

    def test_05_trigger_update_audit(self):
        """Verify AFTER UPDATE OF status trigger logs state transitions."""
        eid = db.register_emergency(
            patient_name="Unit Test Patient B",
            age=25,
            gender="Female",
            contact_phone="+91-9999900002",
            blood_group="B+",
            triage_notes="Severe allergic reaction.",
            address_line="Sector 18 Atta Market",
            zone_area="Sector 18",
            landmark="Near Haldirams",
            postal_code="201301",
            emergency_type_id=6,
            severity=3,
            db_path=TEST_DB,
        )

        # Transition status
        db.transition_emergency_status(eid, "In-Transit", db_path=TEST_DB)

        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT * FROM EMERGENCY_STATUS_HISTORY
            WHERE emergency_id = ? AND status_state = 'In-Transit'
            """,
            (eid,),
        )
        history_entry = cursor.fetchone()
        self.assertIsNotNone(history_entry, "Trigger failed: No audit entry for status update to 'In-Transit'!")
        self.assertIn("Reported' to 'In-Transit'", history_entry["remarks"])

    # -------------------------------------------------------------------------
    # 3. ACID Transactional Resource Allocation Engine
    # -------------------------------------------------------------------------
    def test_06_acid_allocation_success(self):
        """Verify atomic allocation pairs ambulance, bed, and creates allocation record."""
        eid = db.register_emergency(
            patient_name="Unit Test Critical Patient",
            age=52,
            gender="Male",
            contact_phone="+91-9999900003",
            blood_group="O-",
            triage_notes="Severe cardiac arrest.",
            address_line="Sector 62 Expressway Entry",
            zone_area="Sector 62",
            landmark="Near Toll",
            postal_code="201309",
            emergency_type_id=1,  # Cardiac Arrest
            severity=5,
            db_path=TEST_DB,
        )

        result = db.allocate_resources_transactional(emergency_id=eid, db_path=TEST_DB)
        self.assertTrue(result["success"])
        self.assertIsNotNone(result["allocation_id"])

        cursor = self.conn.cursor()

        # Check emergency status
        cursor.execute("SELECT status FROM EMERGENCY WHERE emergency_id = ?", (eid,))
        em_row = cursor.fetchone()
        self.assertEqual(em_row["status"], "Dispatched")

        # Check ambulance operational status
        cursor.execute("SELECT operational_status FROM AMBULANCE WHERE ambulance_id = ?", (result["ambulance"]["id"],))
        amb_row = cursor.fetchone()
        self.assertEqual(amb_row["operational_status"], "Dispatched")

        # Check bed occupancy
        cursor.execute("SELECT is_occupied FROM BED WHERE bed_id = ?", (result["hospital"]["bed_id"],))
        bed_row = cursor.fetchone()
        self.assertEqual(bed_row["is_occupied"], 1)

        # Check audit trail trigger execution
        cursor.execute(
            """
            SELECT * FROM EMERGENCY_STATUS_HISTORY
            WHERE emergency_id = ? AND status_state = 'Dispatched'
            """,
            (eid,),
        )
        audit_row = cursor.fetchone()
        self.assertIsNotNone(audit_row, "Audit trigger did not log 'Dispatched' transition during ACID commit!")

    def test_07_acid_allocation_rollback_already_allocated(self):
        """Verify allocation rolls back with error if emergency is already dispatched."""
        # Emergency 2 is seeded as already 'Dispatched'
        with self.assertRaises(db.EmergencySystemError):
            db.allocate_resources_transactional(emergency_id=2, db_path=TEST_DB)

    # -------------------------------------------------------------------------
    # 4. SQL Views & Analytics Queries
    # -------------------------------------------------------------------------
    def test_08_views_and_aggregates(self):
        """Verify views execute and return well-formed analytical data."""
        hospitals = db.get_hospital_bed_occupancy(db_path=TEST_DB)
        self.assertGreater(len(hospitals), 0)
        self.assertIn("occupancy_percentage", hospitals[0])

        fleet = db.get_ambulance_fleet(db_path=TEST_DB)
        self.assertGreater(len(fleet), 0)
        self.assertIn("functional_equipment_count", fleet[0])

        emergencies = db.get_active_emergencies(db_path=TEST_DB)
        self.assertGreater(len(emergencies), 0)

    # -------------------------------------------------------------------------
    # 5. Flask Web Application Route Tests
    # -------------------------------------------------------------------------
    def test_09_flask_routes(self):
        """Test Flask HTTP endpoints for 200 OK responses."""
        app.config["TESTING"] = True
        client = app.test_client()

        # Dashboard
        res = client.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Urban Emergency Response", res.data)

        # Intake page
        res = client.get("/intake")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Patient Information", res.data)

        # Hospitals page
        res = client.get("/hospitals")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Hospital Departmental Bed Capacity", res.data)

        # Fleet page
        res = client.get("/fleet")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Ambulance Fleet", res.data)

        # Audit page
        res = client.get("/audit")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Audit Trail", res.data)

        # Query Console
        res = client.get("/query")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"SQL Query Editor", res.data)

    # -------------------------------------------------------------------------
    # 6. Edge Cases & Constraint Boundary Tests
    # -------------------------------------------------------------------------
    def test_10_check_constraint_age(self):
        """Verify CHECK constraint rejects invalid patient age (e.g. 0 or 200)."""
        cursor = self.conn.cursor()
        with self.assertRaises(sqlite3.IntegrityError):
            cursor.execute(
                """
                INSERT INTO PATIENT (name, age, gender, contact_phone, blood_group)
                VALUES ('Invalid Age', 0, 'Male', '+91-9000000000', 'O+')
                """
            )
            self.conn.commit()

    def test_11_check_constraint_blood_group(self):
        """Verify CHECK constraint rejects invalid blood group."""
        cursor = self.conn.cursor()
        with self.assertRaises(sqlite3.IntegrityError):
            cursor.execute(
                """
                INSERT INTO PATIENT (name, age, gender, contact_phone, blood_group)
                VALUES ('Invalid Blood', 30, 'Male', '+91-9000000000', 'X_POSITIVE')
                """
            )
            self.conn.commit()

    def test_12_check_constraint_severity(self):
        """Verify CHECK constraint rejects severity out of bounds (1-5)."""
        cursor = self.conn.cursor()
        with self.assertRaises(sqlite3.IntegrityError):
            cursor.execute(
                """
                INSERT INTO EMERGENCY (patient_id, type_id, location_id, severity, status)
                VALUES (1, 1, 1, 9, 'Reported')
                """
            )
            self.conn.commit()

    def test_13_all_lab_queries_execution(self):
        """Verify all 12 queries in queries.sql execute successfully against live DB."""
        queries_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "queries.sql")
        with open(queries_file, "r", encoding="utf-8") as f:
            content = f.read()

        statements = [s.strip() for s in content.split(";") if s.strip()]
        cursor = self.conn.cursor()
        for i, stmt in enumerate(statements, 1):
            clean_lines = [l for l in stmt.splitlines() if not l.strip().startswith("--")]
            q = "\n".join(clean_lines).strip()
            if not q:
                continue
            try:
                cursor.execute(q)
                rows = cursor.fetchall()
                self.assertIsNotNone(rows, f"Query {i} returned None unexpectedly")
            except Exception as e:
                self.fail(f"Query {i} in queries.sql failed: {e}\nQuery text:\n{q}")

    def test_14_query_runner_with_comments(self):
        """Verify arbitrary query runner properly strips leading comments and executes."""
        sql = """-- Sample DBMS evaluation comment
        /* Multi-line comment here */
        SELECT hospital_name, emergency_level FROM HOSPITAL WHERE total_beds > 200;"""
        cols, rows, err = db.execute_arbitrary_query(sql, db_path=TEST_DB)
        self.assertIsNone(err, f"Arbitrary query failed with error: {err}")
        self.assertEqual(len(cols), 2)
        self.assertGreater(len(rows), 0)

    def test_15_intake_form_validation(self):
        """Verify Web intake endpoint rejects invalid / missing inputs."""
        app.config["TESTING"] = True
        client = app.test_client()

        # Missing patient name
        res = client.post("/intake", data={
            "patient_name": "",
            "age": "25",
            "gender": "Male",
            "contact_phone": "+91-9876543210",
            "address_line": "Sector 62",
            "zone_area": "Sector 62",
        }, follow_redirects=True)
        self.assertIn(b"Patient full name is required", res.data)

        # Invalid age
        res = client.post("/intake", data={
            "patient_name": "Valid Name",
            "age": "999",
            "gender": "Male",
            "contact_phone": "+91-9876543210",
            "address_line": "Sector 62",
            "zone_area": "Sector 62",
        }, follow_redirects=True)
        self.assertIn(b"Age must be a positive integer between 1 and 125", res.data)

    def test_16_status_transition_with_remarks(self):
        """Verify transition_emergency_status preserves doctor / operator remarks."""
        eid = db.register_emergency(
            patient_name="Unit Test Remarks Patient",
            age=40,
            gender="Female",
            contact_phone="+91-9999900004",
            blood_group="AB+",
            triage_notes="Suspected stroke.",
            address_line="Sector 50",
            zone_area="Sector 50",
            landmark="Central Park",
            postal_code="201301",
            emergency_type_id=4,
            severity=4,
            db_path=TEST_DB,
        )

        db.transition_emergency_status(
            emergency_id=eid,
            new_status="In-Transit",
            remarks="Patient hemodynamically stable; IV line established.",
            db_path=TEST_DB,
        )

        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT remarks FROM EMERGENCY_STATUS_HISTORY
            WHERE emergency_id = ? AND status_state = 'In-Transit'
            """,
            (eid,),
        )
        row = cursor.fetchone()
        self.assertIsNotNone(row)
        self.assertIn("IV line established", row["remarks"])

    # -------------------------------------------------------------------------
    # 7. DBMS Concepts Visualizer Tests (Faculty Evaluation Suite)
    # -------------------------------------------------------------------------
    def test_17_dbms_concepts_visualizer_routes(self):
        """Verify all DBMS Concept Visualizer routes render 200 OK with expected concepts."""
        app.config["TESTING"] = True
        client = app.test_client()

        # Hub
        res = client.get("/concepts")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"DBMS Concepts Interactive Visualizer", res.data)

        # 1. ER Diagram
        res = client.get("/concepts/er-diagram")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Interactive ER &amp; EER Relational Schema Explorer", res.data)
        self.assertIn(b"RESOURCE_ALLOCATION", res.data)

        # 2. Normalization Stepper
        res = client.get("/concepts/normalization")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Relational Normalization Visualizer", res.data)
        self.assertIn(b"Stage 3: Third Normal Form (3NF)", res.data)

        # 3. ACID Stepper
        res = client.get("/concepts/acid-transactions")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"ACID Transaction Execution &amp; Concurrency Stepper", res.data)
        self.assertIn(b"BEGIN IMMEDIATE", res.data)

        # 4. Triggers Visualizer
        res = client.get("/concepts/triggers")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Database Trigger Architecture", res.data)
        self.assertIn(b"trg_emergency_status_update", res.data)

        # 5. Constraints Sandbox
        res = client.get("/concepts/constraints")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Integrity Constraints Violation Testing Sandbox", res.data)

        # API Constraint Test: FK Violation
        res = client.get("/api/concepts/constraints/test?type=fk_violation")
        self.assertEqual(res.status_code, 200)
        json_data = res.get_json()
        self.assertTrue(json_data["blocked_by_dbms"])
        self.assertEqual(json_data["dbms_error_type"], "sqlite3.IntegrityError")

        # 6. Relational Algebra
        res = client.get("/concepts/relational-algebra")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Relational Algebra &amp; Query Optimizer Execution Plans", res.data)

        # 7. Live Mutation & State Diff Inspector
        res = client.get("/concepts/mutation-inspector")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Live Database Mutation &amp; State Diff Inspector", res.data)
        self.assertIn(b"TABLE: EMERGENCY", res.data)
        self.assertIn(b"TABLE: AMBULANCE", res.data)


if __name__ == "__main__":
    unittest.main()
