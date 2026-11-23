-- ============================================================================
-- URBAN EMERGENCY RESPONSE & RESOURCE ALLOCATION SYSTEM
-- Course: Database Management Systems Lab (24B15CS213)
-- Department of Computer Science & Engineering, JIIT Noida-62
-- Seed Data: Comprehensive Noida / NCR Emergency Response Scenarios
-- ============================================================================

PRAGMA foreign_keys = ON;

-- ----------------------------------------------------------------------------
-- 1. Insert Locations (Noida Urban Zones)
-- ----------------------------------------------------------------------------
INSERT INTO LOCATION (location_id, address_line, zone_area, landmark, postal_code, city_district) VALUES
(1, 'A-10, Sector 62 Institutional Area', 'Sector 62', 'Near JIIT Campus', '201309', 'Noida'),
(2, 'Block B, Sector 18 Commercial Hub', 'Sector 18', 'Atta Market Metro Gate 2', '201301', 'Noida'),
(3, 'Wish Town, Sector 128 Expressway', 'Sector 128', 'Near Jaypee Greens', '201304', 'Noida'),
(4, 'H-Block, Sector 27 Market', 'Sector 27', 'Near Kailash Hospital Roundabout', '201301', 'Noida'),
(5, 'Plot 1, Sector 39 Health Zone', 'Sector 39', 'Opposite City Centre Metro', '201303', 'Noida'),
(6, 'Shipra Suncity, Indirapuram', 'Indirapuram', 'Near Vaibhav Khand', '201014', 'Ghaziabad-NCR'),
(7, 'Gaur City 1, Greater Noida West', 'Gr. Noida West', 'Char Murti Chowk', '201009', 'Gautam Buddha Nagar'),
(8, 'Sector 15A Residential Complex', 'Sector 15A', 'Near DND Flyway Toll Plaza', '201301', 'Noida');

-- ----------------------------------------------------------------------------
-- 2. Insert Clinical Emergency Types
-- ----------------------------------------------------------------------------
INSERT INTO EMERGENCY_TYPE (type_id, type_name, description, severity_default, priority_rank) VALUES
(1, 'Cardiac Arrest', 'Sudden loss of heart function, unconsciousness, pulseless patient requiring immediate ALS and defibrillator.', 5, 'Critical'),
(2, 'Severe Road Trauma', 'Major vehicle collision with polytrauma, crush injury, severe hemorrhaging requiring Level 1 trauma resuscitation.', 5, 'Critical'),
(3, 'Acute Respiratory Failure', 'Severe oxygen desaturation (<85%), respiratory distress requiring mechanical ventilation or CPAP.', 4, 'High'),
(4, 'Acute Ischemic Stroke', 'Focal neurological deficit, facial droop, hemiparesis within thrombolysis golden hour window.', 4, 'High'),
(5, 'Multi-Fracture Injury', 'Compound bone fractures, immobilized patient with stable hemodynamics requiring BLS and splinting.', 3, 'Medium'),
(6, 'Severe Anaphylaxis', 'Acute systemic allergic reaction with bronchospasm, angioedema, requiring epinephrine infusion.', 3, 'Medium'),
(7, 'Moderate Heat Stroke / Dehydration', 'Thermoregulatory failure, dizziness, mild disorientation without cardiovascular collapse.', 2, 'Low');

