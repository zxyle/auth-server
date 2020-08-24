# 配置文件


# redis配置信息
REDIS_HOST = "192.168.1.172"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = "wuwei2020"

# 存储access_token的 redis key
QUEUE = "access_token"

# 企业微信应用有关参数 (在应用页面可以查看)
APP_AGENT_ID = 1000002
APP_SECRET = "aVnPGVXbqF5l3locxT0ktX0AZiwiML0_ORTrBh0OgYQ"

# 企业id (在我的企业页面最下面)
CORP_ID = "ww433d03f29429ce75"

# LDAP配置信息
LDAP_URI = "ldap://192.168.1.193:389"
LDAP_BASE_DN = "cn=admin,dc=example,dc=org"
LDAP_BIND_PWD = "admin"

# LDAP账号默认密码
ENTRY_DEFAULT_PWD = "123456"
