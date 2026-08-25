"""
SQLAlchemy models for the FAO BDS Tracking System.

NOTE ON PHASE/STAGE TRACKING:
Per project decision, there is NO separate history table. Each stage's
current status is stored as a column directly on the Business row and is
overwritten in place when updated. Only the single most recent status per
stage is retained.
"""

from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Float, Text, DateTime

from shared.database.engine import Base


def utcnow():
    return datetime.now(timezone.utc)


class Business(Base):
    __tablename__ = "businesses"

    # ------------------------------------------------------------
    # Internal primary key + auto-generated public Business ID
    # ------------------------------------------------------------
    id = Column(Integer, primary_key=True, autoincrement=True)
    business_id = Column(String(20), unique=True, nullable=False, index=True)  # e.g. BDS-000001

    # ------------------------------------------------------------
    # Business Information
    # ------------------------------------------------------------
    business_id_fao = Column(String(100), nullable=True)
    window = Column(String(10), nullable=True)
    enterprise_name = Column(String(255), nullable=True, index=True)
    verification_status = Column(String(100), nullable=True)  # also serves as Phase 1 / Stage 3
    year_of_establishment = Column(String(10), nullable=True)
    women_led = Column(String(5), nullable=True)      # "Yes" / "No"
    youth_inclusive = Column(String(5), nullable=True)  # "Yes" / "No"

    # ------------------------------------------------------------
    # Contact Information
    # ------------------------------------------------------------
    owner_name_primary = Column(String(150), nullable=True)
    owner_position_primary = Column(String(150), nullable=True)
    phone_primary = Column(String(50), nullable=True)
    email_primary = Column(String(150), nullable=True)

    owner_name_secondary = Column(String(150), nullable=True)
    owner_position_secondary = Column(String(150), nullable=True)
    phone_secondary = Column(String(50), nullable=True)
    email_secondary = Column(String(150), nullable=True)

    # ------------------------------------------------------------
    # Location Information
    # ------------------------------------------------------------
    province = Column(String(100), nullable=True, index=True)
    district = Column(String(150), nullable=True)
    village = Column(String(150), nullable=True)
    exact_address = Column(Text, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    # ------------------------------------------------------------
    # Business Statistics
    # ------------------------------------------------------------
    current_employee_count = Column(Integer, nullable=True)
    current_farmers_linked = Column(Integer, nullable=True)

    # ------------------------------------------------------------
    # Financial Information
    # ------------------------------------------------------------
    annual_turnover_usd = Column(Float, nullable=True)
    grant_requested_usd = Column(Float, nullable=True)
    total_co_contribution_usd = Column(Float, nullable=True)

    # ------------------------------------------------------------
    # Phase & Stage Tracking (current status only, no history)
    # ------------------------------------------------------------
    current_phase = Column(String(60), nullable=True, index=True)

    # Phase 1: Pre-Qualification Verification
    p1_s1_assessment_status = Column(String(30), nullable=True, default="Not Started")
    p1_s2_verification_report_status = Column(String(30), nullable=True, default="Not Started")
    # p1 stage 3 = verification_status field above (shared, per spec)
    p1_s4_selected_for_bds = Column(String(5), nullable=True)  # "Yes" / "No"

    # Phase 2: Business Development Support
    p2_s1_diagnostic_assessment_status = Column(String(30), nullable=True, default="Not Started")
    p2_s2_business_plan_dev_status = Column(String(30), nullable=True, default="Not Started")
    p2_s3_diagnostic_report_submission_status = Column(String(30), nullable=True, default="Not Started")
    p2_s4_virtual_capacity_building_status = Column(String(30), nullable=True, default="Not Started")
    p2_s4_inperson_capacity_building_status = Column(String(30), nullable=True, default="Not Started")
    p2_s5_coaching_status = Column(String(30), nullable=True, default="Not Started")
    p2_s6_monitoring_status = Column(String(30), nullable=True, default="Not Started")

    # ------------------------------------------------------------
    # Timestamps
    # ------------------------------------------------------------
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)

    def __repr__(self):
        return f"<Business {self.business_id} - {self.enterprise_name}>"
