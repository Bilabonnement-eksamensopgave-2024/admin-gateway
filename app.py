from flask import Flask, jsonify, request, make_response
import requests
import sqlite3
import bcrypt
import os
import jwt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flasgger import swag_from
import datetime
from swagger.config import init_swagger
import user
import auth

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# MICROSERVICES:
MICROSERVICES = {
    "room_inventory_service": os.getenv("ROOM_INVENTORY_SERVICE_URL", "http://localhost:5002"),
    "reservation_service": os.getenv("RESERVATION_SERVICE_URL", "http://localhost:5003"),
    "csv_export_service": os.getenv("CSV_EXPORT_SERVICE_URL", "http://localhost:5005"),
    "drinks_service": os.getenv("DRINKS_SERVICE_URL", "http://localhost:5004"),
    "drinks_sales_service": os.getenv("DRINKS_SALES_SERVICE_URL", "http://localhost:5006"),
    "guest_service": os.getenv("GUEST_SERVICE_URL", "http://localhost:5001"),
}

# Initialize Swagger
init_swagger(app)

# ----------------------------------------------------- ENDPOINTS
@app.route('/<service>/<path:path>', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def gateway(service, path):
    if service not in MICROSERVICES:
        return jsonify({"error": "Service not found"}), 404

    # Get the full URL for the microservice
    url = f"{MICROSERVICES[service]}/{path}"

    # Forward request with appropriate HTTP method
    response = requests.request(
        method=request.method,
        url=url,
        headers={key: value for key, value in request.headers},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False
    )

    # Pass response back to client
    return (response.content, response.status_code, response.headers.items())

# ----------------------------------------------------- GET /health
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 80)))
