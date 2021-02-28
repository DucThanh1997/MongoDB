## Update operator
- `$set`: dùng để set mới 1 field hoặc thay đổi giá trị của 1 key
```
db.users.updateOne({"_id":ObjectId("602c83ba4e7c968cb04c38c4")}, {$set: {hobbies:[{title: "Sports", frequency: 5}, {title: "Cooking", frequency: 3}, {title: "Hiking", frequency: 1}]}})
```

- `$inc` và `$dec`:  để tăng giảm
```
db.users.updateOne({name: "Manuel"}, {$inc: {age: 1}})
```
tăng 1 đơnm vị age

- `$min` chỉ thay đổi nếu giá trị được điền vào bé hơn giá trị của trường hiện tại ví dụ age đang là 38. Nếu bạn set min của nó 35 thì sẽ set được age là 35 còn nếu bạn set min là 40 thì nó sẽ ko được, `$max` tương tự như vậy

- `$mul` để nhân với giá trị hiện có

## Remove field
- `$unset` để bỏ 1 field đi
```
db.users.updateMany({isSporty: true}, {$unset: {phone: ""}})
```

## Rename field
- `$rename` để sửa tên 1 trường
```
db.users.updateMany({}, {$rename: {age: "totalAge"}})
```

## Upsert
Nếu có rồi thì sửa nếu chưa có thì thêm 1 docment mới vào luôn
```
db.users.updateOne({name: "Maria"}, {$set: {age: 29, hobbies: [title: "food", frequency: 3]}}, {upsert: true})
```

## Update Match array element
```
db.users.find({hobbies: {$elemMatch: {title: "Sports", frequency: {$gte: 3}}}}).count()
```
Giả dụ chúng ta muốn update cái element mà nó match được trong cái array này thì chúng ta sẽ làm như sau

```
db.users.updateMany({hobbies: {$elemMatch: {title: "Sports", frequency: {$gte: 3}}}}, {$set: {"hobbies.$.highFrequency": true}})
```

- Còn nếu muốn update toàn bộ các element trong array thì sử dụng lệnh này
```
db.users.updateMany({totalAge: {$gt: 30}, {$inc: {"hobbies.$[].frequency": -1}})
```

- Bạn muốn update những element tron array mà nó match với filter thôi còn nhưng element khác mà ko match thì sẽ ko update chúng ta sẽ dùng như này
```
db.users.updateMany({"hobbies.frequency": {$gt: 2}}, {$set: {"hobbies.$[el].goodFrequency": true}}, {arrayFilters: [{"el.frequency":{$gt: 2}}]})
```

- `$push` để thêm element vào array
```
db.users.updateOne({name: "Maria"}, {$push: {hobbies: {title: "Sports", frequency: 2}}})
```
Nếu bạn muốn thêm nhiều users
```
db.users.updateOne({name: "Maria"}, {$push: {hobbies: {$each: [{title: "Good wine", frequency: 1}, {title: "Hiking", frequency: 2}]}}})
```

- `$pull` để xóa element khỏi arrat
```
db.users.updateOne({name: "Maria"}, {$pull: {hobbies: {title: "Hiking}}})
```

- Ngoài ra nếu bạn muốn xóa cái hobbie theo thứ tự thì dùng `$pop` nếu dùng pop ở vị trí 1 thì xóa ở vị trí cuối cùng còn -1 thì bị xóa ở vị trí đầu tiên
```
db.users.updateOne({name: "Chris"}, {$pop: {hobbies: 1}})
```

-`$addToSet` khá giống `$push` nhưng sẽ add những cái element chưa tồn tại vào array còn nếu trùng nó sẽ không thêm vào nữa
