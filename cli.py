"""
Urban Emergency Response & Resource Allocation System
Database Management Systems Lab (24B15CS213)
JIIT Noida-62 - Department of CSE & IT

Interactive CLI Console & Direct Terminal Interface
"""

import sys
import os
import database as db


def print_header(title: str):
    print("\n" + "=" * 75)
    print(f" {title.upper()}")
    print("=" * 75)


def print_table(headers, rows):
    if not rows:
        print("[No records found]")
        return

    # Calculate column widths
    widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            widths[i] = max(widths[i], len(str(val) if val is not None else "NULL"))

    # Format header
    header_str = " | ".join(str(headers[i]).ljust(widths[i]) for i in range(len(headers)))
    sep_str = "-+-".join("-" * widths[i] for i in range(len(headers)))
    print(header_str)
    print(sep_str)

    # Format rows
    for row in rows:
        row_str = " | ".join(
            (str(row[i]) if row[i] is not None else "NULL").ljust(widths[i])
            for i in range(len(headers))
        )
        print(row_str)
    print(f"\nTotal rows: {len(rows)}")


def menu_view_active_emergencies():
    print_header("Live Active Emergency Incidents (vw_active_emergencies)")
    emergencies = db.get_active_emergencies()
    if not emergencies:
        print("No active emergencies.")
        return

    headers = ["ID", "Severity", "Status", "Emergency Type", "Patient", "Phone", "Zone", "Ambulance", "Hospital", "Bed"]
    rows = [
        [
            e["emergency_id"],
            f"Lvl {e['severity']}",
            e["incident_status"],
            e["emergency_category"][:20],
            e["patient_name"],
            e["patient_phone"],
            e["zone_area"],
            e["assigned_ambulance"] or "Unassigned",
            (e["assigned_hospital"] or "Unassigned")[:18],
            e["reserved_bed"] or "None",
        ]
        for e in emergencies
    ]
    print_table(headers, rows)


def menu_register_emergency():
    print_header("Incident Intake & Patient Registration")
    print("Enter incident information:")
    name = input("Patient Full Name: ").strip() or "Anonymous Citizen"
    age = int(input("Age: ").strip() or "30")
    gender = input("Gender (Male/Female/Other) [Male]: ").strip() or "Male"
    phone = input("Contact Phone [+91-9811000000]: ").strip() or "+91-9811000000"
    blood = input("Blood Group (A+/B+/O+/AB+/etc) [O+]: ").strip() or "O+"
    notes = input("Triage Medical Notes: ").strip() or "Reported via emergency helpline."

    print("\nLocation Details (Noida Urban Area):")
    address = input("Address Line: ").strip() or "Sector 62 Main Road"
    zone = input("Zone / Sector [Sector 62]: ").strip() or "Sector 62"
    landmark = input("Landmark: ").strip() or "Near Metro Station"
    postal = input("Postal Code [201309]: ").strip() or "201309"

    print("\nClinical Classification:")
    types = db.get_emergency_types()
    for t in types:
        print(f" [{t['type_id']}] {t['type_name']} (Default Severity: {t['severity_default']}, Priority: {t['priority_rank']})")

    type_id = int(input("Select Emergency Type ID [1]: ").strip() or "1")
    severity = int(input("Severity Rating (1 to 5) [5]: ").strip() or "5")

    eid = db.register_emergency(
        patient_name=name,
        age=age,
        gender=gender,
        contact_phone=phone,
        blood_group=blood,
        triage_notes=notes,
        address_line=address,
        zone_area=zone,
        landmark=landmark,
        postal_code=postal,
        emergency_type_id=type_id,
        severity=severity,
    )
    print(f"\n>>> [SUCCESS] Emergency #{eid} registered successfully! (Trigger automatically logged to audit trail)")


def menu_dispatch_resources():
    print_header("ACID Transactional Resource Allocation")
    emergencies = [e for e in db.get_active_emergencies() if e["incident_status"] in ("Reported", "Pending")]
    if not emergencies:
        print("No pending/reported emergencies requiring dispatch.")
        return

    print("Pending Incidents awaiting allocation:")
    for e in emergencies:
        print(f" - Incident #{e['emergency_id']}: {e['emergency_category']} (Severity {e['severity']}) - Patient: {e['patient_name']} @ {e['zone_area']}")

    try:
        eid_input = input("\nEnter Emergency ID to dispatch atomically: ").strip()
        if not eid_input:
            return
        eid = int(eid_input)

        print(f"\n[BEGIN IMMEDIATE TRANSACTION] Pairing optimal ambulance and reserving hospital bed...")
        result = db.allocate_resources_transactional(emergency_id=eid)
        print(">>> [TRANSACTION COMMITTED]")
        print(f"Message: {result['message']}")
        print(f"Ambulance Assigned: {result['ambulance']['vehicle_no']} ({result['ambulance']['type']}) from {result['ambulance']['base_station']}")
        print(f"Hospital Reserved:  {result['hospital']['name']} - Bed {result['hospital']['bed_number']} ({result['hospital']['bed_type']})")
    except db.EmergencySystemError as err:
        print(f"\n>>> [TRANSACTION ROLLBACK]: {err}")
    except Exception as e:
        print(f"\n>>> [ERROR]: {e}")


