#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Zheng <zxyful@gmail.com>
# Date: 2020-08-30
# Desc:

from flask import jsonify, request, make_response

from app.sdks.wework import AccessToken, WeWorkUser
from app.utils.encrypt import encrypt
from app.utils.ldap_operate import EntryDict, LDAP
from config import USER_DEFAULT_PWD
from . import auth_blue

ldap = LDAP()
token = AccessToken()
wework_user = WeWorkUser()


@auth_blue.route('/login', methods=['POST'])
def login():
    """Normal login"""
    uid = request.form.get("uid")
    pwd = request.form.get("pwd")

    params = {
        "uid": uid,
        "userPassword": encrypt(pwd)
    }
    users = ldap.query_params(params)
    if not users:
        return "wrong username or password."

    body = make_response("login successful.")
    body.set_cookie("uid", uid, max_age=3600)
    return body


@auth_blue.route('/mail_login', methods=['POST'])
def mail_login():
    """Login via email"""
    mail = request.form.get("mail")
    pwd = request.form.get("pwd")

    params = {
        "mail": mail,
        "userPassword": encrypt(pwd)
    }
    users = ldap.query_params(params)
    if not users:
        return "Mail or password is incorrect."

    body = make_response("login successful.")
    body.set_cookie("mail", mail, max_age=3600)
    return body


@auth_blue.route('/logout')
def logout():
    body = make_response("logout.")
    body.delete_cookie("uid")
    return body


@auth_blue.route('/change_pwd', methods=["POST"])
def change_pwd():
    """change password"""
    uid = request.form.get("uid")
    pwd = request.form.get("pwd")

    new_entry = EntryDict()
    new_entry["userPassword"] = [encrypt(pwd)]
    result = ldap.modify(uid, new_entry)

    return result


@auth_blue.route('/add', methods=["POST"])
def add_uid():
    """Add user"""
    # Pinyin of name
    uid = request.form.get("uid")
    # Name Chinese
    given_name = request.form.get("given_name")
    # Gender (1 is male and 2 is female)
    gender = request.form.get("gender")
    # Job number
    uid_number = request.form.get("uid_number")
    # Email
    mail = request.form.get("mail")
    # phone number
    mobile = request.form.get("mobile")
    # Department Number
    department = request.form.get("department", "1")
    # Group
    gid_number = request.form.get("gid_number")
    # Entry Date Format: 2018-05-20
    employee_type = request.form.get("employee_type")

    # add this user on wework
    form = {
        "userid": uid,
        "name": given_name,
        "department": department,
        "email": mail,
        "mobile": mobile,
        "gender": gender,
    }
    json_body = wework_user.create(form)
    if json_body.get("errcode") != 0:
        return jsonify(json_body)

    # Add the user on LDAP
    entry = EntryDict()
    entry["cn"] = uid
    entry["sn"] = uid
    entry["uid"] = uid
    entry["uidNumber"] = uid_number
    entry["gidNumber"] = gid_number
    entry["homeDirectory"] = f"/home/{uid}"
    entry["givenName"] = given_name
    entry["mail"] = mail
    entry["mobile"] = mobile
    entry["objectclass"] = ['inetOrgPerson', 'posixAccount', 'top']
    entry["loginShell"] = "/bin/sh"
    entry["userPassword"] = encrypt(USER_DEFAULT_PWD)
    entry["employeeType"] = employee_type
    # The following key-value pairs are not supported
    # entry["gender"] = gender
    # entry["sambaNTPassword"] = ""
    result = ldap.add_user(entry)

    body = {
        "err": result,
        "weworkCode": json_body.get("errcode"),
        "weworkMsg": json_body.get("errmsg"),
    }

    return jsonify(body)


@auth_blue.route('/del')
def del_uid():
    """Delete user by uid"""
    uid = request.args.get("uid")
    # Delete the uid on wework
    json_body = wework_user.delete(uid)

    # Delete the uid on LDAP
    result = ldap.del_user(uid)

    body = {
        "err": result,
        "weworkCode": json_body.get("errcode"),
        "weworkMsg": json_body.get("errmsg"),
    }

    return jsonify(body)


@auth_blue.route('/search')
def search_uid():
    uid = request.args.get("uid")
    users = ldap.query_by_uid(uid)
    if not users:
        return "The uid does not exist."

    entry = users[0]
    info = {
        "cn": entry.cn,
        "employeeType": entry.employeeType,
        "gidNumber": entry.gidNumber,
        "givenName": entry.givenName,
        "mail": entry.mail,
        "mobile": entry.mobile,
        "uidNumber": entry.uidNumber,
        # "gender": entry.gender
    }
    return jsonify({"info": info})
