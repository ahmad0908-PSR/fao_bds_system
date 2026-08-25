"""
Shared constant lists used across both applications:
dropdown options, province lists, phase/stage definitions, status options,
and the status -> color map used by the Progress Matrix.
Keeping these in one place means App 1 and App 2 are always in sync.
"""

# --------------------------------------------------------------------
# Windows
# --------------------------------------------------------------------
WINDOWS = ["W1A", "W1B", "W2", "W3"]

# --------------------------------------------------------------------
# Afghanistan Provinces (all 34)
# --------------------------------------------------------------------
AFGHANISTAN_PROVINCES = [
    "Badakhshan", "Badghis", "Baghlan", "Balkh", "Bamyan",
    "Daykundi", "Farah", "Faryab", "Ghazni", "Ghor",
    "Helmand", "Herat", "Jowzjan", "Kabul", "Kandahar",
    "Kapisa", "Khost", "Kunar", "Kunduz", "Laghman",
    "Logar", "Nangarhar", "Nimroz", "Nuristan", "Paktika",
    "Paktia", "Panjshir", "Parwan", "Samangan", "Sar-e Pol",
    "Takhar", "Urozgan", "Wardak", "Zabul",
]

# --------------------------------------------------------------------
# Simple Yes/No dropdown (blank first option so nothing is force-selected,
# since all fields are optional)
# --------------------------------------------------------------------
YES_NO_OPTIONS = ["", "Yes", "No"]

# --------------------------------------------------------------------
# Per-stage status vocabularies (matches reference Progress Matrix screenshot)
# --------------------------------------------------------------------
# "Completion-type" stages: things that are simply done or not
COMPLETION_STATUS_OPTIONS = [
    "Not Started",
    "Ongoing",
    "Completed",
    "Not Applicable",
    "Not Selected By FAO",
]

# "Submission-type" stages: reports/documents sent to FAO
SUBMISSION_STATUS_OPTIONS = [
    "Not Started",
    "Ongoing",
    "Submitted to FAO",
    "Not Applicable",
    "Not Selected By FAO",
]

# Selected for BDS (Phase 1, Stage 4)
SELECTED_FOR_BDS_OPTIONS = ["", "Yes", "Not Selected", "Pending/FAO"]

# Verification Status (Phase 1, Stage 3 — shared with Business.verification_status)
VERIFICATION_STATUS_OPTIONS = [
    "",
    "Verified",
    "Verified With Conditions",
    "Significant Conditions",
    "Significant Deficiencies - Redirect to W2",
    "Not Eligible / Not Verified",
    "Rejected",
]

# --------------------------------------------------------------------
# Phases
# --------------------------------------------------------------------
PHASE_OPTIONS = [
    "",
    "Phase 1: Pre-Qualification Verification",
    "Phase 2: Business Development Support",
]

# --------------------------------------------------------------------
# Phase 1 stage labels -> Business model field names
# --------------------------------------------------------------------
PHASE_1_STAGES = {
    "Stage 1: Assessment": "p1_s1_assessment_status",
    "Stage 2: Verification Report Submission to FAO": "p1_s2_verification_report_status",
    # Stage 3 intentionally reuses Business.verification_status (see models.py)
    "Stage 4: Selected for BDS/FAO": "p1_s4_selected_for_bds",
}

# --------------------------------------------------------------------
# Phase 2 stage labels -> Business model field names
# --------------------------------------------------------------------
PHASE_2_STAGES = {
    "Stage 1: Diagnostic Assessment": "p2_s1_diagnostic_assessment_status",
    "Stage 2: Business Plan Development": "p2_s2_business_plan_dev_status",
    "Stage 3: Diagnostic Assessment Report Submission to FAO": "p2_s3_diagnostic_report_submission_status",
    "Stage 4a: Virtual Enterprise Capacity Building": "p2_s4_virtual_capacity_building_status",
    "Stage 4b: In-Person Enterprise Capacity Building": "p2_s4_inperson_capacity_building_status",
    "Stage 5: Coaching": "p2_s5_coaching_status",
    "Stage 6: Monitoring": "p2_s6_monitoring_status",
}

