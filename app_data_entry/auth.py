"""
Simple password gate for the Data Entry App.
Not a full user-management system - a single shared password, bcrypt-hashed
and stored in .env, per the project requirements.
"""

import bcrypt
import streamlit as st

from shared.config import ENTRY_APP_PASSWORD_HASH


def _check_password(password: str) -> bool:
    if not ENTRY_APP_PASSWORD_HASH:
        st.error(
            "No password is configured yet. Run "
            "`python -m shared.generate_password_hash` and add the result "
            "to your .env file as ENTRY_APP_PASSWORD_HASH."
        )
        return False

    return bcrypt.checkpw(
        password.encode("utf-8"),
        ENTRY_APP_PASSWORD_HASH.encode("utf-8"),
    )


def login_screen():
    """Renders a login form. Sets st.session_state.authenticated = True on success."""
    st.title("FAO EFSP — Data Entry System")
    st.caption("Business Development Support (BDS) Tracking — Login")

    with st.form("login_form"):
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Log In")

    if submitted:
        if _check_password(password):
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password.")


def require_login():
    """
    Call this at the top of every page (including main.py).
    Stops execution and shows the login screen if not authenticated.
    """
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        login_screen()
        st.stop()
