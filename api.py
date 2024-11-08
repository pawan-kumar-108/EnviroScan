from flask import Blueprint, jsonify, request, send_file
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import requests
import json
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Creating a Blueprint for the API routes
bp = Blueprint('api', __name__)

@bp.route('/')
def home():
    return jsonify({
        "message": "Welcome to EnviroScan ProÂ® API",
        "endpoints": {
            "/api/fetchWeather": "POST - Fetch real-time weather data",
            "/api/uploadCsv": "POST - Upload and process CSV data",
            "/api/generateImage": "POST - Generate visualization",
            "/api/analyzeData": "POST - Analyze environmental and health data"
        }
    })

ow_key = "3ed6ae1a33d62bce42c347ad500a1326"
# Route to fetch real-time weather data
@bp.route('/api/fetchWeather', methods=['POST'])
def fetch_weather():
    data = request.json
    api_key = data.get("api_key")
    lat = data.get("latitude")
    lon = data.get("longitude")
    
    if not api_key or not lat or not lon:
        return jsonify({"error": "Missing API key or coordinates"}), 400

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={ow_key}"
        response = requests.get(url)
        weather_data = response.json()
        
        # Extract main variables
        temperature = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]

        return jsonify({
            "temperature": temperature,
            "humidity": humidity
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to upload and process CSV data
@bp.route('/api/uploadCsv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400

    try:
        data = pd.read_csv(file)
        summary = data.describe().to_dict()
        return jsonify({"message": "CSV processed successfully", "summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to generate an image for visualization
@bp.route('/api/generateImage', methods=['POST'])
def generate_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400

    try:
        data = pd.read_csv(file, nrows=1000)
        img_buffer = BytesIO()
        plt.figure(figsize=(8, 6))

        if data.shape[1] >= 2:
            plt.scatter(data.iloc[:, 0], data.iloc[:, 1])
        plt.xlabel(data.columns[0])
        plt.ylabel(data.columns[1])
        plt.title("Sample Scatter Plot")
        plt.savefig(img_buffer, format='png')
        plt.close()
        img_buffer.seek(0)
        return send_file(img_buffer, mimetype='image/png')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to analyze environmental and health data using a simple regression model
@bp.route('/api/analyzeData', methods=['POST'])
def analyze_data():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400

    try:
        data = pd.read_csv(file)
        if data.shape[1] < 2:
            return jsonify({"error": "Data must have at least two columns for analysis"}), 400

        X = data.iloc[:, :-1].values
        y = data.iloc[:, -1].values

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = LinearRegression()
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)

        return jsonify({
            "message": "Data analyzed successfully",
            "mse": mse,
            "predictions": predictions[:10].tolist()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500