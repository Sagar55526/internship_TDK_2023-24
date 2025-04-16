from flask import Flask, render_template, jsonify
from flask_cors import CORS
import random
import time
import pyodbc
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib
from threading import Thread

app = Flask(__name__, template_folder='app/templates')
CORS(app)

server = 'LAPTOP-ANRSA6BB\SQLEXPRESS'
database = 'Pred_ML'
username = ''
password = ''

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};\
                      SERVER='+server+';\
                      DATABASE='+database+';\
                      Trusted_Connection=yes;')

cursor = cnxn.cursor()

def generate_random_value():
    return random.uniform(0, 50)

def insert_data_to_sql(value, timestamp):
    query = "INSERT INTO random_val (value, timestamp) VALUES (?, ?)"
    cursor.execute(query, value, timestamp)
    cnxn.commit()

def fetch_historical_data():
    query = "SELECT timestamp, value FROM random_val ORDER BY timestamp"
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows

def train_and_save_model():
    historical_data = fetch_historical_data()

    if not historical_data:
        print("No historical data available. Unable to train the model.")
        return

    timestamps, values = zip(*historical_data)

    numerical_timestamps = np.array([(t - timestamps[0]).total_seconds() for t in timestamps]).reshape(-1, 1)

    model = LinearRegression()
    model.fit(numerical_timestamps, values)

    joblib.dump(model, 'linear_regression_model.pkl')


def load_model():
    try:
        model = joblib.load('linear_regression_model.pkl')
        return model
    except FileNotFoundError:
        print("Model file not found. Please train the model first.")
        return None

def predict_value(model, timestamps, values, timestamp):
    if model is None:
        return None

    numerical_timestamps = np.array([(t - timestamps[0]).total_seconds() for t in timestamps]).reshape(-1, 1)

    model.fit(numerical_timestamps, values)

    numerical_timestamp = (timestamp - timestamps[0]).total_seconds()

    predicted_value = model.predict([[numerical_timestamp]])

    return predicted_value[0]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def get_data():
    historical_data = fetch_historical_data()
    print('Historical Data:', historical_data)
    timestamps, values = zip(*historical_data)

    model = load_model()  
    if model is not None:
        model.fit(np.array([(t - timestamps[0]).total_seconds() for t in timestamps]).reshape(-1, 1), values)
        predictions = model.predict(np.array([(t - timestamps[0]).total_seconds() for t in timestamps]).reshape(-1, 1))
        current_timestamp = timestamps[-1] + (timestamps[-1] - timestamps[-2])  
        predicted_value = predict_value(model, timestamps, values, current_timestamp)
    else:
        predictions = []
        predicted_value = None

    return jsonify({
        'timestamps': timestamps,
        'values': values,
        'predictions': predictions.tolist(),
        'predicted_value': predicted_value
    })

def generate_dummy_data(interval_seconds):
    while True:
        value = generate_random_value()
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        insert_data_to_sql(value, timestamp)

        print(f"{timestamp}: {value} - Data inserted into SQL Server")

        time.sleep(interval_seconds)

if __name__ == "__main__":
    interval = 10

    train_and_save_model()

    dummy_data_thread = Thread(target=generate_dummy_data, args=(interval,))
    dummy_data_thread.start()

    app.run(host='0.0.0.0', port=5000, debug=True)
