
# SUPREMA API

This program is for SUPREMA API to get all visitor management in application name serelo


## Features

- GET data for person check-in
- GET data LOG
- GET data for floor
- GET data for latest visitor on that floor


## Installation

- You have to install [Docker](https://docs.docker.com/engine/).
- Then you can install [Portainer](https://docs.portainer.io/start/install-ce) for organize the container

    
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

1. Create docker-compose.yml
```
version: "3"
services:
  web:
    build: .
    ports:
      - "{PORT_APPLICATION}:{PORT_APPLICATION}"
    volumes:
      - .:/app
    restart: always
```

2. Create Dockerfile
```
FROM python:3.8-slim-buster
WORKDIR /app
RUN apt-get update && apt-get install -y 
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD [ "python", "run.py"]
```

3.Create config.py
```
import os

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'super secret key'
``` 

## Deployment

To deploy this project run

```bash
  docker-compose up -d --build
```

