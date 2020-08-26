# Docker runs LDAP            https://github.com/osixia/docker-openldap
# python-ldap download link:  https://www.lfd.uci.edu/~gohlke/pythonlibs/#python-ldap
# Install command:            pip install python_ldap-3.3.1-cp37-cp37m-win_amd64.whl
# Ldapadmin                   http://www.ldapadmin.org/download/ldapadmin.html

from collections import OrderedDict

import ldap
import ldap.modlist as mod_list

from config import LDAP_URI, LDAP_BIND_PWD, LDAP_BASE_DN


class EntryDict(OrderedDict):
    def __setitem__(self, key, value):
        if isinstance(value, list):
            value = [i.encode() for i in value]
        else:
            value = value.encode()

        super(EntryDict, self).__setitem__(key, value)


class User:
    def __init__(self, dn, attrs):
        self.dn = dn
        for k, v in attrs.items():
            if isinstance(v[0], bytes):
                v = str(v[0], encoding="utf-8")

            self.__dict__.update({k: v})

    def __eq__(self, other):
        return self.dn == other.dn

    def __repr__(self):
        return f"User<{self.dn}>"


class LDAP:
    def __init__(self):
        self.conn = ldap.initialize(LDAP_URI)
        self.conn.simple_bind_s(LDAP_BASE_DN, LDAP_BIND_PWD)

    def add_user(self, entry: EntryDict):
        """
        add user
        :param entry: entry dict
        :return:
        """
        organization_unit = "People"
        uid = str(entry.get("uid"), encoding="utf-8")
        dn = f"uid={uid},ou={organization_unit},{LDAP_BASE_DN}"

        # Convert our dict to nice syntax for the add-function using modlist-module
        ldif = mod_list.addModlist(entry)

        # Do the actual synchronous add-operation to the ldap server
        self.conn.add_s(dn, ldif)

        # Its nice to the server to disconnect and free resources when done
        self.conn.unbind_s()
        return "LDAP created."

    def query_by_uid(self, uid):
        """
        Find users by uid
        :param uid:
        :return:
        """
        return self.query(f"(uid={uid})")

    def query_by_mail(self, mail):
        """
        Find users by mail
        :param mail:
        :return:
        """
        return self.query(f"(mail={mail})")

    def query_params(self, params: dict):
        """
        AND query
        :param params:
        :return:
        """
        condition = ""
        for k, v in params.items():
            condition += f"({k}={v})"

        return self.query(f"(&{condition})")

    def query(self, condition):
        """
        Query operation
        :param condition: 
        :return:
        """
        users = self.conn.search_s(f"ou=People,{LDAP_BASE_DN}", ldap.SCOPE_SUBTREE, condition)
        return [User(user[0], user[1]) for user in users]

    def del_user(self, uid):
        """
        delete user
        :param uid:
        :return:
        """
        dn = f"uid={uid},ou=People,{LDAP_BASE_DN}"
        self.conn.delete(dn)
        return f"{uid} have been deleted in LDAP."

    def modify(self, uid, new_entry: EntryDict):
        """
        Modify operation
        :param uid:
        :param new_entry: new entry
        :return:
        """
        dn = f"uid={uid},ou=People,{LDAP_BASE_DN}"

        # Just build an old entry with the same key, no need to care about what the value is
        old_entry = EntryDict()
        for k, v in new_entry.items():
            old_entry[k] = ["xxx"]

        _mod_list = ldap.modlist.modifyModlist(old_entry, new_entry)
        self.conn.modify_s(dn, _mod_list)
        return "successfully change password"
