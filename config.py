# Configuration file


# redis configuration info
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PWD = None

# Store the redis key of access_token
REDIS_KEY = "access_token"

# Wework application related parameters (can be viewed on the application page)
APP_AGENT_ID = 1000002
APP_SECRET = ""

# wework corporation id
CORP_ID = ""

# LDAP configuration info
LDAP_URI = "ldap://192.168.1.193:389"
LDAP_BASE_DN = "cn=admin,dc=example,dc=org"
LDAP_BIND_PWD = "admin"
USER_DEFAULT_PWD = "123456"
