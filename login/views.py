from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import base64
from importlib import import_module
from django.conf import settings
import requests
response = requests.post('http://localhost:8000/signup', json={'email': '....', 'password': 'zxcv in base64'})

SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
from django.contrib.sessions.backends.db import SessionStore


@csrf_exempt
def login(request):
    body_json = json.loads(request.body)
    u = User.objects.filter(email=body_json['email']).first()
    if u is None:
        return HttpResponse(json.dumps({
            "meta": {
                "errors": [
                    1
                ]
            },
            "session_token": None
        }), status=401)

    if u.check_password(base64.b64decode(body_json['password'].encode('utf-8')).decode('utf-8')):
        s = SessionStore()
        s['user_id'] = u.id
        s.create()

        return HttpResponse(json.dumps({
            "meta": {
                "errors": []
            },
            "session_token": s.session_key
        }))

    else:
        return HttpResponse(json.dumps({
            "meta": {
                "errors": [
                    1
                ]
            },
            "session_token": None
        }), status=401)


def sign_up(request):
    body_json = json.loads(request.body)
    u = User.objects.filter(email=body_json['email']).first()
    if u is not None:
        return HttpResponse(json.dumps({
            "meta": {
                "errors": [
                    2
                ]
            },
            "session_token": None,
            "confirmed": False
        }), status=400)
