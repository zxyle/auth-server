"""
================
企业微信功能 预开发准备
================
"""

import json

import requests

from config import QUEUE, CORP_ID, APP_SECRET, APP_AGENT_ID
from database import r


def verify_response(body: dict):
    assert body.get("errcode") == 0


class AccessToken:
    # 存储access_token的redis键名
    token_queue = QUEUE

    # 获取token接口
    token_url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"

    # 最短有效期(单位: 秒)
    min_period = 1 * 60

    def _generate(self):
        """
        重新生成access_token并存储到redis
        文档地址: https://work.weixin.qq.com/api/doc/90000/90135/91039
        :return:
        """
        params = {
            "corpid": CORP_ID,
            "corpsecret": APP_SECRET
        }

        self._deprecate()

        response = requests.get(self.token_url, params=params)
        json_body = response.json()
        assert json_body.get("errcode") == 0
        access_token = json_body.get("access_token")
        ttl = json_body.get("expires_in")
        self._update_value(access_token, ttl)

        return access_token

    def _update_value(self, value, ttl):
        """
        更新操作
        :param value: 值
        :param ttl: 过期时间(单位: 秒)
        :return:
        """
        r.set(self.token_queue, value)
        r.expire(self.token_queue, ttl)

    def _deprecate(self):
        r.delete(self.token_queue)

    def get_access_token(self):
        """
        获取一个可用的access_token
        :return:
        """
        if r.exists(self.token_queue) and \
                r.ttl(self.token_queue) > self.min_period:
            byte = r.get(self.token_queue)
            return str(byte, encoding="utf-8")

        return self._generate()


class WeWorkUser:
    """企业微信通讯录管理"""
    token = AccessToken()

    def create(self, user):
        """
        企业微信创建成员
        文档地址: https://work.weixin.qq.com/api/doc/90000/90135/90195
        :param user:
        :return:
        """
        url = "https://qyapi.weixin.qq.com/cgi-bin/user/create"
        params = {
            "access_token": self.token.get_access_token(),
        }

        # 为什么这么写? 解决创建用户使用中文到企业微信后台却显示Unicode
        body = json.dumps(user, ensure_ascii=False).encode("utf-8")
        return requests.post(url, params=params, data=body).json()

    def get(self, uid):
        """
        企业微信读取成员
        文档地址: https://work.weixin.qq.com/api/doc/90000/90135/90196
        :param uid:
        :return:
        """
        url = "https://qyapi.weixin.qq.com/cgi-bin/user/get"
        params = {
            "access_token": self.token.get_access_token(),
            "userid": uid,
        }
        return requests.get(url, params=params).json()

    def update(self):
        """
        企业微信更新成员
        文档地址: https://work.weixin.qq.com/api/doc/90000/90135/90197
        :return:
        """
        url = "https://qyapi.weixin.qq.com/cgi-bin/user/update"
        params = {
            "access_token": self.token.get_access_token(),
        }
        form = {

        }
        return requests.post(url, params, json=form).json()

    def delete(self, uid):
        """
        企业微信删除成员
        文档地址: https://work.weixin.qq.com/api/doc/90000/90135/90198
        :param uid:
        :return:
        """
        url = "https://qyapi.weixin.qq.com/cgi-bin/user/delete"
        params = {
            "access_token": self.token.get_access_token(),
            "userid": uid,
        }
        return requests.get(url, params=params).json()


class WeWorkDepartment:
    """企业微信部门管理"""
    token = AccessToken()

    def create(self, name):
        """
        创建部门
        文档地址: https://work.weixin.qq.com/api/doc/90000/90135/90205
        :param name: 部门名称
        :return:
        """
        url = "https://qyapi.weixin.qq.com/cgi-bin/department/create"
        params = {
            "access_token": self.token.get_access_token(),
        }
        form = {
            "name": name,
            "parentid": 1,
            # "name_en": "",
            # "order": 1,
            # "id": 2
        }

        return requests.post(url, params=params, json=form).json()

    def update(self, dep_id):
        """
        更新部门
        文档地址: https://work.weixin.qq.com/api/doc/90000/90135/90206
        :param dep_id: 部门id
        :return:
        """
        url = "https://qyapi.weixin.qq.com/cgi-bin/department/update"
        params = {
            "access_token": self.token.get_access_token(),
        }
        form = {
            "id": dep_id,
            "name": "XXX研发中心",
            "name_en": "",
            "parentid": 1,
            "order": 1
        }

        return requests.post(url, params=params, json=form).json()

    def delete(self, dep_id):
        """
        删除部门
        文档地址: https://work.weixin.qq.com/api/doc/90000/90135/90207
        :param dep_id: 部门id
        :return:
        """
        url = "https://qyapi.weixin.qq.com/cgi-bin/department/delete"
        params = {
            "access_token": self.token.get_access_token(),
            "id": dep_id,
        }
        return requests.get(url, params).json()

    def list(self):
        """
        获取部门列表
        文档地址: https://work.weixin.qq.com/api/doc/90000/90135/90208
        :return:
        """
        url = "https://qyapi.weixin.qq.com/cgi-bin/department/list"
        params = {
            "access_token": self.token.get_access_token(),
            # "id": "ID",
        }
        return requests.get(url, params).json()


def send_msg(access_token, msg):
    """
    发送应用消息
    文档地址: https://open.work.weixin.qq.com/api/doc/90000/90135/90236
    :param access_token:
    :param msg: 待发送的消息
    :return:
    """
    url = "https://qyapi.weixin.qq.com/cgi-bin/message/send"
    params = {
        "access_token": access_token,
    }

    form = {
        "touser": "zhengx",
        # "toparty": "PartyID1|PartyID2",
        # "totag": "TagID1 | TagID2",
        "msgtype": "text",
        "agentid": APP_AGENT_ID,
        "text": {
            "content": msg
        },
        "safe": 0,
        "enable_id_trans": 0,
        "enable_duplicate_check": 0,
        "duplicate_check_interval": 1800
    }
    response = requests.post(url, params=params, json=form)
    print(response.text)