-- ----------------------------------------------------------------------------
-- 3. Insert Patients
-- ----------------------------------------------------------------------------
INSERT INTO PATIENT (patient_id, name, age, gender, contact_phone, blood_group, triage_medical_notes) VALUES
(1, 'Aarav Sharma', 48, 'Male', '+91-9811023451', 'B+', 'Sudden chest pain radiating to left arm, hypertensive, diaphoresis noted.'),
(2, 'Pooja Verma', 26, 'Female', '+91-9871234567', 'O+', 'High-speed motorcycle collision on expressway, compound tibial fracture and head contusion.'),
(3, 'Suresh Chandra Gupta', 71, 'Male', '+91-9958012344', 'AB+', 'History of COPD, severe wheezing, pulse oximetry reading 82%.'),
(4, 'Neha Malhotra', 34, 'Female', '+91-9810987654', 'A+', 'Acute onset right-sided hemiplegia and expressive aphasia, onset 35 mins ago.'),
(5, 'Vikas Mehra', 29, 'Male', '+91-9717012390', 'O-', 'Industrial fall from 15ft scaffolding, multiple rib fractures, conscious and stable.'),
(6, 'Kavita Iyer', 22, 'Female', '+91-9899123499', 'B-', 'Peanut-induced anaphylactic shock, stridor, urticarial rash across neck and chest.'),
(7, 'Rajesh Khanna', 55, 'Male', '+91-9818045612', 'A-', 'Complaining of dizziness, mild dehydration after outdoor marathon training.');

-- ----------------------------------------------------------------------------
-- 4. Insert Hospitals
-- ----------------------------------------------------------------------------
INSERT INTO HOSPITAL (hospital_id, location_id, hospital_name, contact_phone, emergency_level, total_beds) VALUES
(1, 1, 'Fortis Hospital Noida', '+91-120-4300222', 'Level 1 Trauma', 300),
(2, 3, 'Jaypee Hospital Noida', '+91-120-4122222', 'Level 1 Trauma', 500),
(3, 4, 'Kailash Hospital & Neuro Institute', '+91-120-2444444', 'Level 2 Trauma', 250),
(4, 5, 'Noida District Government Hospital', '+91-120-2500100', 'General Hospital', 150);

-- ----------------------------------------------------------------------------
-- 5. Insert Clinical Departments
-- ----------------------------------------------------------------------------
INSERT INTO DEPARTMENT (dept_id, hospital_id, dept_name, total_capacity, head_doctor, contact_ext) VALUES
(1, 1, 'Emergency & Trauma Care', 40, 'Dr. Rajiv Mukhopadhyay', '101'),
(2, 1, 'Intensive Care Unit (ICU)', 25, 'Dr. S. K. Narang', '102'),
(3, 2, 'Emergency Medicine & Resuscitation', 60, 'Dr. Ananya Sen', '201'),
(4, 2, 'Critical Care & Neuro ICU', 40, 'Dr. Pradeep Bhattacharya', '202'),
(5, 3, 'Trauma & Emergency Wing', 30, 'Dr. Mahesh Chandra', '301'),
(6, 3, 'Surgical ICU', 20, 'Dr. Sunita Saxena', '302'),
(7, 4, 'General Emergency Ward', 25, 'Dr. R. K. Singhal', '401');

-- ----------------------------------------------------------------------------
-- 6. Insert Hospital Beds (ICU and General)
-- ----------------------------------------------------------------------------
INSERT INTO BED (bed_id, dept_id, bed_number, floor_no, bed_type, is_occupied) VALUES
-- Fortis Emergency (Dept 1)
(1, 1, 'FOR-EMG-101', 1, 'General', 0),
(2, 1, 'FOR-EMG-102', 1, 'General', 1),
(3, 1, 'FOR-EMG-103', 1, 'General', 0),
-- Fortis ICU (Dept 2)
(4, 2, 'FOR-ICU-201', 2, 'ICU', 0),
(5, 2, 'FOR-ICU-202', 2, 'ICU', 0),
(6, 2, 'FOR-ICU-203', 2, 'ICU', 1),
-- Jaypee Emergency (Dept 3)
(7, 3, 'JAY-EMG-301', 1, 'General', 0),
(8, 3, 'JAY-EMG-302', 1, 'General', 0),
(9, 3, 'JAY-EMG-303', 1, 'General', 1),
-- Jaypee Neuro ICU (Dept 4)
(10, 4, 'JAY-ICU-401', 3, 'ICU', 0),
(11, 4, 'JAY-ICU-402', 3, 'ICU', 0),
(12, 4, 'JAY-ICU-403', 3, 'ICU', 1),
-- Kailash Trauma (Dept 5)
(13, 5, 'KAI-TRM-501', 1, 'General', 0),
(14, 5, 'KAI-TRM-502', 1, 'General', 0),
-- Kailash Surgical ICU (Dept 6)
(15, 6, 'KAI-ICU-601', 2, 'ICU', 0),
(16, 6, 'KAI-ICU-602', 2, 'ICU', 1),
-- District Hospital (Dept 7)
(17, 7, 'DST-GEN-701', 1, 'General', 0),
(18, 7, 'DST-GEN-702', 1, 'General', 0);

