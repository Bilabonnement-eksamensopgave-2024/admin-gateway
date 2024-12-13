from flask import Flask, jsonify, request, make_response
import requests
import os
from dotenv import load_dotenv


app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# MICROSERVICES:
MICROSERVICES = {
    "subscription": os.getenv("ABONNEMENT_MICROSERVICE_URL", "http://localhost:5006"),
    "user": os.getenv("USER_MICROSERVICE_URL", "http://localhost:5005"),
    "damage": os.getenv("SKADE_MICROSERVICE_URL", "http://localhost:5007"),
    "car": os.getenv("CAR_MICROSERVICE_URL", "http://localhost:5008"),
}

# ----------------------------------------------------- GET /
@app.route('/', methods=['GET'])
def service_info():
    return jsonify({
        "service": "Admin Gateway",
        "description": "This gateway has access to all endpoints across all microservices in the system. As long as you are logged into an admin user, you control everything in the system.",
        "endpoints": {
            "subscription": [
                {
                    "path": "/subscription/subscriptions",
                    "method": "GET",
                    "description": "Retrieve a list of subscriptions",
                    "role_required": ["admin", "finance", "sales"]
                },
                {
                    "path": "/subscription/subscriptions/<int:id>",
                    "method": "GET",
                    "description": "Retrieve a specific subscription by ID",
                    "role_required": ["admin", "sales"]
                },
                {
                    "path": "/subscription/subscriptions/current",
                    "method": "GET",
                    "description": "Retrieve a list of current active subscriptions",
                    "role_required": ["admin"]
                },
                {
                    "path": "/subscription/subscriptions/current/total-price",
                    "method": "GET",
                    "description": "Retrieve the total price of current active subscriptions",
                    "role_required": ["admin", "finance"]
                },
                {
                    "path": "/subscription/subscriptions/<int:id>/car",
                    "method": "GET",
                    "description": "Retrieve car information for a specific subscription by ID",
                    "role_required": ["admin", "sales"]
                },
                {
                    "path": "/subscription/subscriptions",
                    "method": "POST",
                    "description": "Add a new subscription",
                    "role_required": ["admin", "sales"]
                },
                {
                    "path": "/subscription/subscriptions/<int:id>",
                    "method": "PATCH",
                    "description": "Update an existing subscription",
                    "role_required": ["admin", "sales"]
                },
                {
                    "path": "/subscription/subscriptions/<int:id>",
                    "method": "DELETE",
                    "description": "Delete a subscription by ID",
                    "role_required": ["admin", "sales"]
                }
            ],
            "user": [
                {
                    "path": "/user/register",
                    "method": "POST",
                    "description": "Register a new user",
                    "response": "JSON object with success or error message",
                    "role_required": ["none"]
                },
                {
                    "path": "/user/login",
                    "method": "POST",
                    "description": "Authenticate a user and return a token",
                    "response": "JSON object with token or error message",
                    "role_required": ["none"]
                },
                {
                    "path": "/user/users",
                    "method": "GET",
                    "description": "Retrieve a list of all users",
                    "response": "JSON array of user objects",
                    "role_required": ["admin"]
                },
                {
                    "path": "/user/users/<int:id>",
                    "method": "PATCH",
                    "description": "Update email or password of a specific user",
                    "response": "JSON object with success or error message",
                    "role_required": ["admin"]
                },
                {
                    "path": "/user/users/<int:id>/add-role",
                    "method": "PATCH",
                    "description": "Add a role to a specific user",
                    "response": "JSON object with success or error message",
                    "role_required": ["admin"]
                },
                {
                    "path": "/user/users/<int:id>/remove-role",
                    "method": "PATCH",
                    "description": "Remove a role from a specific user",
                    "response": "JSON object with success or error message",
                    "role_required": ["admin"]
                },
                {
                    "path": "/user/users/<int:id>",
                    "method": "DELETE",
                    "description": "Delete a user by ID",
                    "response": "JSON object with success or error message",
                    "role_required": ["admin"]
                },
                {
                    "path": "/user/health",
                    "method": "GET",
                    "description": "Check the health status of the microservice",
                    "response": "JSON object indicating the health status",
                    "role_required": ["none"]
                },
                {
                    "path": "/user/logout",
                    "method": "POST",
                    "description": "Logout and delete the authorization cookie",
                    "response": "JSON object with a success message",
                    "role_required": ["none"]
                }
            ],
            "damage": [
                {
                    "path": "/damage/damage-types",
                    "method": "GET",
                    "description": "Retrieve a list of all damage types",
                    "role-required": ["admin", "finance", "maintenance"],
                    "response": "JSON array of damage type objects"
                },
                {
                    "path": "/damage/damage-types/<int:id>",
                    "method": "GET",
                    "description": "Retrieve a specific damage type by ID",
                    "role-required": ["admin", "maintenance"],
                    "response": "JSON object of a specific damage type or 404 error"
                },
                {
                    "path": "/damage/damage-types",
                    "method": "POST",
                    "description": "Add a new damage type",
                    "role-required": ["admin", "maintenance"],
                    "response": "JSON object with success message or error"
                },
                {
                    "path": "/damage/damage-types/<int:id>",
                    "method": "PATCH",
                    "description": "Update an existing damage type by ID",
                    "role-required": ["admin", "maintenance"],
                    "response": "JSON object with success message or 404 error"
                },
                {
                    "path": "/damage/damage-types/<int:id>",
                    "method": "DELETE",
                    "description": "Delete a damage type by ID",
                    "role-required": ["admin", "maintenance"],
                    "response": "JSON object with success message or error"
                }
            ],
            "car": [
                {
                    "path": "/car/cars",
                    "method": "POST",
                    "description": "Add a new car to the system",
                    "response": "JSON object with success or error message",
                    "role_required": ["admin"]
                },
                {
                    "path": "/car/cars",
                    "method": "GET",
                    "description": "Retrieve a list of all cars",
                    "response": "JSON array of car objects",
                    "role_required": ["admin", "maintenance"]
                },
                {
                    "path": "/car/cars/<int:id>",
                    "method": "GET",
                    "description": "Retrieve details of a specific car by ID",
                    "response": "JSON object with car details",
                    "role_required": ["admin", "maintenance"]
                },
                {
                    "path": "/car/cars/<int:id>",
                    "method": "PATCH",
                    "description": "Update details of a specific car (e.g., availability or kilometers driven)",
                    "response": "JSON object with success or error message",
                    "role_required": ["admin", "maintenance"]
                },
                {
                    "path": "/car/cars/<int:id>",
                    "method": "DELETE",
                    "description": "Delete a car by ID",
                    "response": "JSON object with success or error message",
                    "role_required": ["admin"]
                },
                {
                    "path": "/car/cars/available",
                    "method": "GET",
                    "description": "Check the availability of all cars",
                    "response": "JSON array of available cars",
                    "role_required": ["admin", "sales"]
                },
                {
                    "path": "/car/health",
                    "method": "GET",
                    "description": "Check the health status of the microservice",
                    "response": "JSON object indicating the health status",
                    "role_required": ["none"]
                }
            ]
        }
    })

# ----------------------------------------------------- ENDPOINTS /service/path
@app.route('/<service>/<path:path>', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def gateway_service(service, path):
    if service not in MICROSERVICES:
        return jsonify({"error": "Service not found"}), 404
    
    # Get the full URL for the microservice
    url = f"{MICROSERVICES[service]}/{path}"

    print(url)

    # Set Content-Type to application/json for methods that typically have a body 
    headers = {}
    if request.method in ['POST', 'PATCH', 'PUT']: 
        headers['Content-Type'] = 'application/json'

    # Forward request with appropriate HTTP method
    response = requests.request(
        method=request.method,
        url=url,
        headers=headers,
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

# ----------------------------------------------------- Catch-all route for unmatched endpoints 
@app.errorhandler(404)
def page_not_found_404(e):
    return jsonify({"message": "Endpoint does not exist"})

@app.errorhandler(405)
def page_not_found_405(e):
    return jsonify({"message": "Method not allowed - double check the method you are using"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
