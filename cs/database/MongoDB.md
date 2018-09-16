### 密码相关
创建用户, 配置角色
```
use admin  # 进入admin数据库中

db.createUser({
    user:"admin",
    pwd:"password",
    roles:[{
        role:"root",  # root是最高权限
        db:"admin"  # 制定具体数据库, admin是所有可以使用
    }]
})

db.auth("admin", "password")


./mongod --auth  # 使用权限启动mongo
./mongo -u admin -p password  # 密码登录mongo

mongodump -h <hostname><:port> -d dbname  -o  <path>
mongorestore -h <hostname><:port> -d dbname <path>
```