# --------------------------------------------------------------------
# Field name -> which status option list applies (used to build dropdowns
# dynamically instead of hardcoding per-page)
# --------------------------------------------------------------------
STAGE_FIELD_OPTIONS = {
    "p1_s1_assessment_status": COMPLETION_STATUS_OPTIONS,
    "p1_s2_verification_report_status": SUBMISSION_STATUS_OPTIONS,
    "p1_s4_selected_for_bds": SELECTED_FOR_BDS_OPTIONS,
    "p2_s1_diagnostic_assessment_status": COMPLETION_STATUS_OPTIONS,
    "p2_s2_business_plan_dev_status": COMPLETION_STATUS_OPTIONS,
    "p2_s3_diagnostic_report_submission_status": SUBMISSION_STATUS_OPTIONS,
    "p2_s4_virtual_capacity_building_status": COMPLETION_STATUS_OPTIONS,
    "p2_s4_inperson_capacity_building_status": COMPLETION_STATUS_OPTIONS,
    "p2_s5_coaching_status": COMPLETION_STATUS_OPTIONS,
    "p2_s6_monitoring_status": COMPLETION_STATUS_OPTIONS,
}

# --------------------------------------------------------------------
# Short column labels for the Progress Matrix grid (matches screenshot
# abbreviations, which are more compact than the full stage labels above)
# --------------------------------------------------------------------
MATRIX_COLUMN_LABELS = {
    "p1_s1_assessment_status": "Assessment",
    "p1_s2_verification_report_status": "Vf-Report",
    "verification_status": "Verification Status",
    "p1_s4_selected_for_bds": "Selected for BDS/FAO",
    "p2_s1_diagnostic_assessment_status": "Dsg-Assessment",
    "p2_s2_business_plan_dev_status": "BP-Development",
    "p2_s3_diagnostic_report_submission_status": "Dsg-Assessment-Report",
    "p2_s4_virtual_capacity_building_status": "Virtual E-Capacity",
    "p2_s4_inperson_capacity_building_status": "In-Person E-Capacity",
    "p2_s5_coaching_status": "Coaching",
    "p2_s6_monitoring_status": "Monitoring",
}

MATRIX_GROUP_1_LABEL = "Pre-Qualification Verification"
MATRIX_GROUP_1_FIELDS = [
    "p1_s1_assessment_status",
    "p1_s2_verification_report_status",
    "verification_status",
    "p1_s4_selected_for_bds",
]

MATRIX_GROUP_2_LABEL = "Business Development Support"
MATRIX_GROUP_2_FIELDS = [
    "p2_s1_diagnostic_assessment_status",
    "p2_s2_business_plan_dev_status",
    "p2_s3_diagnostic_report_submission_status",
    "p2_s4_virtual_capacity_building_status",
    "p2_s4_inperson_capacity_building_status",
    "p2_s5_coaching_status",
    "p2_s6_monitoring_status",
]

# --------------------------------------------------------------------
# Status -> color map (used by the Progress Matrix cell styling)
# --------------------------------------------------------------------
STATUS_COLOR_MAP = {
    # Completion-type
    "Not Started": "#e0e0e0",
    "Ongoing": "#f4d35e",
    "Completed": "#4d7ea8",
    "Not Applicable": "#bdbdbd",
    "Not Selected By FAO": "#e57373",
    # Submission-type
    "Submitted to FAO": "#3fae8a",
    # Selected for BDS/FAO
    "Yes": "#81c995",
    "Not Selected": "#e57373",
    "Pending/FAO": "#ffe08a",
    # Verification Status
    "Verified": "#7fd17f",
    "Verified With Conditions": "#a8d5a8",
    "Significant Conditions": "#d9c96e",
    "Significant Deficiencies - Redirect to W2": "#e2965a",
    "Not Eligible / Not Verified": "#a8d5a8",
    "Rejected": "#e57373",
    # Fallback for blank/unset
    "": "#f5f5f5",
}

DEFAULT_CELL_COLOR = "#f5f5f5"
