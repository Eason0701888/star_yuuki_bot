# -*- coding: utf-8 -*-
"""
Yuuki_Libs
(c) 2020 Star Inc.
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
import hashlib
import random
import time

from flask import Flask, render_template, request, redirect, jsonify
from flask_bootstrap import Bootstrap
from gevent.pywsgi import WSGIServer

from .api import Yuuki_WebAdminAPI

wa_app = Flask(__name__)
Yuuki_Handle = None
Yuuki_APIHandle = None

passports = []
password = str(hash(random.random()))
shutdown_password = str(hash(random.random()))


class Yuuki_WebAdmin:
    Bootstrap(wa_app)
    http_server = None

    def __init__(self, Yuuki):
        global Yuuki_Handle, Yuuki_APIHandle
        Yuuki_Handle = Yuuki
        Yuuki_APIHandle = Yuuki_WebAdminAPI(Yuuki_Handle, self)

    @staticmethod
    @wa_app.route("/")
    def index():
        if "yuuki_admin" in request.cookies:
            if request.cookies["yuuki_admin"] in passports:
                return render_template(
                    'manage/index.html',
                    version=Yuuki_Handle.YuukiConfigs["version"],
                    LINE_Media_server=Yuuki_Handle.LINE_Media_server,
                    profileName=Yuuki_Handle.profile.displayName,
                    pictureStatus=Yuuki_Handle.profile.pictureStatus
                )
            else:
                response = redirect("/")
                response.set_cookie(
                    key='yuuki_admin',
                    value='',
                    expires=0
                )
                return response
        else:
            return render_template(
                'index.html',
                name=Yuuki_Handle.YuukiConfigs["name"],
                version=Yuuki_Handle.YuukiConfigs["version"]
            )

    @staticmethod
    @wa_app.route("/groups")
    def groups():
        if "yuuki_admin" in request.cookies:
            if request.cookies["yuuki_admin"] in passports:
                return render_template(
                    'manage/groups.html',
                    LINE_Media_server=Yuuki_Handle.LINE_Media_server
                )
        response = redirect("/")
        response.set_cookie(
            key='yuuki_admin',
            value='',
            expires=0
        )
        return response

    @staticmethod
    @wa_app.route("/helpers")
    def helpers():
        if "yuuki_admin" in request.cookies:
            if request.cookies["yuuki_admin"] in passports:
                return render_template(
                    'manage/helpers.html'
                )
        response = redirect("/")
        response.set_cookie(
            key='yuuki_admin',
            value='',
            expires=0
        )
        return response

    @staticmethod
    @wa_app.route("/settings")
    def settings():
        if "yuuki_admin" in request.cookies:
            if request.cookies["yuuki_admin"] in passports:
                return render_template(
                    'manage/settings.html',
                    version=Yuuki_Handle.YuukiConfigs["version"],
                    project_url=Yuuki_Handle.YuukiConfigs["project_url"]
                )
        response = redirect("/")
        response.set_cookie(
            key='yuuki_admin',
            value='',
            expires=0
        )
        return response

    @staticmethod
    @wa_app.route("/verify", methods=['GET', 'POST'])
    def verify():
        result = {"status": 403}
        if request.method == "POST" and "code" in request.values:
            if request.values["code"] == password:
                seed = hash(random.random() + time.time())
                seed = str(seed).encode('utf-8')
                session_key = hashlib.sha256(seed).hexdigest()
                passports.append(session_key)
                result = {"status": 200, "session": session_key}
            else:
                result = {"status": 401}
        return jsonify(result)

    @staticmethod
    @wa_app.route("/logout")
    def logout():
        response = redirect("/")
        if "yuuki_admin" in request.cookies:
            if request.cookies.get("yuuki_admin") in passports:
                passports.remove(request.cookies.get("yuuki_admin"))
            response.set_cookie(
                key='yuuki_admin',
                value='',
                expires=0
            )
        return response

    @staticmethod
    @wa_app.route("/events")
    def events():
        if "yuuki_admin" in request.cookies:
            if request.cookies["yuuki_admin"] in passports:
                return render_template(
                    'manage/events.html'
                )
        response = redirect("/")
        response.set_cookie(
            key='yuuki_admin',
            value='',
            expires=0
        )
        return response

    @staticmethod
    @wa_app.route("/api", methods=['GET', 'POST'])
    def api():
        result = {"status": 403}
        if request.method == "POST" and "task" in request.values:
            if request.cookies.get("yuuki_admin") in passports:
                query_result = Yuuki_APIHandle.action(
                    task=request.values.get("task"),
                    data=request.values.get("data")
                )
                result = {"status": 200, "result": query_result}
            else:
                result = {"status": 401}
        return jsonify(result)

    @staticmethod
    @wa_app.route("/api/shutdown")
    @wa_app.route("/api/shutdown/<code>")
    def shutdown(code=None):
        if code == shutdown_password:
            Yuuki_APIHandle.command_shutdown()
            return "200"
        return "401"

    @staticmethod
    @wa_app.route("/api/i")
    def i():
        return Yuuki_Handle.YuukiConfigs["name"]

    @staticmethod
    def set_shutdown_password(code):
        global shutdown_password
        shutdown_password = code

    @staticmethod
    def set_password(code):
        global password
        password = code

    def wa_shutdown(self):
        self.http_server.stop()
        self.http_server.close()

    def wa_listen(self):
        self.http_server = WSGIServer(('', 2020), wa_app)
        self.http_server.serve_forever()
