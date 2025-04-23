# main.py

import requests
from config import API_KEY, BASE_URL, DEFAULT_CITY
from db import create_table, create_connection

def fetch_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if response.status_code == 200:
        temperature = data["main"]["temp"]
        description = data["weather"][0]["description"]
        return (city, temperature, description)
    else:
        print("Error fetching data:", data)
        return None

def save_to_db(record):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO weather (city, temperature, description)
        VALUES (?, ?, ?)
    ''', record)
    conn.commit()
    conn.close()

def main():
    create_table()
    weather_data = fetch_weather(DEFAULT_CITY)
    if weather_data:
        save_to_db(weather_data)
        print("Data saved:", weather_data)

if __name__ == "__main__":
    main()