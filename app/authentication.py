import requests
import json
from . import app
import os

class LoginSuprema:
    def __init__(self):
        self.bs_session_id = None
    
    def save_session_id_to_json(self):
        data = {
            "bs-session-id": self.bs_session_id
        }
        
        file_path = os.path.join(app.config['SESSION_DIR'], 'session.json')
        with open(file_path, 'w') as outfile:
            json.dump(data, outfile)
    
    def login(self):
        url = app.config['SUPREMA_URL'] + '/api/login'

        payload = json.dumps({
            "User" : {
                "login_id" : app.config['USERNAME_SUPREMA'],
                "password" : app.config['PASSWORD_SUPREMA']
            }
        })

        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        if response.status_code == 200:
            get_session = response.headers.get('bs-session-id')
            self.bs_session_id = get_session
            self.save_session_id_to_json()