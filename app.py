from flask import Flask, render_template, request, redirect, url_for
import requests
import sqlite3
import datetime

app = Flask(__name__)
API_KEY = 'aa0ab5a9b884fd5a7207de839f9db4da'  
DB_NAME = 'weather.db'

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT NOT NULL,
            date TEXT NOT NULL,
            temperature REAL,
            description TEXT,
            humidity INTEGER,
            wind_speed REAL
        )''')
        conn.commit()

init_db()

def get_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    print("DEBUG:", response.status_code, response.text)  # Debug line for tracing
    if response.status_code == 200:
        return response.json()
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city'].strip()
    if not city:
        return render_template('index.html', error='Please enter a city name.')

    data = get_weather_data(city)
    if data:
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        humidity = data['main']['humidity']
        wind = data['wind']['speed']
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute('INSERT INTO weather (location, date, temperature, description, humidity, wind_speed) VALUES (?, ?, ?, ?, ?, ?)',
                      (city, date, temp, desc, humidity, wind))
            conn.commit()

        return render_template('weather.html', city=city, temperature=temp, description=desc, humidity=humidity, wind_speed=wind)
    return render_template('index.html', error=f'City "{city}" not found or API error!')

@app.route('/history')
def history():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM weather ORDER BY date DESC')
        records = c.fetchall()
    return render_template('history.html', rows=records)

@app.route('/delete/<int:record_id>', methods=['POST'])
def delete_record(record_id):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('DELETE FROM weather WHERE id = ?', (record_id,))
        conn.commit()
    return redirect(url_for('history'))

@app.route('/edit/<int:record_id>', methods=['GET', 'POST'])
def edit_record(record_id):
    if request.method == 'GET':
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM weather WHERE id = ?', (record_id,))
            record = c.fetchone()
        if record:
            return render_template('edit.html', record=record)
        else:
            return redirect(url_for('history'))  # If no record is found, redirect to history.

    if request.method == 'POST':
        city = request.form['city']
        temperature = request.form['temperature']
        description = request.form['description']
        humidity = request.form['humidity']
        wind_speed = request.form['wind_speed']

        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute('''UPDATE weather SET location = ?, temperature = ?, description = ?, humidity = ?, wind_speed = ? WHERE id = ?''',
                      (city, temperature, description, humidity, wind_speed, record_id))
            conn.commit()
        return redirect(url_for('history'))

if __name__ == '__main__':
    app.run(debug=True)
