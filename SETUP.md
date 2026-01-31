# Quick Setup Guide

## Local Testing

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app:**
   ```bash
   streamlit run app.py
   ```

3. **Open your browser:**
   The app will automatically open at `http://localhost:8501`

## Deploy to Streamlit Community Cloud

### Step 1: Initialize Git Repository
```bash
cd USA_CA_TRIP
git init
git add .
git commit -m "Initial commit: USA CA Trip Planner"
```

### Step 2: Create GitHub Repository
1. Go to [GitHub](https://github.com) and create a new repository
2. Name it (e.g., `USA_CA_TRIP`)
3. **Don't** initialize with README, .gitignore, or license

### Step 3: Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/USA_CA_TRIP.git
git branch -M main
git push -u origin main
```

### Step 4: Deploy to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click **"New app"**
4. Fill in:
   - **Repository**: Select your `USA_CA_TRIP` repository
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Click **"Deploy"**

The app will be live at: `https://YOUR_APP_NAME.streamlit.app`

## First Time Using the App

1. **Add your places**: Go to the Interactive Map and add all the places you want to visit
2. **Enter trip info**: Add your flight and hotel details in Trip Info
3. **Create packing lists**: Use Before Trip tab to add items for each person
4. **Set budget**: Enter your total budget in Budget Tracker
5. **Add to-dos**: Create your trip to-do list

## Tips

- The app saves all data automatically
- You can add photos to places (they'll be stored locally)
- Use the map to visualize your entire trip route
- Mark places as "completed" after visiting them
- Track expenses in real-time during your trip

## Troubleshooting

**Issue**: Map not showing
- Make sure `folium` and `streamlit-folium` are installed
- Check your internet connection (map tiles load from the web)

**Issue**: Data not saving
- Make sure the `data/` directory exists and is writable
- On Streamlit Cloud, **data is lost when the app sleeps**. To keep data across restarts, set up the **Supabase database** – see **[DATABASE_SETUP.md](DATABASE_SETUP.md)** for step-by-step instructions.

**Issue**: App won't run
- Check Python version (requires Python 3.7+)
- Verify all dependencies are installed: `pip install -r requirements.txt`

