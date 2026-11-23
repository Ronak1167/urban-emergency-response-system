-- ============================================================================
-- URBAN EMERGENCY RESPONSE & RESOURCE ALLOCATION SYSTEM
-- Course: Database Management Systems Lab (24B15CS213)
-- Department of Computer Science & Engineering, JIIT Noida-62
-- Schema: 3NF Relational Database Schema (SQLite Compatible)
-- ============================================================================

PRAGMA foreign_keys = ON;

-- Clean drop for re-initialization
DROP VIEW IF EXISTS vw_response_latency_analytics;
DROP VIEW IF EXISTS vw_active_emergencies;
DROP VIEW IF EXISTS vw_ambulance_fleet_status;
DROP VIEW IF EXISTS vw_hospital_bed_occupancy;

DROP TRIGGER IF EXISTS trg_emergency_status_update;
DROP TRIGGER IF EXISTS trg_emergency_status_insert;

DROP TABLE IF EXISTS EMERGENCY_STATUS_HISTORY;
DROP TABLE IF EXISTS RESOURCE_ALLOCATION;
DROP TABLE IF EXISTS STAFF;
DROP TABLE IF EXISTS BED;
DROP TABLE IF EXISTS DEPARTMENT;
DROP TABLE IF EXISTS HOSPITAL;
DROP TABLE IF EXISTS EQUIPMENT;
DROP TABLE IF EXISTS AMBULANCE;
DROP TABLE IF EXISTS EMERGENCY;
DROP TABLE IF EXISTS EMERGENCY_TYPE;
DROP TABLE IF EXISTS PATIENT;
DROP TABLE IF EXISTS LOCATION;

-- ----------------------------------------------------------------------------
-- 1. LOCATION Table (Normalized 3NF: eliminates transitive address dependencies)
-- ----------------------------------------------------------------------------
CREATE TABLE LOCATION (
    location_id INTEGER PRIMARY KEY AUTOINCREMENT,
    address_line TEXT NOT NULL,
    zone_area TEXT NOT NULL,
    landmark TEXT,
    postal_code TEXT NOT NULL,
    city_district TEXT NOT NULL DEFAULT 'Noida'
);

