import json

import requests

from config import QUEUE, CORP_ID, APP_SECRET, APP_AGENT_ID
from database import r


def verify_response(body: dict):
    assert body.get("errcode") == 0


class AccessToken:
    # The redis key name that stores the access_token
    token_queue = QUEUE

    # Get the token interface
    token_url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"

    # Minimum validity period (unit: second)
    min_period = 1 * 60

    def _generate(self):
        """
        Regenerate access_token and store in redis
        Document link: https://work.weixin.qq.com/api/doc/90000/90135/91039
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
        Update access token
        :param value: 
        :param ttl:
        :return:
        """
        r.set(self.token_queue, value)
        r.expire(self.token_queue, ttl)

    def _deprecate(self):
        r.delete(self.token_queue)

    def get_access_token(self):
        """
        Get a usable access token
        :return:
        """
        if r.exists(self.token_queue) and \
                r.ttl(self.token_queue) > self.min_period:
            byte = r.get(self.token_queue)
            return str(byte, encoding="utf-8")

        return self._generate()


class WeWorkUser:
    """Wework user management"""
    token = AccessToken()

    def create(self, user):
        """
        Create member
        Document link: https://work.weixin.qq.com/api/doc/90000/90135/90195
        :param user:
        :return:
        """
        url = "https://qyapi.weixin.qq.com/cgi-bin/user/create"
        params = {
            "access_token": self.token.get_access_token(),
        }

        body = json.dumps(user, ensure_ascii=False).encode("utf-8")
        return requests.post(url, params=params, data=body).json()

    def get(self, uid):
        """
        Read member
        Document link: https://work.weixin.qq.com/api/doc/90000/90135/90196
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
        Update member
        Document link: https://work.weixin.qq.com/api/doc/90000/90135/90197
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
        Delete member
        Document link: https://work.weixin.qq.com/api/doc/90000/90135/90198
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
    """Wework department management"""
    token = AccessToken()

    def create(self, name):
        """
        
        Document link: https://work.weixin.qq.com/api/doc/90000/90135/90205
        :param name: Department name
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
        
        Document link: https://work.weixin.qq.com/api/doc/90000/90135/90206
        :param dep_id: Department id
        :return:
        """
        url = "https://qyapi.weixin.qq.com/cgi-bin/department/update"
        params = {
            "access_token": self.token.get_access_token(),
        }
        form = {
            "id": dep_id,
            "name": "XXX R&D Center",
            "name_en": "",
            "parentid": 1,
            "order": 1
        }

        return requests.post(url, params=params, json=form).json()

    def delete(self, dep_id):
        """
        
        Document link: https://work.weixin.qq.com/api/doc/90000/90135/90207
        :param dep_id: Department id
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
        Get department list
        Document link: https://work.weixin.qq.com/api/doc/90000/90135/90208
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
    Send application message
    Document link: https://open.work.weixin.qq.com/api/doc/90000/90135/90236
    :param access_token:
    :param msg: 
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
