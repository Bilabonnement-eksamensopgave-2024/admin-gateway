from flasgger import Swagger

# Swagger configuration
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs"
}

template = {
    "info": {
        "title": "Admin gateway",
        "description": "This gateway has access to all microservices in the system.",
        "version": "1.0.0",
    },
    "securityDefinitions": {
        "cookieAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "cookie",
            "description": "Example: '{token}'"
        }
    },
    "security": [
        {
            "cookieAuth": []
        }
    ]
}

def init_swagger(app):
    """Initialize Swagger with the given Flask app"""
    return Swagger(app, config=swagger_config, template=template)
