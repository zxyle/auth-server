#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Zheng <zxyful@gmail.com>
# Date: 2020-08-30
# Desc:
from flask import Blueprint

auth_blue = Blueprint('auth', __name__)


from . import views