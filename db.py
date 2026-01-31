"""
Database layer for Trip Planner app.
Uses Supabase (PostgreSQL) when SUPABASE_URL and SUPABASE_KEY are configured,
otherwise falls back to file-based storage (local only).
"""
import os
import json

# Data keys stored in the database (one row per key, value = JSON)
DATA_KEYS = [
    "places",
    "todo",
    "trip_info",
    "packing",
    "budget",
    "notes",
    "users",
    "weather",
    "exchange_rates",
]

# Prefix for photo keys in DB: photo_<place_id>
PHOTO_KEY_PREFIX = "photo_"


def _get_supabase_client():
    """Get Supabase client if credentials are configured."""
    try:
        import streamlit as st
        if hasattr(st, "secrets"):
            url = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
            key = st.secrets.get("SUPABASE_KEY") or os.getenv("SUPABASE_KEY")
            if url and key:
                from supabase import create_client
                return create_client(url, key)
    except Exception:
        pass
    return None


def use_database():
    """Return True if database (Supabase) is configured and should be used."""
    return _get_supabase_client() is not None


def db_load(key):
    """Load a value from the database by key. Returns None if not found or on error."""
    client = _get_supabase_client()
    if not client:
        return None
    try:
        r = client.table("app_data").select("value").eq("key", key).limit(1).execute()
        if r.data and len(r.data) > 0:
            val = r.data[0].get("value")
            if isinstance(val, dict):
                return val
            if isinstance(val, str):
                return json.loads(val)
            return val
    except Exception:
        pass
    return None


def db_save(key, value):
    """Save a value to the database (upsert by key)."""
    client = _get_supabase_client()
    if not client:
        return False
    try:
        # Supabase/PostgREST accepts JSON; ensure we send a JSON-serializable dict
        payload = {"key": key, "value": value}
        client.table("app_data").upsert(payload, on_conflict="key").execute()
        return True
    except Exception:
        return False


def db_load_photo(place_id):
    """
    Load photo for a place from DB. Returns dict with 'filename' and 'data' (base64)
    or None if not found.
    """
    key = f"{PHOTO_KEY_PREFIX}{place_id}"
    return db_load(key)


def db_save_photo(place_id, filename, base64_data):
    """Save photo for a place to DB. filename and base64_data are strings."""
    key = f"{PHOTO_KEY_PREFIX}{place_id}"
    return db_save(key, {"filename": filename, "data": base64_data})
