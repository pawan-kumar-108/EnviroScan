from flask import Flask
from flask_cors import CORS
import api  # Import the API routes from api.py

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for all routes

#Register the routes from api.py with the app
app.register_blueprint(api.bp)

if __name__ == "__main":
    app.run(host="0.0.0.0", port=5000, debug=True)
