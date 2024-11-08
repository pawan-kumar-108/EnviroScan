from flask import Flask
from flask_cors import CORS
import api  # Import the API routes from api.py

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for all routes

# Register the routes from api.py with the app
app.register_blueprint(api.bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
else:
    # Use Gunicorn to run the application
    import gunicorn
    from gunicorn.app.base import Application

    class FlaskApplication(Application):
        def __init__(self, app):
            self.application = app
            super().__init__()

        def load_config(self):
            self.cfg.set("worker_class", "gevent")
            self.cfg.set("bind", "0.0.0.0:5000")
            self.cfg.set("pathConfig", "")

        def load(self):
            return self.application

    if __name__ == "__main__":
        FlaskApplication(app).run()
