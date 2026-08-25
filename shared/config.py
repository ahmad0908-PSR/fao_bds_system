"""
Central configuration for the FAO BDS Tracking System.
Both Application 1 (Data Entry) and Application 2 (Dashboard) import from here,
so there is exactly one source of truth for paths, DB connection, and settings.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# --------------------------------------------------------------------
# Project root = the folder that contains this "shared" package,
# one level up from this file (shared/config.py -> project_root)
# --------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env at project root (if present)
load_dotenv(BASE_DIR / ".env")

# --------------------------------------------------------------------
# Database
# --------------------------------------------------------------------
# If DATABASE_URL is set (e.g. a Postgres connection string from Neon,
# Supabase, etc.), that takes priority — this is what production/hosted
# deployments use, so App 1 and App 2 point at the SAME remote database
# no matter where each is deployed.
#
# If DATABASE_URL is NOT set, we fall back to a local SQLite file, so you
# can still develop and test locally in PyCharm without needing a Postgres
# server running on your machine.
_raw_database_url = os.getenv("DATABASE_URL", "").strip()

if _raw_database_url:
    # Some providers hand out "postgres://" URLs (old Heroku-style scheme).
    # SQLAlchemy 2.x requires "postgresql://" — normalize it here so either
    # form works without the person needing to know about this quirk.
    if _raw_database_url.startswith("postgres://"):
        _raw_database_url = _raw_database_url.replace("postgres://", "postgresql://", 1)
    DATABASE_URL = _raw_database_url
else:
    DATABASE_PATH = BASE_DIR / os.getenv("DATABASE_PATH", "data/bds_system.db")
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# --------------------------------------------------------------------
# Data Entry App authentication
# --------------------------------------------------------------------
# This should be a bcrypt hash, generated once via shared/generate_password_hash.py
# and stored in .env as ENTRY_APP_PASSWORD_HASH. We never store the plaintext
# password anywhere in the project.
ENTRY_APP_PASSWORD_HASH = os.getenv("ENTRY_APP_PASSWORD_HASH", "").strip()

# --------------------------------------------------------------------
# Business ID formatting
# --------------------------------------------------------------------
BUSINESS_ID_PREFIX = "BDS"
BUSINESS_ID_PADDING = 6  # BDS-000001
