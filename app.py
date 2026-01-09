import streamlit as st
import json
import os
from datetime import datetime, timedelta
import folium
from streamlit_folium import st_folium
from PIL import Image
import io
import base64
import pandas as pd
import altair as alt
import math
import requests

# Page configuration
st.set_page_config(
    page_title="USA CA Trip Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Data file paths
DATA_DIR = "data"
PHOTOS_DIR = os.path.join(DATA_DIR, "photos")
PLACES_FILE = os.path.join(DATA_DIR, "places.json")
TODO_FILE = os.path.join(DATA_DIR, "todo.json")
TRIP_INFO_FILE = os.path.join(DATA_DIR, "trip_info.json")
PACKING_FILE = os.path.join(DATA_DIR, "packing.json")
BUDGET_FILE = os.path.join(DATA_DIR, "budget.json")
NOTES_FILE = os.path.join(DATA_DIR, "notes.json")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
WEATHER_FILE = os.path.join(DATA_DIR, "weather.json")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PHOTOS_DIR, exist_ok=True)

# Initialize default data
def init_default_data():
    """Initialize default data files if they don't exist"""
    
    # Default places (attractions and restaurants)
    if not os.path.exists(PLACES_FILE):
        default_places = {
            "places": [
                {
                    "id": 1,
                    "name": "Hollywood Walk of Fame",
                    "type": "attraction",
                    "lat": 34.1016,
                    "lon": -118.3269,
                    "description": "Famous sidewalk with stars honoring celebrities",
                    "photo": None,
                    "day": None,
                    "completed": False
                },
                {
                    "id": 2,
                    "name": "Griffith Observatory",
                    "type": "attraction",
                    "lat": 34.1183,
                    "lon": -118.3003,
                    "description": "Iconic observatory with stunning views of LA",
                    "photo": None,
                    "day": None,
                    "completed": False
                },
                {
                    "id": 3,
                    "name": "Las Vegas Strip",
                    "type": "attraction",
                    "lat": 36.1215,
                    "lon": -115.1739,
                    "description": "Famous 4.2-mile stretch of Las Vegas Boulevard",
                    "photo": None,
                    "day": None,
                    "completed": False
                },
                {
                    "id": 4,
                    "name": "Grand Canyon National Park",
                    "type": "attraction",
                    "lat": 36.1069,
                    "lon": -112.1129,
                    "description": "One of the world's most spectacular natural wonders",
                    "photo": None,
                    "day": None,
                    "completed": False
                },
                {
                    "id": 5,
                    "name": "San Diego Zoo",
                    "type": "attraction",
                    "lat": 32.7353,
                    "lon": -117.1490,
                    "description": "World-famous zoo with over 3,700 animals",
                    "photo": None,
                    "day": None,
                    "completed": False
                },
                {
                    "id": 6,
                    "name": "Palm Springs Aerial Tramway",
                    "type": "attraction",
                    "lat": 33.8153,
                    "lon": -116.6200,
                    "description": "Scenic tramway to Mount San Jacinto",
                    "photo": None,
                    "day": None,
                    "completed": False
                }
            ]
        }
        with open(PLACES_FILE, 'w') as f:
            json.dump(default_places, f, indent=2)
    
    # Default trip info
    if not os.path.exists(TRIP_INFO_FILE):
        default_trip_info = {
            "flights": [],
            "hotels": []
        }
        with open(TRIP_INFO_FILE, 'w') as f:
            json.dump(default_trip_info, f, indent=2)
    
    # Default todo list
    if not os.path.exists(TODO_FILE):
        default_todo = {"items": []}
        with open(TODO_FILE, 'w') as f:
            json.dump(default_todo, f, indent=2)
    
    # Default users list
    if not os.path.exists(USERS_FILE):
        default_users = ["Piotr", "Weronika", "Magda", "Marek", "Przemek"]
        with open(USERS_FILE, 'w') as f:
            json.dump({"users": default_users}, f, indent=2)
    
    # Default packing lists (will be initialized based on users)
    if not os.path.exists(PACKING_FILE):
        users_data = load_users()
        default_packing = {user: [] for user in users_data.get("users", [])}
        with open(PACKING_FILE, 'w') as f:
            json.dump(default_packing, f, indent=2)
    
    # Default budget
    if not os.path.exists(BUDGET_FILE):
        default_budget = {
            "expenses": []
        }
        with open(BUDGET_FILE, 'w') as f:
            json.dump(default_budget, f, indent=2)
    
    # Default notes
    if not os.path.exists(NOTES_FILE):
        default_notes = {"notes": []}
        with open(NOTES_FILE, 'w') as f:
            json.dump(default_notes, f, indent=2)

# Load data functions
def load_places():
    if os.path.exists(PLACES_FILE):
        with open(PLACES_FILE, 'r') as f:
            return json.load(f)
    return {"places": []}

def save_places(data):
    with open(PLACES_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def load_todo():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, 'r') as f:
            return json.load(f)
    return {"items": []}

