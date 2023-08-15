from flask import jsonify, request
import json
import requests
from . import app
from . import authentication
from genericpath import exists

@app.route('/api/v1/all/door', methods=['GET'])
def getAllDoor():
    file_path = app.config['SESSION_DIR'] + '/session.json'

    if file_path is not exists:
        authentication.login()
    
    with open(file_path, 'r') as f:
        data = json.load(f)
        session_id = data['bs-session-id']

    url = app.config['SUPREMA_URL'] + '/api/doors?limit=0&order_by=id:true'
    headers = {
        'bs-session-id' : session_id
    }

    try:
        data = requests.get(url, headers=headers)
        if data.status_code == 200:
            data = data.json()
            if data['Response']['message'] != 'success' and data['Response']['code'] != '0':
                return jsonify({'error': 'failed to get all door', 'data' : data}), 500
            else:
                return jsonify({'message': 'success', 'data' : data }), 200
        else:
            return jsonify({'error': 'failed to get all door', 'data' : data}), 500
    except Exception as e:
        return jsonify({'error': 'failed to get all door', 'data' : str(e)}), 500

            
        






