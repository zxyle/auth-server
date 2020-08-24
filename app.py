from flask import Flask
from flask import jsonify, request, make_response

from config import ENTRY_DEFAULT_PWD
from encrypt import encrypt
from ldap_operate import EntryDict, LDAP
from wework import AccessToken, WeWorkUser

app = Flask(__name__)
ldap = LDAP()
token = AccessToken()
wework_user = WeWorkUser()


@app.route('/login', methods=['POST'])
def login():
    """普通登录"""
    uid = request.form.get("uid")
    pwd = request.form.get("pwd")

    params = {
        "uid": uid,
        "userPassword": encrypt(pwd)
    }
    users = ldap.query_params(params)
    if not users:
        return "用户名或密码错误."

    body = make_response("登录成功.")
    body.set_cookie("uid", uid, max_age=3600)
    return body


@app.route('/mail_login', methods=['POST'])
def mail_login():
    """通过邮箱登录"""
    mail = request.form.get("mail")
    pwd = request.form.get("pwd")

    params = {
        "mail": mail,
        "userPassword": encrypt(pwd)
    }
    users = ldap.query_params(params)
    if not users:
        return "邮箱或密码错误."

    body = make_response("登录成功.")
    body.set_cookie("mail", mail, max_age=3600)
    return body


@app.route('/logout')
def logout():
    """登出"""
    body = make_response("logout.")
    body.delete_cookie("uid")
    return body


@app.route('/change_pwd', methods=["POST"])
def change_pwd():
    """修改密码"""
    uid = request.form.get("uid")
    pwd = request.form.get("pwd")

    new_entry = EntryDict()
    new_entry["userPassword"] = [encrypt(pwd)]
    result = ldap.modify(uid, new_entry)

    return result


@app.route('/add', methods=["POST"])
def add_uid():
    """添加用户"""
    # 姓名拼音
    uid = request.form.get("uid")
    # 姓名中文
    given_name = request.form.get("given_name")
    # 性别(1为男性 2为女性)
    gender = request.form.get("gender")
    # 工号
    uid_number = request.form.get("uid_number")
    # 邮箱
    mail = request.form.get("mail")
    # 手机号
    mobile = request.form.get("mobile")
    # 部门编号
    department = request.form.get("department", "1")
    # 500：技术部；501：行政人事；502：产品部；503：运营部；504：客服部；505：管理部；506：金融部；507：财务部；508：公关部
    gid_number = request.form.get("gid_number")
    # 入职日期 格式：2018-05-20
    employee_type = request.form.get("employee_type")
    # 企业微信上增加该用户
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

    # LDAP上增加该用户
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
    entry["userPassword"] = encrypt(ENTRY_DEFAULT_PWD)
    entry["employeeType"] = employee_type
    # 不支持键值对
    # entry["gender"] = gender
    # entry["sambaNTPassword"] = ""
    result = ldap.add_user(entry)

    body = {
        "err": result,
        "weworkCode": json_body.get("errcode"),
        "weworkMsg": json_body.get("errmsg"),
    }

    return jsonify(body)


@app.route('/del')
def del_uid():
    """通过uid删除用户"""
    uid = request.args.get("uid")
    # 删除企业微信上该uid
    json_body = wework_user.delete(uid)

    # 删除LDAP上该uid
    result = ldap.del_user(uid)

    body = {
        "err": result,
        "weworkCode": json_body.get("errcode"),
        "weworkMsg": json_body.get("errmsg"),
    }

    return jsonify(body)


@app.route('/search')
def search_uid():
    """查找"""
    uid = request.args.get("uid")
    users = ldap.query_by_uid(uid)
    if not users:
        return "不存在该uid."

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


if __name__ == '__main__':
    app.run()
