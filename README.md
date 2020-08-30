# auth-server

## Intro
A unified identity authentication system based on `LDAP` and [wework](https://work.weixin.qq.com/). 
Will support dingtalk and feishu in the future.

## Quick Start
Compose is a tool for defining and running multi-container Docker applications.
Here is its [documentation](https://docs.docker.com/compose/)

### Run
```
docker-compose up -d --build
```

### Browse
```
curl http://127.0.0.1/ping
```

### Restart
```
docker-compose restart
```

### Shutdown & Remove
```
docker-compose down -v --rmi all
```

## License
MIT