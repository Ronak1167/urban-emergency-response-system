-- ============================================================================
-- URBAN EMERGENCY RESPONSE & RESOURCE ALLOCATION SYSTEM
-- Course: Database Management Systems Lab (24B15CS213)
-- Department of Computer Science & Engineering, JIIT Noida-62
-- Schema: 3NF Relational Database Schema (MySQL 8.0+ Compatible)
-- ============================================================================

CREATE DATABASE IF NOT EXISTS urban_emergency_db;
USE urban_emergency_db;

-- Drop views if exist
DROP VIEW IF EXISTS vw_response_latency_analytics;
DROP VIEW IF EXISTS vw_active_emergencies;
DROP VIEW IF EXISTS vw_ambulance_fleet_status;
DROP VIEW IF EXISTS vw_hospital_bed_occupancy;

-- Drop tables with foreign key constraints
SET FOREIGN_KEY_CHECKS = 0;
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
SET FOREIGN_KEY_CHECKS = 1;

-- ----------------------------------------------------------------------------
-- 1. LOCATION Table
-- ----------------------------------------------------------------------------
CREATE TABLE LOCATION (
    location_id INT AUTO_INCREMENT PRIMARY KEY,
    address_line VARCHAR(255) NOT NULL,
    zone_area VARCHAR(100) NOT NULL,
    landmark VARCHAR(150),
    postal_code VARCHAR(20) NOT NULL,
    city_district VARCHAR(100) NOT NULL DEFAULT 'Noida'
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 2. PATIENT Table
-- ----------------------------------------------------------------------------
CREATE TABLE PATIENT (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    age INT CHECK (age > 0 AND age <= 125),
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    contact_phone VARCHAR(20) NOT NULL,
    blood_group ENUM('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'),
    triage_medical_notes TEXT
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 3. EMERGENCY_TYPE Table
-- ----------------------------------------------------------------------------
CREATE TABLE EMERGENCY_TYPE (
    type_id INT AUTO_INCREMENT PRIMARY KEY,
    type_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    severity_default INT CHECK (severity_default BETWEEN 1 AND 5) NOT NULL,
    priority_rank ENUM('Low', 'Medium', 'High', 'Critical') NOT NULL
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 4. EMERGENCY Table
-- ----------------------------------------------------------------------------
CREATE TABLE EMERGENCY (
    emergency_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    type_id INT NOT NULL,
    location_id INT NOT NULL,
    reported_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    severity INT CHECK (severity BETWEEN 1 AND 5) NOT NULL,
    status ENUM('Reported', 'Pending', 'Dispatched', 'In-Transit', 'Admitted', 'Resolved', 'Cancelled') DEFAULT 'Reported' NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES PATIENT(patient_id) ON DELETE RESTRICT,
    FOREIGN KEY (type_id) REFERENCES EMERGENCY_TYPE(type_id) ON DELETE RESTRICT,
    FOREIGN KEY (location_id) REFERENCES LOCATION(location_id) ON DELETE RESTRICT
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 5. AMBULANCE Table
-- ----------------------------------------------------------------------------
CREATE TABLE AMBULANCE (
    ambulance_id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_no VARCHAR(30) NOT NULL UNIQUE,
    type ENUM('BLS', 'ALS') NOT NULL,
    operational_status ENUM('Available', 'Dispatched', 'In-Transit', 'Maintenance') DEFAULT 'Available' NOT NULL,
    base_station VARCHAR(120) NOT NULL
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 6. EQUIPMENT Table
-- ----------------------------------------------------------------------------
CREATE TABLE EQUIPMENT (
    equipment_id INT AUTO_INCREMENT PRIMARY KEY,
    ambulance_id INT NOT NULL,
    equipment_name VARCHAR(120) NOT NULL,
    serial_no VARCHAR(80) UNIQUE NOT NULL,
    is_functional TINYINT(1) DEFAULT 1 NOT NULL,
    FOREIGN KEY (ambulance_id) REFERENCES AMBULANCE(ambulance_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 7. HOSPITAL Table
-- ----------------------------------------------------------------------------
CREATE TABLE HOSPITAL (
    hospital_id INT AUTO_INCREMENT PRIMARY KEY,
    location_id INT NOT NULL,
    hospital_name VARCHAR(150) NOT NULL,
    contact_phone VARCHAR(20) NOT NULL,
    emergency_level ENUM('Level 1 Trauma', 'Level 2 Trauma', 'General Hospital') NOT NULL,
    total_beds INT CHECK (total_beds >= 0) NOT NULL,
    FOREIGN KEY (location_id) REFERENCES LOCATION(location_id) ON DELETE RESTRICT
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 8. DEPARTMENT Table
-- ----------------------------------------------------------------------------
CREATE TABLE DEPARTMENT (
    dept_id INT AUTO_INCREMENT PRIMARY KEY,
    hospital_id INT NOT NULL,
    dept_name VARCHAR(120) NOT NULL,
    total_capacity INT CHECK (total_capacity >= 0) NOT NULL,
    head_doctor VARCHAR(120),
    contact_ext VARCHAR(20),
    FOREIGN KEY (hospital_id) REFERENCES HOSPITAL(hospital_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 9. BED Table
-- ----------------------------------------------------------------------------
CREATE TABLE BED (
    bed_id INT AUTO_INCREMENT PRIMARY KEY,
    dept_id INT NOT NULL,
    bed_number VARCHAR(20) NOT NULL,
    floor_no INT NOT NULL,
    bed_type ENUM('ICU', 'General') NOT NULL,
    is_occupied TINYINT(1) DEFAULT 0 NOT NULL,
    UNIQUE KEY uk_dept_bed (dept_id, bed_number),
    FOREIGN KEY (dept_id) REFERENCES DEPARTMENT(dept_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 10. STAFF Table
-- ----------------------------------------------------------------------------
CREATE TABLE STAFF (
    staff_id INT AUTO_INCREMENT PRIMARY KEY,
    hospital_id INT NULL,
    ambulance_id INT NULL,
    full_name VARCHAR(120) NOT NULL,
    role_type ENUM('Doctor', 'Paramedic', 'Driver', 'Nurse') NOT NULL,
    license_no VARCHAR(80) UNIQUE NOT NULL,
    phone_no VARCHAR(20) NOT NULL,
    FOREIGN KEY (hospital_id) REFERENCES HOSPITAL(hospital_id) ON DELETE SET NULL,
    FOREIGN KEY (ambulance_id) REFERENCES AMBULANCE(ambulance_id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 11. RESOURCE_ALLOCATION Table
-- ----------------------------------------------------------------------------
CREATE TABLE RESOURCE_ALLOCATION (
    allocation_id INT AUTO_INCREMENT PRIMARY KEY,
    emergency_id INT NOT NULL,
    ambulance_id INT NOT NULL,
    hospital_id INT NOT NULL,
    bed_id INT NULL,
    dispatch_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    arrival_time DATETIME NULL,
    status ENUM('Dispatched', 'En-Route', 'Handover-Complete', 'Cancelled') DEFAULT 'Dispatched' NOT NULL,
    FOREIGN KEY (emergency_id) REFERENCES EMERGENCY(emergency_id) ON DELETE RESTRICT,
    FOREIGN KEY (ambulance_id) REFERENCES AMBULANCE(ambulance_id) ON DELETE RESTRICT,
    FOREIGN KEY (hospital_id) REFERENCES HOSPITAL(hospital_id) ON DELETE RESTRICT,
    FOREIGN KEY (bed_id) REFERENCES BED(bed_id) ON DELETE RESTRICT
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 12. EMERGENCY_STATUS_HISTORY Table (Trigger-Driven Audit Trail)
-- ----------------------------------------------------------------------------
CREATE TABLE EMERGENCY_STATUS_HISTORY (
    history_id INT AUTO_INCREMENT PRIMARY KEY,
    emergency_id INT NOT NULL,
    status_state VARCHAR(50) NOT NULL,
    changed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(50) DEFAULT 'SYSTEM_TRIGGER' NOT NULL,
    remarks TEXT,
    FOREIGN KEY (emergency_id) REFERENCES EMERGENCY(emergency_id) ON DELETE RESTRICT
) ENGINE=InnoDB;

-- ============================================================================
-- TRIGGERS
-- ============================================================================
DELIMITER $$

CREATE TRIGGER trg_emergency_status_insert
AFTER INSERT ON EMERGENCY
FOR EACH ROW
BEGIN
    INSERT INTO EMERGENCY_STATUS_HISTORY (
        emergency_id, status_state, changed_at, updated_by, remarks
    ) VALUES (
        NEW.emergency_id,
        NEW.status,
        NOW(),
        'SYSTEM_TRIGGER',
        CONCAT('Initial emergency incident registered with Severity Level ', NEW.severity)
    );
END$$

CREATE TRIGGER trg_emergency_status_update
AFTER UPDATE ON EMERGENCY
FOR EACH ROW
BEGIN
    IF OLD.status <> NEW.status THEN
        INSERT INTO EMERGENCY_STATUS_HISTORY (
            emergency_id, status_state, changed_at, updated_by, remarks
        ) VALUES (
            NEW.emergency_id,
            NEW.status,
            NOW(),
            'SYSTEM_TRIGGER',
            CONCAT('Incident status transitioned from ''', OLD.status, ''' to ''', NEW.status, '''')
        );
    END IF;
END$$

DELIMITER ;

-- ============================================================================
-- VIEWS
-- ============================================================================

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
    ROUND((SUM(CASE WHEN b.is_occupied = 1 THEN 1 ELSE 0 END) / NULLIF(COUNT(b.bed_id), 0)) * 100, 2) AS occupancy_percentage
FROM HOSPITAL h
JOIN LOCATION l ON h.location_id = l.location_id
LEFT JOIN DEPARTMENT d ON h.hospital_id = d.hospital_id
LEFT JOIN BED b ON d.dept_id = b.dept_id
GROUP BY h.hospital_id, h.hospital_name, h.emergency_level, l.zone_area;

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
    TIMESTAMPDIFF(MINUTE, e.reported_time, ra.dispatch_time) AS dispatch_delay_minutes,
    TIMESTAMPDIFF(MINUTE, ra.dispatch_time, ra.arrival_time) AS transit_duration_minutes
FROM EMERGENCY e
JOIN EMERGENCY_TYPE t ON e.type_id = t.type_id
JOIN RESOURCE_ALLOCATION ra ON e.emergency_id = ra.emergency_id
JOIN AMBULANCE a ON ra.ambulance_id = a.ambulance_id
JOIN HOSPITAL h ON ra.hospital_id = h.hospital_id
WHERE ra.dispatch_time IS NOT NULL;
