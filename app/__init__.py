#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Zheng <zxyful@gmail.com>
# Date: 2020-08-30
# Desc:

import os

from flask import Flask

basedir = os.path.abspath(os.path.dirname(__file__))


def create_app():
    app = Flask(__name__)

    from .auth import auth_blue
    app.register_blueprint(auth_blue, url_prefix='/user')

    return app
