"""
Urban Emergency Response & Resource Allocation System
Database Management Systems Lab (24B15CS213)
JIIT Noida-62 - Department of CSE & IT

High-Resolution Professional Vector Graphics & Diagram Exporter:
1. EER Diagram (Chen/EER standard shapes matching user reference)
2. System Flowchart (End-to-end incident lifecycle)
3. EER-to-Relational Table Conversion (Schema mappings with PK/FK arrows)
"""

import os
import subprocess

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIAGRAMS_DIR = os.path.join(PROJECT_DIR, "static", "diagrams")
DOWNLOADS_DIR = os.path.join(os.path.expanduser("~"), "Downloads")
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

os.makedirs(STATIC_DIAGRAMS_DIR, exist_ok=True)
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

# =============================================================================
# 1. GENERATE EER DIAGRAM (CHEN & EER NOTATION MATCHING USER'S IMAGE)
# =============================================================================
def generate_eer_diagram_html():
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>EER Diagram - Urban Emergency Response System</title>
<style>
  body {
    margin: 0;
    padding: 20px;
    background: #ffffff;
    font-family: 'Segoe UI', Arial, sans-serif;
  }
  svg {
    display: block;
    margin: 0 auto;
    background: #ffffff;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    border-radius: 8px;
  }
  .title-text { font-size: 26px; font-weight: 800; fill: #14532D; text-anchor: middle; }
  .subtitle-text { font-size: 14px; font-weight: 600; fill: #4B5563; text-anchor: middle; }
  
  /* Entity Rectangles */
  .entity-rect { fill: #DCFCE7; stroke: #15803D; stroke-width: 2.2; rx: 4; ry: 4; }
  .entity-weak-outer { fill: #DCFCE7; stroke: #15803D; stroke-width: 2.2; rx: 5; ry: 5; }
  .entity-weak-inner { fill: none; stroke: #15803D; stroke-width: 1.5; rx: 3; ry: 3; }
  .entity-subclass { fill: #ECFDF5; stroke: #059669; stroke-width: 2; rx: 4; ry: 4; }
  .entity-text { font-size: 15px; font-weight: 700; fill: #064E3B; text-anchor: middle; dominant-baseline: middle; }
  .subclass-text { font-size: 13px; font-weight: 700; fill: #065F46; text-anchor: middle; dominant-baseline: middle; }

  /* Attribute Ovals */
  .attr-oval { fill: #F0FDF4; stroke: #22C55E; stroke-width: 1.6; }
  .attr-multivalued-outer { fill: #F0FDF4; stroke: #22C55E; stroke-width: 1.6; }
  .attr-multivalued-inner { fill: none; stroke: #22C55E; stroke-width: 1.2; }
  .attr-text { font-size: 11.5px; font-weight: 600; fill: #14532D; text-anchor: middle; dominant-baseline: middle; }
  .pk-text { text-decoration: underline; font-weight: 800; fill: #064E3B; }

  /* Relationship Diamonds */
  .rel-diamond { fill: #BBF7D0; stroke: #16A34A; stroke-width: 2; }
  .rel-weak-outer { fill: #BBF7D0; stroke: #16A34A; stroke-width: 2; }
  .rel-weak-inner { fill: none; stroke: #16A34A; stroke-width: 1.4; }
  .rel-text { font-size: 12.5px; font-weight: 700; fill: #14532D; text-anchor: middle; dominant-baseline: middle; }

  /* IsA Triangles */
  .isa-tri { fill: #FEF08A; stroke: #CA8A04; stroke-width: 2; }
  .isa-text { font-size: 12px; font-weight: 800; fill: #713F12; text-anchor: middle; dominant-baseline: middle; }

  /* Connector Lines */
  .line-conn { stroke: #374151; stroke-width: 1.5; stroke-linecap: round; }
  .line-attr { stroke: #6B7280; stroke-width: 1.1; stroke-linecap: round; }
  .line-ident { stroke: #15803D; stroke-width: 2.2; }
  
  /* Cardinality Labels */
  .card-text { font-size: 13px; font-weight: 800; fill: #1E293B; text-anchor: middle; background: white; }
  
  /* Border Frame */
  .frame-border { fill: none; stroke: #991B1B; stroke-width: 4; }
</style>
</head>
<body>

<svg width="2400" height="1650" viewBox="0 0 2400 1650" xmlns="http://www.w3.org/2000/svg">

  <!-- Outer Decorative Border Frame matching sample image -->
  <rect x="15" y="15" width="2370" height="1620" class="frame-border" rx="6" ry="6"/>

  <!-- Diagram Title Header -->
  <text x="1200" y="55" class="title-text">URBAN EMERGENCY RESPONSE & RESOURCE ALLOCATION SYSTEM</text>
  <text x="1200" y="85" class="subtitle-text">Enhanced Entity-Relationship (EER) Conceptual Schema with Chen Standard Notations &bull; DBMS Lab (24B15CS213) &bull; JIIT Noida-62</text>

  <!-- ===================================================================== -->
  <!-- 1. PATIENT ENTITY & ATTRIBUTES (Top Left) -->
  <!-- ===================================================================== -->
  <!-- Entity Box: Patient -->
  <g id="entity-patient">
    <!-- Lines to Attributes -->
    <line x1="260" y1="230" x2="130" y2="150" class="line-attr"/>
    <line x1="260" y1="230" x2="200" y2="120" class="line-attr"/>
    <line x1="260" y1="230" x2="280" y2="110" class="line-attr"/>
    <line x1="260" y1="230" x2="360" y2="120" class="line-attr"/>
    <line x1="260" y1="230" x2="430" y2="150" class="line-attr"/>
    <line x1="260" y1="230" x2="120" y2="240" class="line-attr"/>
    <line x1="260" y1="230" x2="130" y2="310" class="line-attr"/>

    <!-- Patient Entity Box -->
    <rect x="200" y="210" width="120" height="50" class="entity-rect"/>
    <text x="260" y="235" class="entity-text">Patient</text>

    <!-- Attributes -->
    <!-- P-ID (PK) -->
    <ellipse cx="130" cy="150" rx="45" ry="20" class="attr-oval"/>
    <text x="130" y="150" class="attr-text pk-text">P-ID</text>

    <!-- Name -->
    <ellipse cx="200" cy="120" rx="40" ry="18" class="attr-oval"/>
    <text x="200" y="120" class="attr-text">Name</text>

    <!-- Age -->
    <ellipse cx="280" cy="110" rx="35" ry="18" class="attr-oval"/>
    <text x="280" y="110" class="attr-text">Age</text>

    <!-- Gender -->
    <ellipse cx="360" cy="120" rx="38" ry="18" class="attr-oval"/>
    <text x="360" y="120" class="attr-text">Gender</text>

    <!-- Blood-Group -->
    <ellipse cx="430" cy="150" rx="45" ry="18" class="attr-oval"/>
    <text x="430" y="150" class="attr-text">Blood-Grp</text>

    <!-- Contact Phone (Multivalued - Double Oval) -->
    <ellipse cx="120" cy="240" rx="48" ry="22" class="attr-multivalued-outer"/>
    <ellipse cx="120" cy="240" rx="42" ry="17" class="attr-multivalued-inner"/>
    <text x="120" y="240" class="attr-text">Phone-No</text>

    <!-- Triage Notes -->
    <ellipse cx="130" cy="310" rx="52" ry="18" class="attr-oval"/>
    <text x="130" y="310" class="attr-text">Triage-Notes</text>
  </g>

  <!-- ===================================================================== -->
  <!-- 2. EMERGENCY ENTITY & RELATIONSHIP WITH PATIENT -->
  <!-- ===================================================================== -->
  <!-- Relationship: Involves (Patient to Emergency) -->
  <line x1="320" y1="235" x2="480" y2="235" class="line-conn"/>
  <polygon points="530,205 580,235 530,265 480,235" class="rel-diamond"/>
  <text x="530" y="235" class="rel-text">Involves</text>
  <line x1="580" y1="235" x2="740" y2="235" class="line-conn"/>
  <text x="340" y="225" class="card-text">1</text>
  <text x="720" y="225" class="card-text">N</text>

  <!-- Entity Box: Emergency -->
  <g id="entity-emergency">
    <!-- Attributes for Emergency -->
    <line x1="800" y1="235" x2="740" y2="140" class="line-attr"/>
    <line x1="800" y1="235" x2="810" y2="130" class="line-attr"/>
    <line x1="800" y1="235" x2="880" y2="140" class="line-attr"/>
    <line x1="800" y1="235" x2="940" y2="180" class="line-attr"/>

    <rect x="740" y="210" width="130" height="55" class="entity-rect"/>
    <text x="805" y="238" class="entity-text">Emergency</text>

    <!-- Emg-ID (PK) -->
    <ellipse cx="740" cy="140" rx="45" ry="19" class="attr-oval"/>
    <text x="740" y="140" class="attr-text pk-text">Emg-ID</text>

    <!-- Severity -->
    <ellipse cx="810" cy="130" rx="40" ry="18" class="attr-oval"/>
    <text x="810" y="130" class="attr-text">Severity</text>

    <!-- Status -->
    <ellipse cx="880" cy="140" rx="40" ry="18" class="attr-oval"/>
    <text x="880" y="140" class="attr-text">Status</text>

    <!-- Time -->
    <ellipse cx="940" cy="180" rx="38" ry="18" class="attr-oval"/>
    <text x="940" y="180" class="attr-text">Call-Time</text>
  </g>

  <!-- ===================================================================== -->
  <!-- 3. EMERGENCY TYPE & LOCATION RELATIONS TO EMERGENCY -->
  <!-- ===================================================================== -->
  <!-- Emergency_Type Entity (Above Emergency) -->
  <g id="entity-type">
    <line x1="805" y1="210" x2="805" y2="330" class="line-conn"/>
    
    <!-- Relationship: Classifies (Between Type and Emergency) -->
    <!-- Positioned below Emergency for clean layout -->
    <polygon points="805,330 850,360 805,390 760,360" class="rel-diamond"/>
    <text x="805" y="360" class="rel-text">Classifies</text>
    <line x1="805" y1="390" x2="805" y2="470" class="line-conn"/>
    <text x="825" y="280" class="card-text">N</text>
    <text x="825" y="450" class="card-text">1</text>

    <!-- Emergency_Type Entity Box -->
    <rect x="730" y="470" width="150" height="50" class="entity-rect"/>
    <text x="805" y="495" class="entity-text">Emergency_Type</text>

    <!-- Attributes -->
    <line x1="805" y1="520" x2="730" y2="590" class="line-attr"/>
    <line x1="805" y1="520" x2="805" y2="600" class="line-attr"/>
    <line x1="805" y1="520" x2="880" y2="590" class="line-attr"/>

    <ellipse cx="730" cy="590" rx="45" ry="19" class="attr-oval"/>
    <text x="730" y="590" class="attr-text pk-text">Type-ID</text>

    <ellipse cx="805" cy="600" rx="45" ry="18" class="attr-oval"/>
    <text x="805" y="600" class="attr-text">Category</text>

    <ellipse cx="880" cy="590" rx="48" ry="18" class="attr-oval"/>
    <text x="880" y="590" class="attr-text">Priority-Rank</text>
  </g>

  <!-- Location Entity (Far Right) & Relationship: Occurs_At -->
  <g id="entity-location">
    <line x1="870" y1="235" x2="1040" y2="235" class="line-conn"/>
    <!-- Occurs_At Diamond -->
    <polygon points="1090,205 1145,235 1090,265 1035,235" class="rel-diamond"/>
    <text x="1090" y="235" class="rel-text">Occurs_At</text>
    <line x1="1145" y1="235" x2="1310" y2="235" class="line-conn"/>
    <text x="890" y="225" class="card-text">N</text>
    <text x="1290" y="225" class="card-text">1</text>

    <!-- Location Entity Box -->
    <rect x="1310" y="210" width="120" height="50" class="entity-rect"/>
    <text x="1370" y="235" class="entity-text">Location</text>

    <!-- Attributes for Location -->
    <line x1="1370" y1="210" x2="1310" y2="130" class="line-attr"/>
    <line x1="1370" y1="210" x2="1430" y2="130" class="line-attr"/>

    <!-- Loc-ID (PK) -->
    <ellipse cx="1310" cy="130" rx="45" ry="19" class="attr-oval"/>
    <text x="1310" y="130" class="attr-text pk-text">Loc-ID</text>

    <!-- Composite Address Attribute (branching) -->
    <ellipse cx="1430" cy="130" rx="45" ry="19" class="attr-oval"/>
    <text x="1430" y="130" class="attr-text">Address</text>

    <!-- Sub-attributes of Address -->
    <line x1="1430" y1="110" x2="1370" y2="60" class="line-attr"/>
    <line x1="1430" y1="110" x2="1440" y2="55" class="line-attr"/>
    <line x1="1430" y1="110" x2="1510" y2="60" class="line-attr"/>

    <ellipse cx="1370" cy="60" rx="35" ry="16" class="attr-oval"/>
    <text x="1370" y="60" class="attr-text">Line</text>

    <ellipse cx="1440" cy="55" rx="35" ry="16" class="attr-oval"/>
    <text x="1440" y="55" class="attr-text">Zone</text>

    <ellipse cx="1510" cy="60" rx="38" ry="16" class="attr-oval"/>
    <text x="1510" y="60" class="attr-text">Pin-Code</text>
  </g>

  <!-- ===================================================================== -->
  <!-- 4. TERNARY RELATIONSHIP: RESOURCE_ALLOCATION (Center Center) -->
  <!-- ===================================================================== -->
  <!-- Connects Emergency, Ambulance, and Hospital -->
  <g id="ternary-allocation">
    <!-- Lines from Emergency, Ambulance, and Hospital to Resource_Allocation -->
    <line x1="770" y1="265" x2="520" y2="650" class="line-conn"/>
    
    <!-- Ternary Diamond: Resource_Allocation -->
    <polygon points="520,610 600,655 520,700 440,655" class="rel-diamond" style="fill:#A7F3D0; stroke:#059669; stroke-width:2.5;"/>
    <text x="520" y="650" class="rel-text" style="font-size:12px; font-weight:800;">Resource</text>
    <text x="520" y="665" class="rel-text" style="font-size:12px; font-weight:800;">Allocation</text>

    <!-- Cardinality Labels for Ternary -->
    <text x="680" y="420" class="card-text">N (Request)</text>
    <text x="410" y="780" class="card-text">1 (Ambulance)</text>
    <text x="820" y="710" class="card-text">1 (Hospital)</text>

    <!-- Attributes on the Ternary Relationship -->
    <line x1="440" y1="655" x2="310" y2="620" class="line-attr"/>
    <line x1="440" y1="655" x2="310" y2="670" class="line-attr"/>
    <line x1="440" y1="655" x2="330" y2="720" class="line-attr"/>

    <!-- Alloc-ID (PK) -->
    <ellipse cx="310" cy="620" rx="48" ry="19" class="attr-oval"/>
    <text x="310" y="620" class="attr-text pk-text">Alloc-ID</text>

    <ellipse cx="310" cy="670" rx="50" ry="18" class="attr-oval"/>
    <text x="310" y="670" class="attr-text">Dispatch-Time</text>

    <ellipse cx="330" cy="720" rx="42" ry="18" class="attr-oval"/>
    <text x="330" y="720" class="attr-text">Alloc-Status</text>
  </g>

  <!-- ===================================================================== -->
  <!-- 5. AMBULANCE ENTITY & EER SPECIALIZATION (Bottom Left) -->
  <!-- ===================================================================== -->
  <g id="entity-ambulance">
    <!-- Connecting Line from Ternary to Ambulance -->
    <line x1="480" y1="680" x2="380" y2="820" class="line-conn"/>

    <!-- Ambulance Entity Box -->
    <rect x="310" y="820" width="130" height="50" class="entity-rect"/>
    <text x="375" y="845" class="entity-text">Ambulance</text>

    <!-- Attributes -->
    <line x1="310" y1="845" x2="200" y2="800" class="line-attr"/>
    <line x1="310" y1="845" x2="190" y2="850" class="line-attr"/>
    <line x1="310" y1="845" x2="210" y2="900" class="line-attr"/>

    <!-- Amb-ID (PK) -->
    <ellipse cx="200" cy="800" rx="48" ry="19" class="attr-oval"/>
    <text x="200" y="800" class="attr-text pk-text">Amb-ID</text>

    <!-- Vehicle-No (Candidate Key - Underlined) -->
    <ellipse cx="190" cy="850" rx="52" ry="19" class="attr-oval"/>
    <text x="190" y="850" class="attr-text pk-text">Vehicle-No</text>

    <!-- Base-Station -->
    <ellipse cx="210" cy="900" rx="50" ry="18" class="attr-oval"/>
    <text x="210" y="900" class="attr-text">Base-Station</text>

    <!-- EER SPECIALIZATION (IsA Triangle) -->
    <line x1="375" y1="870" x2="375" y2="940" class="line-conn"/>
    <polygon points="350,940 400,940 375,980" class="isa-tri"/>
    <text x="375" y="955" class="isa-text">IsA</text>

    <!-- Branches to Subclasses -->
    <line x1="375" y1="980" x2="290" y2="1030" class="line-conn"/>
    <line x1="375" y1="980" x2="460" y2="1030" class="line-conn"/>

    <!-- Subclass 1: ALS Ambulance -->
    <rect x="220" y="1030" width="130" height="45" class="entity-subclass"/>
    <text x="285" y="1053" class="subclass-text">ALS_Ambulance</text>

    <!-- Subclass 2: BLS Ambulance -->
    <rect x="400" y="1030" width="130" height="45" class="entity-subclass"/>
    <text x="465" y="1053" class="subclass-text">BLS_Ambulance</text>

    <!-- Subclass Attributes -->
    <line x1="250" y1="1075" x2="210" y2="1120" class="line-attr"/>
    <ellipse cx="210" cy="1120" rx="55" ry="18" class="attr-oval"/>
    <text x="210" y="1120" class="attr-text">Ventilator-Equip</text>

    <line x1="500" y1="1075" x2="540" y2="1120" class="line-attr"/>
    <ellipse cx="540" cy="1120" rx="45" ry="18" class="attr-oval"/>
    <text x="540" y="1120" class="attr-text">AED-Kit</text>
  </g>

  <!-- ===================================================================== -->
  <!-- 6. EQUIPMENT WEAK ENTITY (Connected to Ambulance) -->
  <!-- ===================================================================== -->
  <g id="entity-equipment">
    <!-- Identifying Relationship: Carries (Double Diamond) -->
    <line x1="440" y1="845" x2="560" y2="845" class="line-ident"/>
    <polygon points="610,815 660,845 610,875 560,845" class="rel-weak-outer"/>
    <polygon points="610,821 650,845 610,869 570,845" class="rel-weak-inner"/>
    <text x="610" y="845" class="rel-text">Carries</text>
    <line x1="660" y1="845" x2="770" y2="845" class="line-ident"/>
    <text x="460" y="835" class="card-text">1</text>
    <text x="750" y="835" class="card-text">N</text>

    <!-- Weak Entity Box: Equipment (Double Rectangle) -->
    <rect x="770" y="820" width="120" height="50" class="entity-weak-outer"/>
    <rect x="775" y="825" width="110" height="40" class="entity-weak-inner"/>
    <text x="830" y="845" class="entity-text">Equipment</text>

    <!-- Attributes -->
    <line x1="830" y1="870" x2="780" y2="940" class="line-attr"/>
    <line x1="830" y1="870" x2="880" y2="940" class="line-attr"/>
    <line x1="830" y1="870" x2="930" y2="890" class="line-attr"/>

    <!-- Equip-ID (PK) -->
    <ellipse cx="780" cy="940" rx="48" ry="19" class="attr-oval"/>
    <text x="780" y="940" class="attr-text pk-text">Equip-ID</text>

    <!-- Name -->
    <ellipse cx="880" cy="940" rx="40" ry="18" class="attr-oval"/>
    <text x="880" y="940" class="attr-text">Name</text>

    <!-- Is-Functional -->
    <ellipse cx="930" cy="890" rx="45" ry="18" class="attr-oval"/>
    <text x="930" y="890" class="attr-text">Functional</text>
  </g>

  <!-- ===================================================================== -->
  <!-- 7. HOSPITAL ENTITY & HIERARCHY (Center Right) -->
  <!-- ===================================================================== -->
  <g id="entity-hospital">
    <!-- Connecting Line from Ternary to Hospital -->
    <line x1="570" y1="670" x2="1140" y2="670" class="line-conn"/>

    <!-- Hospital Entity Box -->
    <rect x="1140" y="645" width="120" height="50" class="entity-rect"/>
    <text x="1200" y="670" class="entity-text">Hospital</text>

    <!-- Hospital Attributes -->
    <line x1="1200" y1="645" x2="1150" y2="570" class="line-attr"/>
    <line x1="1200" y1="645" x2="1240" y2="570" class="line-attr"/>
    <line x1="1200" y1="645" x2="1320" y2="610" class="line-attr"/>

    <!-- Hosp-ID (PK) -->
    <ellipse cx="1150" cy="570" rx="48" ry="19" class="attr-oval"/>
    <text x="1150" y="570" class="attr-text pk-text">Hosp-ID</text>

    <!-- Name -->
    <ellipse cx="1240" cy="570" rx="42" ry="18" class="attr-oval"/>
    <text x="1240" y="570" class="attr-text">Name</text>

    <!-- Emergency Level -->
    <ellipse cx="1320" cy="610" rx="55" ry="18" class="attr-oval"/>
    <text x="1320" y="610" class="attr-text">Trauma-Level</text>

    <!-- Relationship: Located_At (Hospital to Location) -->
    <line x1="1220" y1="645" x2="1340" y2="350" class="line-conn"/>
    <polygon points="1340,320 1390,350 1340,380 1290,350" class="rel-diamond"/>
    <text x="1340" y="350" class="rel-text">Located_At</text>
    <line x1="1340" y1="320" x2="1360" y2="260" class="line-conn"/>
    <text x="1240" y="620" class="card-text">N</text>
    <text x="1380" y="280" class="card-text">1</text>

    <!-- Relationship: Houses (Hospital to Department) -->
    <line x1="1200" y1="695" x2="1200" y2="800" class="line-conn"/>
    <polygon points="1200,800 1250,830 1200,860 1150,830" class="rel-diamond"/>
    <text x="1200" y="830" class="rel-text">Houses</text>
    <line x1="1200" y1="860" x2="1200" y2="950" class="line-conn"/>
    <text x="1220" y="730" class="card-text">1</text>
    <text x="1220" y="930" class="card-text">N</text>
  </g>

  <!-- ===================================================================== -->
  <!-- 8. DEPARTMENT ENTITY (Below Hospital) -->
  <!-- ===================================================================== -->
  <g id="entity-department">
    <rect x="1130" y="950" width="140" height="50" class="entity-rect"/>
    <text x="1200" y="975" class="entity-text">Department</text>

    <!-- Attributes -->
    <line x1="1130" y1="975" x2="1030" y2="940" class="line-attr"/>
    <line x1="1130" y1="975" x2="1030" y2="1000" class="line-attr"/>

    <!-- Dept-ID (PK) -->
    <ellipse cx="1030" cy="940" rx="48" ry="19" class="attr-oval"/>
    <text x="1030" y="940" class="attr-text pk-text">Dept-ID</text>

    <ellipse cx="1030" cy="1000" rx="45" ry="18" class="attr-oval"/>
    <text x="1030" y="1000" class="attr-text">Capacity</text>

    <!-- Relationship: Contains (Department to Bed) -->
    <line x1="1200" y1="1000" x2="1200" y2="1100" class="line-conn"/>
    <polygon points="1200,1100 1250,1130 1200,1160 1150,1130" class="rel-diamond"/>
    <text x="1200" y="1130" class="rel-text">Contains</text>
    <line x1="1200" y1="1160" x2="1200" y2="1250" class="line-conn"/>
    <text x="1220" y="1030" class="card-text">1</text>
    <text x="1220" y="1230" class="card-text">N</text>
  </g>

  <!-- ===================================================================== -->
  <!-- 9. BED ENTITY & EER SPECIALIZATION (Bottom Right Center) -->
  <!-- ===================================================================== -->
  <g id="entity-bed">
    <rect x="1140" y="1250" width="120" height="50" class="entity-rect"/>
    <text x="1200" y="1275" class="entity-text">Bed</text>

    <!-- Attributes -->
    <line x1="1140" y1="1275" x2="1030" y2="1250" class="line-attr"/>
    <line x1="1140" y1="1275" x2="1040" y2="1310" class="line-attr"/>

    <!-- Bed-ID (PK) -->
    <ellipse cx="1030" cy="1250" rx="45" ry="19" class="attr-oval"/>
    <text x="1030" y="1250" class="attr-text pk-text">Bed-ID</text>

    <ellipse cx="1040" cy="1310" rx="48" ry="18" class="attr-oval"/>
    <text x="1040" y="1310" class="attr-text">Is-Occupied</text>

    <!-- EER SPECIALIZATION (IsA Triangle for Bed) -->
    <line x1="1200" y1="1300" x2="1200" y2="1370" class="line-conn"/>
    <polygon points="1175,1370 1225,1370 1200,1410" class="isa-tri"/>
    <text x="1200" y="1385" class="isa-text">IsA</text>

    <!-- Branches to Subclasses -->
    <line x1="1200" y1="1410" x2="1110" y2="1470" class="line-conn"/>
    <line x1="1200" y1="1410" x2="1290" y2="1470" class="line-conn"/>

    <!-- Subclass 1: ICU Bed -->
    <rect x="1060" y="1470" width="100" height="40" class="entity-subclass"/>
    <text x="1110" y="1490" class="subclass-text">ICU_Bed</text>

    <!-- Subclass 2: General Bed -->
    <rect x="1240" y="1470" width="110" height="40" class="entity-subclass"/>
    <text x="1295" y="1490" class="subclass-text">General_Bed</text>
  </g>

  <!-- ===================================================================== -->
  <!-- 10. STAFF ENTITY & EER SPECIALIZATION (Far Right Bottom) -->
  <!-- ===================================================================== -->
  <g id="entity-staff">
    <!-- Hospital Employs Staff -->
    <line x1="1260" y1="670" x2="1700" y2="670" class="line-conn"/>
    <polygon points="1700,640 1750,670 1700,700 1650,670" class="rel-diamond"/>
    <text x="1700" y="670" class="rel-text">Employs</text>
    <line x1="1750" y1="670" x2="1880" y2="670" class="line-conn"/>
    <text x="1300" y="660" class="card-text">1</text>
    <text x="1860" y="660" class="card-text">N</text>

    <!-- Staff Entity Box -->
    <rect x="1880" y="645" width="120" height="50" class="entity-rect"/>
    <text x="1940" y="670" class="entity-text">Staff</text>

    <!-- Attributes -->
    <line x1="1940" y1="645" x2="1870" y2="570" class="line-attr"/>
    <line x1="1940" y1="645" x2="1960" y2="570" class="line-attr"/>
    <line x1="1940" y1="645" x2="2040" y2="590" class="line-attr"/>

    <!-- Staff-ID (PK) -->
    <ellipse cx="1870" cy="570" rx="48" ry="19" class="attr-oval"/>
    <text x="1870" y="570" class="attr-text pk-text">Staff-ID</text>

    <ellipse cx="1960" cy="570" rx="40" ry="18" class="attr-oval"/>
    <text x="1960" y="570" class="attr-text">Name</text>

    <ellipse cx="2040" cy="590" rx="48" ry="18" class="attr-oval"/>
    <text x="2040" y="590" class="attr-text">License-No</text>

    <!-- EER SPECIALIZATION (IsA Triangle for Staff - matches Employee in user sample) -->
    <line x1="1940" y1="695" x2="1940" y2="760" class="line-conn"/>
    <polygon points="1915,760 1965,760 1940,800" class="isa-tri"/>
    <text x="1940" y="775" class="isa-text">IsA</text>

    <!-- 3 Subclasses: Doctor, Paramedic, Driver -->
    <line x1="1940" y1="800" x2="1810" y2="860" class="line-conn"/>
    <line x1="1940" y1="800" x2="1940" y2="860" class="line-conn"/>
    <line x1="1940" y1="800" x2="2070" y2="860" class="line-conn"/>

    <!-- Doctor -->
    <rect x="1760" y="860" width="100" height="42" class="entity-subclass"/>
    <text x="1810" y="881" class="subclass-text">Doctor</text>

    <!-- Paramedic -->
    <rect x="1885" y="860" width="110" height="42" class="entity-subclass"/>
    <text x="1940" y="881" class="subclass-text">Paramedic</text>

    <!-- Driver -->
    <rect x="2020" y="860" width="100" height="42" class="entity-subclass"/>
    <text x="2070" y="881" class="subclass-text">Driver</text>

    <!-- Subclass Attributes -->
    <line x1="1810" y1="902" x2="1810" y2="950" class="line-attr"/>
    <ellipse cx="1810" cy="950" rx="45" ry="18" class="attr-oval"/>
    <text x="1810" y="950" class="attr-text">Specialty</text>

    <line x1="1940" y1="902" x2="1940" y2="950" class="line-attr"/>
    <ellipse cx="1940" cy="950" rx="50" ry="18" class="attr-oval"/>
    <text x="1940" y="950" class="attr-text">Cert-Level</text>

    <line x1="2070" y1="902" x2="2070" y2="950" class="line-attr"/>
    <ellipse cx="2070" cy="950" rx="45" ry="18" class="attr-oval"/>
    <text x="2070" y="950" class="attr-text">DL-Class</text>

    <!-- Ambulance Crews Paramedic & Driver -->
    <path d="M 440 850 Q 1100 1020 1885 880" fill="none" class="line-conn" stroke-dasharray="5,5"/>
    <text x="1450" y="950" class="card-text" style="fill:#065F46;">Crews (Ambulance Staffing)</text>
  </g>

  <!-- ===================================================================== -->
  <!-- 11. EMERGENCY STATUS HISTORY (Weak Audit Entity - Top Center Right) -->
  <!-- ===================================================================== -->
  <g id="entity-history">
    <!-- Identifying Relationship: Logs (Double Diamond) -->
    <line x1="805" y1="265" x2="805" y2="290" class="line-ident"/>
    <line x1="870" y1="250" x2="980" y2="350" class="line-ident"/>
    
    <polygon points="1030,320 1080,350 1030,380 980,350" class="rel-weak-outer"/>
    <polygon points="1030,326 1070,350 1030,374 990,350" class="rel-weak-inner"/>
    <text x="1030" y="350" class="rel-text">Logs</text>
    <line x1="1080" y1="350" x2="1180" y2="430" class="line-ident"/>
    <text x="910" y="290" class="card-text">1</text>
    <text x="1140" y="410" class="card-text">N</text>

    <!-- Weak Entity Box: Status_History (Double Rectangle) -->
    <rect x="1170" y="420" width="140" height="50" class="entity-weak-outer"/>
    <rect x="1175" y="425" width="130" height="40" class="entity-weak-inner"/>
    <text x="1240" y="445" class="entity-text">Status_History</text>

    <!-- Attributes -->
    <line x1="1240" y1="470" x2="1190" y2="530" class="line-attr"/>
    <line x1="1240" y1="470" x2="1290" y2="530" class="line-attr"/>

    <!-- Hist-ID (PK) -->
    <ellipse cx="1190" cy="530" rx="48" ry="19" class="attr-oval"/>
    <text x="1190" y="530" class="attr-text pk-text">Hist-ID</text>

    <ellipse cx="1290" cy="530" rx="45" ry="18" class="attr-oval"/>
    <text x="1290" y="530" class="attr-text">Status-State</text>
  </g>

  <!-- ===================================================================== -->
  <!-- LEGEND BOX (Bottom Left Corner) -->
  <!-- ===================================================================== -->
  <g id="legend" transform="translate(60, 1340)">
    <rect x="0" y="0" width="620" height="240" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="2" rx="8" ry="8"/>
    <text x="310" y="28" font-size="14px" font-weight="800" fill="#1E293B" text-anchor="middle">CHEN &amp; EER STANDARD NOTATION LEGEND</text>

    <!-- Legend items -->
    <rect x="30" y="50" width="60" height="26" class="entity-rect"/>
    <text x="100" y="67" font-size="12px" font-weight="600" fill="#334155">Regular Entity Set (Strong)</text>

    <rect x="30" y="90" width="60" height="26" class="entity-weak-outer"/>
    <rect x="33" y="93" width="54" height="20" class="entity-weak-inner"/>
    <text x="100" y="107" font-size="12px" font-weight="600" fill="#334155">Weak Entity Set (Double Rect)</text>

    <polygon points="50,135 70,150 50,165 30,150" class="rel-diamond"/>
    <text x="100" y="154" font-size="12px" font-weight="600" fill="#334155">Relationship Set (Diamond)</text>

    <polygon points="50,185 70,200 50,215 30,200" class="rel-weak-outer"/>
    <polygon points="50,188 66,200 50,212 34,200" class="rel-weak-inner"/>
    <text x="100" y="204" font-size="12px" font-weight="600" fill="#334155">Identifying Relationship (Weak)</text>

    <!-- Column 2 of legend -->
    <ellipse cx="360" cy="63" rx="30" ry="14" class="attr-oval"/>
    <text x="360" y="63" font-size="10px" font-weight="800" fill="#064E3B" class="pk-text" text-anchor="middle" dominant-baseline="middle">Key</text>
    <text x="405" y="67" font-size="12px" font-weight="600" fill="#334155">Primary Key Attribute (Underlined)</text>

    <ellipse cx="360" cy="103" rx="30" ry="14" class="attr-multivalued-outer"/>
    <ellipse cx="360" cy="103" rx="26" ry="11" class="attr-multivalued-inner"/>
    <text x="405" y="107" font-size="12px" font-weight="600" fill="#334155">Multivalued Attribute (Double Oval)</text>

    <polygon points="345,140 375,140 360,165" class="isa-tri"/>
    <text x="360" y="150" font-size="9px" font-weight="800" fill="#713F12" text-anchor="middle">IsA</text>
    <text x="405" y="154" font-size="12px" font-weight="600" fill="#334155">EER Specialization / Generalization</text>

    <text x="360" y="204" font-size="14px" font-weight="800" fill="#1E293B" text-anchor="middle">1 : N : M</text>
    <text x="405" y="204" font-size="12px" font-weight="600" fill="#334155">Structural Cardinality Ratios</text>
  </g>

</svg>

</body>
</html>
"""

# =============================================================================
# 2. GENERATE FLOWCHART HTML (FIGURE 2 OPERATIONAL LIFECYCLE)
# =============================================================================
def generate_flowchart_html():
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>System Flowchart - Urban Emergency Response System</title>
<style>
  body {
    margin: 0;
    padding: 20px;
    background: #ffffff;
    font-family: 'Segoe UI', Arial, sans-serif;
  }
  svg {
    display: block;
    margin: 0 auto;
    background: #ffffff;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    border-radius: 8px;
  }
  .title-text { font-size: 24px; font-weight: 800; fill: #0F172A; text-anchor: middle; }
  .subtitle-text { font-size: 13px; font-weight: 600; fill: #64748B; text-anchor: middle; }
  
  /* Phase Header Boxes */
  .phase-header-1 { fill: #EFF6FF; stroke: #3B82F6; stroke-width: 2; rx: 6; ry: 6; }
  .phase-header-2 { fill: #ECFDF5; stroke: #10B981; stroke-width: 2; rx: 6; ry: 6; }
  .phase-title { font-size: 15px; font-weight: 800; text-anchor: middle; dominant-baseline: middle; }
  
  /* Flowchart Process Boxes */
  .proc-box { fill: #FFFFFF; stroke: #1E293B; stroke-width: 2; rx: 4; ry: 4; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.05)); }
  .proc-title { font-size: 13.5px; font-weight: 800; fill: #0F172A; text-anchor: middle; }
  .proc-desc { font-size: 11.5px; font-weight: 500; fill: #475569; text-anchor: middle; }
  
  /* Decision Diamonds */
  .decision-diamond { fill: #FEF3C7; stroke: #D97706; stroke-width: 2.2; }
  .decision-text { font-size: 12.5px; font-weight: 800; fill: #78350F; text-anchor: middle; dominant-baseline: middle; }

  /* Start/End Pills */
  .terminal-start { fill: #10B981; stroke: #047857; stroke-width: 2.5; rx: 25; ry: 25; }
  .terminal-end { fill: #EF4444; stroke: #B91C1C; stroke-width: 2.5; rx: 25; ry: 25; }
  .terminal-text { font-size: 14px; font-weight: 800; fill: #FFFFFF; text-anchor: middle; dominant-baseline: middle; }
  
  /* Connectors */
  .connector-circle { fill: #6366F1; stroke: #4338CA; stroke-width: 2; }
  .connector-text { font-size: 14px; font-weight: 800; fill: #FFFFFF; text-anchor: middle; dominant-baseline: middle; }
  
  /* Arrow Lines */
  .flow-arrow { stroke: #1E293B; stroke-width: 2; fill: none; marker-end: url(#arrowhead); }
  .flow-arrow-dashed { stroke: #DC2626; stroke-width: 2; stroke-dasharray: 5,4; fill: none; marker-end: url(#arrowhead-red); }
  
  /* Branch Labels */
  .branch-yes { font-size: 12px; font-weight: 800; fill: #059669; }
  .branch-no { font-size: 12px; font-weight: 800; fill: #DC2626; }
</style>
</head>
<body>

<svg width="1700" height="2050" viewBox="0 0 1700 2050" xmlns="http://www.w3.org/2000/svg">

  <defs>
    <!-- Arrowhead definitions -->
    <marker id="arrowhead" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto">
      <polygon points="0 0, 9 3.5, 0 7" fill="#1E293B" />
    </marker>
    <marker id="arrowhead-red" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto">
      <polygon points="0 0, 9 3.5, 0 7" fill="#DC2626" />
    </marker>
  </defs>

  <!-- Title Block -->
  <text x="850" y="55" class="title-text">URBAN EMERGENCY RESPONSE & RESOURCE ALLOCATION SYSTEM</text>
  <text x="850" y="85" class="subtitle-text">Figure 2: End-to-End System Operational Lifecycle Flowchart (Intake, ACID Resource Allocation, Triggers & Reporting)</text>

  <!-- ===================================================================== -->
  <!-- PHASE I: INTAKE & VERIFICATION (Left Column) -->
  <!-- ===================================================================== -->
  <!-- Phase I Boundary Container -->
  <rect x="80" y="120" width="720" height="1820" fill="#F8FAFC" stroke="#94A3B8" stroke-width="2" stroke-dasharray="8,6" rx="10" ry="10"/>
  
  <!-- Phase Header -->
  <rect x="180" y="145" width="520" height="45" class="phase-header-1"/>
  <text x="440" y="172" class="phase-title" fill="#1E40AF">PHASE I: INTAKE &amp; CLINICAL VERIFICATION</text>

  <!-- 1. START Terminal -->
  <rect x="360" y="240" width="160" height="50" class="terminal-start"/>
  <text x="440" y="268" class="terminal-text">START</text>

  <!-- Arrow to Step 1 -->
  <line x1="440" y1="290" x2="440" y2="360" class="flow-arrow"/>

  <!-- Step 1: Emergency Incident Reported -->
  <rect x="230" y="360" width="420" height="80" class="proc-box"/>
  <text x="440" y="392" class="proc-title">1. Emergency Incident Reported</text>
  <text x="440" y="415" class="proc-desc">Citizen emergency intake via 112 helpline / automated caller interface</text>

  <!-- Arrow to Step 2 -->
  <line x1="440" y1="440" x2="440" y2="510" class="flow-arrow"/>

  <!-- Step 2: Record Emergency Details -->
  <rect x="230" y="510" width="420" height="85" class="proc-box"/>
  <text x="440" y="542" class="proc-title">2. Record Emergency Details</text>
  <text x="440" y="565" class="proc-desc">Atomically insert victim demographics, phone, location into</text>
  <text x="440" y="582" class="proc-desc font-mono" style="font-weight:700; fill:#1E40AF;">PATIENT, EMERGENCY, and LOCATION relations</text>

  <!-- Arrow to Step 3 -->
  <line x1="440" y1="595" x2="440" y2="670" class="flow-arrow"/>

  <!-- Step 3: Check Severity & Requirements -->
  <rect x="230" y="670" width="420" height="85" class="proc-box"/>
  <text x="440" y="702" class="proc-title">3. Check Severity &amp; Clinical Needs</text>
  <text x="440" y="725" class="proc-desc">Query EMERGENCY_TYPE (Severity 1–5, Priority Rank)</text>
  <text x="440" y="742" class="proc-desc">Determine vehicle apparatus requirement (BLS vs. ALS Ventilator)</text>

  <!-- Arrow to Decision 1 -->
  <line x1="440" y1="755" x2="440" y2="850" class="flow-arrow"/>

  <!-- Decision 1: Ambulance Available? -->
  <polygon points="440,850 590,920 440,990 290,920" class="decision-diamond"/>
  <text x="440" y="915" class="decision-text">Ambulance</text>
  <text x="440" y="935" class="decision-text">Available?</text>

  <!-- Decision 1 NO Branch: Loop/Retry -->
  <path d="M 590 920 L 730 920 L 730 870" class="flow-arrow-dashed"/>
  <text x="610" y="910" class="branch-no">NO</text>
  <rect x="650" y="810" width="130" height="60" fill="#FEE2E2" stroke="#DC2626" stroke-width="1.5" rx="4"/>
  <text x="715" y="835" font-size="11px" font-weight="800" fill="#991B1B" text-anchor="middle">Queue Call /</text>
  <text x="715" y="852" font-size="11px" font-weight="700" fill="#991B1B" text-anchor="middle">Fleet Escalation</text>
  <path d="M 715 810 L 715 712 L 650 712" class="flow-arrow-dashed"/>

  <!-- Decision 1 YES Branch: Down to Bed Check -->
  <line x1="440" y1="990" x2="440" y2="1080" class="flow-arrow"/>
  <text x="455" y="1030" class="branch-yes">YES (Vehicle Allocated)</text>

  <!-- Decision 2: Hospital Bed Available? -->
  <polygon points="440,1080 590,1150 440,1220 290,1150" class="decision-diamond"/>
  <text x="440" y="1145" class="decision-text">Hospital Bed</text>
  <text x="440" y="1165" class="decision-text">Available?</text>

  <!-- Decision 2 NO Branch: Alternative Bed / Escalation -->
  <path d="M 590 1150 L 730 1150 L 730 1100" class="flow-arrow-dashed"/>
  <text x="610" y="1140" class="branch-no">NO</text>
  <rect x="650" y="1040" width="130" height="60" fill="#FEE2E2" stroke="#DC2626" stroke-width="1.5" rx="4"/>
  <text x="715" y="1065" font-size="11px" font-weight="800" fill="#991B1B" text-anchor="middle">Query Secondary</text>
  <text x="715" y="1082" font-size="11px" font-weight="700" fill="#991B1B" text-anchor="middle">Trauma Center</text>
  <path d="M 715 1040 L 715 970 L 520 970" class="flow-arrow-dashed"/>

  <!-- Decision 2 YES Branch: Down to Connector A -->
  <line x1="440" y1="1220" x2="440" y2="1320" class="flow-arrow"/>
  <text x="455" y="1265" class="branch-yes">YES (Bed Vacant)</text>

  <!-- Connector (A) at bottom of Phase I -->
  <circle cx="440" cy="1350" r="28" class="connector-circle"/>
  <text x="440" y="1355" class="connector-text">A</text>

  <!-- ===================================================================== -->
  <!-- PHASE II: ALLOCATION & AUDIT (Right Column) -->
  <!-- ===================================================================== -->
  <!-- Phase II Boundary Container -->
  <rect x="880" y="120" width="740" height="1820" fill="#F0FDF4" stroke="#86EFAC" stroke-width="2" stroke-dasharray="8,6" rx="10" ry="10"/>

  <!-- Phase Header -->
  <rect x="990" y="145" width="520" height="45" class="phase-header-2"/>
  <text x="1250" y="172" class="phase-title" fill="#065F46">PHASE II: ATOMIC ALLOCATION &amp; AUDIT TRAIL</text>

  <!-- Connector (A) at top of Phase II -->
  <circle cx="1250" cy="250" r="28" class="connector-circle"/>
  <text x="1250" y="255" class="connector-text">A</text>

  <!-- Connecting dashed line across phases -->
  <path d="M 468 1350 L 840 1350 L 840 250 L 1222 250" fill="none" stroke="#6366F1" stroke-width="2.5" stroke-dasharray="6,5"/>
  <text x="850" y="235" font-size="12px" font-weight="800" fill="#4F46E5" text-anchor="middle">Phase Handoff (A)</text>

  <!-- Arrow to Step 4 -->
  <line x1="1250" y1="278" x2="1250" y2="350" class="flow-arrow"/>

  <!-- Step 4: Allocate Suitable Resources -->
  <rect x="1040" y="350" width="420" height="85" class="proc-box"/>
  <text x="1250" y="382" class="proc-title">4. Allocate Suitable Resources</text>
  <text x="1250" y="405" class="proc-desc">Pair verified ALS/BLS Ambulance with onboard life-support</text>
  <text x="1250" y="422" class="proc-desc">Reserve ICU or General Trauma Bed at eligible receiving hospital</text>

  <!-- Arrow to Step 5 -->
  <line x1="1250" y1="435" x2="1250" y2="510" class="flow-arrow"/>

  <!-- Step 5: Atomic SQL Transaction COMMIT -->
  <rect x="1040" y="510" width="420" height="95" class="proc-box" style="stroke:#059669; stroke-width:2.5; fill:#ECFDF5;"/>
  <text x="1250" y="542" class="proc-title" style="fill:#065F46;">5. Atomic SQL Transaction COMMIT</text>
  <text x="1250" y="565" class="proc-desc font-mono" style="font-weight:700; fill:#047857;">BEGIN IMMEDIATE TRANSACTION;</text>
  <text x="1250" y="582" class="proc-desc">SET Ambulance = 'Dispatched', Bed = Occupied, Insert ALLOCATION</text>
  <text x="1250" y="598" class="proc-desc font-mono" style="font-weight:700; fill:#047857;">COMMIT; (Guarantees ACID - Zero Race Conditions)</text>

  <!-- Arrow to Step 6 -->
  <line x1="1250" y1="605" x2="1250" y2="680" class="flow-arrow"/>

  <!-- Step 6: Dispatch Ambulance & Care -->
  <rect x="1040" y="680" width="420" height="85" class="proc-box"/>
  <text x="1250" y="712" class="proc-title">6. Dispatch Ambulance &amp; Clinical Care</text>
  <text x="1250" y="735" class="proc-desc">Update EMERGENCY status = 'In-Transit'</text>
  <text x="1250" y="752" class="proc-desc">Paramedics deploy telemetry and stabilize victim during transit</text>

  <!-- Arrow to Step 7 -->
  <line x1="1250" y1="765" x2="1250" y2="840" class="flow-arrow"/>

  <!-- Step 7: Hospital Handover & Triage -->
  <rect x="1040" y="840" width="420" height="85" class="proc-box"/>
  <text x="1250" y="872" class="proc-title">7. Hospital Handover &amp; Emergency Triage</text>
  <text x="1250" y="895" class="proc-desc">Patient admitted into reserved hospital bed</text>
  <text x="1250" y="912" class="proc-desc">Update RESOURCE_ALLOCATION arrival_time; response concluded</text>

  <!-- Arrow to Step 8 -->
  <line x1="1250" y1="925" x2="1250" y2="1000" class="flow-arrow"/>

  <!-- Step 8: Trigger Log Status & Free Units -->
  <rect x="1040" y="1000" width="420" height="95" class="proc-box" style="stroke:#DC2626; stroke-width:2.2; fill:#FEF2F2;"/>
  <text x="1250" y="1030" class="proc-title" style="fill:#991B1B;">8. Trigger: Log Status &amp; Free Units</text>
  <text x="1250" y="1052" class="proc-desc font-mono" style="font-weight:700; fill:#B91C1C;">AFTER UPDATE TRIGGER trg_emergency_status_update</text>
  <text x="1250" y="1070" class="proc-desc">Engine writes chronological audit into EMERGENCY_STATUS_HISTORY</text>
  <text x="1250" y="1086" class="proc-desc">Frees ambulance operational_status back to 'Available'</text>

  <!-- Arrow to Step 9 -->
  <line x1="1250" y1="1095" x2="1250" y2="1170" class="flow-arrow"/>

  <!-- Step 9: Generate Analytical Reports -->
  <rect x="1040" y="1170" width="420" height="85" class="proc-box"/>
  <text x="1250" y="1202" class="proc-title">9. Generate Analytical Reports &amp; KPIs</text>
  <text x="1250" y="1225" class="proc-desc">Execute SQL analytical views (vw_hospital_bed_occupancy,</text>
  <text x="1250" y="1242" class="proc-desc">vw_ambulance_fleet_status, vw_response_latency_analytics)</text>

  <!-- Arrow to END -->
  <line x1="1250" y1="1255" x2="1250" y2="1330" class="flow-arrow"/>

  <!-- END Terminal -->
  <rect x="1170" y="1330" width="160" height="50" class="terminal-end"/>
  <text x="1250" y="1358" class="terminal-text">END</text>

  <!-- Bottom Summary Banner -->
  <rect x="80" y="1850" width="1540" height="80" fill="#1E293B" rx="8" ry="8"/>
  <text x="850" y="1885" font-size="14px" font-weight="800" fill="#F8FAFC" text-anchor="middle">
    ACID TRANSACTION CONCURRENCY &bull; 3NF NORMALIZED RELATIONAL REPOSITORY &bull; AUTOMATED TRIGGER AUDITING
  </text>
  <text x="850" y="1910" font-size="12px" font-weight="600" fill="#94A3B8" text-anchor="middle">
    Designed for Department of CSE &amp; IT &bull; Jaypee Institute of Information Technology, Noida-62
  </text>

</svg>

</body>
</html>
"""

# =============================================================================
# 3. GENERATE EER-TO-RELATIONAL TABLE CONVERSION HTML (SECTION 7 SPEC)
# =============================================================================
def generate_relational_mapping_html():
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>EER-to-Relational Table Conversion - Urban Emergency Response System</title>
<style>
  body {
    margin: 0;
    padding: 20px;
    background: #ffffff;
    font-family: 'Segoe UI', Arial, sans-serif;
  }
  svg {
    display: block;
    margin: 0 auto;
    background: #ffffff;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    border-radius: 8px;
  }
  .title-text { font-size: 24px; font-weight: 800; fill: #0F172A; text-anchor: middle; }
  .subtitle-text { font-size: 13px; font-weight: 600; fill: #475569; text-anchor: middle; }
  
  /* Table Container */
  .tbl-box { fill: #FFFFFF; stroke: #0F172A; stroke-width: 2; rx: 6; ry: 6; }
  .tbl-header { fill: #1E293B; rx: 5; ry: 5; }
  .tbl-name { font-size: 13.5px; font-weight: 800; fill: #FFFFFF; text-anchor: middle; dominant-baseline: middle; font-family: monospace; }
  .tbl-badge { font-size: 10px; font-weight: 700; fill: #94A3B8; text-anchor: end; dominant-baseline: middle; }
  
  /* Attributes and Keys */
  .attr-text { font-size: 11.5px; font-weight: 600; fill: #334155; font-family: monospace; }
  .pk-pill { fill: #FEF08A; stroke: #CA8A04; stroke-width: 1.2; rx: 3; ry: 3; }
  .pk-label { font-size: 11px; font-weight: 800; fill: #854D0E; font-family: monospace; }
  
  .fk-pill { fill: #DBEAFE; stroke: #3B82F6; stroke-width: 1.2; rx: 3; ry: 3; }
  .fk-label { font-size: 11px; font-weight: 800; fill: #1E40AF; font-family: monospace; }
  
  /* FK Pointer Lines & Markers */
  .fk-arrow { stroke: #2563EB; stroke-width: 1.8; fill: none; marker-end: url(#fk-arrowhead); stroke-linecap: round; }
  .fk-arrow-purple { stroke: #9333EA; stroke-width: 1.8; fill: none; marker-end: url(#fk-arrowhead-purple); stroke-linecap: round; }
  
  /* Rules Card */
  .rule-card { fill: #F8FAFC; stroke: #CBD5E1; stroke-width: 1.5; rx: 6; ry: 6; }
  .rule-title { font-size: 12px; font-weight: 800; fill: #0F172A; }
  .rule-desc { font-size: 11px; font-weight: 500; fill: #475569; }
</style>
</head>
<body>

<svg width="2200" height="1550" viewBox="0 0 2200 1550" xmlns="http://www.w3.org/2000/svg">

  <defs>
    <!-- Arrowhead markers for Foreign Key Referential Integrity links -->
    <marker id="fk-arrowhead" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#2563EB" />
    </marker>
    <marker id="fk-arrowhead-purple" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#9333EA" />
    </marker>
  </defs>

  <!-- Title Header -->
  <text x="1100" y="50" class="title-text">EER-TO-RELATIONAL TABLE CONVERSION & SCHEMA SPECIFICATION</text>
  <text x="1100" y="78" class="subtitle-text">Formal Mapping Rules, Primary Keys (PK), Foreign Keys (FK), and Referential Integrity Constraints (3NF Schema)</text>

  <!-- ===================================================================== -->
  <!-- 4 MAPPING RULES SUMMARY BANNER (Top) -->
  <!-- ===================================================================== -->
  <g transform="translate(60, 105)">
    <!-- Rule 1 -->
    <rect x="0" y="0" width="500" height="65" class="rule-card"/>
    <text x="15" y="25" class="rule-title" fill="#1D4ED8">(1) Strong Entity Mapping (Rule 1)</text>
    <text x="15" y="45" class="rule-desc">Regular entities map directly to base relations: declared PKs</text>
    <text x="15" y="58" class="rule-desc font-mono" fill="#2563EB">PATIENT, LOCATION, EMERGENCY_TYPE, AMBULANCE, HOSPITAL</text>

    <!-- Rule 2 -->
    <rect x="525" y="0" width="500" height="65" class="rule-card"/>
    <text x="540" y="25" class="rule-title" fill="#059669">(2) 1:N Relationship Mapping (Rule 2)</text>
    <text x="540" y="45" class="rule-desc">Inject PK of 1-side entity as Foreign Key into N-side child</text>
    <text x="540" y="58" class="rule-desc font-mono" fill="#059669">hospital_id &rarr; DEPARTMENT, dept_id &rarr; BED, amb_id &rarr; EQUIPMENT</text>

    <!-- Rule 3 -->
    <rect x="1050" y="0" width="500" height="65" class="rule-card"/>
    <text x="1065" y="25" class="rule-title" fill="#7C3AED">(3) Ternary Associative Mapping (Rule 3)</text>
    <text x="1065" y="45" class="rule-desc">Ternary dispatch between Emergency, Ambulance & Hospital</text>
    <text x="1065" y="58" class="rule-desc font-mono" fill="#7C3AED">Mapped to associative relation: RESOURCE_ALLOCATION</text>

    <!-- Rule 4 -->
    <rect x="1575" y="0" width="505" height="65" class="rule-card"/>
    <text x="1590" y="25" class="rule-title" fill="#DC2626">(4) Trigger-Driven Audit Mapping (Rule 4)</text>
    <text x="1590" y="45" class="rule-desc">1:N Logs relationship mapped to audit trail table</text>
    <text x="1590" y="58" class="rule-desc font-mono" fill="#DC2626">Populated by AFTER UPDATE OF status triggers on EMERGENCY</text>
  </g>

  <!-- ===================================================================== -->
  <!-- ROW 1 OF TABLES: PATIENT, LOCATION, EMERGENCY_TYPE -->
  <!-- ===================================================================== -->
  <!-- Table: PATIENT -->
  <g id="tbl-patient" transform="translate(60, 200)">
    <rect x="0" y="0" width="480" height="180" class="tbl-box"/>
    <rect x="0" y="0" width="480" height="36" class="tbl-header"/>
    <text x="240" y="22" class="tbl-name">PATIENT (Rule 1)</text>
    
    <!-- Columns -->
    <g transform="translate(15, 55)">
      <rect x="0" y="-12" width="90" height="20" class="pk-pill"/>
      <text x="5" y="2" class="pk-label">patient_id</text>
      <text x="100" y="2" class="attr-text">[PK] INTEGER AUTOINCREMENT</text>
    </g>
    <text x="15" y="85" class="attr-text">name : TEXT NOT NULL</text>
    <text x="15" y="105" class="attr-text">age : INTEGER CHECK(age > 0 AND age &le; 125)</text>
    <text x="15" y="125" class="attr-text">gender : TEXT CHECK(IN 'Male','Female','Other')</text>
    <text x="15" y="145" class="attr-text">contact_phone : TEXT NOT NULL</text>
    <text x="15" y="165" class="attr-text">blood_group, triage_medical_notes : TEXT</text>
  </g>

  <!-- Table: LOCATION -->
  <g id="tbl-location" transform="translate(580, 200)">
    <rect x="0" y="0" width="480" height="180" class="tbl-box"/>
    <rect x="0" y="0" width="480" height="36" class="tbl-header"/>
    <text x="240" y="22" class="tbl-name">LOCATION (Rule 1 - 3NF)</text>
    
    <!-- Columns -->
    <g transform="translate(15, 55)">
      <rect x="0" y="-12" width="90" height="20" class="pk-pill"/>
      <text x="5" y="2" class="pk-label">location_id</text>
      <text x="100" y="2" class="attr-text">[PK] INTEGER AUTOINCREMENT</text>
    </g>
    <text x="15" y="85" class="attr-text">address_line : TEXT NOT NULL</text>
    <text x="15" y="105" class="attr-text">zone_area : TEXT NOT NULL (e.g. Sector 62)</text>
    <text x="15" y="125" class="attr-text">landmark : TEXT</text>
    <text x="15" y="145" class="attr-text">postal_code : TEXT NOT NULL</text>
    <text x="15" y="165" class="attr-text">city_district : TEXT NOT NULL DEFAULT 'Noida'</text>
  </g>

  <!-- Table: EMERGENCY_TYPE -->
  <g id="tbl-type" transform="translate(1100, 200)">
    <rect x="0" y="0" width="460" height="180" class="tbl-box"/>
    <rect x="0" y="0" width="460" height="36" class="tbl-header"/>
    <text x="230" y="22" class="tbl-name">EMERGENCY_TYPE (Rule 1)</text>
    
    <!-- Columns -->
    <g transform="translate(15, 55)">
      <rect x="0" y="-12" width="75" height="20" class="pk-pill"/>
      <text x="5" y="2" class="pk-label">type_id</text>
      <text x="85" y="2" class="attr-text">[PK] INTEGER AUTOINCREMENT</text>
    </g>
    <text x="15" y="85" class="attr-text">type_name : TEXT UNIQUE NOT NULL</text>
    <text x="15" y="105" class="attr-text">description : TEXT</text>
    <text x="15" y="125" class="attr-text">severity_default : INTEGER CHECK(1 to 5)</text>
    <text x="15" y="145" class="attr-text">priority_rank : TEXT (Low,Med,High,Critical)</text>
  </g>

  <!-- Table: EMERGENCY_STATUS_HISTORY -->
  <g id="tbl-history" transform="translate(1600, 200)">
    <rect x="0" y="0" width="540" height="180" class="tbl-box" style="stroke:#DC2626; stroke-width:2.2;"/>
    <rect x="0" y="0" width="540" height="36" class="tbl-header" style="fill:#991B1B;"/>
    <text x="270" y="22" class="tbl-name">EMERGENCY_STATUS_HISTORY (Rule 4)</text>
    
    <!-- Columns -->
    <g transform="translate(15, 55)">
      <rect x="0" y="-12" width="85" height="20" class="pk-pill"/>
      <text x="5" y="2" class="pk-label">history_id</text>
      <text x="95" y="2" class="attr-text">[PK] INTEGER AUTOINCREMENT</text>
    </g>
    <g transform="translate(15, 80)">
      <rect x="0" y="-12" width="115" height="20" class="fk-pill"/>
      <text x="5" y="2" class="fk-label">emergency_id</text>
      <text x="125" y="2" class="attr-text">[FK &rarr; EMERGENCY] RESTRICT</text>
    </g>
    <text x="15" y="110" class="attr-text">status_state : TEXT NOT NULL</text>
    <text x="15" y="130" class="attr-text">changed_at : TIMESTAMP DEFAULT CURRENT_TIMESTAMP</text>
    <text x="15" y="150" class="attr-text">updated_by : TEXT DEFAULT 'SYSTEM_TRIGGER'</text>
    <text x="15" y="170" class="attr-text">remarks : TEXT (Logs state transitions automatically)</text>
  </g>

  <!-- ===================================================================== -->
  <!-- ROW 2: CENTRAL EMERGENCY RELATION (Rule 2) -->
  <!-- ===================================================================== -->
  <g id="tbl-emergency" transform="translate(480, 470)">
    <rect x="0" y="0" width="680" height="200" class="tbl-box" style="stroke:#2563EB; stroke-width:2.5;"/>
    <rect x="0" y="0" width="680" height="38" class="tbl-header" style="fill:#1E3A8A;"/>
    <text x="340" y="23" class="tbl-name">EMERGENCY (Rule 2: 1:N FK Insertion from Patient, Type, Location)</text>

    <!-- PK -->
    <g transform="translate(20, 60)">
      <rect x="0" y="-12" width="115" height="20" class="pk-pill"/>
      <text x="5" y="2" class="pk-label">emergency_id</text>
      <text x="125" y="2" class="attr-text">[PK] PRIMARY KEY AUTOINCREMENT</text>
    </g>

    <!-- FKs -->
    <g transform="translate(20, 90)">
      <rect x="0" y="-12" width="90" height="20" class="fk-pill"/>
      <text x="5" y="2" class="fk-label">patient_id</text>
      <text x="100" y="2" class="attr-text">[FK &rarr; PATIENT(patient_id)] ON DELETE RESTRICT</text>
    </g>

    <g transform="translate(20, 115)">
      <rect x="0" y="-12" width="75" height="20" class="fk-pill"/>
      <text x="5" y="2" class="fk-label">type_id</text>
      <text x="85" y="2" class="attr-text">[FK &rarr; EMERGENCY_TYPE(type_id)] ON DELETE RESTRICT</text>
    </g>

    <g transform="translate(20, 140)">
      <rect x="0" y="-12" width="95" height="20" class="fk-pill"/>
      <text x="5" y="2" class="fk-label">location_id</text>
      <text x="105" y="2" class="attr-text">[FK &rarr; LOCATION(location_id)] ON DELETE RESTRICT</text>
    </g>

    <text x="20" y="170" class="attr-text">reported_time : TIMESTAMP DEFAULT CURRENT_TIMESTAMP</text>
    <text x="20" y="190" class="attr-text">severity : INTEGER CHECK(1-5) &bull; status : TEXT CHECK(Reported,Dispatched...)</text>
  </g>

  <!-- FK ARROWS from EMERGENCY to PATIENT, LOCATION, EMERGENCY_TYPE -->
  <!-- Emergency -> Patient -->
  <path d="M 500 560 L 300 560 L 300 380" class="fk-arrow"/>
  <!-- Emergency -> Location -->
  <path d="M 700 610 L 700 640 L 800 640 L 800 380" class="fk-arrow"/>
  <!-- Emergency -> Emergency_Type -->
  <path d="M 1160 585 L 1250 585 L 1250 380" class="fk-arrow"/>
  <!-- History -> Emergency -->
  <path d="M 1600 280 L 1160 280 L 1160 470" class="fk-arrow"/>

  <!-- ===================================================================== -->
  <!-- ROW 3: ASSOCIATIVE TERNARY RELATION (RESOURCE_ALLOCATION) -->
  <!-- ===================================================================== -->
  <g id="tbl-resource-allocation" transform="translate(480, 750)">
    <rect x="0" y="0" width="680" height="210" class="tbl-box" style="stroke:#7C3AED; stroke-width:2.5; fill:#FAF5FF;"/>
    <rect x="0" y="0" width="680" height="38" class="tbl-header" style="fill:#5B21B6;"/>
    <text x="340" y="23" class="tbl-name">RESOURCE_ALLOCATION (Rule 3: Associative Ternary Relation)</text>

    <!-- PK -->
    <g transform="translate(20, 60)">
      <rect x="0" y="-12" width="115" height="20" class="pk-pill"/>
      <text x="5" y="2" class="pk-label">allocation_id</text>
      <text x="125" y="2" class="attr-text">[PK] PRIMARY KEY AUTOINCREMENT</text>
    </g>

    <!-- Ternary FKs -->
    <g transform="translate(20, 88)">
      <rect x="0" y="-12" width="115" height="20" class="fk-pill"/>
      <text x="5" y="2" class="fk-label">emergency_id</text>
      <text x="125" y="2" class="attr-text">[FK &rarr; EMERGENCY(emergency_id)] ON DELETE RESTRICT</text>
    </g>

    <g transform="translate(20, 112)">
      <rect x="0" y="-12" width="115" height="20" class="fk-pill"/>
      <text x="5" y="2" class="fk-label">ambulance_id</text>
      <text x="125" y="2" class="attr-text">[FK &rarr; AMBULANCE(ambulance_id)] ON DELETE RESTRICT</text>
    </g>

    <g transform="translate(20, 136)">
      <rect x="0" y="-12" width="95" height="20" class="fk-pill"/>
      <text x="5" y="2" class="fk-label">hospital_id</text>
      <text x="105" y="2" class="attr-text">[FK &rarr; HOSPITAL(hospital_id)] ON DELETE RESTRICT</text>
    </g>

    <g transform="translate(20, 160)">
      <rect x="0" y="-12" width="65" height="20" class="fk-pill"/>
      <text x="5" y="2" class="fk-label">bed_id</text>
      <text x="75" y="2" class="attr-text">[FK &rarr; BED(bed_id)] ON DELETE RESTRICT</text>
    </g>

    <text x="20" y="188" class="attr-text">dispatch_time : TIMESTAMP DEFAULT CURRENT_TIMESTAMP &bull; arrival_time : TIMESTAMP</text>
    <text x="20" y="204" class="attr-text">status : TEXT CHECK(IN 'Dispatched','En-Route','Handover-Complete','Cancelled')</text>
  </g>

  <!-- FK Arrow from Resource_Allocation to Emergency -->
  <path d="M 820 750 L 820 670" class="fk-arrow-purple"/>

  <!-- ===================================================================== -->
  <!-- ROW 4: AMBULANCE, EQUIPMENT, HOSPITAL, DEPARTMENT, BED, STAFF -->
  <!-- ===================================================================== -->
  <!-- Table: AMBULANCE -->
  <g id="tbl-ambulance" transform="translate(60, 1040)">
    <rect x="0" y="0" width="460" height="190" class="tbl-box"/>
    <rect x="0" y="0" width="460" height="36" class="tbl-header"/>
    <text x="230" y="22" class="tbl-name">AMBULANCE (Rule 1)</text>

    <g transform="translate(15, 55)">
      <rect x="0" y="-12" width="115" height="20" class="pk-pill"/>
      <text x="5" y="2" class="pk-label">ambulance_id</text>
      <text x="125" y="2" class="attr-text">[PK] INTEGER AUTOINCREMENT</text>
    </g>
    <text x="15" y="85" class="attr-text">vehicle_no : TEXT NOT NULL UNIQUE</text>
    <text x="15" y="105" class="attr-text">type : TEXT CHECK(type IN ('BLS','ALS'))</text>
    <text x="15" y="125" class="attr-text">operational_status : TEXT (Available, Dispatched...)</text>
    <text x="15" y="145" class="attr-text">base_station : TEXT NOT NULL</text>
  </g>

  <!-- Table: EQUIPMENT -->
  <g id="tbl-equipment" transform="translate(60, 1280)">
    <rect x="0" y="0" width="460" height="170" class="tbl-box"/>
    <rect x="0" y="0" width="460" height="36" class="tbl-header"/>
    <text x="230" y="22" class="tbl-name">EQUIPMENT (Rule 2: Decoupled 1NF)</text>

    <g transform="translate(15, 55)">
      <rect x="0" y="-12" width="115" height="20" class="pk-pill"/>
      <text x="5" y="2" class="pk-label">equipment_id</text>
      <text x="125" y="2" class="attr-text">[PK] INTEGER AUTOINCREMENT</text>
    </g>
    <g transform="translate(15, 80)">
      <rect x="0" y="-12" width="115" height="20" class="fk-pill"/>
      <text x="5" y="2" class="fk-label">ambulance_id</text>
      <text x="125" y="2" class="attr-text">[FK &rarr; AMBULANCE] CASCADE</text>
    </g>
    <text x="15" y="110" class="attr-text">equipment_name : TEXT NOT NULL</text>
    <text x="15" y="130" class="attr-text">serial_no : TEXT UNIQUE NOT NULL</text>
    <text x="15" y="150" class="attr-text">is_functional : INTEGER CHECK(0 or 1)</text>
  </g>

  <!-- Equipment -> Ambulance FK Arrow -->
  <path d="M 230 1280 L 230 1230" class="fk-arrow"/>

  <!-- Table: HOSPITAL -->
  <g id="tbl-hospital" transform="translate(580, 1040)">
    <rect x="0" y="0" width="460" height="190" class="tbl-box"/>
    <rect x="0" y="0" width="460" height="36" class="tbl-header"/>
    <text x="230" y="22" class="tbl-name">HOSPITAL (Rule 2: FK location_id)</text>

    <g transform="translate(15, 55)">
      <rect x="0" y="-12" width="95" height="20" class="pk-pill"/>
      <text x="5" y="2" class="pk-label">hospital_id</text>
      <text x="105" y="2" class="attr-text">[PK] INTEGER AUTOINCREMENT</text>
    </g>
    <g transform="translate(15, 80)">
      <rect x="0" y="-12" width="95" height="20" class="fk-pill"/>
      <text x="5" y="2" class="fk-label">location_id</text>
      <text x="105" y="2" class="attr-text">[FK &rarr; LOCATION] RESTRICT</text>
    </g>
    <text x="15" y="110" class="attr-text">hospital_name : TEXT NOT NULL</text>
    <text x="15" y="130" class="attr-text">contact_phone : TEXT NOT NULL</text>
    <text x="15" y="150" class="attr-text">emergency_level : Level 1, Level 2, General</text>
    <text x="15" y="170" class="attr-text">total_beds : INTEGER CHECK(total_beds &ge; 0)</text>
  </g>

  <!-- Table: DEPARTMENT -->
  <g id="tbl-department" transform="translate(580, 1280)">
    <rect x="0" y="0" width="460" height="170" class="tbl-box"/>
    <rect x="0" y="0" width="460" height="36" class="tbl-header"/>
    <text x="230" y="22" class="tbl-name">DEPARTMENT (Rule 2: 1:N)</text>

    <g transform="translate(15, 55)">
      <rect x="0" y="-12" width="75" height="20" class="pk-pill"/>
      <text x="5" y="2" class="pk-label">dept_id</text>
      <text x="85" y="2" class="attr-text">[PK] INTEGER AUTOINCREMENT</text>
    </g>
    <g transform="translate(15, 80)">
      <rect x="0" y="-12" width="95" height="20" class="fk-pill"/>
      <text x="5" y="2" class="fk-label">hospital_id</text>
      <text x="105" y="2" class="attr-text">[FK &rarr; HOSPITAL] CASCADE</text>
    </g>
    <text x="15" y="110" class="attr-text">dept_name : TEXT NOT NULL</text>
    <text x="15" y="130" class="attr-text">total_capacity : INTEGER CHECK(&ge; 0)</text>
    <text x="15" y="150" class="attr-text">head_doctor, contact_ext : TEXT</text>
  </g>

  <!-- Department -> Hospital FK Arrow -->
  <path d="M 750 1280 L 750 1230" class="fk-arrow"/>

  <!-- Table: BED -->
  <g id="tbl-bed" transform="translate(1100, 1040)">
    <rect x="0" y="0" width="480" height="190" class="tbl-box"/>
    <rect x="0" y="0" width="480" height="36" class="tbl-header"/>
    <text x="240" y="22" class="tbl-name">BED (Rule 2: 1:N from Department)</text>

    <g transform="translate(15, 55)">
      <rect x="0" y="-12" width="65" height="20" class="pk-pill"/>
      <text x="5" y="2" class="pk-label">bed_id</text>
      <text x="75" y="2" class="attr-text">[PK] INTEGER AUTOINCREMENT</text>
    </g>
    <g transform="translate(15, 80)">
      <rect x="0" y="-12" width="75" height="20" class="fk-pill"/>
      <text x="5" y="2" class="fk-label">dept_id</text>
      <text x="85" y="2" class="attr-text">[FK &rarr; DEPARTMENT] CASCADE</text>
    </g>
    <text x="15" y="110" class="attr-text">bed_number : TEXT NOT NULL</text>
    <text x="15" y="130" class="attr-text">floor_no : INTEGER NOT NULL</text>
    <text x="15" y="150" class="attr-text">bed_type : TEXT CHECK('ICU','General')</text>
    <text x="15" y="170" class="attr-text">is_occupied : INTEGER CHECK(0 or 1)</text>
    <text x="15" y="185" class="attr-text font-bold" fill="#7C3AED">UNIQUE(dept_id, bed_number)</text>
  </g>

  <!-- Bed -> Department FK Arrow -->
  <path d="M 1100 1120 L 1060 1120 L 1060 1350 L 1040 1350" class="fk-arrow"/>

  <!-- Table: STAFF -->
  <g id="tbl-staff" transform="translate(1640, 1040)">
    <rect x="0" y="0" width="500" height="210" class="tbl-box"/>
    <rect x="0" y="0" width="500" height="36" class="tbl-header"/>
    <text x="250" y="22" class="tbl-name">STAFF (Rule 2: Hospital / Ambulance)</text>

    <g transform="translate(15, 55)">
      <rect x="0" y="-12" width="75" height="20" class="pk-pill"/>
      <text x="5" y="2" class="pk-label">staff_id</text>
      <text x="85" y="2" class="attr-text">[PK] INTEGER AUTOINCREMENT</text>
    </g>
    <g transform="translate(15, 80)">
      <rect x="0" y="-12" width="95" height="20" class="fk-pill"/>
      <text x="5" y="2" class="fk-label">hospital_id</text>
      <text x="105" y="2" class="attr-text">[FK &rarr; HOSPITAL] NULL ON DELETE</text>
    </g>
    <g transform="translate(15, 105)">
      <rect x="0" y="-12" width="115" height="20" class="fk-pill"/>
      <text x="5" y="2" class="fk-label">ambulance_id</text>
      <text x="125" y="2" class="attr-text">[FK &rarr; AMBULANCE] NULL ON DELETE</text>
    </g>
    <text x="15" y="135" class="attr-text">full_name : TEXT NOT NULL</text>
    <text x="15" y="155" class="attr-text">role_type : Doctor, Paramedic, Driver</text>
    <text x="15" y="175" class="attr-text">license_no : TEXT UNIQUE NOT NULL</text>
    <text x="15" y="195" class="attr-text">phone_no : TEXT NOT NULL</text>
  </g>

  <!-- Resource_Allocation Arrows to Ambulance and Hospital -->
  <path d="M 500 870 L 300 870 L 300 1040" class="fk-arrow-purple"/>
  <path d="M 780 960 L 780 1040" class="fk-arrow-purple"/>
  <path d="M 1160 880 L 1300 880 L 1300 1040" class="fk-arrow-purple"/>

</svg>

</body>
</html>
"""

# =============================================================================
# EXPORTER RUNNER (HTML -> SVG -> CHROME HEADLESS HIGH-RES PNG)
# =============================================================================
def export_html_to_png(html_content, html_filename, png_filename, width, height):
    html_path = os.path.join(STATIC_DIAGRAMS_DIR, html_filename)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    dest_project = os.path.join(STATIC_DIAGRAMS_DIR, png_filename)
    dest_downloads = os.path.join(DOWNLOADS_DIR, png_filename)

    cmd = [
        CHROME_PATH,
        "--headless",
        "--disable-gpu",
        "--hide-scrollbars",
        f"--window-size={width},{height}",
        f"--screenshot={dest_downloads}",
        html_path
    ]
    subprocess.run(cmd, check=True)

    # Also copy to static directory
    import shutil
    shutil.copy2(dest_downloads, dest_project)
    print(f"Exported: {dest_downloads} ({width}x{height})")
    print(f"  Copy:   {dest_project}")

def main():
    print("Generating High-Resolution Diagrams...")

    # 1. EER Diagram
    eer_html = generate_eer_diagram_html()
    export_html_to_png(
        eer_html,
        "Urban_Emergency_EER_Diagram.html",
        "Urban_Emergency_EER_Diagram.png",
        2400,
        1680
    )

    # 2. System Flowchart
    flow_html = generate_flowchart_html()
    export_html_to_png(
        flow_html,
        "Urban_Emergency_System_Flowchart.html",
        "Urban_Emergency_System_Flowchart.png",
        1700,
        2100
    )

    # 3. Relational Mapping
    rel_html = generate_relational_mapping_html()
    export_html_to_png(
        rel_html,
        "Urban_Emergency_EER_to_Relational_Mapping.html",
        "Urban_Emergency_EER_to_Relational_Mapping.png",
        2200,
        1580
    )

    print("\nAll 3 diagrams successfully generated and saved to:")
    print(f"  1. {os.path.join(DOWNLOADS_DIR, 'Urban_Emergency_EER_Diagram.png')}")
    print(f"  2. {os.path.join(DOWNLOADS_DIR, 'Urban_Emergency_System_Flowchart.png')}")
    print(f"  3. {os.path.join(DOWNLOADS_DIR, 'Urban_Emergency_EER_to_Relational_Mapping.png')}")

if __name__ == "__main__":
    main()
