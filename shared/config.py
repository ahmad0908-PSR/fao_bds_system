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
DATABASE_PATH = BASE_DIR / os.getenv("DATABASE_PATH", "data/bds_system.db")

# Make sure the data/ folder exists so SQLite doesn't fail on first run
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