-- ----------------------------------------------------------------------------
-- 7. Insert Ambulance Fleet
-- ----------------------------------------------------------------------------
INSERT INTO AMBULANCE (ambulance_id, vehicle_no, type, operational_status, base_station) VALUES
(1, 'UP-16-AM-1001', 'ALS', 'Available', 'Sector 62 Emergency Post'),
(2, 'UP-16-AM-1002', 'ALS', 'Available', 'Fortis Hospital Bay'),
(3, 'UP-16-AM-1003', 'BLS', 'Available', 'Sector 18 Metro Post'),
(4, 'UP-16-AM-1004', 'ALS', 'Available', 'Sector 128 Expressway Hub'),
(5, 'UP-16-AM-1005', 'BLS', 'Available', 'Kailash Hospital Bay'),
(6, 'UP-16-AM-1006', 'ALS', 'Maintenance', 'Sector 39 Central Depot'),
(7, 'UP-16-AM-1007', 'BLS', 'Dispatched', 'Indirapuram Border Post');

-- ----------------------------------------------------------------------------
-- 8. Insert Onboard Equipment (1NF Normalized Repeating Groups)
-- ----------------------------------------------------------------------------
INSERT INTO EQUIPMENT (equipment_id, ambulance_id, equipment_name, serial_no, is_functional) VALUES
-- UP-16-AM-1001 (ALS - Full setup)
(1, 1, 'Biphasic Defibrillator', 'DEF-Z-99011', 1),
(2, 1, 'Transport Ventilator (Oxylog 3000)', 'VENT-DR-4401', 1),
(3, 1, 'Multiparameter Patient Monitor', 'MON-PHI-8821', 1),
(4, 1, 'Suction Machine Electric', 'SUC-DEV-1092', 1),
-- UP-16-AM-1002 (ALS - Full setup)
(5, 2, 'Biphasic Defibrillator', 'DEF-Z-99012', 1),
(6, 2, 'Transport Ventilator (Oxylog 3000)', 'VENT-DR-4402', 1),
(7, 2, 'Multiparameter Patient Monitor', 'MON-PHI-8822', 1),
-- UP-16-AM-1003 (BLS)
(8, 3, 'Automated External Defibrillator (AED)', 'AED-PHI-3301', 1),
(9, 3, 'Portable Oxygen Delivery Kit', 'OXY-KIT-1103', 1),
(10, 3, 'Spine Board & Immobilizer', 'SPN-BRD-7701', 1),
-- UP-16-AM-1004 (ALS)
(11, 4, 'Biphasic Defibrillator', 'DEF-Z-99014', 1),
(12, 4, 'Transport Ventilator (Oxylog 3000)', 'VENT-DR-4404', 1),
(13, 4, 'Syringe Infusion Pump', 'PMP-BB-5501', 1),
-- UP-16-AM-1005 (BLS)
(14, 5, 'Automated External Defibrillator (AED)', 'AED-PHI-3305', 1),
(15, 5, 'Portable Oxygen Delivery Kit', 'OXY-KIT-1105', 1),
-- UP-16-AM-1006 (Maintenance)
(16, 6, 'Transport Ventilator', 'VENT-DR-4406', 0);

