# auth-server

## Intro
A unified identity authentication system based on `LDAP` and [wework](https://work.weixin.qq.com/). 
Will support [dingtalk](https://ding-doc.dingtalk.com/) and [feishu](https://open.feishu.cn/) in the future.

## Quick Start
Compose is a tool for defining and running multi-container Docker applications.
Here is its [documentation](https://docs.docker.com/compose/)

### Build & Run
```
docker-compose up -d --build
```

### Test & Browse
```
curl http://127.0.0.1/ping
```

### Restart Containers Group:
```
docker-compose restart
```

### Shutdown & Remove
```
docker-compose down -v --rmi all
```

## License
MIT