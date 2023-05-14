from flask import Flask, request, render_template

import sqlite3

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['DATABASE'] = 'sensor_data.db'

def get_db():
    """Connect to the SQLite database."""
    db = sqlite3.connect(app.config['DATABASE'])
    db.row_factory = sqlite3.Row
    return db

def init_db():
    """Create the database tables."""
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/save-sensor-data', methods=['POST'])
def save_sensor_data():
    data = request.get_json()
    db = get_db()
    db.execute('INSERT INTO SensorData (temperature, humidity, light_intensity, carbon_monoxide) VALUES (?, ?, ?, ?)', (data['temperature'], data['humidity'], data['light_intensity'], data['carbon_monoxide']))
    db.commit()
    return 'Data saved successfully!'

@app.route('/view-sensor-data', methods=['GET'])
def view_sensor_data():
    db = get_db()
    cursor = db.execute('SELECT * FROM SensorData ORDER BY id DESC')
    rows = cursor.fetchall()
    return render_template('sensor_data.html', rows=rows)

if __name__ == '__main__':
    init_db()
    app.run()
