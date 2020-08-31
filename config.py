# Configuration file


# redis configuration info
REDIS_HOST = "redis"
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
# The variables here need to be consistent with the environment variables in docker-compose.yml
LDAP_URI = "ldap://ldap:389"
LDAP_BASE_DN = "cn=admin,dc=my-company,dc=com "
LDAP_BIND_PWD = "admin"
USER_DEFAULT_PWD = "admin123"
