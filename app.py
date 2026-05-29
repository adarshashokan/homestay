from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template
from config import Config
from models import db
from routes.auth import auth
from routes.properties import properties
from routes.bookings import bookings
from routes.admin import admin

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Register blueprints
app.register_blueprint(auth, url_prefix='/api')
app.register_blueprint(properties, url_prefix='/api')
app.register_blueprint(bookings, url_prefix='/api')
app.register_blueprint(admin, url_prefix='/api')

# Security headers
@app.after_request
def set_security_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/properties')
def properties_page():
    return render_template('properties.html')

@app.route('/booking')
def booking_page():
    return render_template('booking.html')

@app.route('/admin')
def admin_page():
    return render_template('admin.html')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()
