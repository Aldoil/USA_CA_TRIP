# Database setup for Trip Planner (Supabase)

When your app runs on **Streamlit Cloud**, the server can shut down after inactivity. Without a database, all data (places, budget, notes, photos, etc.) is lost because it was only stored in local files.

This guide shows how to create a **free Supabase database** and connect your Trip Planner app so that data is saved online and restored when the app restarts.

---

## Step 1: Create a Supabase account

1. Go to **[https://supabase.com](https://supabase.com)** and click **Start your project**.
2. Sign in with GitHub (or Google / email).
3. After signing in, you’ll see the Supabase dashboard.

---

## Step 2: Create a new project

1. Click **New project**.
2. Choose your **Organization** (or create one).
3. Fill in:
   - **Name**: e.g. `trip-planner`
   - **Database Password**: choose a strong password and **save it** (you need it only for direct DB access; the app uses the API key).
   - **Region**: pick one close to you or your users.
4. Click **Create new project** and wait 1–2 minutes until the project is ready.

---

## Step 3: Create the table

1. In the left sidebar, open **SQL Editor**.
2. Click **New query**.
3. Paste this SQL and run it (click **Run** or press Ctrl+Enter):

```sql
-- Single table for all app data (key-value style).
-- Each row = one “file” (places, budget, notes, photos, etc.).
create table if not exists public.app_data (
  key   text primary key,
  value jsonb not null default '{}'
);

-- Allow the anon key to read and write (needed for the app).
alter table public.app_data enable row level security;

create policy "Allow all for anon"
  on public.app_data
  for all
  to anon
  using (true)
  with check (true);
```

4. You should see a success message. The table `app_data` is now ready.

---

## Step 4: Get your project URL and API key

1. In the left sidebar, click **Project Settings** (gear icon).
2. Open **API** in the left menu.
3. Copy and save:
   - **Project URL** (e.g. `https://xxxxxxxxxxxx.supabase.co`) → this is your **SUPABASE_URL**.
   - **anon public** key (under “Project API keys”) → this is your **SUPABASE_KEY**.  
     Use the **anon** key, not the `service_role` key.

---

## Step 5: Configure Streamlit Cloud secrets

1. Open your app repo on **GitHub** and go to **Streamlit Community Cloud** ([share.streamlit.io](https://share.streamlit.io)).
2. Open your app (or deploy it if you haven’t yet).
3. Click the **⋮** menu next to your app → **Settings** → **Secrets**.
4. Add the same secrets you use locally. For database persistence, include Supabase:

```toml
# Required: app password
password = "your_app_password"

# Database (so data survives restarts)
SUPABASE_URL = "https://xxxxxxxxxxxx.supabase.co"
SUPABASE_KEY = "your_anon_public_key_here"
```

Replace:
- `your_app_password` with your real app password.
- `https://xxxxxxxxxxxx.supabase.co` with your **Project URL**.
- `your_anon_public_key_here` with your **anon public** API key.

5. Save. Streamlit will redeploy the app with the new secrets.

---

## Step 6: (Optional) Use the database locally

To test with the same database on your machine:

1. Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` (if you don’t have it yet).
2. In `.streamlit/secrets.toml` add:

```toml
password = "your_app_password"
SUPABASE_URL = "https://xxxxxxxxxxxx.supabase.co"
SUPABASE_KEY = "your_anon_public_key_here"
```

3. Run the app locally. If `SUPABASE_URL` and `SUPABASE_KEY` are set, the app will use the database instead of local files.

---

## How it works

- **If `SUPABASE_URL` and `SUPABASE_KEY` are set** (in Streamlit secrets or in `.streamlit/secrets.toml`):  
  All trip data (places, todo, trip info, packing, budget, notes, users, weather cache, exchange rates, place photos) is stored in the Supabase table `app_data`. When the app restarts (e.g. after being idle on Streamlit Cloud), it loads data from the database, so nothing is lost.

- **If Supabase is not configured**:  
  The app uses local JSON files and the `data/` folder as before. This is fine for local use but data will not persist on Streamlit Cloud.

---

## How updates work: saving and reacting to changes

### Where data lives in the database

The app uses **one table**, `app_data`, with two columns:

| Column | Type   | Meaning                                      |
|--------|--------|----------------------------------------------|
| `key`  | text   | Identifier: `"trip_info"`, `"places"`, etc.  |
| `value`| jsonb  | The whole JSON for that key (e.g. all hotels, all places) |

So there is **one row per “data type”**, not one row per hotel or per place. For example:

- Row `key = "trip_info"` → `value = { "flights": [...], "hotels": [...] }`
- Row `key = "places"` → `value = { "places": [...] }`

### What happens when you change something (e.g. edit a hotel)

1. **In the app (UI)**  
   You edit a hotel and click “Save Changes”. The app updates the in-memory `trip_info` object (the `hotels` list inside it).

2. **Save call**  
   The app calls `save_trip_info(trip_info)` with that **entire** object (all flights + all hotels).

3. **Inside `save_trip_info`**  
   - If the database is configured: it calls `db_save("trip_info", data)`.  
   - If not: it writes `trip_info.json` to disk.

4. **Inside `db_save`**  
   It sends one row to Supabase:  
   `{ "key": "trip_info", "value": <whole trip_info object> }`  
   and runs an **upsert** on `app_data` with `on_conflict="key"`. So:
   - If a row with `key = "trip_info"` already exists → that row’s `value` is **replaced** with the new JSON.
   - If it doesn’t exist → a new row is **inserted**.

So every time you save (edit hotel, add flight, delete place, etc.), the app **overwrites the whole blob** for that key. The database does not “patch” individual hotels or flights; it just stores the latest full JSON.

### What happens when the app loads (e.g. after restart)

1. The app calls e.g. `load_trip_info()`.
2. If the database is configured, that calls `db_load("trip_info")`, which runs:  
   `SELECT value FROM app_data WHERE key = 'trip_info'`  
   and returns the **one** jsonb value for that key.
3. The app uses that object as its in-memory `trip_info` (flights + hotels). So the next time you open Trip Info, you see the last saved state.

### Summary

- **Saving** = replace the whole value for that key in `app_data` (upsert by `key`).
- **Loading** = read the value for that key from `app_data` and use it in the app.
- **Reacting to changes** = the app does not “subscribe” to the database. Each user sees changes only after a reload/rerun that calls `load_*` again. So: you edit → save (writes to DB) → the same session reruns and reads from DB (or from memory), so you see the update. Another user or another device will see the update the next time the app loads data (e.g. when they open the app or refresh).

---

## Troubleshooting

- **“relation app_data does not exist”**  
  Run the SQL from Step 3 in the Supabase SQL Editor and make sure it completes without errors.

- **“new row violates row-level security”**  
  Make sure you created the RLS policy exactly as in Step 3 (policy name can differ, but it must allow `anon` to `select`/`insert`/`update`/`delete` on `app_data`).

- **Data still disappears on Streamlit Cloud**  
  Check that in **App settings → Secrets** you have both `SUPABASE_URL` and `SUPABASE_KEY` set (no typos, no extra spaces). Redeploy after changing secrets.

- **Local app: “No module named 'supabase'”**  
  Run: `pip install -r requirements.txt` (the list includes `supabase`).
