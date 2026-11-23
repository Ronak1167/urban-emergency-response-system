"""
Urban Emergency Response & Resource Allocation System
Database Management Systems Lab (24B15CS213)
JIIT Noida-62 - Department of CSE & IT

Flask Web Application - Command Center & Lab Evaluation Interface
"""

import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import database as db
import concept_service

app = Flask(__name__)
app.secret_key = "urban-emergency-response-lab-secret-key"

# Ensure database exists on startup
if not os.path.exists(db.DB_FILE):
    db.init_db()


@app.route("/")
def dashboard():
    """Main command center dashboard showing KPIs, live emergency queue, and mutation diffs."""
    metrics = db.get_dashboard_metrics()
    emergencies = db.get_active_emergencies()
    resources = db.get_available_resources()
    last_mutation = session.pop("last_mutation", None)
    return render_template(
        "index.html",
        metrics=metrics,
        emergencies=emergencies,
        resources=resources,
        last_mutation=last_mutation,
        title="Emergency Operations Command Center",
    )


@app.route("/intake", methods=["GET", "POST"])
def emergency_intake():
    """Incident Intake: Register emergency calls and victim medical demographics."""
    if request.method == "POST":
        try:
            patient_name = request.form.get("patient_name", "").strip()
            age_raw = request.form.get("age", "").strip()
            gender = request.form.get("gender", "Other")
            contact_phone = request.form.get("contact_phone", "").strip()
            blood_group = request.form.get("blood_group", "O+")
            triage_notes = request.form.get("triage_notes", "").strip()

            address_line = request.form.get("address_line", "").strip()
            zone_area = request.form.get("zone_area", "").strip()
            landmark = request.form.get("landmark", "").strip()
            postal_code = request.form.get("postal_code", "201301").strip()

            emergency_type_id_raw = request.form.get("emergency_type_id", "1").strip()
            severity_raw = request.form.get("severity", "3").strip()

            # Validation
            if not patient_name:
                flash("Validation Error: Patient full name is required.", "danger")
                return redirect(url_for("emergency_intake"))

            try:
                age = int(age_raw)
                if not (1 <= age <= 125):
                    raise ValueError()
            except ValueError:
                flash("Validation Error: Age must be a positive integer between 1 and 125.", "danger")
                return redirect(url_for("emergency_intake"))

            if not contact_phone:
                flash("Validation Error: Contact phone number is required.", "danger")
                return redirect(url_for("emergency_intake"))

            if not address_line or not zone_area:
                flash("Validation Error: Address and Zone/Sector are required for emergency dispatch.", "danger")
                return redirect(url_for("emergency_intake"))

            emergency_type_id = int(emergency_type_id_raw) if emergency_type_id_raw.isdigit() else 1
            severity = int(severity_raw) if severity_raw.isdigit() else 3
            severity = max(1, min(5, severity))

            emergency_id = db.register_emergency(
                patient_name=patient_name,
                age=age,
                gender=gender,
                contact_phone=contact_phone,
                blood_group=blood_group,
                triage_notes=triage_notes,
                address_line=address_line,
                zone_area=zone_area,
                landmark=landmark,
                postal_code=postal_code,
                emergency_type_id=emergency_type_id,
                severity=severity,
            )

            flash(
                f"Emergency Incident #{emergency_id} successfully registered! Database trigger created initial audit entry.",
                "success",
            )
            return redirect(url_for("dashboard"))
        except Exception as e:
            flash(f"Failed to register emergency: {str(e)}", "danger")

    types = db.get_emergency_types()
    return render_template("intake.html", types=types, title="Emergency Intake & Triage")


