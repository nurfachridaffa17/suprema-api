from flask import jsonify, request
import json
import requests
from . import app
from .user import check_image, create_user, get_next_id

@app.route('/api/v1/check/image', methods=['PUT'])
def check_image_user():
    return check_image()

@app.route('/api/v1/get/next_id', methods=['GET'])
def get_id():
    return get_next_id()

@app.route('/api/v1/create/users', methods=['POST'])
def create_users():
    return create_user()