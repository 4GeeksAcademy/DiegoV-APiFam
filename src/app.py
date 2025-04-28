"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)


jackson_family = FamilyStructure("Jackson")


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/members', methods=['POST'])
def add_a_member(): 
    try: 
        request_body = request.get_json() 
        if not request_body: 
            return jsonify({"msg": "No request body"}), 400
        new_member = jackson_family.add_member(request_body)
        return jsonify(new_member), 200
    except Exception as e:
        return jsonify({"msg": "Internal server error", "error": str(e)}), 500


@app.route('/members/<int:id>', methods=['GET'])
def get_member(id): 
    try: 
        member = jackson_family.get_member(id)
        if member: 
            return jsonify(member), 200 
        else:
            return jsonify({"msg": "Member not found"}), 404 
    except Exception as e:
        return jsonify({"msg": "Internal server error", "error": str(e)}), 500


@app.route('/members/<int:id>', methods=['DELETE'])
def delete_a_member(id): 
    try: 
        deleted = jackson_family.delete_member(id)
        if deleted:
            return jsonify({"done": True}), 200
        else:
            return jsonify({"done": False}), 404
    except Exception as e:
        return jsonify({"msg": "Internal server error", "error": str(e)}), 500

@app.route('/members/<int:id>', methods=['PUT'])
def update_a_member(id): 
    try:
        updated_data = request.get_json()
        if not updated_data:
            return jsonify({"msg": "No data provided"}), 400
        updated = jackson_family.update_member(id, updated_data)
        if updated:
            return jsonify(updated), 200
        return jsonify({"msg": "Member not found"}), 404
    except Exception as e:
        return jsonify({"msg": "Internal server error", "error": str(e)}), 500


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
