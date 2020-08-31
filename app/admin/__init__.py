#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Zheng <zxyful@gmail.com>
# Date: 2020-08-30
# Desc:

from flask import Blueprint

admin_blue = Blueprint('admin', __name__)

from . import views, errors
