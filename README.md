# FAO EFSP — BDS Tracking System

## Application 1: Data Entry & Business Tracking

### First-time setup

1. **Create your `.env` file**
   ```
   cp .env.example .env
   ```

2. **Generate your login password hash**
   ```
   python -m shared.generate_password_hash
   ```
   Copy the printed hash into `.env` as `ENTRY_APP_PASSWORD_HASH`.

3. **Initialize the database** (optional — it also auto-creates on first run)
   ```
   python -m shared.database.init_db
   ```

4. **Run the app**
   ```
   streamlit run app_data_entry/main.py
   ```

### Notes

- The database is SQLite, stored at `data/bds_system.db` (auto-created).
- There is **no history table** — phase/stage status fields are overwritten
  in place on the `Business` row when updated via "Update Phase & Stage."
- All business profile fields are optional; only `Business_ID` is
  auto-generated (format `BDS-000001`, `BDS-000002`, ...).
- `shared/` is imported by both Application 1 (this one) and the future
  Application 2 (Dashboard) — never duplicate model/constant definitions,
  always add to `shared/`.
