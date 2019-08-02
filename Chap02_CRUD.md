## Insert
- Cú pháp 
```
db.foo.insert({"bar" : "baz"})
```

### Batch Insert
- Khi bạn muốn insert nhiều document vào collection thì bạn sẽ dùng
```
db.foo.batchInsert([{"_id" : 0}, {"_id" : 1}, {"_id" : 2}])
```

- Khi Insert vào Mongo sẽ thêm vào trường `_id` nếu không có và check xem doucment đó có dưới 16Mb không


## Remove
- Cú pháp
Xóa toàn bộ document trong collection foo
```
db.foo.remove()
```

Xóa toàn bộ document trong collection mailing mà opt-out = true
```
db.mailing.list.remove({"opt-out" : true})
```


## Update
- Giả sử nếu có 2 update xảy ra cái nào được update trước thì sẽ update trước rồi cái update đến sau update lại, thời gian tính bằng
millisecond. Tức là cái update nào đến sau sẽ thắng

- Ngoài ra khi update chúng ta phải đề cập đến cả object _id đề phòng trường hợp bị trùng
```
db.people.update({"_id" : ObjectId("4b2b9f67a1f631733d917a7c")}, joe)
```
vì có thể trong collection của chúng ta có tới 3 joe thì sao 
```
{"_id" : ObjectId("4b2b9f67a1f631733d917a7b"), "name" : "joe", "age" : 65},
{"_id" : ObjectId("4b2b9f67a1f631733d917a7c"), "name" : "joe", "age" : 20},
{"_id" : ObjectId("4b2b9f67a1f631733d917a7d"), "name" : "joe", "age" : 49},

```
nếu không đề cập thì object sẽ fail

### modifier
Chúng ta có 1 document như này
```
{
 "_id" : ObjectId("4b253b067525f35f94b60a31"),
 "url" : "www.example.com",
 "pageviews" : 52
}
```
Chúng ta sẽ dùng upadte modifiers để tăng lượng pageviews khi cần
```
db.analytics.update({"url" : "www.example.com"},
... {"$inc" : {"pageviews" : 1}})
```

`$inc` là increase đó

- $set: để đặt giá trị cho field, nếu field chưa có thì nó sẽ tạo cái field đấy
Ví dụ
CHúng ta có bản ghi
```
{
 "_id" : ObjectId("4b253b067525f35f94b60a31"),
 "name" : "joe",
 "age" : 30,
 "sex" : "male",
 "location" : "Wisconsin"
}
```

Bây giờ update
```
db.users.update({"_id" : ObjectId("4b253b067525f35f94b60a31")},
... {"$set" : {"favorite book" : "War and Peace"}})

{
 "_id" : ObjectId("4b253b067525f35f94b60a31"),
 "name" : "joe",
 "age" : 30,
 "sex" : "male",
 "location" : "Wisconsin",
 "favorite book" : "War and Peace"
}

```

- $unset để xóa key 

- set value với embedded
```
post2 = {
... "title": "A Blog Post2",
... "content": "...",
... "author": {
...     "name": "joe",
...     "email": "joe@example.com"
...      }
... }

 db.blog.insert(post2)
 
 db.blog.update({"_id": ObjectId("5d4267d7f550333b3a3ff642")}, {"$set": {"author.name": "joe2 schmoe"}})
```

### Increment or Decrement

- Incre: Là tăng đơn vị, nếu key chưa exist nó sẽ tạo key còn nếu có rồi nó sẽ cộng 50 vào
```
db.games.insert({"game" : "pinball", "user" : "joe"})

db.games.update({"game" : "pinball", "user" : "joe"},
... {"$inc" : {"score" : 50}})
```

- Decre: Là giảm đơn vị

- Lưu ý: inc và decre chỉ dùng cho int float long và double thôi nếu dùng cho cái khác thì fail ngay

### Array
- Dùng push để update kiểu dữ liệu array
```
db.blog.update({"title": "A Blog Post3"},
              {"$push": {"comments":  {"name":"joe", "email": "joe@example.com", "content": "nice post"}}})

``` 

- Bạn có thể push nhiều giá trị vào 1 lúc ví dụ
```
db.stock.insert({"_id": "GOOG", "hourly": [1,2]})

db.stock.update({"_id":"GOOG"},
... {"$push": {"hourly": {"$each": [10,11,12]}}})
```

- Bạn có thể sử dụng list của mình như queue nó chỉ nhận 10 cái đến cái thứ 11 đẩy vào nó sẽ xóa cái số 1 đi và đẩy cái 11 vào vị trí
thứ 10
```
db.movies.find({"genre" : "horror"},
... {"$push" : {"top10" : {
... "$each" : ["Nightmare"]
... "$slice" : -10}}})
```

- Ngoài ra bạn có thể sort nó theo 1 key nào đó ở đây t sẽ sort theo ratings
```
db.movies.find({"genre" : "horror"},
... {"$push" : {"top10" : {
... "$each" : [{"name" : "Nightmare on Elm Street", "rating" : 6.6},
... {"name" : "Saw", "rating" : 4.3}],
... "$slice" : -10,
... "$sort" : {"rating" : -1}}}})
```

- Dùng `$ne` để tránh những dữ liệu bị lặp
```
db.papers.update({"authors cited" : {"$ne" : "Richie"}},
... {$push : {"authors cited" : "Richie"}})
```
insert vào nếu không có authors cited nào là richie

- Upsert là kiểu nếu có thì update còn nếu không có thì insert vào

Cú pháp
```
db.analytics.update({"url" : "/blog"}, {"$inc" : {"pageviews" : 1}}, true)
```

- Bạn muốn set 1 thuộc tính nào đó không thể update thì sẽ dùng #setoninsert
```
> db.users.update({}, {"$setOnInsert" : {"createdAt" : new Date()}}, true)
```

- Để update nhiều user
```
db.users.update({"birthday" : "10/13/1978"},
... {"$set" : {"gift" : "Happy Birthday!"}}, false, true)
```











