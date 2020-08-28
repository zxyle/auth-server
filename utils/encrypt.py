# Encryption and decryption module


import base64
import binascii
import hashlib


def get_hash_method(algor):
    """
    Get the hash method
    :param algor: Hash algorithm, such as md5 sha1
    :return:
    """
    try:
        return getattr(hashlib, algor)
    except AssertionError:
        print(f"There is no {algor} hash algorithm.")


def checksum(method, raw):
    """
    Calculate hash
    :param method: Hash method
    :param raw: Text to be encrypted
    :return:
    """
    m = method()
    m.update(raw.encode())
    return m.hexdigest()


def encrypt(raw, algor="md5"):
    """
    LDAP format encryption
    :param raw: Original password
    :param algor: Hash algorithm name
    :return:
    """
    encrypted = checksum(get_hash_method(algor), raw)
    binascii_string = binascii.a2b_hex(encrypted)
    b64_string = base64.b64encode(binascii_string).decode()
    return "{%s}%s" % (algor.upper(), b64_string)


def decrypt(pwd, algor="md5"):
    """
    LDAP format decryption
    :param pwd: Ciphertext
    :param algor: Hash algorithm name
    :return:
    """
    old = "{%s}" % algor.upper()
    pwd = pwd.replace(old, "")
    binascii_string = base64.b64decode(pwd)
    bytes_value = binascii.b2a_hex(binascii_string)
    return str(bytes_value, encoding="utf-8")