-- ----------------------------------------------------------------------------
-- 9. Insert Medical & Operational Staff
-- ----------------------------------------------------------------------------
INSERT INTO STAFF (staff_id, hospital_id, ambulance_id, full_name, role_type, license_no, phone_no) VALUES
(1, 1, NULL, 'Dr. Vikramaditya Rathore', 'Doctor', 'MCI-DEL-2012-8812', '+91-9811122334'),
(2, 2, NULL, 'Dr. Meenakshi Sundaram', 'Doctor', 'MCI-UP-2015-4421', '+91-9822233445'),
(3, NULL, 1, 'Sunil Kumar Yadav', 'Paramedic', 'EMT-P-UP-2019-109', '+91-9877711223'),
(4, NULL, 1, 'Dharmendra Rawat', 'Driver', 'DL-UP-16-2014-9988', '+91-9866655443'),
(5, NULL, 2, 'Amitabh Sengupta', 'Paramedic', 'EMT-P-UP-2020-221', '+91-9855544332'),
(6, NULL, 2, 'Ramesh Chander', 'Driver', 'DL-UP-16-2011-3321', '+91-9844433221'),
(7, NULL, 3, 'Pankaj Goswami', 'Paramedic', 'EMT-B-UP-2021-309', '+91-9833322110'),
(8, NULL, 3, 'Kuldeep Singh', 'Driver', 'DL-UP-16-2018-7711', '+91-9822211009'),
(9, 3, NULL, 'Dr. Aniruddh Joshi', 'Doctor', 'MCI-UP-2010-9011', '+91-9811100998');

-- ----------------------------------------------------------------------------
-- 10. Insert Historical & Initial Emergencies (Triggers will fire automatically!)
-- ----------------------------------------------------------------------------
-- Emergency 1: High severity cardiac arrest (Pending dispatch demonstration)
INSERT INTO EMERGENCY (emergency_id, patient_id, type_id, location_id, reported_time, severity, status) VALUES
(1, 1, 1, 1, datetime('now', '-25 minutes'), 5, 'Reported');

-- Emergency 2: Road accident (Demonstration of already allocated/dispatched case)
INSERT INTO EMERGENCY (emergency_id, patient_id, type_id, location_id, reported_time, severity, status) VALUES
(2, 2, 2, 3, datetime('now', '-50 minutes'), 5, 'Dispatched');

-- Emergency 3: Severe respiratory distress (Reported)
INSERT INTO EMERGENCY (emergency_id, patient_id, type_id, location_id, reported_time, severity, status) VALUES
(3, 3, 3, 2, datetime('now', '-15 minutes'), 4, 'Reported');

-- Emergency 4: Acute ischemic stroke (Reported)
INSERT INTO EMERGENCY (emergency_id, patient_id, type_id, location_id, reported_time, severity, status) VALUES
(4, 4, 4, 8, datetime('now', '-10 minutes'), 4, 'Reported');

-- Emergency 5: Multi-fracture fall (Resolved historical case)
INSERT INTO EMERGENCY (emergency_id, patient_id, type_id, location_id, reported_time, severity, status) VALUES
(5, 5, 5, 6, datetime('now', '-180 minutes'), 3, 'Admitted');

-- ----------------------------------------------------------------------------
-- 11. Insert Historical Resource Allocations
-- ----------------------------------------------------------------------------
-- Allocation for Emergency 2
INSERT INTO RESOURCE_ALLOCATION (allocation_id, emergency_id, ambulance_id, hospital_id, bed_id, dispatch_time, arrival_time, status) VALUES
(1, 2, 7, 2, 9, datetime('now', '-45 minutes'), datetime('now', '-30 minutes'), 'En-Route');

-- Allocation for Emergency 5
INSERT INTO RESOURCE_ALLOCATION (allocation_id, emergency_id, ambulance_id, hospital_id, bed_id, dispatch_time, arrival_time, status) VALUES
(2, 5, 5, 1, 2, datetime('now', '-175 minutes'), datetime('now', '-140 minutes'), 'Handover-Complete');
