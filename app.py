from flask import Flask
from flask_cors import CORS
import api  # Import the API routes from api.py

application = Flask(__name__)  # Create 'application' variable for Gunicorn
app = application  # Create app alias for Flask conventions
CORS(app)  # Enable Cross-Origin Resource Sharing for all routes

# Register the routes from api.py with the app
app.register_blueprint(api.bp)

if __name__ == "__main__":  # Fixed typo in "__main__"
    app.run(host="0.0.0.0", port=5000, debug=True)
