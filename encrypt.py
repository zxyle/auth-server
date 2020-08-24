"""
================
加密解密功能 预开发准备
================
"""

import base64
import binascii
import hashlib


def get_hash_method(algor):
    """
    获取哈希方法
    :param algor: 哈希算法名称 类似md5 sha1
    :return:
    """
    try:
        return getattr(hashlib, algor)
    except AssertionError:
        print(f"无{algor}哈希算法.")


def checksum(method, raw):
    """
    计算hash
    :param method: 哈希方法
    :param raw: 待加密文本
    :return:
    """
    m = method()
    m.update(raw.encode())
    return m.hexdigest()


def encrypt(raw, algor="md5"):
    """
    LDAP 格式加密
    :param raw: 密码原文
    :param algor: 哈希算法名称
    :return:
    """
    # 已加密串
    encrypted = checksum(get_hash_method(algor), raw)
    # ascii码加密串
    binascii_string = binascii.a2b_hex(encrypted)
    # base64加密串
    b64_string = base64.b64encode(binascii_string).decode()
    return "{%s}%s" % (algor.upper(), b64_string)


def decrypt(pwd, algor="md5"):
    """
    LDAP 格式解密
    :param pwd: 密码密文
    :param algor: 哈希算法名称
    :return:
    """
    old = "{%s}" % algor.upper()
    pwd = pwd.replace(old, "")
    binascii_string = base64.b64decode(pwd)
    bytes_value = binascii.b2a_hex(binascii_string)
    return str(bytes_value, encoding="utf-8")
