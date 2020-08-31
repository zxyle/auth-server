# Configuration file

# Store the redis key of access_token
REDIS_KEY = "access_token"

# LDAP configuration info
# The variables here need to be consistent with the environment variables in docker-compose.yml
LDAP_URI = "ldap://ldap:389"
LDAP_BASE_DN = "dc=example,dc=org"
LDAP_BIND_DN = f"cn=admin,{LDAP_BASE_DN}"
LDAP_BIND_PWD = "admin"
USER_DEFAULT_PWD = "123456"
