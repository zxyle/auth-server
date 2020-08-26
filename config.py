# Configuration file


# redis configuration info
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = None

# Store the redis key of access_token
QUEUE = "access_token"

# Wework application related parameters (can be viewed on the application page)
APP_AGENT_ID = 1000002
APP_SECRET = ""

# wework corp id
CORP_ID = ""

# LDAP configuration information
LDAP_URI = "ldap://192.168.1.193:389"
LDAP_BASE_DN = "cn=admin,dc=example,dc=org"
LDAP_BIND_PWD = "admin"
ENTRY_DEFAULT_PWD = "123456"
