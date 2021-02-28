- Authentication là xem bạn có vào được ko
- Authorization là xem bạn được làm gì


## Tạo user
- Enable chức năng vào bằng user `mongod --auth`
- Chúng ta vẫn vào được mongo như bình thường nhưng chúng ta sẽ chả làm được gì

## Các role có sẵn
- database user: read, readWrite
- database admin: dbAdmin, userAdmin, dbOwner
- All databaseRole: readAny database, readWriteAnyDatabase, userAdminAnyDatabase, dbAdminAnyDatabase
- backupRestore: backup restore

## Cách đăng nhập vào
```
mongo -u thanhh -p 1 -authenticationDatabase admin
```

authenticationDatabase là cái database mà bạn tạo user khi ở trong nó

```
use Shop
db.createUser({user: 'appdev', pwd: 'dev', roles: ["readWrite"]})
```

Ở trên chúng ta vào db shop rồi tạo 1 user mới có role readwrite tức là được đọc và viết