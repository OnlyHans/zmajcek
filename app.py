from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sensor_data.db'
db = SQLAlchemy(app)

class SenzorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperatura = db.Column(db.Float)
    vlaznost = db.Column(db.Float)
    svetlost = db.Column(db.Float)
    glasnost = db.Column(db.Float)
    CO = db.Column(db.Float)

@app.route('/save-sensor-data', methods=['POST'])
def shrani_podatke():
    data = request.get_json()
    sensor_data = SenzorData(
        temperatura=data['temperatura'],
        vlaznost=data['vlaznost'],
        glasnost=data['glasnost'],
        svetlost=data['svetlost'],
        CO=data['CO']
    )
    db.session.add(sensor_data)
    db.session.commit()
    return 'Data saved successfully!'

if __name__ == '__main__':
    app.run(host='0.0.0.0')