@app.route("/dispatch/<int:emergency_id>", methods=["POST"])
def dispatch_emergency(emergency_id: int):
    """
    Executes ACID-compliant Transaction:
    Pairs eligible ambulance, reserves hospital bed, and updates emergency status atomically.
    """
    pref_ambulance = request.form.get("preferred_ambulance_id")
    pref_hospital = request.form.get("preferred_hospital_id")
    return_to = request.form.get("return_to")

    pref_ambulance_id = int(pref_ambulance) if pref_ambulance and pref_ambulance.isdigit() else None
    pref_hospital_id = int(pref_hospital) if pref_hospital and pref_hospital.isdigit() else None

    try:
        result = db.allocate_resources_transactional(
            emergency_id=emergency_id,
            preferred_ambulance_id=pref_ambulance_id,
            preferred_hospital_id=pref_hospital_id,
        )
        session["last_mutation"] = result
        flash(result["message"], "success")
    except db.EmergencySystemError as e:
        flash(f"ACID Transaction Rollback: {str(e)}", "danger")
    except Exception as e:
        flash(f"System Error: {str(e)}", "danger")

    if return_to:
        return redirect(return_to)
    return redirect(url_for("dashboard"))


@app.route("/transition/<int:emergency_id>", methods=["POST"])
def transition_status(emergency_id: int):
    """Transition emergency lifecycle status (In-Transit, Admitted, Resolved, Cancelled)."""
    new_status = request.form.get("new_status")
    remarks = request.form.get("remarks")
    return_to = request.form.get("return_to")
    try:
        db.transition_emergency_status(emergency_id, new_status, remarks)
        flash(f"Incident #{emergency_id} state updated to '{new_status}'. Trigger logged to audit table.", "info")
    except Exception as e:
        flash(f"Status transition failed: {str(e)}", "danger")

    if return_to:
        return redirect(return_to)
    return redirect(url_for("dashboard"))


@app.route("/hospitals")
def hospital_capacity():
    """Live hospital departmental bed occupancy monitor."""
    data = db.get_hospital_bed_occupancy()
    return render_template("hospitals.html", hospitals=data, title="Hospital Bed Capacity Monitor")


@app.route("/fleet")
def fleet_status():
    """Ambulance fleet status and onboard life-support equipment."""
    ambulances = db.get_ambulance_fleet()
    return render_template("fleet.html", ambulances=ambulances, title="Fleet & Equipment Tracking")


@app.route("/audit")
def audit_trail():
    """Immutable chronological audit trail from EMERGENCY_STATUS_HISTORY."""
    emergency_id = request.args.get("emergency_id")
    eid = int(emergency_id) if emergency_id and emergency_id.isdigit() else None
    history = db.get_status_history(eid)
    return render_template("audit.html", history=history, selected_eid=eid, title="Trigger Audit Trail")


