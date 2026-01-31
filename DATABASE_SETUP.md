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

## Troubleshooting

- **“relation app_data does not exist”**  
  Run the SQL from Step 3 in the Supabase SQL Editor and make sure it completes without errors.

- **“new row violates row-level security”**  
  Make sure you created the RLS policy exactly as in Step 3 (policy name can differ, but it must allow `anon` to `select`/`insert`/`update`/`delete` on `app_data`).

- **Data still disappears on Streamlit Cloud**  
  Check that in **App settings → Secrets** you have both `SUPABASE_URL` and `SUPABASE_KEY` set (no typos, no extra spaces). Redeploy after changing secrets.

- **Local app: “No module named 'supabase'”**  
  Run: `pip install -r requirements.txt` (the list includes `supabase`).
