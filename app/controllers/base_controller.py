"""Base controller"""

import json
from flask import Response

class BaseController:
    """Base controller class"""

    def convert_object_to_dict(self, item):
        """Funtion to convert an object to dictionary"""
        item.__dict__.pop("_sa_instance_state")
        return item.__dict__

    def formatt_response(self, status_code, message, data):
        """Function to formatt the service response"""
        response = {
            "status": True if status_code in (200, 201, 202) else False,
            "status_code": status_code,
            "message": message,
            "data": data
        }
        return Response(
            response=json.dumps(response, default=str),
            status=status_code,
            mimetype='application/json'
        )