@app.route("/query", methods=["GET", "POST"])
def query_console():
    """DBMS Lab Evaluation SQL Console: Predefined queries and live SQL runner."""
    sample_queries = [
        {
            "name": "5-Table Incident Dispatch Join",
            "sql": """SELECT 
    e.emergency_id,
    p.name AS patient,
    p.blood_group,
    t.type_name AS emergency,
    e.severity,
    l.zone_area,
    COALESCE(a.vehicle_no, 'UNASSIGNED') AS ambulance,
    COALESCE(h.hospital_name, 'UNRESERVED') AS hospital,
    COALESCE(b.bed_number, 'NONE') AS bed,
    e.status
FROM EMERGENCY e
JOIN PATIENT p ON e.patient_id = p.patient_id
JOIN EMERGENCY_TYPE t ON e.type_id = t.type_id
JOIN LOCATION l ON e.location_id = l.location_id
LEFT JOIN RESOURCE_ALLOCATION ra ON e.emergency_id = ra.emergency_id
LEFT JOIN AMBULANCE a ON ra.ambulance_id = a.ambulance_id
LEFT JOIN HOSPITAL h ON ra.hospital_id = h.hospital_id
LEFT JOIN BED b ON ra.bed_id = b.bed_id
ORDER BY e.severity DESC;""",
        },
        {
            "name": "Available ALS Ambulances with Defibrillator & Ventilator (Nested Subqueries)",
            "sql": """SELECT a.ambulance_id, a.vehicle_no, a.type, a.base_station
FROM AMBULANCE a
WHERE a.operational_status = 'Available'
  AND a.type = 'ALS'
  AND a.ambulance_id IN (
      SELECT ambulance_id FROM EQUIPMENT 
      WHERE equipment_name LIKE '%Ventilator%' AND is_functional = 1
  )
  AND a.ambulance_id IN (
      SELECT ambulance_id FROM EQUIPMENT 
      WHERE equipment_name LIKE '%Defibrillator%' AND is_functional = 1
  );""",
        },
        {
            "name": "Hospitals with Higher-than-Average Vacant ICU Beds (Correlated Subquery)",
            "sql": """SELECT 
    h.hospital_id,
    h.hospital_name,
    h.emergency_level,
    (
        SELECT COUNT(*)
        FROM BED b
        JOIN DEPARTMENT d ON b.dept_id = d.dept_id
        WHERE d.hospital_id = h.hospital_id 
          AND b.bed_type = 'ICU' 
          AND b.is_occupied = 0
    ) AS available_icu_beds
FROM HOSPITAL h
WHERE (
    SELECT COUNT(*)
    FROM BED b
    JOIN DEPARTMENT d ON b.dept_id = d.dept_id
    WHERE d.hospital_id = h.hospital_id 
      AND b.bed_type = 'ICU' 
      AND b.is_occupied = 0
) > (
    SELECT AVG(vacant_count)
    FROM (
        SELECT COUNT(b2.bed_id) AS vacant_count
        FROM HOSPITAL h2
        JOIN DEPARTMENT d2 ON h2.hospital_id = d2.hospital_id
        JOIN BED b2 ON d2.dept_id = b2.dept_id
        WHERE b2.bed_type = 'ICU' AND b2.is_occupied = 0
        GROUP BY h2.hospital_id
    )
);""",
        },
        {
            "name": "Departmental Bed Utilization (GROUP BY & HAVING)",
            "sql": """SELECT 
    h.hospital_name,
    d.dept_name,
    COUNT(b.bed_id) AS total_beds,
    SUM(CASE WHEN b.is_occupied = 1 THEN 1 ELSE 0 END) AS occupied,
    SUM(CASE WHEN b.is_occupied = 0 THEN 1 ELSE 0 END) AS vacant,
    ROUND(AVG(b.is_occupied) * 100, 2) AS occupancy_pct
FROM HOSPITAL h
JOIN DEPARTMENT d ON h.hospital_id = d.hospital_id
JOIN BED b ON d.dept_id = b.dept_id
GROUP BY h.hospital_name, d.dept_name
HAVING COUNT(b.bed_id) > 1
ORDER BY occupancy_pct DESC;""",
        },
        {
            "name": "Trigger-Generated Audit History (Status Log)",
            "sql": """SELECT 
    h.history_id,
    h.emergency_id,
    p.name AS patient_name,
    h.status_state,
    h.changed_at,
    h.updated_by,
    h.remarks
FROM EMERGENCY_STATUS_HISTORY h
JOIN EMERGENCY e ON h.emergency_id = e.emergency_id
JOIN PATIENT p ON e.patient_id = p.patient_id
ORDER BY h.history_id DESC;""",
        },
    ]

    selected_query = sample_queries[0]["sql"]
    columns = []
    rows = []
    error = None

    if request.method == "POST":
        selected_query = request.form.get("sql_query", "").strip()
        if selected_query:
            columns, rows, error = db.execute_arbitrary_query(selected_query)

    return render_template(
        "query.html",
        sample_queries=sample_queries,
        selected_query=selected_query,
        columns=columns,
        rows=rows,
        error=error,
        title="DBMS Lab SQL Query Console",
    )


@app.route("/reset-db", methods=["POST"])
def reset_database():
    """Resets database schema and reseeds initial scenario data."""
    try:
        db.init_db(force=True)
        flash("Database successfully reset and re-seeded with pristine scenario data!", "success")
    except Exception as e:
        flash(f"Database reset error: {str(e)}", "danger")
    return redirect(url_for("dashboard"))


