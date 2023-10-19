from . import app
from flask import request, jsonify, session
import json
import requests
from . import authentication
from genericpath import exists
import base64
from datetime import datetime

def check_session_id():
    file_path = app.config['SESSION_DIR'] + 'session.json'

    if file_path is not exists:
        getData = authentication.LoginSuprema()
        getData.login_api()
    
    with open(file_path, 'r') as f:
        data = json.load(f)
        session_id = data['bs-session-id']
    
    return session_id

def convert_image_base64(image_data):
    base64_bytes = base64.b64encode(image_data)
    base64_string = base64_bytes.decode('utf-8')  # Convert bytes to a UTF-8 encoded string
    return base64_string

def check_image():
    image = request.files['image']
    image_data = image.read()  # Read the binary data of the image

    session = check_session_id()
    
    base64_image = convert_image_base64(image_data)
    
    payload = json.dumps({
        "template_ex_picture": base64_image
    })

    url = app.config['SUPREMA_URL'] + '/api/users/check/upload_picture'
    headers = {
        'Content-Type': 'application/json',
        'bs-session-id': session
    }

    try:
        data = requests.put(url, headers=headers, data=payload, verify=False)
        if data.status_code == 200:
            data = data.json()
            if data['Response']['code'] != '0':
                return jsonify({'error': 'error image', 'data' : data}), 410
            else:
                return jsonify({'message': 'success', 'data' : data }), 200
        else:
            return jsonify({'message' : data.json()}), 500
    except Exception as e:
        return jsonify({'error': 'failed to check image', 'data' : str(e)}), 500


def get_next_id():
    session = check_session_id()
    url = app.config['SUPREMA_URL'] + '/api/users/next_user_id'

    payload = {}
    headers = {
    'bs-session-id': session
    }

    try:
        response = requests.request("GET", url, headers=headers, data=payload, verify=False)
        data = response.json()
        user_id = data["User"]["user_id"]
        return user_id
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to create user", "details": str(e)})
    

def create_user():
    name = request.form.get('name')
    email = request.form.get('email')
    first_image = request.form.get('first_image')
    second_image = request.form.get('second_image')
    group_id = app.config["USER_GROUP"]
    # first_image = request.files['first_image']
    # second_image = request.files['second_image']

    # data_first_image = first_image.read()
    # data_second_image = second_image.read()

    # base64_first_image = convert_image_base64(data_first_image)
    # base64_second_image = convert_image_base64(data_second_image)
    
    next_id = get_next_id()
    id_user = next_id

    session = check_session_id()
    usertype = request.form.get('type')

    url = app.config['SUPREMA_URL'] + '/api/users'
    url_visualface = app.config['SUPREMA_URL'] + '/api/users/' + id_user

    now = datetime.date.today().strftime('%Y-%m-%d')

    headers = {
        'Content-Type': 'application/json',
        'bs-session-id': session
    }

    if second_image:
        payload_visualface = json.dumps({
            "User": {
                "credentials": {
                    "visualFaces": [
                        {
                            "template_ex_picture": first_image
                        },
                        {
                            "template_ex_picture": second_image
                        }
                    ]
                }
            }
        })
    else:
        payload_visualface = json.dumps({
            "User": {
                "credentials": {
                    "visualFaces": [
                        {
                            "template_ex_picture": first_image
                        }
                    ]
                }
            }
        })

    if usertype == "employee":
        payload = json.dumps({
        "User": {
            "name": name,
            "user_id": id_user,
            "email": email,
            "user_group_id": {
                "id": 1
            },
            "disabled": "false",
            "start_datetime": "2023-01-01T00:00:00.00Z",
            "expiry_datetime": "2030-12-31T23:59:00.00Z"
        }
        })
    elif usertype == "visitor":
        payload = json.dumps({
        "User": {
            "name": name,
            "user_id": id_user,
            "email": email,
            "user_group_id": {
                "id": int(group_id)
            },
            "disabled": "false",
            "start_datetime": "2023-01-01T00:00:00.00Z",
            "expiry_datetime": "2023-01-01T23:59:00.00Z"
        }
        })
    try:
        response_user = requests.request("POST", url, headers=headers, data=payload, verify=False)
        if response_user.status_code == 200:
            data_user = response_user.json()
            if data_user["Response"]["code"] == "0":
                response_visualface = requests.request("PUT", url=url_visualface, headers=headers, data=payload_visualface, verify=False)
                if response_visualface.status_code == 200:
                    data_photo = response_visualface.json()
                    if data_photo["Response"]["code"] == "0":
                        return jsonify({"message" : "Successfully Create User", "data photo" : data_photo, "data user" : data_user}), 200
                    else:
                        return jsonify(data_photo), 400
                else:
                    return jsonify({'message' : response_visualface.json()}), 400
            else:
                return jsonify(data_user), 400
        else:
            return jsonify(response_user.json()), 500
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to create user", "details": str(e)})

def update_visitor():
    id = request.form.get('id')
    starttime = request.form.get('starttime')
    endtime = request.form.get('endtime')

    date_time_start = datetime.strptime(starttime, '%Y-%m-%d %H:%M')
    date_start = date_time_start.strftime('%Y-%m-%d')
    timestart = date_time_start.strftime('%H:%M')

    date_time_end = datetime.strptime(endtime, '%Y-%m-%d %H:%M')
    date_end = date_time_end.strftime('%Y-%m-%d')
    timeend = date_time_end.strftime('%H:%M')

    session = check_session_id()

    headers = {
        'Content-Type': 'application/json',
        'bs-session-id': session
    }

    payload = json.dumps({
        "User": {
            "start_datetime": f"{date_start}T{timestart}:00.00Z",
            "expiry_datetime": f"{date_end}T{timeend}:00.00Z"
        }
    })

    url = app.config['SUPREMA_URL'] + '/api/users/' + id

    try:
        response = requests.request("PUT", url, headers=headers, data=payload, verify=False)
        if response.status_code == 200:
            data_user = response.json()
            if data_user["Response"]["code"] == "0":
                return jsonify({"message" : "Successfully Update Visitor", "data user" : data_user}), 200
            else:
                return jsonify(data_user), 400
        else:
            return jsonify({'message' : response.json()}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to update visitor", "details": str(e)})