def save_todo(data):
    with open(TODO_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def load_trip_info():
    if os.path.exists(TRIP_INFO_FILE):
        with open(TRIP_INFO_FILE, 'r') as f:
            return json.load(f)
    return {"flights": {}, "hotels": []}

def save_trip_info(data):
    with open(TRIP_INFO_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def load_packing():
    if os.path.exists(PACKING_FILE):
        with open(PACKING_FILE, 'r') as f:
            return json.load(f)
    return {"Piotr": [], "Weronika": [], "Magda": [], "Marek": [], "Przemek": []}

def save_packing(data):
    with open(PACKING_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def load_budget():
    if os.path.exists(BUDGET_FILE):
        with open(BUDGET_FILE, 'r') as f:
            return json.load(f)
    return {"expenses": []}

def save_budget(data):
    with open(BUDGET_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, 'r') as f:
            return json.load(f)
    return {"notes": []}

def save_notes(data):
    with open(NOTES_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {"users": []}

def save_users(data):
    with open(USERS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def load_weather():
    if os.path.exists(WEATHER_FILE):
        with open(WEATHER_FILE, 'r') as f:
            return json.load(f)
    return {"forecasts": []}

def save_weather(data):
    with open(WEATHER_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_city_from_coordinates(lat, lon):
    """Get city name from coordinates using Nominatim (OpenStreetMap) - free, no API key"""
    try:
        url = "https://nominatim.openstreetmap.org/reverse"
        params = {
            "lat": lat,
            "lon": lon,
            "format": "json",
            "addressdetails": 1
        }
        headers = {
            "User-Agent": "USA_Trip_Planner/1.0"
        }
        response = requests.get(url, params=params, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            address = data.get("address", {})
            # Try to get city name (can be city, town, village, or municipality)
            city = address.get("city") or address.get("town") or address.get("village") or address.get("municipality")
            if city:
                return city
            # Fallback to county or state
            return address.get("county") or address.get("state", "Unknown")
    except:
        pass
    return None

def geocode_city_name(city_name):
    """Validate and geocode city name using Open-Meteo Geocoding API"""
    try:
        url = "https://geocoding-api.open-meteo.com/v1/search"
        params = {
            "name": city_name,
            "count": 1,
            "language": "en"
        }
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            if results:
                result = results[0]
                return {
                    "name": result.get("name", city_name),
                    "lat": result.get("latitude"),
                    "lon": result.get("longitude"),
                    "country": result.get("country", ""),
                    "admin1": result.get("admin1", "")  # State/Province
                }
    except Exception as e:
        pass
    return None

def group_places_by_city(places):
    """Group places by city name and calculate average coordinates"""
    city_groups = {}
    
    for place in places:
        if place.get("lat") and place.get("lon"):
            # Try to get city name from coordinates
            city_name = get_city_from_coordinates(place.get("lat"), place.get("lon"))
            
            if not city_name:
                # Fallback: use place name or "Unknown"
                city_name = place.get("name", "Unknown")
            
            if city_name not in city_groups:
                city_groups[city_name] = {
                    "name": city_name,
                    "places": [],
                    "lats": [],
                    "lons": [],
                    "dates": set()
                }
            
            city_groups[city_name]["places"].append(place)
            city_groups[city_name]["lats"].append(place.get("lat"))
            city_groups[city_name]["lons"].append(place.get("lon"))
            
            # Collect dates
            if place.get("day"):
                try:
                    date_obj = datetime.strptime(place.get("day"), "%Y-%m-%d").date()
                    city_groups[city_name]["dates"].add(date_obj)
                except:
                    pass
    
    # Calculate average coordinates for each city
    for city_name, city_data in city_groups.items():
        if city_data["lats"] and city_data["lons"]:
            city_data["lat"] = sum(city_data["lats"]) / len(city_data["lats"])
            city_data["lon"] = sum(city_data["lons"]) / len(city_data["lons"])
            city_data["dates"] = sorted(list(city_data["dates"]))
        else:
            city_data["lat"] = None
            city_data["lon"] = None
    
    return city_groups

def get_weather_from_api(lat, lon, date):
    """Fetch weather data from Open-Meteo API (free, no API key required)"""
    try:
        # Open-Meteo API - completely free, no API key needed
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "daily": "temperature_2m_max,temperature_2m_min,weathercode,precipitation_sum,windspeed_10m_max,winddirection_10m_dominant",
            "temperature_unit": "fahrenheit",
            "windspeed_unit": "mph",
            "precipitation_unit": "inch",
            "timezone": "auto",
            "forecast_days": 16  # Get 16-day forecast
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            daily = data.get("daily", {})
            
            # Find the forecast for the requested date
            dates = daily.get("time", [])
            target_date_str = date.strftime("%Y-%m-%d")
            
            if target_date_str in dates:
                idx = dates.index(target_date_str)
                
                # Weather code mapping (WMO codes)
                weather_codes = {
                    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
                    45: "Foggy", 48: "Depositing rime fog",
                    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
                    56: "Light freezing drizzle", 57: "Dense freezing drizzle",
                    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
                    66: "Light freezing rain", 67: "Heavy freezing rain",
                    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
                    77: "Snow grains", 80: "Slight rain showers", 81: "Moderate rain showers",
                    82: "Violent rain showers", 85: "Slight snow showers", 86: "Heavy snow showers",
                    95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
                }
                
                weathercode = daily.get("weathercode", [0])[idx] if idx < len(daily.get("weathercode", [])) else 0
                condition = weather_codes.get(weathercode, "Unknown")
                
                # Simplify condition for display
                if weathercode in [0, 1]:
                    condition_short = "Clear"
                elif weathercode in [2, 3]:
                    condition_short = "Cloudy"
                elif weathercode in [45, 48]:
                    condition_short = "Foggy"
                elif weathercode in [51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82]:
                    condition_short = "Rain"
                elif weathercode in [71, 73, 75, 77, 85, 86]:
                    condition_short = "Snow"
                elif weathercode in [95, 96, 99]:
                    condition_short = "Thunderstorm"
                else:
                    condition_short = "Unknown"
                
                temp_max = daily.get("temperature_2m_max", [0])[idx] if idx < len(daily.get("temperature_2m_max", [])) else 0
                temp_min = daily.get("temperature_2m_min", [0])[idx] if idx < len(daily.get("temperature_2m_min", [])) else 0
                temp_avg = (temp_max + temp_min) / 2
                
                precipitation = daily.get("precipitation_sum", [0])[idx] if idx < len(daily.get("precipitation_sum", [])) else 0
                wind_speed = daily.get("windspeed_10m_max", [0])[idx] if idx < len(daily.get("windspeed_10m_max", [])) else 0
                wind_direction = daily.get("winddirection_10m_dominant", [0])[idx] if idx < len(daily.get("winddirection_10m_dominant", [])) else 0
                
                return {
                    "temperature": round(temp_avg),
                    "temp_max": round(temp_max),
                    "temp_min": round(temp_min),
                    "feels_like": round(temp_avg),  # Open-Meteo doesn't provide feels_like, use average
                    "condition": condition_short,
                    "description": condition,
                    "precipitation": round(precipitation, 2),
                    "wind_speed": round(wind_speed),
                    "wind_direction": round(wind_direction),
                    "weathercode": weathercode,
                    "forecast_time": target_date_str
                }
            else:
                return None
        else:
            return None
    except Exception as e:
        st.error(f"Error fetching weather: {str(e)}")
        return None
    
    return None

# Distance calculation functions
def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points using Haversine formula (in miles)"""
    R = 3959  # Earth radius in miles
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

def calculate_route_distance(places_list):
    """Calculate total distance for a route through multiple places"""
    if len(places_list) < 2:
        return 0
    total = 0
    for i in range(len(places_list) - 1):
        p1 = places_list[i]
        p2 = places_list[i + 1]
        total += haversine_distance(p1['lat'], p1['lon'], p2['lat'], p2['lon'])
    return total

def estimate_travel_time(distance_miles, mode="driving"):
    """Estimate travel time based on distance and mode"""
    if mode == "driving":
        avg_speed = 60  # mph
    else:  # walking
        avg_speed = 3  # mph
    hours = distance_miles / avg_speed
    return hours

# Photo helper functions
def save_photo(uploaded_file, place_id):
    """Save uploaded photo and return the file path"""
    if uploaded_file is not None:
        # Get file extension
        file_ext = os.path.splitext(uploaded_file.name)[1]
        photo_path = os.path.join(PHOTOS_DIR, f"place_{place_id}{file_ext}")
        
        # Save the file
        with open(photo_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        return photo_path
    return None

def get_photo_base64(photo_path):
    """Convert photo to base64 for HTML display"""
    if photo_path and os.path.exists(photo_path):
        with open(photo_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

def display_photo_in_streamlit(photo_path):
    """Display photo in Streamlit"""
    if photo_path and os.path.exists(photo_path):
        img = Image.open(photo_path)
        st.image(img, width=300)

# Translation dictionaries
TRANSLATIONS = {
    "en": {
        "title": "✈️ USA Trip Planner",
        "subtitle": "Your all-in-one trip planning companion",
        "nav": "Navigation",
        "choose_page": "Choose a page",
        "map": "🗺️ Interactive Map",
        "todo": "✅ To-Do List",
        "trip_info": "📋 Trip Info",
        "before_trip": "🎒 Before Trip",
        "budget": "💰 Budget Tracker",
        "notes": "📝 Notes",
        "users": "👥 Users",
        "weather": "🌤️ Weather",
        "routes": "🗺️ Routes & Distance",
        "language": "Language",
        "english": "English",
        "polish": "Polish",
        # Common
        "add": "Add",
        "delete": "Delete",
        "save": "Save",
        "cancel": "Cancel",
        "edit": "Edit",
        "close": "Close",
        "name": "Name",
        "description": "Description",
        "date": "Date",
        "time": "Time",
        "type": "Type",
        "amount": "Amount",
        "category": "Category",
        "total": "Total",
        "filter": "Filter",
        "all": "All",
        "completed": "Completed",
        "active": "Active",
        # Map
        "map_header": "🗺️ Interactive Map",
        "map_instructions": "Click on markers to see details. Green = completed, Blue = to visit, Red = restaurant",
        "filter_by_date": "📅 Filter by Date",
        "all_dates": "All Dates",
        "unassigned": "Unassigned",
        "showing_places": "Showing {} of {} places",
        "manage_places": "Manage Places",
        "add_new_place": "Add New Place",
        "place_name": "Place Name",
        "place_type": "Type",
        "attraction": "attraction",
        "restaurant": "restaurant",
        "latitude": "Latitude",
        "longitude": "Longitude",
        "optional": "optional",
        "upload_photo": "Upload Photo",
        "existing_places": "Existing Places",
        "mark_as_completed": "Mark as completed",
        "update_photo": "Update Photo",
        "no_places": "No places added yet. Add your first place using the form on the left!",
        "unassign": "Unassign",
        "location": "Location",
        "no_description": "No description",
        "find_coordinates": "Find Coordinates",
        "coordinates_found": "Coordinates found:",
        "coordinates_not_found": "Could not find coordinates for this place. Please enter coordinates manually.",
        "places_without_coordinates": "Places Without Coordinates",
        "geocode_place": "Find Location",
        "enter_place_name": "Enter place name to find coordinates",
        # To-Do
        "todo_header": "✅ To-Do List",
        "new_todo_item": "New to-do item",
        "priority": "Priority",
        "low": "Low",
        "medium": "Medium",
        "high": "High",
        "add_item": "Add Item",
        "todo_empty": "Your to-do list is empty! Add your first item above.",
        # Trip Info
        "trip_info_header": "📋 Trip Information",
        "flights": "✈️ Flights",
        "add_flight": "Add Flight",
        "flight_type": "Flight Type",
        "outbound": "Outbound",
        "return": "Return",
        "domestic": "Domestic (US)",
        "from": "From",
        "to": "To",
        "airline": "Airline",
        "flight_number": "Flight Number",
        "landing_time": "Landing Time",
        "duration": "Duration",
        "duration_hours": "hours",
        "duration_minutes": "minutes",
        "your_flights": "Your Flights",
        "delete_flight": "Delete Flight",
        "no_flights": "No flights added yet. Add your first flight above!",
        "hotels": "🏨 Hotels",
        "add_hotel": "Add Hotel",
        "hotel_name": "Hotel Name",
        "location": "Location",
        "check_in": "Check-in Date",
        "check_out": "Check-out Date",
        "confirmation": "Confirmation Number",
        "room_info": "Room Info (e.g., 2 rooms, 4 people)",
        "no_hotels": "No hotels added yet. Add your first hotel above!",
        # Before Trip
        "before_trip_header": "🎒 Before Trip Checklist",
        "manage_packing": "Manage packing lists for each traveler",
        "packing_list": "'s Packing List",
        "add_item_pack": "Add item to pack",
        "packed": "Packed",
        "no_items": "No items in {}'s packing list yet. Add items above!",
        "no_users_packing": "No users added yet! Please add users in the Users page first.",
        # Budget
        "budget_header": "💰 Expense Tracker",
        "track_expenses": "Track expenses per person and per category",
        "total_expenses": "Total Expenses",
        "number_expenses": "Number of Expenses",
        "expense_desc": "Description",
        "amount_usd": "Amount (USD)",
        "split_expense": "Split this expense among people",
        "select_people": "Select people to split with",
        "add_expense": "Add Expense",
        "expenses_by_category": "📊 By Category",
        "expenses_by_person": "👥 By Person",
        "all_expenses": "📝 All Expenses",
        "expenses_by_category_header": "Expenses by Category",
        "category_breakdown": "Category Breakdown",
        "expenses_by_person_header": "Expenses by Person",
        "per_person_breakdown": "Per-Person Breakdown",
        "expense": "expense(s)",
        "split_among": "Split among",
        "per_person": "Per person",
        "group_expense": "Group expense (not split)",
        "no_expenses": "No expenses tracked yet. Add expenses and mark them as 'split' to see per-person totals.",
        "no_users_budget": "No users added yet! Add users in the Users page to track expenses per person.",
        "no_expenses_recorded": "No expenses recorded yet. Add your first expense above!",
        "food": "Food",
        "transportation": "Transportation",
        "accommodation": "Accommodation",
        "activities": "Activities",
        "shopping": "Shopping",
        "other": "Other",
        # Notes
        "notes_header": "📝 Trip Notes",
        "keep_notes": "Keep notes, ideas, and reminders for your trip",
        "note_title": "Note Title",
        "note_content": "Note Content",
        "note_link": "Link (optional)",
        "add_note": "Add Note",
        "no_notes": "No notes yet. Add your first note above!",
        "edit_flight": "Edit Flight",
        "save_changes": "Save Changes",
        "place_link": "Link (optional)",
        # Users
        "users_header": "👥 Manage Users",
        "users_description": "Add or remove users. This list is used in Budget Tracker and Before Trip sections.",
        "user_name": "User Name",
        "add_user": "Add User",
        "users_count": "Users ({})",
        "no_users": "No users added yet. Add your first user above!",
        "default_users": "Default users: The app will use default users (Piotr, Weronika, Magda, Marek, Przemek) until you add your own users.",
        "route": "Route",
        "items": "items",
        "please_select_photo": "Please select a photo to upload",
        "already_in_list": "is already in the list!",
        "please_enter_name": "Please enter a user name!",
        # Weather
        "weather_header": "🌤️ Weather Forecast",
        "weather_description": "Check weather for your trip locations and dates",
        "select_location": "Select Location",
        "select_date": "Select Date",
        "get_weather": "Get Weather",
        "or_enter_city": "Or Enter City Name",
        "enter_city_name": "Enter City Name",
        "city_not_found": "City not found. Please check the spelling and try again.",
        "city_found": "City found:",
        "select_city_or_place": "Select City or Place",
        "manual_city": "Manual City Input",
        "temperature": "Temperature",
        "condition": "Condition",
        "humidity": "Humidity",
        "wind": "Wind",
        "weather_link": "View Full Forecast",
        "no_weather_data": "No weather data available. Click 'Get Weather' to fetch forecast.",
        "get_weather_forecast": "Get Weather Forecast",
        "feels_like": "Feels Like",
        "wind_direction": "Wind Direction",
        "forecast_time": "Forecast Time",
        "weather_condition": "Condition",
        "wind_speed": "Wind Speed",
        "mph": "mph",
        "hpa": "hpa",
        "degrees": "°",
        "fahrenheit": "°F",
        # Routes
        "routes_header": "🗺️ Routes & Distance Calculator",
        "routes_description": "Calculate distances and plan routes between your places",
        "select_from": "From",
        "select_to": "To",
        "calculate_distance": "Calculate Distance",
        "distance": "Distance",
        "estimated_time": "Estimated Travel Time",
        "route_optimization": "Route Optimization",
        "optimize_route": "Optimize Route",
        "route_order": "Optimized Route Order",
        "total_distance": "Total Distance",
        "total_time": "Total Travel Time",
        "no_places": "Add at least 2 places to calculate distances",
        "miles": "miles",
        "km": "km",
        "hours": "hours",
        "minutes": "minutes",
        "driving": "Driving",
        "walking": "Walking",
    },
    "pl": {
        "title": "✈️ Planer Podrozy USA",
        "subtitle": "Twoj kompletny planer podrozy",
        "nav": "Nawigacja",
        "choose_page": "Wybierz strone",
        "map": "🗺️ Interaktywna Mapa",
        "todo": "✅ Lista Zadan",
        "trip_info": "📋 Informacje o Podrozy",
        "before_trip": "🎒 Przed Podroza",
        "budget": "💰 Sledzenie Wydatkow",
        "notes": "📝 Notatki",
        "users": "👥 Uzytkownicy",
        "weather": "🌤️ Pogoda",
        "routes": "🗺️ Trasy i Odleglosci",
        "language": "Jezyk",
        "english": "English",
        "polish": "Polski",
        # Common
        "add": "Dodaj",
        "delete": "Usun",
        "save": "Zapisz",
        "cancel": "Anuluj",
        "edit": "Edytuj",
        "close": "Zamknij",
        "name": "Nazwa",
        "description": "Opis",
        "date": "Data",
        "time": "Godzina",
        "type": "Typ",
        "amount": "Kwota",
        "category": "Kategoria",
        "total": "Suma",
        "filter": "Filtruj",
        "all": "Wszystkie",
        "completed": "Zakonczone",
        "active": "Aktywne",
        # Map
        "map_header": "🗺️ Interaktywna Mapa",
        "map_instructions": "Kliknij na znaczniki, aby zobaczyc szczegoly. Zielony = zakonczone, Niebieski = do odwiedzenia, Czerwony = restauracja",
        "filter_by_date": "📅 Filtruj wedlug Daty",
        "all_dates": "Wszystkie Daty",
        "unassigned": "Nieprzypisane",
        "showing_places": "Pokazuje {} z {} miejsc",
        "manage_places": "Zarzadzaj Miejscami",
        "add_new_place": "Dodaj Nowe Miejsce",
        "place_name": "Nazwa Miejsca",
        "place_type": "Typ",
        "attraction": "atrakcja",
        "restaurant": "restauracja",
        "latitude": "Szerokosc Geograficzna",
        "longitude": "Dlugosc Geograficzna",
        "optional": "opcjonalne",
        "upload_photo": "Wgraj Zdjecie",
        "existing_places": "Istniejace Miejsca",
        "mark_as_completed": "Oznacz jako zakonczone",
        "update_photo": "Aktualizuj Zdjecie",
        "no_places": "Nie dodano jeszcze miejsc. Dodaj pierwsze miejsce uzywajac formularza po lewej!",
        "unassign": "Usun przypisanie",
        "location": "Lokalizacja",
        "no_description": "Brak opisu",
        "find_coordinates": "Znajdz Wspolrzedne",
        "coordinates_found": "Znalezione wspolrzedne:",
        "coordinates_not_found": "Nie mozna znalezc wspolrzednych dla tego miejsca. Wprowadz wspolrzedne recznie.",
        "places_without_coordinates": "Miejsca Bez Wspolrzednych",
        "geocode_place": "Znajdz Lokalizacje",
        "enter_place_name": "Wprowadz nazwe miejsca, aby znalezc wspolrzedne",
        # To-Do
        "todo_header": "✅ Lista Zadan",
        "new_todo_item": "Nowe zadanie",
        "priority": "Priorytet",
        "low": "Niski",
        "medium": "Sredni",
        "high": "Wysoki",
        "add_item": "Dodaj Zadanie",
        "todo_empty": "Twoja lista zadan jest pusta! Dodaj pierwsze zadanie powyzej.",
        # Trip Info
        "trip_info_header": "📋 Informacje o Podrozy",
        "flights": "✈️ Loty",
        "add_flight": "Dodaj Lot",
        "flight_type": "Typ Lotu",
        "outbound": "Wylot",
        "return": "Powrot",
        "domestic": "Krajowy (USA)",
        "from": "Z",
        "to": "Do",
        "airline": "Linia Lotnicza",
        "flight_number": "Numer Lotu",
        "landing_time": "Czas Ladowania",
        "duration": "Czas Trwania",
        "duration_hours": "godzin",
        "duration_minutes": "minut",
        "your_flights": "Twoje Loty",
        "delete_flight": "Usun Lot",
        "no_flights": "Nie dodano jeszcze lotow. Dodaj pierwszy lot powyzej!",
        "hotels": "🏨 Hotele",
        "add_hotel": "Dodaj Hotel",
        "hotel_name": "Nazwa Hotelu",
        "location": "Lokalizacja",
        "check_in": "Data Zameldowania",
        "check_out": "Data Wymeldowania",
        "confirmation": "Numer Potwierdzenia",
        "room_info": "Informacje o Pokoju (np. 2 pokoje, 4 osoby)",
        "no_hotels": "Nie dodano jeszcze hoteli. Dodaj pierwszy hotel powyzej!",
        # Before Trip
        "before_trip_header": "🎒 Lista Przed Podroza",
        "manage_packing": "Zarzadzaj listami pakowania dla kazdego podroznika",
        "packing_list": " Lista Pakowania",
        "add_item_pack": "Dodaj przedmiot do spakowania",
        "packed": "Spakowane",
        "no_items": "Brak przedmiotow na liscie pakowania {}. Dodaj przedmioty powyzej!",
        "no_users_packing": "Nie dodano jeszcze uzytkownikow! Prosze dodac uzytkownikow na stronie Uzytkownicy najpierw.",
        # Budget
        "budget_header": "💰 Sledzenie Wydatkow",
        "track_expenses": "Sledz wydatki na osobe i kategorie",
        "total_expenses": "Laczne Wydatki",
        "number_expenses": "Liczba Wydatkow",
        "expense_desc": "Opis",
        "amount_usd": "Kwota (USD)",
        "split_expense": "Podziel ten wydatek miedzy osoby",
        "select_people": "Wybierz osoby do podzialu",
        "add_expense": "Dodaj Wydatek",
        "expenses_by_category": "📊 Wedlug Kategorii",
        "expenses_by_person": "👥 Wedlug Osoby",
        "all_expenses": "📝 Wszystkie Wydatki",
        "expenses_by_category_header": "Wydatki wedlug Kategorii",
        "category_breakdown": "Podzial Kategorii",
        "expenses_by_person_header": "Wydatki wedlug Osoby",
        "per_person_breakdown": "Podzial na Osobe",
        "expense": "wydatek(ow)",
        "split_among": "Podzielone miedzy",
        "per_person": "Na osobe",
        "group_expense": "Wydatek grupowy (niepodzielony)",
        "no_expenses": "Nie sledzono jeszcze wydatkow. Dodaj wydatki i oznacz je jako 'podzielone', aby zobaczyc sumy na osobe.",
        "no_users_budget": "Nie dodano jeszcze uzytkownikow! Dodaj uzytkownikow na stronie Uzytkownicy, aby sledzic wydatki na osobe.",
        "no_expenses_recorded": "Nie zarejestrowano jeszcze wydatkow. Dodaj pierwszy wydatek powyzej!",
        "food": "Jedzenie",
        "transportation": "Transport",
        "accommodation": "Nocleg",
        "activities": "Atrakcje",
        "shopping": "Zakupy",
        "other": "Inne",
        # Notes
        "notes_header": "📝 Notatki z Podrozy",
        "keep_notes": "Przechowuj notatki, pomysly i przypomnienia do swojej podrozy",
        "note_title": "Tytul Notatki",
        "note_content": "Tresc Notatki",
        "note_link": "Link (opcjonalnie)",
        "add_note": "Dodaj Notatke",
        "no_notes": "Brak notatek. Dodaj pierwsza notatke powyzej!",
        "edit_flight": "Edytuj Lot",
        "save_changes": "Zapisz Zmiany",
        "place_link": "Link (opcjonalnie)",
        # Users
        "users_header": "👥 Zarzadzaj Uzytkownikami",
        "users_description": "Dodaj lub usun uzytkownikow. Ta lista jest uzywana w Sledzeniu Wydatkow i Przed Podroza.",
        "user_name": "Nazwa Uzytkownika",
        "add_user": "Dodaj Uzytkownika",
        "users_count": "Uzytkownicy ({})",
        "no_users": "Nie dodano jeszcze uzytkownikow. Dodaj pierwszego uzytkownika powyzej!",
        "default_users": "Domyślni uzytkownicy: Aplikacja bedzie uzywac domyslnych uzytkownikow (Piotr, Weronika, Magda, Marek, Przemek), dopoki nie dodasz wlasnych uzytkownikow.",
        "route": "Trasa",
        "items": "przedmiotow",
        "please_select_photo": "Prosze wybrac zdjecie do wgrania",
        "already_in_list": "jest juz na liscie!",
        "please_enter_name": "Prosze podac nazwe uzytkownika!",
        # Weather
        "weather_header": "🌤️ Prognoza Pogody",
        "weather_description": "Sprawdz pogode dla lokalizacji i dat twojej podrozy",
        "select_location": "Wybierz Lokalizacje",
        "select_date": "Wybierz Date",
        "get_weather": "Pobierz Pogode",
        "or_enter_city": "Lub Wprowadz Nazwe Miasta",
        "enter_city_name": "Wprowadz Nazwe Miasta",
        "city_not_found": "Miasto nie znalezione. Sprawdz pisownie i sprobuj ponownie.",
        "city_found": "Znalezione miasto:",
        "select_city_or_place": "Wybierz Miasto lub Miejsce",
        "manual_city": "Reczne Wprowadzenie Miasta",
        "temperature": "Temperatura",
        "condition": "Warunki",
        "humidity": "Wilgotnosc",
        "wind": "Wiatr",
        "weather_link": "Zobacz Pelna Prognoze",
        "no_weather_data": "Brak danych pogodowych. Kliknij 'Pobierz Pogode', aby pobrac prognoze.",
        "get_weather_forecast": "Pobierz Prognoze Pogody",
        "feels_like": "Odczuwalna",
        "wind_direction": "Kierunek Wiatru",
        "forecast_time": "Czas Prognozy",
        "weather_condition": "Warunki",
        "wind_speed": "Predkosc Wiatru",
        "mph": "mph",
        "hpa": "hpa",
        "degrees": "°",
        "fahrenheit": "°F",
        # Routes
        "routes_header": "🗺️ Kalkulator Tras i Odleglosci",
        "routes_description": "Oblicz odleglosci i planuj trasy miedzy miejscami",
        "select_from": "Z",
        "select_to": "Do",
        "calculate_distance": "Oblicz Odleglosc",
        "distance": "Odleglosc",
        "estimated_time": "Szacowany Czas Podrozy",
        "route_optimization": "Optymalizacja Trasy",
        "optimize_route": "Optymalizuj Trase",
        "route_order": "Zoptymalizowana Kolejnosc Trasy",
        "total_distance": "Laczna Odleglosc",
        "total_time": "Laczny Czas Podrozy",
        "no_places": "Dodaj co najmniej 2 miejsca, aby obliczyc odleglosci",
        "miles": "mil",
        "km": "km",
        "hours": "godzin",
        "minutes": "minut",
        "driving": "Jazda samochodem",
        "walking": "Pieszo",
    }
}

def t(key, lang="en"):
    """Get translation for a key"""
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)

# Initialize default data
init_default_data()

# Main app
def main():
    # Initialize language in session state
    if "language" not in st.session_state:
        st.session_state.language = "en"
    
    lang = st.session_state.language
    
    st.title(t("title", lang))
    st.markdown(f"**{t('subtitle', lang)}**")
    
    # Language selector in sidebar
    st.sidebar.markdown("---")
    selected_lang = st.sidebar.selectbox(
        t("language", lang),
        ["en", "pl"],
        index=0 if lang == "en" else 1,
        format_func=lambda x: t("english", x) if x == "en" else t("polish", x),
        key="lang_selector"
    )
    if selected_lang != lang:
        st.session_state.language = selected_lang
        st.rerun()
    
    # Sidebar navigation
    st.sidebar.markdown("---")
    st.sidebar.title(t("nav", lang))
    page = st.sidebar.radio(
        t("choose_page", lang),
        [t("users", lang), t("map", lang), t("todo", lang), t("trip_info", lang), t("before_trip", lang), t("budget", lang), t("weather", lang), t("notes", lang)]
    )
    
    # Get current language
    lang = st.session_state.language
    
    if page == t("map", lang) or "Map" in page:
        show_map(lang)
    elif page == t("todo", lang) or "To-Do" in page or "Zadan" in page:
        show_todo(lang)
    elif page == t("trip_info", lang) or "Trip Info" in page or "Podrozy" in page:
        show_trip_info(lang)
    elif page == t("before_trip", lang) or "Before Trip" in page or "Przed" in page:
        show_before_trip(lang)
    elif page == t("budget", lang) or "Budget" in page or "Wydatkow" in page:
        show_budget(lang)
    elif page == t("users", lang) or "Users" in page or "Uzytkownicy" in page:
        show_users(lang)
    elif page == t("weather", lang) or "Weather" in page or "Pogoda" in page:
        show_weather(lang)
    elif page == t("notes", lang) or "Notes" in page or "Notatki" in page:
        show_notes(lang)

def show_map(lang="en"):
    st.header(t("map_header", lang))
    st.markdown(t("map_instructions", lang))
    
    places_data = load_places()
    places = places_data.get("places", [])
    
    # Day filter with buttons
    st.subheader(t("filter_by_date", lang))
    
    # Get all unique dates from places
    all_dates = sorted(set([p.get("day") for p in places if p.get("day") is not None]))
    has_unassigned = any(p.get("day") is None for p in places)
    
    # Initialize session state for selected day filter
    if "selected_day_filter" not in st.session_state:
        st.session_state.selected_day_filter = "all"
    
    # Create button layout - first row with "All Days" and dates
    buttons_per_row = 8
    all_buttons = ["all"] + all_dates + (["unassigned"] if has_unassigned else [])
    
    # Split buttons into rows
    for row_start in range(0, len(all_buttons), buttons_per_row):
        row_buttons = all_buttons[row_start:row_start + buttons_per_row]
        cols = st.columns(len(row_buttons))
        
        for col, btn_value in zip(cols, row_buttons):
            with col:
                if btn_value == "all":
                    btn_label = t("all_dates", lang)
                    btn_key = "filter_all"
                elif btn_value == "unassigned":
                    btn_label = t("unassigned", lang)
                    btn_key = "filter_unassigned"
                else:
                    # Format date for display (e.g., "Feb 1" or "Feb 15")
                    try:
                        date_obj = datetime.strptime(btn_value, "%Y-%m-%d")
                        btn_label = date_obj.strftime("%b %d")
                    except:
                        btn_label = btn_value
                    btn_key = f"filter_date_{btn_value}"
                
                is_selected = st.session_state.selected_day_filter == btn_value
                if st.button(btn_label, key=btn_key, use_container_width=True,
                           type="primary" if is_selected else "secondary"):
                    st.session_state.selected_day_filter = btn_value
                    st.rerun()
    
    # Determine which date to filter by
    filter_day = None
    if st.session_state.selected_day_filter == "unassigned":
        filter_day = "unassigned"
    elif st.session_state.selected_day_filter != "all":
        filter_day = st.session_state.selected_day_filter
    
    # Filter places by day
    filtered_places = places
    if filter_day == "unassigned":
        filtered_places = [p for p in places if p.get("day") is None]
    elif filter_day is not None:
        filtered_places = [p for p in places if p.get("day") == filter_day]
    
    # Separate places with and without coordinates
    places_with_coords = [p for p in filtered_places if p.get("lat") is not None and p.get("lon") is not None]
    places_without_coords = [p for p in filtered_places if p.get("lat") is None or p.get("lon") is None]
    
    # Create map centered on the trip area
    m = folium.Map(
        location=[35.0, -117.0],
        zoom_start=6,
        tiles='OpenStreetMap'
    )
    
    # Add markers for each filtered place with coordinates
    for place in places_with_coords:
        # Determine marker color
        if place.get("completed", False):
            color = "green"
        elif place.get("type") == "restaurant":
            color = "red"
        else:
            color = "blue"
        
        # Get photo for popup
        photo_html = ""
        photo_path = place.get("photo")
        if photo_path and os.path.exists(photo_path):
            photo_b64 = get_photo_base64(photo_path)
            if photo_b64:
                photo_html = f'<img src="data:image/jpeg;base64,{photo_b64}" style="width: 100%; max-width: 280px; margin: 10px 0; border-radius: 5px;">'
        
        # Date info
        day_info = ""
        if place.get("day"):
            try:
                date_obj = datetime.strptime(place.get("day"), "%Y-%m-%d")
                formatted_date = date_obj.strftime("%B %d, %Y")
                day_info = f'<p><strong>Date:</strong> {formatted_date}</p>'
            except:
                day_info = f'<p><strong>Date:</strong> {place.get("day")}</p>'
        
        # Link info
        link_html = ""
        if place.get('link'):
            link_html = f'<p><strong>Link:</strong> <a href="{place["link"]}" target="_blank">{place["link"]}</a></p>'
        
        # Create popup content
        popup_html = f"""
        <div style="width: 300px;">
            <h3>{place['name']}</h3>
            {photo_html}
            <p><strong>Type:</strong> {place.get('type', 'attraction').title()}</p>
            {day_info}
            <p>{place.get('description', 'No description available')}</p>
            {link_html}
        </div>
        """
        
        folium.Marker(
            location=[place['lat'], place['lon']],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=place['name'],
            icon=folium.Icon(color=color, icon='info-sign')
        ).add_to(m)
    
    # Display map
    st.info(t("showing_places", lang).format(len(places_with_coords), len(filtered_places)))
    map_data = st_folium(m, width=1200, height=600)
    
    # Show places without coordinates
    if places_without_coords:
        st.divider()
        st.subheader(t("places_without_coordinates", lang))
        st.info(f"These {len(places_without_coords)} place(s) don't have coordinates and can't be shown on the map. Use the 'Find Location' button to add coordinates.")
        
        for place in places_without_coords:
            with st.expander(f"📍 {place['name']} ({place.get('type', 'attraction')})"):
                st.write(f"**{t('description', lang)}:** {place.get('description', '')}")
                
                # Geocode button
                col1, col2 = st.columns([3, 1])
                with col1:
                    geocode_name = st.text_input(
                        t("enter_place_name", lang),
                        value=place['name'],
                        key=f"geocode_name_{place['id']}"
                    )
                with col2:
                    if st.button(t("geocode_place", lang), key=f"geocode_{place['id']}"):
                        with st.spinner("Searching for location..."):
                            city_info = geocode_city_name(geocode_name.strip())
                            if city_info:
                                place["lat"] = city_info["lat"]
                                place["lon"] = city_info["lon"]
                                save_places(places_data)
                                st.success(f"✅ {t('coordinates_found', lang)} {city_info['lat']:.4f}, {city_info['lon']:.4f}")
                                st.rerun()
                            else:
                                st.error(t("coordinates_not_found", lang))
                
                # Manual coordinate input
                st.markdown("**Or enter coordinates manually:**")
                col1, col2 = st.columns(2)
                with col1:
                    manual_lat = st.number_input("Latitude", value=place.get("lat") or 0.0, format="%.6f", key=f"manual_lat_{place['id']}")
                with col2:
                    manual_lon = st.number_input("Longitude", value=place.get("lon") or 0.0, format="%.6f", key=f"manual_lon_{place['id']}")
                
                if st.button("Save Coordinates", key=f"save_coords_{place['id']}"):
                    if manual_lat != 0.0 or manual_lon != 0.0:
                        place["lat"] = manual_lat
                        place["lon"] = manual_lon
                        save_places(places_data)
                        st.success("Coordinates saved!")
                        st.rerun()
                    else:
                        st.warning("Please enter valid coordinates (not 0,0)")
    
    # Place management section
    st.divider()
    st.subheader(t("manage_places", lang))
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### {t('add_new_place', lang)}")
        
        # Geocoding section (outside form)
        place_name_for_geocode = st.text_input("Place name for coordinates lookup", key="geocode_place_name", placeholder="Enter place name to find coordinates")
        if place_name_for_geocode:
            if st.button(t("find_coordinates", lang), key="find_coords_new"):
                with st.spinner("Searching for location..."):
                    city_info = geocode_city_name(place_name_for_geocode.strip())
                    if city_info:
                        st.session_state.new_place_lat = city_info["lat"]
                        st.session_state.new_place_lon = city_info["lon"]
                        st.success(f"✅ {t('coordinates_found', lang)} {city_info['lat']:.4f}, {city_info['lon']:.4f}")
                    else:
                        st.error(t("coordinates_not_found", lang))
        
        with st.form("add_place_form"):
            place_name = st.text_input(t("place_name", lang))
            place_type = st.selectbox(t("place_type", lang), [t("attraction", lang), t("restaurant", lang)])
            
            # Coordinates section
            st.markdown("**Coordinates (optional):**")
            place_lat = st.number_input(
                t("latitude", lang) + f" ({t('optional', lang)})", 
                value=st.session_state.get("new_place_lat", 34.0522), 
                format="%.6f",
                key="new_place_lat_input"
            )
            place_lon = st.number_input(
                t("longitude", lang) + f" ({t('optional', lang)})", 
                value=st.session_state.get("new_place_lon", -118.2437), 
                format="%.6f",
                key="new_place_lon_input"
            )
            
            place_desc = st.text_area(t("description", lang))
            place_link = st.text_input(t("place_link", lang), placeholder="https://...")
            default_date = datetime.now().date()
            place_day_input = st.date_input(f"{t('date', lang)} ({t('optional', lang)})", value=default_date, key="new_place_day")
            place_day = place_day_input.strftime("%Y-%m-%d") if place_day_input else None
            place_photo = st.file_uploader(t("upload_photo", lang), type=['png', 'jpg', 'jpeg'])
            
            submitted = st.form_submit_button(t("add", lang) + " " + t("place_name", lang).split()[0] if " " in t("place_name", lang) else t("add", lang))
            if submitted and place_name:
                # Clear session state after use
                if "new_place_lat" in st.session_state:
                    del st.session_state.new_place_lat
                if "new_place_lon" in st.session_state:
                    del st.session_state.new_place_lon
                new_id = max([p.get("id", 0) for p in places] + [0]) + 1
                photo_path = None
                
                # Save photo if uploaded
                if place_photo is not None:
                    photo_path = save_photo(place_photo, new_id)
                
                new_place = {
                    "id": new_id,
                    "name": place_name,
                    "type": place_type,
                    "lat": place_lat if place_lat != 0.0 else None,
                    "lon": place_lon if place_lon != 0.0 else None,
                    "description": place_desc,
                    "link": place_link if place_link else None,
                    "day": place_day if place_day else None,
                    "photo": photo_path,
                    "completed": False
                }
                places.append(new_place)
                places_data["places"] = places
                save_places(places_data)
                st.success(f"{t('add', lang)} {place_name}!")
                st.rerun()
    
    with col2:
        st.markdown(f"### {t('existing_places', lang)}")
        if places:
            # Sort by date, then by name
            def sort_key(place):
                day = place.get("day")
                if day:
                    try:
                        date_obj = datetime.strptime(day, "%Y-%m-%d")
                        return (date_obj, place['name'])
                    except:
                        # If date parsing fails, use far future date
                        return (datetime(9999, 12, 31), place['name'])
                # Unassigned places go to the end
                return (datetime(9999, 12, 31), place['name'])
            sorted_places = sorted(places, key=sort_key)
            
            for place in sorted_places:
                # Format date label
                if place.get("day"):
                    try:
                        date_obj = datetime.strptime(place.get("day"), "%Y-%m-%d")
                        day_label = date_obj.strftime("%b %d, %Y")
                    except:
                        day_label = place.get("day")
                else:
                    day_label = t("unassigned", lang)
                expander_title = f"{place['name']} ({place.get('type', 'attraction')}) - {day_label}"
                
                with st.expander(expander_title):
                    # Display photo if exists
                    photo_path = place.get("photo")
                    if photo_path and os.path.exists(photo_path):
                        display_photo_in_streamlit(photo_path)
                    
                    st.write(f"**{t('description', lang)}:** {place.get('description', '')}")
                    if place.get('link'):
                        st.markdown(f"🔗 [Link]({place['link']})")
                    if place.get("lat") is not None and place.get("lon") is not None:
                        st.write(f"**{t('location', lang)}:** {place['lat']}, {place['lon']}")
                    else:
                        st.warning("⚠️ No coordinates - this place won't appear on the map")
                        # Quick geocode option
                        if st.button(t("find_coordinates", lang), key=f"quick_geocode_{place['id']}"):
                            with st.spinner("Searching..."):
                                city_info = geocode_city_name(place['name'])
                                if city_info:
                                    place["lat"] = city_info["lat"]
                                    place["lon"] = city_info["lon"]
                                    save_places(places_data)
                                    st.success(f"✅ {t('coordinates_found', lang)}")
                                    st.rerun()
                                else:
                                    st.error(t("coordinates_not_found", lang))
                    
                    # Date selector
                    current_day = place.get("day")
                    # Convert string date to date object for date_input
                    default_date = datetime.now().date()
                    if current_day:
                        try:
                            default_date = datetime.strptime(current_day, "%Y-%m-%d").date()
                        except:
                            default_date = datetime.now().date()
                    
                    unassign_date = st.checkbox(f"{t('unassign', lang)} {t('date', lang).lower()}", value=False, key=f"unassign_{place['id']}")
                    
                    if not unassign_date:
                        new_day_input = st.date_input(
                            t("date", lang),
                            value=default_date,
                            key=f"day_{place['id']}"
                        )
                        new_day = new_day_input.strftime("%Y-%m-%d") if new_day_input else None
                    else:
                        new_day = None
                    
                    if new_day != current_day:
                        place["day"] = new_day
                        save_places(places_data)
                        st.rerun()
                    
                    # Photo upload/update
                    st.markdown(f"**{t('update_photo', lang)}:**")
                    with st.form(f"photo_form_{place['id']}"):
                        new_photo = st.file_uploader(
                            t("upload_photo", lang),
                            type=['png', 'jpg', 'jpeg'],
                            key=f"photo_{place['id']}"
                        )
                        if st.form_submit_button(t("update_photo", lang)):
                            if new_photo is not None:
                                photo_path = save_photo(new_photo, place['id'])
                                place["photo"] = photo_path
                                save_places(places_data)
                                st.success(t("update_photo", lang) + "!")
                                st.rerun()
                            else:
                                st.warning(t("please_select_photo", lang))
                    
                    completed = st.checkbox(
                        t("mark_as_completed", lang),
                        value=place.get("completed", False),
                        key=f"completed_{place['id']}"
                    )
                    if completed != place.get("completed", False):
                        place["completed"] = completed
                        save_places(places_data)
                        st.rerun()
                    
                    if st.button(f"{t('delete', lang)} {place['name']}", key=f"delete_{place['id']}"):
                        # Delete photo file if exists
                        if place.get("photo") and os.path.exists(place.get("photo")):
                            try:
                                os.remove(place.get("photo"))
                            except:
                                pass
                        places.remove(place)
                        places_data["places"] = places
                        save_places(places_data)
                        st.rerun()
        else:
            st.info(t("no_places", lang))

def show_todo(lang="en"):
    st.header(t("todo_header", lang))
    
    todo_data = load_todo()
    items = todo_data.get("items", [])
    
    # Add new item
    with st.form("add_todo_form"):
        col1, col2 = st.columns([3, 1])
        with col1:
            new_item = st.text_input(t("new_todo_item", lang))
        with col2:
            priority = st.selectbox(t("priority", lang), [t("low", lang), t("medium", lang), t("high", lang)], key="priority_select")
        submitted = st.form_submit_button(t("add_item", lang))
        
        if submitted and new_item:
            items.append({
                "id": max([item.get("id", 0) for item in items] + [0]) + 1,
                "text": new_item,
                "completed": False,
                "priority": priority
            })
            todo_data["items"] = items
            save_todo(todo_data)
            st.rerun()
    
    st.divider()
    
    # Display items
    if items:
        # Filter options
        filter_option = st.radio(t("filter", lang), [t("all", lang), t("active", lang), t("completed", lang)], horizontal=True)
        
        filtered_items = items
        if filter_option == t("active", lang):
            filtered_items = [item for item in items if not item.get("completed", False)]
        elif filter_option == t("completed", lang):
            filtered_items = [item for item in items if item.get("completed", False)]
        
        # Sort by priority
        priority_order = {t("high", lang): 3, t("medium", lang): 2, t("low", lang): 1}
        filtered_items.sort(key=lambda x: (x.get("completed", False), -priority_order.get(x.get("priority", "Low"), 1)))
        
        for item in filtered_items:
            col1, col2, col3 = st.columns([1, 10, 1])
            with col1:
                completed = st.checkbox("", value=item.get("completed", False), key=f"todo_{item['id']}")
            with col2:
                if completed:
                    st.markdown(f"~~{item['text']}~~")
                else:
                    priority_emoji = {t("high", lang): "🔴", t("medium", lang): "🟡", t("low", lang): "🟢"}
                    default_priority = t("low", lang)
                    st.markdown(f"{priority_emoji.get(item.get('priority', default_priority), '🟢')} {item['text']}")
            with col3:
                if st.button("🗑️", key=f"del_{item['id']}"):
                    items.remove(item)
                    todo_data["items"] = items
                    save_todo(todo_data)
                    st.rerun()
            
            if completed != item.get("completed", False):
                item["completed"] = completed
                todo_data["items"] = items
                save_todo(todo_data)
                st.rerun()
    else:
        st.info(t("todo_empty", lang))

def show_trip_info(lang="en"):
    st.header(t("trip_info_header", lang))
    
    trip_info = load_trip_info()
    
    # Flights section
    st.subheader(t("flights", lang))
    
    # Handle migration from old format (dict) to new format (list)
    flights_data = trip_info.get("flights", [])
    if isinstance(flights_data, dict):
        # Old format - convert to list
        flights = []
        if "outbound" in flights_data:
            outbound = flights_data["outbound"]
            if outbound and isinstance(outbound, dict):
                flights.append({
                    "id": 1,
                    "date": outbound.get("date", ""),
                    "time": outbound.get("time", ""),
                    "airline": outbound.get("airline", ""),
                    "flight_number": outbound.get("flight_number", ""),
                    "from": outbound.get("from", ""),
                    "to": outbound.get("to", ""),
                    "type": "Outbound"
                })
        if "return" in flights_data:
            return_flight = flights_data["return"]
            if return_flight and isinstance(return_flight, dict):
                flights.append({
                    "id": 2,
                    "date": return_flight.get("date", ""),
                    "time": return_flight.get("time", ""),
                    "airline": return_flight.get("airline", ""),
                    "flight_number": return_flight.get("flight_number", ""),
                    "from": return_flight.get("from", ""),
                    "to": return_flight.get("to", ""),
                    "type": "Return"
                })
        trip_info["flights"] = flights
        save_trip_info(trip_info)
    else:
        flights = flights_data if isinstance(flights_data, list) else []
    
    # Add flight form
    with st.form("add_flight_form"):
        col1, col2 = st.columns(2)
        with col1:
            flight_date = st.date_input(t("date", lang))
            airline = st.text_input(t("airline", lang))
            flight_num = st.text_input(t("flight_number", lang))
            from_airport = st.text_input(t("from", lang))
        with col2:
            to_airport = st.text_input(t("to", lang))
            flight_type = st.selectbox(t("flight_type", lang), [t("outbound", lang), t("return", lang), t("domestic", lang)])
        
        # Time and landing time in the same row
        time_col1, time_col2 = st.columns(2)
        with time_col1:
            flight_time = st.time_input(t("time", lang))
        with time_col2:
            landing_time = st.time_input(t("landing_time", lang), value=datetime.now().time())
        
        # Duration input
        st.markdown("**" + t("duration", lang) + ":**")
        dur_col1, dur_col2 = st.columns(2)
        with dur_col1:
            duration_hours = st.number_input(t("duration_hours", lang), min_value=0, max_value=24, value=0, step=1)
        with dur_col2:
            duration_minutes = st.number_input(t("duration_minutes", lang), min_value=0, max_value=59, value=0, step=1)
        
        if st.form_submit_button(t("add_flight", lang)):
            # Format duration as "Xh Ym" or just "Xh" or "Ym"
            duration_str = ""
            if duration_hours > 0 and duration_minutes > 0:
                duration_str = f"{duration_hours}h {duration_minutes}m"
            elif duration_hours > 0:
                duration_str = f"{duration_hours}h"
            elif duration_minutes > 0:
                duration_str = f"{duration_minutes}m"
            
            flights.append({
                "id": max([f.get("id", 0) for f in flights] + [0]) + 1,
                "date": flight_date.strftime("%Y-%m-%d"),
                "time": flight_time.strftime("%H:%M"),
                "landing_time": landing_time.strftime("%H:%M"),
                "duration": duration_str,
                "airline": airline,
                "flight_number": flight_num,
                "from": from_airport,
                "to": to_airport,
                "type": flight_type
            })
            trip_info["flights"] = flights
            save_trip_info(trip_info)
            st.success(f"{t('add', lang)} {flight_type} {t('flights', lang).lower()}!")
            st.rerun()
    
    # Display flights
    if flights:
        st.markdown(f"### {t('your_flights', lang)}")
        # Sort flights by date (handle both dict and string dates)
        def get_date_for_sort(flight):
            date_val = flight.get("date", "") if isinstance(flight, dict) else ""
            return date_val if date_val else "9999-99-99"
        
        sorted_flights = sorted(flights, key=get_date_for_sort)
        for flight in sorted_flights:
            if not isinstance(flight, dict):
                continue
            
            # Check if this flight is being edited
            edit_key = f"edit_flight_{flight['id']}"
            is_editing = st.session_state.get(edit_key, False)
            
            with st.expander(f"✈️ {flight.get('type', t('flights', lang))}: {flight.get('from', 'N/A')} → {flight.get('to', 'N/A')} ({flight.get('date', 'N/A')})"):
                if is_editing:
                    # Edit form
                    with st.form(f"edit_flight_form_{flight['id']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            # Parse existing date
                            current_date = datetime.now().date()
                            if flight.get('date'):
                                try:
                                    current_date = datetime.strptime(flight.get('date'), "%Y-%m-%d").date()
                                except:
                                    pass
                            flight_date = st.date_input(t("date", lang), value=current_date, key=f"edit_date_{flight['id']}")
                            
                            # Parse existing times
                            current_time = datetime.now().time()
                            current_landing = datetime.now().time()
                            if flight.get('time'):
                                try:
                                    time_parts = flight.get('time').split(':')
                                    current_time = datetime.now().replace(hour=int(time_parts[0]), minute=int(time_parts[1])).time()
                                except:
                                    pass
                            if flight.get('landing_time'):
                                try:
                                    landing_parts = flight.get('landing_time').split(':')
                                    current_landing = datetime.now().replace(hour=int(landing_parts[0]), minute=int(landing_parts[1])).time()
                                except:
                                    pass
                            
                            airline = st.text_input(t("airline", lang), value=flight.get('airline', ''), key=f"edit_airline_{flight['id']}")
                            flight_num = st.text_input(t("flight_number", lang), value=flight.get('flight_number', ''), key=f"edit_num_{flight['id']}")
                            from_airport = st.text_input(t("from", lang), value=flight.get('from', ''), key=f"edit_from_{flight['id']}")
                        with col2:
                            to_airport = st.text_input(t("to", lang), value=flight.get('to', ''), key=f"edit_to_{flight['id']}")
                            flight_type_options = [t("outbound", lang), t("return", lang), t("domestic", lang)]
                            current_type = flight.get('type', t("outbound", lang))
                            try:
                                type_index = flight_type_options.index(current_type) if current_type in flight_type_options else 0
                            except:
                                type_index = 0
                            flight_type = st.selectbox(
                                t("flight_type", lang), 
                                flight_type_options,
                                index=type_index,
                                key=f"edit_type_{flight['id']}"
                            )
                        
                        # Time and landing time in the same row
                        time_col1, time_col2 = st.columns(2)
                        with time_col1:
                            flight_time = st.time_input(t("time", lang), value=current_time, key=f"edit_time_{flight['id']}")
                        with time_col2:
                            landing_time = st.time_input(t("landing_time", lang), value=current_landing, key=f"edit_landing_{flight['id']}")
                        
                        # Duration input
                        duration_hours = 0
                        duration_minutes = 0
                        if flight.get('duration'):
                            dur_str = flight.get('duration', '')
                            if 'h' in dur_str:
                                try:
                                    duration_hours = int(dur_str.split('h')[0])
                                except:
                                    pass
                            if 'm' in dur_str:
                                try:
                                    dur_min_part = dur_str.split('m')[0].split()[-1] if ' ' in dur_str else dur_str.split('m')[0]
                                    duration_minutes = int(dur_min_part)
                                except:
                                    pass
                        
                        st.markdown("**" + t("duration", lang) + ":**")
                        dur_col1, dur_col2 = st.columns(2)
                        with dur_col1:
                            duration_hours = st.number_input(t("duration_hours", lang), min_value=0, max_value=24, value=duration_hours, step=1, key=f"edit_dur_h_{flight['id']}")
                        with dur_col2:
                            duration_minutes = st.number_input(t("duration_minutes", lang), min_value=0, max_value=59, value=duration_minutes, step=1, key=f"edit_dur_m_{flight['id']}")
                        
                        col_btn1, col_btn2 = st.columns(2)
                        with col_btn1:
                            if st.form_submit_button(t("save_changes", lang)):
                                # Format duration
                                duration_str = ""
                                if duration_hours > 0 and duration_minutes > 0:
                                    duration_str = f"{duration_hours}h {duration_minutes}m"
                                elif duration_hours > 0:
                                    duration_str = f"{duration_hours}h"
                                elif duration_minutes > 0:
                                    duration_str = f"{duration_minutes}m"
                                
                                flight.update({
                                    "date": flight_date.strftime("%Y-%m-%d"),
                                    "time": flight_time.strftime("%H:%M"),
                                    "landing_time": landing_time.strftime("%H:%M"),
                                    "duration": duration_str,
                                    "airline": airline,
                                    "flight_number": flight_num,
                                    "from": from_airport,
                                    "to": to_airport,
                                    "type": flight_type
                                })
                                trip_info["flights"] = flights
                                save_trip_info(trip_info)
                                st.session_state[edit_key] = False
                                st.success(t("save_changes", lang) + "!")
                                st.rerun()
                        with col_btn2:
                            if st.form_submit_button(t("cancel", lang)):
                                st.session_state[edit_key] = False
                                st.rerun()
                else:
                    # Display mode
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**{t('date', lang)}:** {flight.get('date', 'N/A')}")
                        st.write(f"**{t('time', lang)}:** {flight.get('time', 'N/A')}")
                        if flight.get('landing_time'):
                            st.write(f"**{t('landing_time', lang)}:** {flight.get('landing_time', 'N/A')}")
                        if flight.get('duration'):
                            st.write(f"**{t('duration', lang)}:** {flight.get('duration', 'N/A')}")
                        st.write(f"**{t('type', lang)}:** {flight.get('type', 'N/A')}")
                    with col2:
                        st.write(f"**{t('airline', lang)}:** {flight.get('airline', 'N/A')}")
                        st.write(f"**{t('flight_number', lang)}:** {flight.get('flight_number', 'N/A')}")
                        st.write(f"**{t('route', lang)}:** {flight.get('from', 'N/A')} → {flight.get('to', 'N/A')}")
                    
                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1:
                        if st.button(t("edit_flight", lang), key=f"btn_edit_{flight['id']}"):
                            st.session_state[edit_key] = True
                            st.rerun()
                    with col_btn2:
                        if st.button(t("delete_flight", lang), key=f"del_flight_{flight['id']}"):
                            flights.remove(flight)
                            trip_info["flights"] = flights
                            save_trip_info(trip_info)
                            st.rerun()
    else:
        st.info(t("no_flights", lang))
    
    st.divider()
    
    # Hotels section
    st.subheader(t("hotels", lang))
    
    hotels = trip_info.get("hotels", [])
    
    # Add hotel form
    with st.form("add_hotel_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            hotel_name = st.text_input(t("hotel_name", lang))
            check_in = st.date_input(t("check_in", lang))
        with col2:
            hotel_location = st.text_input(t("location", lang))
            check_out = st.date_input(t("check_out", lang))
        with col3:
            confirmation_num = st.text_input(t("confirmation", lang))
            room_info = st.text_input(t("room_info", lang))
        
        if st.form_submit_button(t("add_hotel", lang)):
            if hotel_name:
                hotels.append({
                    "id": max([h.get("id", 0) for h in hotels] + [0]) + 1,
                    "name": hotel_name,
                    "location": hotel_location,
                    "check_in": check_in.strftime("%Y-%m-%d"),
                    "check_out": check_out.strftime("%Y-%m-%d"),
                    "confirmation": confirmation_num,
                    "room_info": room_info
                })
                trip_info["hotels"] = hotels
                save_trip_info(trip_info)
                st.success(f"{t('add', lang)} {hotel_name}!")
                st.rerun()
    
    # Display hotels
    if hotels:
        for hotel in hotels:
            with st.expander(f"🏨 {hotel['name']} - {hotel.get('location', 'N/A')}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**{t('check_in', lang)}:** {hotel.get('check_in', 'N/A')}")
                    st.write(f"**{t('check_out', lang)}:** {hotel.get('check_out', 'N/A')}")
                with col2:
                    st.write(f"**{t('confirmation', lang)}:** {hotel.get('confirmation', 'N/A')}")
                    st.write(f"**{t('room_info', lang).split('(')[0].strip()}:** {hotel.get('room_info', 'N/A')}")
                
                if st.button(f"{t('delete', lang)} {hotel['name']}", key=f"del_hotel_{hotel['id']}"):
                    hotels.remove(hotel)
                    trip_info["hotels"] = hotels
                    save_trip_info(trip_info)
                    st.rerun()
    else:
        st.info(t("no_hotels", lang))

def show_before_trip(lang="en"):
    st.header(t("before_trip_header", lang))
    st.markdown(t("manage_packing", lang))
    
    packing_data = load_packing()
    users_data = load_users()
    people = users_data.get("users", [])
    
    if not people:
        st.warning(t("no_users_packing", lang))
        return
    
    # Create tabs for each person
    tabs = st.tabs(people)
    
    for idx, person in enumerate(people):
        with tabs[idx]:
            st.subheader(f"🎒 {person}{t('packing_list', lang)}")
            
            items = packing_data.get(person, [])
            
            # Add item form
            with st.form(f"add_item_{person}"):
                new_item = st.text_input(t("add_item_pack", lang), key=f"input_{person}")
                submitted = st.form_submit_button(t("add_item", lang))
                
                if submitted and new_item:
                    items.append({
                        "id": max([item.get("id", 0) for item in items] + [0]) + 1,
                        "text": new_item,
                        "packed": False
                    })
                    packing_data[person] = items
                    save_packing(packing_data)
                    st.rerun()
            
            st.divider()
            
            # Display items
            if items:
                for item in items:
                    col1, col2, col3 = st.columns([1, 10, 1])
                    with col1:
                        packed = st.checkbox("", value=item.get("packed", False), key=f"packed_{person}_{item['id']}")
                    with col2:
                        if packed:
                            st.markdown(f"~~{item['text']}~~")
                        else:
                            st.markdown(item['text'])
                    with col3:
                        if st.button("🗑️", key=f"del_{person}_{item['id']}"):
                            items.remove(item)
                            packing_data[person] = items
                            save_packing(packing_data)
                            st.rerun()
                    
                    if packed != item.get("packed", False):
                        item["packed"] = packed
                        packing_data[person] = items
                        save_packing(packing_data)
                        st.rerun()
                
                # Progress
                packed_count = sum(1 for item in items if item.get("packed", False))
                total_count = len(items)
                progress = packed_count / total_count if total_count > 0 else 0
                st.progress(progress)
                st.caption(f"{t('packed', lang)}: {packed_count}/{total_count} {t('items', lang)} ({int(progress*100)}%)")
            else:
                st.info(t("no_items", lang).format(person))

def show_budget(lang="en"):
    st.header(t("budget_header", lang))
    st.markdown(t("track_expenses", lang))
    
    budget_data = load_budget()
    expenses = budget_data.get("expenses", [])
    users_data = load_users()
    users_list = users_data.get("users", [])
    
    # Calculate totals
    total_spent = sum(exp.get("amount", 0) for exp in expenses)
    
    # Summary metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric(t("total_expenses", lang), f"${total_spent:,.2f}")
    with col2:
        st.metric(t("number_expenses", lang), len(expenses))
    
    st.divider()
    
    # Add expense
    with st.form("add_expense"):
        col1, col2, col3 = st.columns(3)
        with col1:
            expense_desc = st.text_input(t("expense_desc", lang))
        with col2:
            expense_amount = st.number_input(t("amount_usd", lang), min_value=0.0, step=10.0)
        with col3:
            # Store categories in English, display in selected language
            category_options_en = ["Food", "Transportation", "Accommodation", "Activities", "Shopping", "Other"]
            category_options_display = [t("food", lang), t("transportation", lang), t("accommodation", lang), t("activities", lang), t("shopping", lang), t("other", lang)]
            selected_category_idx = st.selectbox(t("category", lang), range(len(category_options_display)), format_func=lambda x: category_options_display[x])
            expense_category = category_options_en[selected_category_idx]
        
        # Split expense option
        split_expense = st.checkbox(t("split_expense", lang), key="split_expense")
        selected_users = []
        if split_expense and users_list:
            selected_users = st.multiselect(t("select_people", lang), users_list, default=users_list, key="expense_users")
        
        if st.form_submit_button(t("add_expense", lang)):
            if expense_desc and expense_amount > 0:
                expense_data = {
                    "id": max([e.get("id", 0) for e in expenses] + [0]) + 1,
                    "description": expense_desc,
                    "amount": expense_amount,
                    "category": expense_category,
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "split": split_expense,
                    "split_users": selected_users if split_expense else []
                }
                expenses.append(expense_data)
                budget_data["expenses"] = expenses
                save_budget(budget_data)
                st.success(t("add_expense", lang) + "!")
                st.rerun()
    
    st.divider()
    
    # Display expenses
    if expenses:
        # Summary tabs
        summary_tab1, summary_tab2, summary_tab3 = st.tabs([t("expenses_by_category", lang), t("expenses_by_person", lang), t("all_expenses", lang)])
        
        with summary_tab1:
            st.subheader(t("expenses_by_category_header", lang))
            category_totals = {}
            category_counts = {}
            category_map = {"Food": t("food", lang), "Transportation": t("transportation", lang), "Accommodation": t("accommodation", lang), 
                          "Activities": t("activities", lang), "Shopping": t("shopping", lang), "Other": t("other", lang)}
            for exp in expenses:
                cat_en = exp.get("category", "Other")
                cat_display = category_map.get(cat_en, cat_en)
                category_totals[cat_display] = category_totals.get(cat_display, 0) + exp.get("amount", 0)
                category_counts[cat_display] = category_counts.get(cat_display, 0) + 1
            
            if category_totals:
                # Show chart with proper labels
                df_categories = pd.DataFrame({
                    t("category", lang): list(category_totals.keys()),
                    t("amount", lang): list(category_totals.values())
                })
                chart = alt.Chart(df_categories).mark_bar().encode(
                    x=alt.X(t("category", lang), sort='-y', title=t("category", lang)),
                    y=alt.Y(t("amount", lang), title=f"{t('amount', lang)} ($)"),
                    color=alt.Color(t("category", lang), scale=alt.Scale(scheme='category10'))
                ).properties(width=600, height=400)
                st.altair_chart(chart, use_container_width=True)
                
                # Show detailed breakdown
                st.markdown(f"**{t('category_breakdown', lang)}:**")
                for cat, total in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.write(f"**{cat}**")
                    with col2:
                        st.write(f"${total:,.2f}")
                    with col3:
                        st.write(f"{category_counts[cat]} {t('expense', lang)}")
        
        with summary_tab2:
            st.subheader(t("expenses_by_person_header", lang))
            if users_list:
                # Calculate per-person totals
                user_totals = {}
                user_expense_counts = {}
                
                for exp in expenses:
                    if exp.get("split") and exp.get("split_users"):
                        # Split expense
                        per_person = exp.get("amount", 0) / len(exp.get("split_users", []))
                        for user in exp.get("split_users", []):
                            user_totals[user] = user_totals.get(user, 0) + per_person
                            user_expense_counts[user] = user_expense_counts.get(user, 0) + 1
                    else:
                        # Not split - show as "Group" expense
                        if "Group" not in user_totals:
                            user_totals["Group"] = 0
                            user_expense_counts["Group"] = 0
                        user_totals["Group"] = user_totals.get("Group", 0) + exp.get("amount", 0)
                        user_expense_counts["Group"] = user_expense_counts.get("Group", 0) + 1
                
                if user_totals:
                    # Show chart with different colors per person
                    df_persons = pd.DataFrame({
                        'Person': list(user_totals.keys()),
                        'Amount': list(user_totals.values())
                    })
                    # Create color scheme - one color per person
                    color_palette = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E2']
                    chart = alt.Chart(df_persons).mark_bar().encode(
                        x=alt.X('Person', sort='-y', title='Person'),
                        y=alt.Y('Amount', title=f"{t('amount', lang)} ($)"),
                        color=alt.Color('Person', scale=alt.Scale(domain=list(user_totals.keys()), 
                                                                   range=color_palette[:len(user_totals)]))
                    ).properties(width=600, height=400)
                    st.altair_chart(chart, use_container_width=True)
                    
                    # Show detailed breakdown
                    st.markdown(f"**{t('per_person_breakdown', lang)}:**")
                    for user, total in sorted(user_totals.items(), key=lambda x: x[1], reverse=True):
                        col1, col2, col3 = st.columns([2, 1, 1])
                        with col1:
                            st.write(f"**{user}**")
                        with col2:
                            st.write(f"${total:,.2f}")
                        with col3:
                            st.write(f"{user_expense_counts.get(user, 0)} {t('expense', lang)}")
                else:
                    st.info(t("no_expenses", lang))
            else:
                st.warning(t("no_users_budget", lang))
        
        with summary_tab3:
            st.subheader(t("all_expenses", lang))
            # List expenses
            for exp in sorted(expenses, key=lambda x: x.get("date", ""), reverse=True):
                split_info = ""
                if exp.get("split") and exp.get("split_users"):
                    num_people = len(exp.get("split_users", []))
                    if num_people > 0:
                        per_person = exp.get("amount", 0) / num_people
                        split_info = f" | {t('split_among', lang)}: ${per_person:.2f} {t('per_person', lang).lower()} ({', '.join(exp.get('split_users', []))})"
                
                # Translate category for display
                cat_en = exp.get("category", "Other")
                category_map = {"Food": t("food", lang), "Transportation": t("transportation", lang), "Accommodation": t("accommodation", lang), 
                              "Activities": t("activities", lang), "Shopping": t("shopping", lang), "Other": t("other", lang)}
                cat_display = category_map.get(cat_en, cat_en)
                
                with st.expander(f"${exp['amount']:.2f} - {exp['description']} ({cat_display}){split_info}"):
                    st.write(f"**{t('date', lang)}:** {exp.get('date', 'N/A')}")
                    st.write(f"**{t('category', lang)}:** {cat_display}")
                    if exp.get("split") and exp.get("split_users"):
                        num_people = len(exp.get("split_users", []))
                        if num_people > 0:
                            per_person = exp.get("amount", 0) / num_people
                            st.write(f"**{t('split_among', lang)}:** {', '.join(exp.get('split_users', []))}")
                            st.write(f"**{t('per_person', lang)}:** ${per_person:.2f}")
                    else:
                        st.write(f"**{t('type', lang)}:** {t('group_expense', lang)}")
                    if st.button(t("delete", lang), key=f"del_exp_{exp['id']}"):
                        expenses.remove(exp)
                        budget_data["expenses"] = expenses
                        save_budget(budget_data)
                        st.rerun()
    else:
        st.info(t("no_expenses_recorded", lang))

def show_notes(lang="en"):
    st.header(t("notes_header", lang))
    st.markdown(t("keep_notes", lang))
    
    notes_data = load_notes()
    notes = notes_data.get("notes", [])
    
    # Add note
    with st.form("add_note_form"):
        note_title = st.text_input(t("note_title", lang))
        note_content = st.text_area(t("note_content", lang), height=150)
        note_link = st.text_input(t("note_link", lang), placeholder="https://...")
        if st.form_submit_button(t("add_note", lang)):
            if note_title and note_content:
                notes.append({
                    "id": max([n.get("id", 0) for n in notes] + [0]) + 1,
                    "title": note_title,
                    "content": note_content,
                    "link": note_link if note_link else None,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                notes_data["notes"] = notes
                save_notes(notes_data)
                st.success(t("add_note", lang) + "!")
                st.rerun()
    
    st.divider()
    
    # Display notes
    if notes:
        for note in sorted(notes, key=lambda x: x.get("date", ""), reverse=True):
            with st.expander(f"📌 {note['title']} - {note.get('date', 'N/A')}"):
                st.write(note['content'])
                if note.get('link'):
                    st.markdown(f"🔗 [Link]({note['link']})")
                if st.button(f"{t('delete', lang)} {t('notes', lang).split()[0] if ' ' in t('notes', lang) else t('notes', lang)}", key=f"del_note_{note['id']}"):
                    notes.remove(note)
                    notes_data["notes"] = notes
                    save_notes(notes_data)
                    st.rerun()
    else:
        st.info(t("no_notes", lang))

def show_users(lang="en"):
    st.header(t("users_header", lang))
    st.markdown(t("users_description", lang))
    
    users_data = load_users()
    users = users_data.get("users", [])
    
    # Add user form
    with st.form("add_user_form"):
        new_user = st.text_input(t("user_name", lang))
        if st.form_submit_button(t("add_user", lang)):
            if new_user and new_user.strip():
                if new_user not in users:
                    users.append(new_user.strip())
                    users_data["users"] = users
                    save_users(users_data)
                    
                    # Update packing list to include new user
                    packing_data = load_packing()
                    if new_user not in packing_data:
                        packing_data[new_user] = []
                        save_packing(packing_data)
                    
                    st.success(f"{t('add', lang)} {new_user}!")
                    st.rerun()
                else:
                    st.warning(f"{new_user} {t('already_in_list', lang)}")
            else:
                st.warning(t("please_enter_name", lang))
    
    st.divider()
    
    # Display users
    if users:
        st.subheader(t("users_count", lang).format(len(users)))
        for user in users:
            col1, col2 = st.columns([10, 1])
            with col1:
                st.write(f"👤 {user}")
            with col2:
                if st.button("🗑️", key=f"del_user_{user}"):
                    users.remove(user)
                    users_data["users"] = users
                    save_users(users_data)
                    
                    # Remove from packing list
                    packing_data = load_packing()
                    if user in packing_data:
                        del packing_data[user]
                        save_packing(packing_data)
                    
                    st.rerun()
    else:
        st.info(t("no_users", lang))
        st.markdown(f"**{t('default_users', lang).split(':')[0]}:** {t('default_users', lang).split(':', 1)[1] if ':' in t('default_users', lang) else ''}")

def show_weather(lang="en"):
    st.header(t("weather_header", lang))
    st.markdown(t("weather_description", lang))
    
    places_data = load_places()
    places = places_data.get("places", [])
    trip_info = load_trip_info()
    flights = trip_info.get("flights", [])
    
    # Get trip dates from flights
    trip_dates = []
    if flights:
        for flight in flights:
            if isinstance(flight, dict) and flight.get("date"):
                try:
                    trip_dates.append(datetime.strptime(flight.get("date"), "%Y-%m-%d").date())
                except:
                    pass
    
    # Group places by city
    city_groups = {}
    individual_places = {}
    
    if places:
        city_groups = group_places_by_city(places)
        
        # Also create individual place options
        for place in places:
            if place.get("day") and place.get("lat") and place.get("lon"):
                try:
                    date_obj = datetime.strptime(place.get("day"), "%Y-%m-%d").date()
                    loc_key = f"{place['name']} ({place.get('lat', 0):.2f}, {place.get('lon', 0):.2f})"
                    if loc_key not in individual_places:
                        individual_places[loc_key] = {
                            "name": place['name'],
                            "lat": place.get("lat"),
                            "lon": place.get("lon"),
                            "dates": []
                        }
                    individual_places[loc_key]["dates"].append(date_obj)
                except:
                    pass
    
    # Build location options
    location_options = []
    location_data = {}
    
    # Add city groups
    for city_name, city_info in city_groups.items():
        if city_info.get("lat") and city_info.get("lon"):
            city_key = f"🏙️ {city_name} (City - {len(city_info['places'])} places)"
            location_options.append(city_key)
            location_data[city_key] = {
                "name": city_name,
                "lat": city_info["lat"],
                "lon": city_info["lon"],
                "dates": city_info.get("dates", []),
                "type": "city"
            }
    
    # Add individual places
    for loc_key, loc_info in individual_places.items():
        place_key = f"📍 {loc_info['name']}"
        location_options.append(place_key)
        location_data[place_key] = {
            "name": loc_info['name'],
            "lat": loc_info["lat"],
            "lon": loc_info["lon"],
            "dates": loc_info.get("dates", []),
            "type": "place"
        }
    
    # Location and date selector
    col1, col2 = st.columns(2)
    
    with col1:
        selected_location = None
        if location_options:
            selected_key = st.selectbox(t("select_city_or_place", lang), location_options)
            selected_location = location_data.get(selected_key)
        
        # Manual city input
        st.divider()
        st.subheader(t("manual_city", lang))
        manual_city = st.text_input(t("enter_city_name", lang), placeholder="e.g., Los Angeles, Las Vegas")
        
        if manual_city and manual_city.strip():
            if st.button(t("get_weather_forecast", lang), key="manual_city_btn"):
                with st.spinner("Searching for city..."):
                    city_info = geocode_city_name(manual_city.strip())
                    if city_info:
                        selected_location = {
                            "name": f"{city_info['name']}, {city_info.get('admin1', '')} {city_info.get('country', '')}".strip(),
                            "lat": city_info["lat"],
                            "lon": city_info["lon"],
                            "dates": trip_dates if trip_dates else [datetime.now().date()],
                            "type": "manual"
                        }
                        st.success(f"✅ {t('city_found', lang)} {selected_location['name']}")
                        # Fetch weather immediately for manual city
                        if selected_date:
                            with st.spinner("Fetching weather data..."):
                                weather_data = get_weather_from_api(city_info["lat"], city_info["lon"], selected_date)
                                st.session_state.weather_data = weather_data
                                st.rerun()
                    else:
                        st.error(t("city_not_found", lang))
                        selected_location = None
    
    with col2:
        # Date selector
        if selected_location:
            available_dates = selected_location.get("dates", [])
            if not available_dates:
                available_dates = trip_dates if trip_dates else [datetime.now().date()]
            
            if len(available_dates) == 1:
                selected_date = available_dates[0]
                st.write(f"**{t('select_date', lang)}:** {selected_date.strftime('%B %d, %Y')}")
            else:
                selected_date = st.selectbox(t("select_date", lang), available_dates)
        else:
            if trip_dates:
                selected_date = st.selectbox(t("select_date", lang), trip_dates)
            else:
                selected_date = datetime.now().date()
                st.write(f"**{t('select_date', lang)}:** {selected_date.strftime('%B %d, %Y')}")
    
    if not selected_location:
        if not places:
            st.warning(t("no_places", lang))
        return
    
    # Weather display
    st.divider()
    
    lat = selected_location.get("lat")
    lon = selected_location.get("lon")
    
    if lat and lon:
        location_type_icon = "🏙️" if selected_location.get("type") == "city" else "📍"
        st.subheader(f"{location_type_icon} {selected_location['name']} - {selected_date.strftime('%B %d, %Y')}")
        
        # Fetch weather data (Open-Meteo is free, no API key needed)
        weather_data = None
        if st.button(t("get_weather_forecast", lang)):
            with st.spinner("Fetching weather data..."):
                weather_data = get_weather_from_api(lat, lon, selected_date)
        
        # Display weather data
        if weather_data:
            # Main weather display
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                # Temperature display
                temp = weather_data.get("temperature", 0)
                temp_max = weather_data.get("temp_max", temp)
                temp_min = weather_data.get("temp_min", temp)
                condition = weather_data.get("condition", "N/A")
                description = weather_data.get("description", "")
                
                st.markdown(f"## {temp}{t('fahrenheit', lang)}")
                st.markdown(f"**High:** {temp_max}{t('fahrenheit', lang)} | **Low:** {temp_min}{t('fahrenheit', lang)}")
                st.markdown(f"**{t('weather_condition', lang)}:** {condition}")
                if description:
                    st.markdown(f"*{description}*")
            
            with col2:
                # Weather icon (using emoji based on condition)
                icon_map = {
                    "Clear": "☀️",
                    "Cloudy": "☁️",
                    "Rain": "🌧️",
                    "Drizzle": "🌦️",
                    "Thunderstorm": "⛈️",
                    "Snow": "❄️",
                    "Foggy": "🌫️",
                    "Unknown": "🌤️"
                }
                icon_emoji = icon_map.get(condition, "🌤️")
                st.markdown(f"# {icon_emoji}")
            
            with col3:
                # Forecast date
                forecast_time = weather_data.get("forecast_time", "")
                if forecast_time:
                    st.caption(f"{t('forecast_time', lang)}:\n{forecast_time}")
            
            st.divider()
            
            # Detailed weather metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                precipitation = weather_data.get("precipitation", 0)
                st.metric("Precipitation", f"{precipitation} in")
            
            with col2:
                wind_speed = weather_data.get("wind_speed", 0)
                st.metric(t("wind_speed", lang), f"{wind_speed} {t('mph', lang)}")
            
            with col3:
                wind_dir = weather_data.get("wind_direction", 0)
                if wind_dir:
                    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", 
                                 "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
                    dir_idx = int((wind_dir + 11.25) / 22.5) % 16
                    st.metric(t("wind_direction", lang), f"{directions[dir_idx]}")
            
            with col4:
                weathercode = weather_data.get("weathercode", 0)
                st.caption(f"Weather Code: {weathercode}")
        
        # Weather links as additional info
        st.divider()
        st.subheader(t("weather_link", lang))
        col1, col2, col3 = st.columns(3)
        with col1:
            weather_url = f"https://www.weather.com/weather/tenday/l/{lat},{lon}"
            st.markdown(f"[🌤️ Weather.com]({weather_url})")
        with col2:
            accuweather_url = f"https://www.accuweather.com/en/search-locations?query={lat},{lon}"
            st.markdown(f"[🌦️ AccuWeather]({accuweather_url})")
        with col3:
            wunderground_url = f"https://www.wunderground.com/weather/{lat},{lon}"
            st.markdown(f"[🌡️ Weather Underground]({wunderground_url})")
    else:
        st.warning("Location coordinates not available for weather forecast.")

def show_routes(lang="en"):
    st.header(t("routes_header", lang))
    st.markdown(t("routes_description", lang))
    
    places_data = load_places()
    places = places_data.get("places", [])
    
    if len(places) < 2:
        st.info(t("no_places", lang))
        return
    
    # Distance calculator between two places
    st.subheader(t("calculate_distance", lang))
    col1, col2 = st.columns(2)
    
    with col1:
        place_names = [f"{p['name']} ({p.get('day', 'No date')})" for p in places]
        from_idx = st.selectbox(t("select_from", lang), range(len(places)), format_func=lambda x: place_names[x])
        from_place = places[from_idx]
    
    with col2:
        to_idx = st.selectbox(t("select_to", lang), range(len(places)), format_func=lambda x: place_names[x], key="to_place")
        to_place = places[to_idx]
    
    if from_idx != to_idx:
        distance_miles = haversine_distance(
            from_place['lat'], from_place['lon'],
            to_place['lat'], to_place['lon']
        )
        distance_km = distance_miles * 1.60934
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(t("distance", lang), f"{distance_miles:.1f} {t('miles', lang)} ({distance_km:.1f} {t('km', lang)})")
        
        # Travel time estimates
        driving_time = estimate_travel_time(distance_miles, "driving")
        walking_time = estimate_travel_time(distance_miles, "walking")
        
        with col2:
            hours = int(driving_time)
            minutes = int((driving_time - hours) * 60)
            st.metric(f"{t('estimated_time', lang)} ({t('driving', lang)})", f"{hours}h {minutes}m")
        
        with col3:
            hours_w = int(walking_time)
            minutes_w = int((walking_time - hours_w) * 60)
            st.metric(f"{t('estimated_time', lang)} ({t('walking', lang)})", f"{hours_w}h {minutes_w}m")
        
        # Show on map
        st.divider()
        st.subheader("Route Map")
        route_map = folium.Map(
            location=[(from_place['lat'] + to_place['lat'])/2, (from_place['lon'] + to_place['lon'])/2],
            zoom_start=7
        )
        
        # Add markers
        folium.Marker(
            [from_place['lat'], from_place['lon']],
            popup=f"From: {from_place['name']}",
            icon=folium.Icon(color="green", icon="play")
        ).add_to(route_map)
        
        folium.Marker(
            [to_place['lat'], to_place['lon']],
            popup=f"To: {to_place['name']}",
            icon=folium.Icon(color="red", icon="stop")
        ).add_to(route_map)
        
        # Add line between points
        folium.PolyLine(
            [[from_place['lat'], from_place['lon']], [to_place['lat'], to_place['lon']]],
            color="blue",
            weight=3,
            opacity=0.7
        ).add_to(route_map)
        
        st_folium(route_map, width=1200, height=400)
    
    st.divider()
    
    # Route optimization for multiple places
    st.subheader(t("route_optimization", lang))
    
    # Filter places by date or select manually
    places_with_dates = [p for p in places if p.get("day")]
    
    if len(places_with_dates) >= 2:
        # Group by date
        places_by_date = {}
        for place in places_with_dates:
            date_str = place.get("day")
            if date_str not in places_by_date:
                places_by_date[date_str] = []
            places_by_date[date_str].append(place)
        
        if places_by_date:
            selected_date_opt = st.selectbox("Select date for route optimization", sorted(places_by_date.keys()))
            places_to_optimize = places_by_date[selected_date_opt]
            
            if len(places_to_optimize) >= 2:
                if st.button(t("optimize_route", lang)):
                    # Simple optimization: start from first place, go to nearest unvisited
                    optimized = [places_to_optimize[0]]
                    remaining = places_to_optimize[1:]
                    
                    while remaining:
                        current = optimized[-1]
                        nearest = min(remaining, key=lambda p: haversine_distance(
                            current['lat'], current['lon'], p['lat'], p['lon']
                        ))
                        optimized.append(nearest)
                        remaining.remove(nearest)
                    
                    # Display optimized route
                    st.markdown(f"**{t('route_order', lang)}:**")
                    total_dist = calculate_route_distance(optimized)
                    total_time = estimate_travel_time(total_dist, "driving")
                    
                    route_text = " → ".join([p['name'] for p in optimized])
                    st.write(route_text)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric(t("total_distance", lang), f"{total_dist:.1f} {t('miles', lang)} ({total_dist * 1.60934:.1f} {t('km', lang)})")
                    with col2:
                        hours = int(total_time)
                        minutes = int((total_time - hours) * 60)
                        st.metric(t("total_time", lang), f"{hours}h {minutes}m")
                    
                    # Show optimized route on map
                    opt_map = folium.Map(
                        location=[optimized[0]['lat'], optimized[0]['lon']],
                        zoom_start=7
                    )
                    
                    # Add all markers
                    for i, place in enumerate(optimized):
                        folium.Marker(
                            [place['lat'], place['lon']],
                            popup=f"{i+1}. {place['name']}",
                            icon=folium.Icon(color="blue", icon=str(i+1))
                        ).add_to(opt_map)
                    
                    # Add route lines
                    for i in range(len(optimized) - 1):
                        folium.PolyLine(
                            [[optimized[i]['lat'], optimized[i]['lon']], 
                             [optimized[i+1]['lat'], optimized[i+1]['lon']]],
                            color="blue",
                            weight=2,
                            opacity=0.7
                        ).add_to(opt_map)
                    
                    st_folium(opt_map, width=1200, height=500)
            else:
                st.info(f"Need at least 2 places on {selected_date_opt} for route optimization")
        else:
            st.info("Add dates to your places to enable route optimization by date")
    else:
        st.info("Add dates to at least 2 places to enable route optimization")

if __name__ == "__main__":
    main()

