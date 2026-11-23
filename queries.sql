-- ============================================================================
-- URBAN EMERGENCY RESPONSE & RESOURCE ALLOCATION SYSTEM
-- Course: Database Management Systems Lab (24B15CS213)
-- Department of Computer Science & Engineering, JIIT Noida-62
-- Lab Evaluation Queries: Joins, Nested Subqueries, Aggregates & Views
-- ============================================================================

-- ============================================================================
-- CATEGORY 1: COMPLEX MULTI-TABLE JOINS (3, 4, and 5-Table Joins)
-- ============================================================================

-- Query 1.1: Comprehensive Emergency Dispatch Dossier (5-Table Join)
-- Connects Emergency, Patient, Incident Type, Location, and Resource Allocation.
SELECT 
    e.emergency_id,
    p.name AS patient_name,
    p.age,
    p.blood_group,
    t.type_name AS emergency_nature,
    e.severity,
    l.zone_area,
    l.address_line,
    COALESCE(a.vehicle_no, 'UNASSIGNED') AS dispatched_ambulance,
    COALESCE(h.hospital_name, 'UNRESERVED') AS receiving_hospital,
    COALESCE(b.bed_number, 'NONE') AS assigned_bed,
    e.status
FROM EMERGENCY e
JOIN PATIENT p ON e.patient_id = p.patient_id
JOIN EMERGENCY_TYPE t ON e.type_id = t.type_id
JOIN LOCATION l ON e.location_id = l.location_id
LEFT JOIN RESOURCE_ALLOCATION ra ON e.emergency_id = ra.emergency_id
LEFT JOIN AMBULANCE a ON ra.ambulance_id = a.ambulance_id
LEFT JOIN HOSPITAL h ON ra.hospital_id = h.hospital_id
LEFT JOIN BED b ON ra.bed_id = b.bed_id
ORDER BY e.severity DESC, e.reported_time ASC;

-- Query 1.2: Ambulance Crew & Functional Equipment Roster (4-Table Join)
-- Joins Ambulance, Staff, Location, and Equipment to produce field readiness.
SELECT 
    a.vehicle_no,
    a.type AS ambulance_type,
    a.operational_status,
    a.base_station,
    s.full_name AS crew_member,
    s.role_type,
    e.equipment_name,
    e.serial_no,
    CASE WHEN e.is_functional = 1 THEN 'OPERATIONAL' ELSE 'FAULTY' END AS equip_status
FROM AMBULANCE a
LEFT JOIN STAFF s ON a.ambulance_id = s.ambulance_id
LEFT JOIN EQUIPMENT e ON a.ambulance_id = e.ambulance_id
ORDER BY a.vehicle_no, s.role_type;


-- ============================================================================
-- CATEGORY 2: NESTED SUBQUERIES (Correlated & Non-Correlated)
-- ============================================================================

-- Query 2.1: Find Available ALS Ambulances that possess BOTH a functional Ventilator AND Defibrillator
-- (Subquery with INTERSECT / IN)
SELECT 
    a.ambulance_id,
    a.vehicle_no,
    a.type,
    a.base_station
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
  );

-- Query 2.2: Find Hospitals with Higher-than-Average Vacant ICU Beds
-- (Correlated Subquery comparing hospital capacity to global average)
SELECT 
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
);

-- Query 2.3: Unallocated High-Severity Emergencies requiring immediate intervention
-- (Subquery with NOT EXISTS)
SELECT 
    e.emergency_id,
    p.name AS patient_name,
    p.contact_phone,
    t.type_name,
    e.severity,
    e.reported_time
FROM EMERGENCY e
JOIN PATIENT p ON e.patient_id = p.patient_id
JOIN EMERGENCY_TYPE t ON e.type_id = t.type_id
WHERE e.severity >= 4
  AND NOT EXISTS (
      SELECT 1 FROM RESOURCE_ALLOCATION ra 
      WHERE ra.emergency_id = e.emergency_id
  );


-- ============================================================================
-- CATEGORY 3: AGGREGATE FUNCTIONS, GROUP BY & HAVING
-- ============================================================================

-- Query 3.1: Hospital Department Bed Utilization Statistics
-- Demonstrates COUNT, SUM, AVG, and GROUP BY with HAVING clause
SELECT 
    h.hospital_name,
    d.dept_name,
    COUNT(b.bed_id) AS total_beds_in_dept,
    SUM(CASE WHEN b.is_occupied = 1 THEN 1 ELSE 0 END) AS occupied_count,
    SUM(CASE WHEN b.is_occupied = 0 THEN 1 ELSE 0 END) AS vacant_count,
    ROUND(AVG(b.is_occupied) * 100, 2) AS dept_occupancy_pct
FROM HOSPITAL h
JOIN DEPARTMENT d ON h.hospital_id = d.hospital_id
JOIN BED b ON d.dept_id = b.dept_id
GROUP BY h.hospital_name, d.dept_name
HAVING COUNT(b.bed_id) > 1
ORDER BY dept_occupancy_pct DESC;

-- Query 3.2: Emergency Incident Count & Average Severity by Zone
SELECT 
    l.zone_area,
    COUNT(e.emergency_id) AS total_emergencies_reported,
    ROUND(AVG(e.severity), 2) AS avg_severity_score,
    MAX(e.severity) AS peak_severity,
    MIN(e.severity) AS lowest_severity
FROM LOCATION l
JOIN EMERGENCY e ON l.location_id = e.location_id
GROUP BY l.zone_area
HAVING COUNT(e.emergency_id) >= 1
ORDER BY avg_severity_score DESC;


-- ============================================================================
-- CATEGORY 4: QUERYING ANALYTICAL VIEWS
-- ============================================================================

-- Query 4.1: Live Hospital Bed Occupancy View
SELECT * FROM vw_hospital_bed_occupancy
ORDER BY vacant_icu_beds DESC;

-- Query 4.2: Fleet Readiness View
SELECT * FROM vw_ambulance_fleet_status
ORDER BY functional_equipment_count DESC;

-- Query 4.3: Active Emergencies View
SELECT * FROM vw_active_emergencies
WHERE incident_status IN ('Reported', 'Pending', 'Dispatched');

-- Query 4.4: Response Latency Analytics View
SELECT * FROM vw_response_latency_analytics;


-- ============================================================================
-- CATEGORY 5: TRIGGER AUDIT TRAIL VERIFICATION
-- ============================================================================

-- Query 5.1: Chronological Audit Trail from EMERGENCY_STATUS_HISTORY
-- Shows state changes created automatically by the database triggers
SELECT 
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
ORDER BY h.history_id ASC;