# -----------------------------------------------------------------------------
# DBMS Concepts Visualizer Routes (Academic Evaluation Suite)
# -----------------------------------------------------------------------------
@app.route("/concepts")
def concepts_hub():
    """Master visualizer hub for academic DBMS evaluations."""
    return render_template("concepts/hub.html", title="DBMS Concepts Interactive Visualizer")


@app.route("/concepts/er-diagram")
def concepts_er_diagram():
    """Concept 1: Interactive ER & EER Relational Schema Explorer."""
    tables = concept_service.get_all_tables_metadata()
    return render_template("concepts/er_diagram.html", tables=tables, title="Interactive ER/EER Schema Visualizer")


@app.route("/concepts/normalization")
def concepts_normalization():
    """Concept 2: 3NF Normalization Step-by-Step Proofs & FD Graphs."""
    return render_template("concepts/normalization.html", title="3NF Relational Normalization Stepper")


@app.route("/concepts/acid-transactions")
def concepts_acid_transactions():
    """Concept 3: Step-by-Step ACID Transaction Execution & Concurrency Locks."""
    return render_template("concepts/acid_transactions.html", title="ACID Transaction Stepper")


@app.route("/concepts/triggers")
def concepts_triggers():
    """Concept 4: Database Trigger Execution & State Transition Visualizer."""
    emergencies = db.get_active_emergencies()
    history = db.get_status_history()
    return render_template("concepts/triggers.html", emergencies=emergencies, history=history, title="Database Trigger Visualizer")


@app.route("/concepts/triggers/fire", methods=["POST"])
def fire_trigger_demo():
    """Live trigger test pad: advance status and watch the trigger fire."""
    try:
        emergency_id = int(request.form.get("emergency_id"))
        new_status = request.form.get("new_status")
        remarks = request.form.get("remarks")
        db.transition_emergency_status(emergency_id, new_status, remarks)
        flash(f"Trigger trg_emergency_status_update fired! Status updated to '{new_status}' and logged to audit table.", "success")
    except Exception as e:
        flash(f"Trigger execution error: {str(e)}", "danger")
    return redirect(url_for("concepts_triggers"))


@app.route("/concepts/constraints")
def concepts_constraints():
    """Concept 5: Integrity Constraint Violation Sandbox."""
    return render_template("concepts/constraints.html", title="Integrity Constraint Testing Sandbox")


@app.route("/api/concepts/constraints/test")
def api_test_constraint():
    """Executes intentional constraint violation to prove DBMS enforcement."""
    test_type = request.args.get("type", "fk_violation")
    result = concept_service.run_constraint_violation_test(test_type)
    return jsonify(result)


@app.route("/concepts/mutation-inspector")
def concepts_mutation_inspector():
    """Live Database Mutation & State Diff Inspector (Before-and-After Raw Row State)."""
    all_emergencies = db.get_active_emergencies()
    selected_eid = request.args.get("emergency_id")
    if not selected_eid and all_emergencies:
        reported = [e for e in all_emergencies if e["incident_status"] in ("Reported", "Pending")]
        selected_eid = reported[0]["emergency_id"] if reported else all_emergencies[0]["emergency_id"]
    else:
        selected_eid = int(selected_eid) if selected_eid and selected_eid.isdigit() else 1

    state = concept_service.get_emergency_live_state(selected_eid)
    return render_template(
        "concepts/mutation_inspector.html",
        all_emergencies=all_emergencies,
        selected_eid=selected_eid,
        state=state,
        title="Live Data Mutation & State Diff Inspector",
    )


@app.route("/concepts/relational-algebra")
def concepts_relational_algebra():
    """Concept 6: Relational Algebra & Query Optimizer Execution Plans."""
    return render_template("concepts/relational_algebra.html", title="Relational Algebra & Optimizer Plans")


if __name__ == "__main__":
    print("=" * 70)
    print("URBAN EMERGENCY RESPONSE & RESOURCE ALLOCATION SYSTEM")
    print("Department of CSE & IT - Jaypee Institute of Information Technology")
    print("DBMS Lab (24B15CS213) - Starting Web Server on http://127.0.0.1:5000")
    print("=" * 70)
    app.run(host="127.0.0.1", port=5000, debug=False)