-- ----------------------------------------------------------------------------
-- 2. PATIENT Table (Victim demographics, emergency contact, triage notes)
-- ----------------------------------------------------------------------------
CREATE TABLE PATIENT (
    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER CHECK (age > 0 AND age <= 125),
    gender TEXT CHECK (gender IN ('Male', 'Female', 'Other')) NOT NULL,
    contact_phone TEXT NOT NULL,
    blood_group TEXT CHECK (blood_group IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
    triage_medical_notes TEXT
);

-- ----------------------------------------------------------------------------
-- 3. EMERGENCY_TYPE Table (Clinical classification, baseline severity rating)
-- ----------------------------------------------------------------------------
CREATE TABLE EMERGENCY_TYPE (
    type_id INTEGER PRIMARY KEY AUTOINCREMENT,
    type_name TEXT NOT NULL UNIQUE,
    description TEXT,
    severity_default INTEGER CHECK (severity_default BETWEEN 1 AND 5) NOT NULL,
    priority_rank TEXT CHECK (priority_rank IN ('Low', 'Medium', 'High', 'Critical')) NOT NULL
);

-- ----------------------------------------------------------------------------
-- 4. EMERGENCY Table (Incident intake, severity, lifecycle state)
-- ----------------------------------------------------------------------------
CREATE TABLE EMERGENCY (
    emergency_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL REFERENCES PATIENT(patient_id) ON DELETE RESTRICT,
    type_id INTEGER NOT NULL REFERENCES EMERGENCY_TYPE(type_id) ON DELETE RESTRICT,
    location_id INTEGER NOT NULL REFERENCES LOCATION(location_id) ON DELETE RESTRICT,
    reported_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    severity INTEGER CHECK (severity BETWEEN 1 AND 5) NOT NULL,
    status TEXT CHECK (status IN ('Reported', 'Pending', 'Dispatched', 'In-Transit', 'Admitted', 'Resolved', 'Cancelled')) DEFAULT 'Reported' NOT NULL
);

-- ----------------------------------------------------------------------------
-- 5. AMBULANCE Table (Vehicle fleet inventory and operational readiness)
-- ----------------------------------------------------------------------------
CREATE TABLE AMBULANCE (
    ambulance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_no TEXT NOT NULL UNIQUE,
    type TEXT CHECK (type IN ('BLS', 'ALS')) NOT NULL,
    operational_status TEXT CHECK (operational_status IN ('Available', 'Dispatched', 'In-Transit', 'Maintenance')) DEFAULT 'Available' NOT NULL,
    base_station TEXT NOT NULL
);

-- ----------------------------------------------------------------------------
-- 6. EQUIPMENT Table (1:N isolated repeating group for 1NF compliance)
-- ----------------------------------------------------------------------------
CREATE TABLE EQUIPMENT (
    equipment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ambulance_id INTEGER NOT NULL REFERENCES AMBULANCE(ambulance_id) ON DELETE CASCADE,
    equipment_name TEXT NOT NULL,
    serial_no TEXT UNIQUE NOT NULL,
    is_functional INTEGER CHECK (is_functional IN (0, 1)) DEFAULT 1 NOT NULL
);

-- ----------------------------------------------------------------------------
-- 7. HOSPITAL Table (Receiving facilities and trauma tiers)
-- ----------------------------------------------------------------------------
CREATE TABLE HOSPITAL (
    hospital_id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id INTEGER NOT NULL REFERENCES LOCATION(location_id) ON DELETE RESTRICT,
    hospital_name TEXT NOT NULL,
    contact_phone TEXT NOT NULL,
    emergency_level TEXT CHECK (emergency_level IN ('Level 1 Trauma', 'Level 2 Trauma', 'General Hospital')) NOT NULL,
    total_beds INTEGER CHECK (total_beds >= 0) NOT NULL
);

-- ----------------------------------------------------------------------------
-- 8. DEPARTMENT Table (Clinical hospital divisions)
-- ----------------------------------------------------------------------------
CREATE TABLE DEPARTMENT (
    dept_id INTEGER PRIMARY KEY AUTOINCREMENT,
    hospital_id INTEGER NOT NULL REFERENCES HOSPITAL(hospital_id) ON DELETE CASCADE,
    dept_name TEXT NOT NULL,
    total_capacity INTEGER CHECK (total_capacity >= 0) NOT NULL,
    head_doctor TEXT,
    contact_ext TEXT
);

-- ----------------------------------------------------------------------------
-- 9. BED Table (Granular hospital capacity tracking across ICU and General)
-- ----------------------------------------------------------------------------
CREATE TABLE BED (
    bed_id INTEGER PRIMARY KEY AUTOINCREMENT,
    dept_id INTEGER NOT NULL REFERENCES DEPARTMENT(dept_id) ON DELETE CASCADE,
    bed_number TEXT NOT NULL,
    floor_no INTEGER NOT NULL,
    bed_type TEXT CHECK (bed_type IN ('ICU', 'General')) NOT NULL,
    is_occupied INTEGER CHECK (is_occupied IN (0, 1)) DEFAULT 0 NOT NULL,
    UNIQUE(dept_id, bed_number)
);

-- ----------------------------------------------------------------------------
-- 10. STAFF Table (Medical doctors, paramedics, ambulance drivers)
-- ----------------------------------------------------------------------------
CREATE TABLE STAFF (
    staff_id INTEGER PRIMARY KEY AUTOINCREMENT,
    hospital_id INTEGER REFERENCES HOSPITAL(hospital_id) ON DELETE SET NULL,
    ambulance_id INTEGER REFERENCES AMBULANCE(ambulance_id) ON DELETE SET NULL,
    full_name TEXT NOT NULL,
    role_type TEXT CHECK (role_type IN ('Doctor', 'Paramedic', 'Driver', 'Nurse')) NOT NULL,
    license_no TEXT UNIQUE NOT NULL,
    phone_no TEXT NOT NULL
);

-- ----------------------------------------------------------------------------
-- 11. RESOURCE_ALLOCATION Table (Associative Ternary Relation)
-- ----------------------------------------------------------------------------
CREATE TABLE RESOURCE_ALLOCATION (
    allocation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    emergency_id INTEGER NOT NULL REFERENCES EMERGENCY(emergency_id) ON DELETE RESTRICT,
    ambulance_id INTEGER NOT NULL REFERENCES AMBULANCE(ambulance_id) ON DELETE RESTRICT,
    hospital_id INTEGER NOT NULL REFERENCES HOSPITAL(hospital_id) ON DELETE RESTRICT,
    bed_id INTEGER REFERENCES BED(bed_id) ON DELETE RESTRICT,
    dispatch_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    arrival_time TIMESTAMP,
    status TEXT CHECK (status IN ('Dispatched', 'En-Route', 'Handover-Complete', 'Cancelled')) DEFAULT 'Dispatched' NOT NULL
);

-- ----------------------------------------------------------------------------
-- 12. EMERGENCY_STATUS_HISTORY Table (Trigger-Driven Immutable Audit Trail)
-- ----------------------------------------------------------------------------
CREATE TABLE EMERGENCY_STATUS_HISTORY (
    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
    emergency_id INTEGER NOT NULL REFERENCES EMERGENCY(emergency_id) ON DELETE RESTRICT,
    status_state TEXT NOT NULL,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by TEXT DEFAULT 'SYSTEM_TRIGGER' NOT NULL,
    remarks TEXT
);

-- ============================================================================
-- DATABASE TRIGGERS (Automated Audit Logging & State Synchronization)
-- ============================================================================

-- Trigger 1: Automatically log initial emergency creation
CREATE TRIGGER trg_emergency_status_insert
AFTER INSERT ON EMERGENCY
BEGIN
    INSERT INTO EMERGENCY_STATUS_HISTORY (
        emergency_id,
        status_state,
        changed_at,
        updated_by,
        remarks
    )
    VALUES (
        NEW.emergency_id,
        NEW.status,
        CURRENT_TIMESTAMP,
        'SYSTEM_TRIGGER',
        'Initial emergency incident registered with Severity Level ' || NEW.severity
    );
END;

-- Trigger 2: Automatically capture any status transition on EMERGENCY
CREATE TRIGGER trg_emergency_status_update
AFTER UPDATE OF status ON EMERGENCY
BEGIN
    INSERT INTO EMERGENCY_STATUS_HISTORY (
        emergency_id,
        status_state,
        changed_at,
        updated_by,
        remarks
    )
    VALUES (
        NEW.emergency_id,
        NEW.status,
        CURRENT_TIMESTAMP,
        'SYSTEM_TRIGGER',
        'Incident status transitioned from ''' || OLD.status || ''' to ''' || NEW.status || ''''
    );
END;

-- ============================================================================
-- ANALYTICAL VIEWS (Multi-table joins, subqueries, and aggregate metrics)
-- ============================================================================

-- View 1: Hospital bed capacity & dynamic occupancy rate
CREATE VIEW vw_hospital_bed_occupancy AS
SELECT 
    h.hospital_id,
    h.hospital_name,
    h.emergency_level,
    l.zone_area AS location_zone,
    COUNT(b.bed_id) AS total_beds_configured,
    SUM(CASE WHEN b.is_occupied = 1 THEN 1 ELSE 0 END) AS occupied_beds,
    SUM(CASE WHEN b.is_occupied = 0 THEN 1 ELSE 0 END) AS vacant_beds,
    SUM(CASE WHEN b.bed_type = 'ICU' AND b.is_occupied = 0 THEN 1 ELSE 0 END) AS vacant_icu_beds,
    SUM(CASE WHEN b.bed_type = 'General' AND b.is_occupied = 0 THEN 1 ELSE 0 END) AS vacant_general_beds,
    ROUND(
        (CAST(SUM(CASE WHEN b.is_occupied = 1 THEN 1 ELSE 0 END) AS REAL) / 
        NULLIF(COUNT(b.bed_id), 0)) * 100, 
        2
    ) AS occupancy_percentage
FROM HOSPITAL h
JOIN LOCATION l ON h.location_id = l.location_id
LEFT JOIN DEPARTMENT d ON h.hospital_id = d.hospital_id
LEFT JOIN BED b ON d.dept_id = b.dept_id
GROUP BY h.hospital_id, h.hospital_name, h.emergency_level, l.zone_area;

-- View 2: Ambulance fleet readiness and functional onboard equipment
CREATE VIEW vw_ambulance_fleet_status AS
SELECT 
    a.ambulance_id,
    a.vehicle_no,
    a.type AS ambulance_type,
    a.operational_status,
    a.base_station,
    COUNT(e.equipment_id) AS total_equipment_count,
    SUM(CASE WHEN e.is_functional = 1 THEN 1 ELSE 0 END) AS functional_equipment_count,
    SUM(CASE WHEN e.is_functional = 0 THEN 1 ELSE 0 END) AS faulty_equipment_count
FROM AMBULANCE a
LEFT JOIN EQUIPMENT e ON a.ambulance_id = e.ambulance_id
GROUP BY a.ambulance_id, a.vehicle_no, a.type, a.operational_status, a.base_station;

-- View 3: Live active emergencies with patient, location, and assigned resources
CREATE VIEW vw_active_emergencies AS
SELECT 
    e.emergency_id,
    e.reported_time,
    e.severity,
    e.status AS incident_status,
    t.type_name AS emergency_category,
    t.priority_rank,
    p.name AS patient_name,
    p.age AS patient_age,
    p.gender AS patient_gender,
    p.blood_group,
    p.contact_phone AS patient_phone,
    l.address_line,
    l.zone_area,
    l.landmark,
    ra.allocation_id,
    a.vehicle_no AS assigned_ambulance,
    a.type AS ambulance_class,
    h.hospital_name AS assigned_hospital,
    b.bed_number AS reserved_bed,
    b.bed_type AS reserved_bed_type
FROM EMERGENCY e
JOIN PATIENT p ON e.patient_id = p.patient_id
JOIN EMERGENCY_TYPE t ON e.type_id = t.type_id
JOIN LOCATION l ON e.location_id = l.location_id
LEFT JOIN RESOURCE_ALLOCATION ra ON e.emergency_id = ra.emergency_id
LEFT JOIN AMBULANCE a ON ra.ambulance_id = a.ambulance_id
LEFT JOIN HOSPITAL h ON ra.hospital_id = h.hospital_id
LEFT JOIN BED b ON ra.bed_id = b.bed_id;

-- View 4: Response latency analytics for completed/dispatched cases
CREATE VIEW vw_response_latency_analytics AS
SELECT 
    e.emergency_id,
    t.type_name AS emergency_type,
    e.severity,
    e.reported_time,
    ra.dispatch_time,
    ra.arrival_time,
    a.vehicle_no,
    h.hospital_name,
    ROUND((JULIANDAY(ra.dispatch_time) - JULIANDAY(e.reported_time)) * 24 * 60, 2) AS dispatch_delay_minutes,
    ROUND((JULIANDAY(ra.arrival_time) - JULIANDAY(ra.dispatch_time)) * 24 * 60, 2) AS transit_duration_minutes
FROM EMERGENCY e
JOIN EMERGENCY_TYPE t ON e.type_id = t.type_id
JOIN RESOURCE_ALLOCATION ra ON e.emergency_id = ra.emergency_id
JOIN AMBULANCE a ON ra.ambulance_id = a.ambulance_id
JOIN HOSPITAL h ON ra.hospital_id = h.hospital_id
WHERE ra.dispatch_time IS NOT NULL;
