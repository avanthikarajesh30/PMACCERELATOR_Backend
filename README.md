# PMACCERELATOR_Backend

# 🌦️ Weather App Backend (Flask)

A Flask-based backend API that lets users enter a location and a date range to fetch and store weather data using OpenWeatherMap. Includes full CRUD functionality, export features, and API key management using `.env`.

---

## 🚀 Features

- ✅ Add weather info by location and date range  
- ✅ Read, update, and delete stored entries  
- ✅ Export weather data to CSV, JSON, or PDF  
- ✅ Supports multiple cities worldwide  
- ✅ Simple REST API with examples

---

## 📦 Setup Instructions

### 1. Create & Activate Virtual Environment


python -m venv venv
source venv/bin/activate

### 2. Install Dependencies
pip install -r requirements.txt


### 3. Get Your OpenWeatherMap API Key

	1.	Sign up at: https://home.openweathermap.org/users/sign_up
	2.	Go to the API Keys section
	3.	Copy your API key

### 4. Create a .env File
In your project root, create a .env file like this:
OPENWEATHER_API_KEY=your_actual_api_key_here

### 5. Run the Flask App

python app.py

## 📦 Sample JSON Inputs for POST /weather
{
  "location": "Dubai,AE",
  "start_date": "2024-09-10",
  "end_date": "2024-09-12"
}

{
  "location": "Toronto,CA",
  "start_date": "2024-08-01",
  "end_date": "2024-08-03"
}


