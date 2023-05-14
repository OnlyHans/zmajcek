from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sensor_data.db'
db = SQLAlchemy(app)

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperatura = db.Column(db.Float)
    vlaga = db.Column(db.Float)
    svetlost = db.Column(db.Float)
    GLasnost = db.Column(db.Float)

@app.route('/save-sensor-data', methods=['POST'])
def save_sensor_data():
    data = request.get_json()
    sensor_data = SensorData(
        temperaturq=data['temperature'],
        vlaga=data['humidity'],
        svetlost=data['light_intensity'],
        glasnost=data['carbon_monoxide']
    )
    db.session.add(sensor_data)
    db.session.commit()
    return 'Data saved successfully!'

@app.route('/get-sensor-data', methods=['GET'])
def get_sensor_data():
    sensor_data = SensorData.query.all()
    data = []
    for row in sensor_data:
        data.append({
            'temperatura': row.temperatura,
            'vlaga': row.vlaga,
            'svetlsot': row.svetlsot,
            'glasnost': row.glasnost
        })
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0')