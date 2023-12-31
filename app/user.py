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
    id = request.form.get('id')
    name = request.form.get('name')
    email = request.form.get('email')
    first_image = request.form.get('first_image')
    second_image = request.form.get('second_image')
    department_id = request.form.get('department_id')

    session = check_session_id()
    usertype = request.form.get('type')

    url = app.config['SUPREMA_URL'] + '/api/users'
    url_visualface = app.config['SUPREMA_URL'] + '/api/users/' + id

    headers = {
        'Content-Type': 'application/json',
        'bs-session-id': session
    }
    if first_image and second_image:
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
        send_visualface_request = True
    elif first_image or second_image:
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
        send_visualface_request = True
    else:
        payload_visualface = None
        send_visualface_request = False

    if usertype == "employee" and department_id == "1":
        payload = json.dumps({
        "User": {
            "name": name,
            "user_id": id,
            "email": email,
            "user_group_id": {
                "id": 1062
            },
            "access_groups": {
                "id": 10
            },
            "disabled": "false",
            "start_datetime": "2023-01-01T00:00:00.00Z",
            "expiry_datetime": "2030-12-31T23:59:00.00Z"
        }
        })
    elif usertype == "employee" and department_id == "2":
        payload = json.dumps({
        "User": {
            "name": name,
            "user_id": id,
            "email": email,
            "user_group_id": {
                "id": 1016
            },
            "access_groups": {
                "id": 3
            },
            "disabled": "false",
            "start_datetime": "2023-01-01T00:00:00.00Z",
            "expiry_datetime": "2030-12-31T23:59:00.00Z"
        }
        })
    elif usertype == "employee" and department_id == "3":
        payload = json.dumps({
        "User": {
            "name": name,
            "user_id": id,
            "email": email,
            "user_group_id": {
                "id": 1015
            },
            "access_groups": {
                "id": 15
            },
            "disabled": "false",
            "start_datetime": "2023-01-01T00:00:00.00Z",
            "expiry_datetime": "2030-12-31T23:59:00.00Z"
        }
        })
    elif usertype == "employee" and department_id == "6":
        payload = json.dumps({
        "User": {
            "name": name,
            "user_id": id,
            "email": email,
            "user_group_id": {
                "id": 1069
            },
            "access_groups": {
                "id": 15,
            },
            "disabled": "false",
            "start_datetime": "2023-01-01T00:00:00.00Z",
            "expiry_datetime": "2030-12-31T23:59:00.00Z"
        }
        })
    elif usertype == "employee" and department_id == "7":
        payload = json.dumps({
        "User": {
            "name": name,
            "user_id": id,
            "email": email,
            "user_group_id": {
                "id": 1071
            },
            "access_groups": {
                "id": 4,
            },
            "disabled": "false",
            "start_datetime": "2023-01-01T00:00:00.00Z",
            "expiry_datetime": "2030-12-31T23:59:00.00Z"
        }
        })
    elif usertype == "employee" and department_id == "8":
        payload = json.dumps({
        "User": {
            "name": name,
            "user_id": id,
            "email": email,
            "user_group_id": {
                "id": 1075
            },
            "access_groups": {
                "id": 4,
            },
            "disabled": "false",
            "start_datetime": "2023-01-01T00:00:00.00Z",
            "expiry_datetime": "2030-12-31T23:59:00.00Z"
        }
        })
    elif usertype == "employee" and department_id == "9":
        payload = json.dumps({
        "User": {
            "name": name,
            "user_id": id,
            "email": email,
            "user_group_id": {
                "id": 1069
            },
            "access_groups": {
                "id": 4,
            },
            "disabled": "false",
            "start_datetime": "2023-01-01T00:00:00.00Z",
            "expiry_datetime": "2030-12-31T23:59:00.00Z"
        }
        })
    elif usertype == "employee" and department_id == "10":
        payload = json.dumps({
        "User": {
            "name": name,
            "user_id": id,
            "email": email,
            "user_group_id": {
                "id": 1076
            },
            "access_groups": {
                "id": 4,
            },
            "disabled": "false",
            "start_datetime": "2023-01-01T00:00:00.00Z",
            "expiry_datetime": "2030-12-31T23:59:00.00Z"
        }
        })
    elif usertype == "employee" and department_id == "11":
        payload = json.dumps({
        "User": {
            "name": name,
            "user_id": id,
            "email": email,
            "user_group_id": {
                "id": 1018
            },
            "access_groups": {
                "id": 4,
            },
            "disabled": "false",
            "start_datetime": "2023-01-01T00:00:00.00Z",
            "expiry_datetime": "2030-12-31T23:59:00.00Z"
        }
        })
    elif usertype == "employee" and department_id == "12":
        payload = json.dumps({
        "User": {
            "name": name,
            "user_id": id,
            "email": email,
            "user_group_id": {
                "id": 1074
            },
            "access_groups": {
                "id": 4,
            },
            "disabled": "false",
            "start_datetime": "2023-01-01T00:00:00.00Z",
            "expiry_datetime": "2030-12-31T23:59:00.00Z"
        }
        })
    else :
        payload = json.dumps({
        "User": {
            "name": name,
            "user_id": id,
            "email": email,
            "user_group_id": {
                "id": 1025
            },
            "access_groups": {
                "id": 17,
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
            if data_user["Response"]["code"] == "0" and send_visualface_request:
                response_visualface = requests.request("PUT", url=url_visualface, headers=headers, data=payload_visualface, verify=False)
                if response_visualface.status_code == 200:
                    data_photo = response_visualface.json()
                    if data_photo["Response"]["code"] == "0":
                        return jsonify({"message": "Successfully Create User", "data photo": data_photo, "data user": data_user}), 200
                    else:
                        return jsonify(data_photo), 400
                else:
                    return jsonify({'message': response_visualface.json()}), 400
            elif data_user["Response"]["code"] == "0" and send_visualface_request != True:
                return jsonify({"message": "Successfully Create User", "data user" : data_user}), 200
            else:
                return jsonify(data_user)
        else:
            return jsonify(response_user.json(), payload), 500
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


def update_employee():
    id = request.form.get('id')
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    department_id = request.form.get('department_id')
    first_image = request.form.get('first_image')
    second_image = request.form.get('second_image')

    session = check_session_id()

    url = app.config['SUPREMA_URL'] + '/api/users/' + id

    headers = {
        'Content-Type': 'application/json',
        'bs-session-id': session
    }

    if first_image and second_image:
        payload = json.dumps({
            "User": {
                "name": name,
                "phone" : str(phone),
                "email": email,
                "user_group_id": {
                    "id": int(department_id)
                },
                "disabled": False,
                "start_datetime": "2001-01-02T00:00:00.00Z",
                "expiry_datetime": "2030-12-31T23:59:00.00Z",
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
    elif first_image == True and second_image != True:
        payload = json.dumps({
            "User": {
                "name": name,
                "phone" : str(phone),
                "email": email,
                "user_group_id": {
                    "id": int(department_id)
                },
                "disabled": "false",
                "start_datetime": "2023-01-01T00:00:00.00Z",
                "expiry_datetime": "2030-12-31T23:59:00.00Z",
                "credentials": {
                        "visualFaces": [
                            {
                                "template_ex_picture": first_image
                            }
                        ]
                    }
                }
        })
    elif first_image and second_image != True:
        payload = json.dumps({
        "User": {
            "name": name,
            "email": email,
            "phone" : str(phone),
            "user_group_id": {
                "id": int(department_id)
            },
            "disabled": "false",
            "start_datetime": "2023-01-01T00:00:00.00Z",
            "expiry_datetime": "2030-12-31T23:59:00.00Z"
        }
        })
    
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
    