def menu_view_hospitals():
    print_header("Hospital Department Bed Capacity (vw_hospital_bed_occupancy)")
    hospitals = db.get_hospital_bed_occupancy()
    headers = ["Hospital ID", "Hospital Name", "Trauma Level", "Zone", "Total Beds", "Occupied", "Vacant", "Vacant ICU", "Occupancy %"]
    rows = [
        [
            h["hospital_id"],
            h["hospital_name"][:25],
            h["emergency_level"],
            h["location_zone"],
            h["total_beds_configured"],
            h["occupied_beds"],
            h["vacant_beds"],
            h["vacant_icu_beds"],
            f"{h['occupancy_percentage']}%",
        ]
        for h in hospitals
    ]
    print_table(headers, rows)


def menu_view_fleet():
    print_header("Ambulance Fleet & Equipment Readiness (vw_ambulance_fleet_status)")
    fleet = db.get_ambulance_fleet()
    headers = ["ID", "Vehicle No", "Type", "Status", "Base Station", "Equip Count", "Functional", "Faulty"]
    rows = [
        [
            a["ambulance_id"],
            a["vehicle_no"],
            a["ambulance_type"],
            a["operational_status"],
            a["base_station"][:25],
            a["total_equipment_count"],
            a["functional_equipment_count"],
            a["faulty_equipment_count"],
        ]
        for a in fleet
    ]
    print_table(headers, rows)


def menu_view_audit():
    print_header("Trigger-Driven Chronological Audit Trail (EMERGENCY_STATUS_HISTORY)")
    history = db.get_status_history()
    headers = ["Log ID", "Emergency ID", "Patient", "Status State", "Timestamp", "Logged By", "Remarks"]
    rows = [
        [
            h["history_id"],
            h["emergency_id"],
            h["patient_name"],
            h["status_state"],
            h["changed_at"],
            h["updated_by"],
            h["remarks"][:35] if h["remarks"] else "",
        ]
        for h in history[:20]
    ]
    print_table(headers, rows)


def menu_run_sql():
    print_header("DBMS Lab Evaluation SQL Query Runner")
    print("Enter a read-only SELECT query (or press Enter to return):")
    query = input("SQL> ").strip()
    if not query:
        return

    cols, rows, err = db.execute_arbitrary_query(query)
    if err:
        print(f"[SQL ERROR]: {err}")
    else:
        print_table(cols, rows)


def main():
    if not os.path.exists(db.DB_FILE):
        print("Database not found. Initializing schema and scenario seeds...")
        db.init_db(force=True)

    while True:
        print("\n" + "=" * 75)
        print(" URBAN EMERGENCY RESPONSE & RESOURCE ALLOCATION SYSTEM")
        print(" Course: Database Management Systems Lab (24B15CS213) | JIIT Noida-62")
        print(" Team: Pragya Ahlawat, Ronak Jain, Rishabh Tyagi, Shobhit Khatana (Batch B2)")
        print("=" * 75)
        print(" [1] View Active Emergency Queue & Live Dispatches")
        print(" [2] Register New Emergency Incident (Intake & Triage)")
        print(" [3] Execute ACID Transactional Resource Dispatch")
        print(" [4] View Hospital & Bed Capacity (ICU / General)")
        print(" [5] View Ambulance Fleet & Equipment Readiness")
        print(" [6] View Trigger-Driven Immutable Audit Trail")
        print(" [7] Run DBMS Lab Analytical Queries")
        print(" [8] Reset Database to Pristine Seed State")
        print(" [0] Exit")
        choice = input("\nSelect an option [0-8]: ").strip()

        if choice == "1":
            menu_view_active_emergencies()
        elif choice == "2":
            menu_register_emergency()
        elif choice == "3":
            menu_dispatch_resources()
        elif choice == "4":
            menu_view_hospitals()
        elif choice == "5":
            menu_view_fleet()
        elif choice == "6":
            menu_view_audit()
        elif choice == "7":
            menu_run_sql()
        elif choice == "8":
            db.init_db(force=True)
            print(">>> [SUCCESS] Database successfully re-initialized and seeded!")
        elif choice == "0":
            print("\nExiting Urban Emergency Response System. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid option. Please enter 0-8.")


if __name__ == "__main__":
    main()
