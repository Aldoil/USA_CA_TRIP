# ✈️ Trip Planner

A comprehensive, all-in-one trip planning application for US trip. Perfect for planning and managing your trip on mobile devices during your travels.

## 🌟 Features

### 👥 User Management
- Add and manage trip participants
- User list syncs across Budget Tracker and Before Trip sections
- Default users: Piotr, Weronika, Magda, Marek, Przemek
- Easy user addition and removal

### 🗺️ Interactive Map
- View all your places on an interactive map with Folium
- Click markers to see photos, descriptions, and details
- Color-coded markers:
  - 🟢 Green = Completed places
  - 🔵 Blue = Places to visit
  - 🔴 Red = Restaurants
- **Date filtering**: Filter places by specific dates or view all
- **Photo uploads**: Upload and display photos for each place
- Add custom places with coordinates from the interactive map
- Calendar-based date assignment (not abstract "Day 1, Day 2")

### ✅ To-Do List
- Create and manage trip tasks
- Priority levels (High, Medium, Low)
- Mark items as completed
- Filter by status (All, Active, Completed)
- Persistent storage across sessions

### 📋 Trip Info
- **Multiple flights support**: Add outbound, return, and domestic flights
- Store flight details: airline, flight number, from/to locations, dates
- Manage hotel bookings with check-in/check-out dates
- Track confirmation numbers and room details
- All flight information sorted by date

### 🎒 Before Trip
- Individual packing lists for each traveler
- Dynamic user list (syncs with Users page)
- Track packing progress with checkboxes
- Visual progress indicators
- Separate lists per person

### 💰 Budget Tracker
- Track expenses by category (Food, Transportation, Accommodation, Activities, Shopping, Other)
- **Expense splitting**: Split expenses among selected users
- Per-person expense tracking and totals
- Visual charts using Altair:
  - Expenses by category
  - Expenses by person
- View all expenses with detailed breakdowns
- Track group expenses (not split) vs. individual expenses

### 🌤️ Weather Forecast
- **Free weather API**: Uses Open-Meteo (no API key required)
- **City grouping**: Automatically groups places by city and calculates average coordinates
- **Manual city input**: Enter any city name with validation
- Get weather forecasts for specific dates and locations
- Displays temperature (high/low), conditions, precipitation, wind speed/direction
- Weather links to Weather.com, AccuWeather, and Weather Underground

### 📝 Notes
- Keep trip notes, ideas, and reminders
- Timestamped entries
- Easy note management with expandable cards
- Delete notes as needed

### 🌍 Language Support
- **Bilingual interface**: English and Polish (without special characters)
- Language switcher in sidebar
- All UI elements fully translated
- Switch languages anytime

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Local Development

1. **Clone the repository:**
```bash
git clone https://github.com/Aldoil/USA_CA_TRIP.git
cd USA_CA_TRIP
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the app:**
```bash
streamlit run app.py
```

4. **Access the app:**
   - Open your browser to `http://localhost:8501`
   - The app will automatically create the `data/` directory for storing your trip information

### Deploy to Streamlit Community Cloud

1. **Push your code to GitHub** (already done if you're reading this!)

2. **Go to [share.streamlit.io](https://share.streamlit.io)**

3. **Sign in with GitHub**

4. **Click "New app"**

5. **Configure your app:**
   - Repository: `Aldoil/USA_CA_TRIP`
   - Branch: `main`
   - Main file path: `app.py`

6. **Click "Deploy"**

7. **Access your app** from anywhere, including mobile devices!

## 📁 Data Storage

**Local (no database):** The app stores data in JSON files in the `data/` directory (places, todo, trip info, packing, budget, notes, users, weather cache, photos).

**Streamlit Cloud:** When the app is idle, Streamlit may shut it down and **local file data is lost**. To keep your trip data across restarts, use the **Supabase database**:

- See **[DATABASE_SETUP.md](DATABASE_SETUP.md)** for step-by-step instructions to create a free Supabase project and connect it to the app.
- Once `SUPABASE_URL` and `SUPABASE_KEY` are set in Streamlit secrets, all data (including place photos) is stored in the database and restored when the app runs again.

## 💡 Usage Tips

### Getting Started
1. **Users**: Start by adding or confirming your trip participants in the Users page
2. **Map**: Add your planned destinations with dates. Upload photos to make them more memorable!
3. **Trip Info**: Enter your flight and hotel details as soon as you book them
4. **Before Trip**: Use the packing lists to ensure everyone has what they need
5. **Budget**: Track expenses in real-time during your trip
6. **Weather**: Check weather forecasts for your destinations and dates
7. **Notes**: Jot down ideas, restaurant recommendations, or anything else you want to remember

### Map Features
- Click on the map to add new places
- Assign dates to places for better organization
- Filter by date to see your itinerary for specific days
- Upload photos when adding or editing places

### Budget Tracker
- Add expenses and mark them as "split" to divide costs among people
- Select which users to split expenses with
- View charts to see spending patterns
- Track both group expenses and individual expenses

### Weather
- Places are automatically grouped by city
- Select a city to see weather for all places in that city
- Or manually enter any city name to check weather
- Get forecasts up to 16 days in advance

## 🛠️ Technology Stack

- **Streamlit** - Web framework for the app
- **Folium** - Interactive map creation
- **Pillow (PIL)** - Image processing for photos
- **Pandas** - Data manipulation
- **Altair** - Advanced charting for budget visualization
- **Open-Meteo API** - Free weather forecasts (no API key needed)
- **Nominatim (OpenStreetMap)** - Reverse geocoding for city detection

## 📱 Mobile-Friendly Design

The app is designed to work seamlessly on mobile devices:
- Responsive layout
- Touch-friendly interface
- Optimized for phone screens
- Perfect for use during your trip

## 🔧 Customization

You can easily customize:
- Default places in the map (edit `init_default_data()` function)
- Default users (edit `init_default_data()` function)
- Expense categories (edit category options in `show_budget()`)
- Map center and zoom level (edit map initialization in `show_map()`)
- Language translations (edit `TRANSLATIONS` dictionary)

## 📝 Project Structure

```
USA_CA_TRIP/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── SETUP.md              # Quick setup guide
├── .streamlit/
│   └── config.toml       # Streamlit configuration
├── .gitignore           # Git ignore rules
└── data/                # Data storage (created automatically)
    ├── photos/          # Uploaded place photos
    └── *.json          # JSON data files
```

## 🌐 API Services Used

- **Open-Meteo Weather API** - Free weather forecasts
  - No API key required
  - 16-day forecast support
  - Global coverage

- **Open-Meteo Geocoding API** - City name validation
  - No API key required
  - City name to coordinates conversion

- **Nominatim (OpenStreetMap)** - Reverse geocoding
  - No API key required
  - Coordinates to city name conversion

## 🎯 Key Features Summary

✅ Interactive map with date filtering  
✅ Photo uploads for places  
✅ To-do list with priorities  
✅ Multiple flights support  
✅ Hotel management  
✅ Per-user packing lists  
✅ Budget tracker with expense splitting  
✅ Weather forecasts with city grouping  
✅ Manual city weather lookup  
✅ Notes section  
✅ User management  
✅ Bilingual support (English/Polish)  
✅ Mobile-friendly design  

## 📄 License

This project is for personal use. Feel free to customize it for your own trips!

## 🎉 Enjoy Your Trip!

Have a wonderful time exploring Los Angeles, Las Vegas, Palm Springs, Grand Canyon, and San Diego! This app will help you stay organized and make the most of your February adventure.

---

**Built with ❤️ using Streamlit**
