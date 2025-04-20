from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from database import db
from models import WeatherQuery
from weather_api import fetch_weather
from export_utils import export_csv, export_json, export_pdf
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

# CREATE
@app.route('/weather', methods=['POST'])
def create_weather_entry():
    data = request.get_json()
    location = data.get('location')
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    try:
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")
    except:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    weather = fetch_weather(location)
    if not weather:
        return jsonify({"error": "Invalid location or weather API error"}), 400

    new_entry = WeatherQuery(
        location=location,
        start_date=start_date,
        end_date=end_date,
        weather_data=weather
    )
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({"message": "Weather data saved", "id": new_entry.id}), 201

# READ
@app.route('/weather', methods=['GET'])
def get_all_weather():
    entries = WeatherQuery.query.all()
    return jsonify([{
        "id": e.id,
        "location": e.location,
        "start_date": e.start_date,
        "end_date": e.end_date,
        "weather_data": e.weather_data
    } for e in entries])

# UPDATE
@app.route('/weather/<int:id>', methods=['PUT'])
def update_weather(id):
    entry = WeatherQuery.query.get_or_404(id)
    data = request.get_json()
    location = data.get('location')
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    if location:
        entry.location = location
        new_weather = fetch_weather(location)
        if not new_weather:
            return jsonify({"error": "Invalid location"}), 400
        entry.weather_data = new_weather

    if start_date:
        entry.start_date = start_date
    if end_date:
        entry.end_date = end_date

    db.session.commit()
    return jsonify({"message": "Entry updated"})

# DELETE
@app.route('/weather/<int:id>', methods=['DELETE'])
def delete_weather(id):
    entry = WeatherQuery.query.get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    return jsonify({"message": "Entry deleted"})

# EXPORT
@app.route('/export', methods=['GET'])
def export_data():
    fmt = request.args.get('format')
    entries = WeatherQuery.query.all()
    data = [{
        "location": e.location,
        "start_date": e.start_date,
        "end_date": e.end_date,
        "weather": e.weather_data['weather'][0]['description'] if 'weather' in e.weather_data else "N/A",
        "temperature": e.weather_data['main']['temp'] if 'main' in e.weather_data else "N/A"
    } for e in entries]

    if fmt == 'csv':
        filename = export_csv(data)
    elif fmt == 'json':
        filename = export_json(data)
    elif fmt == 'pdf':
        filename = export_pdf(data)
    else:
        return jsonify({"error": "Unsupported format"}), 400

    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)