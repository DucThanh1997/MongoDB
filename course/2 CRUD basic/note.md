## Tạo Database
- Show database dùng lệnh: `show dbs`
- Muốn sử dụng database thì dùng lệnh: `use ten_database` nếu database chưa có thì lệnh này sẽ tạo luôn
- Muốn tạo 1 document vào collection flightData trong database flight ta làm như này
```
use flights
db.flightData.insertOne({
    ... "departureAirport":"MUC",
... "arrivalAirport":"SFO",
... "aircraft":"Airbus A380",
... "distance": 12000,
... "intercontinental":true
... })
```
Ta có kết quả 
```
{
    "acknowledged" : true,
    "insertedId" : ObjectId("6026642a6ca27285a6a01810")
}
```
Khi insert vào nó sẽ auto gen ra 1 cái objectID mà mongo tự gen ra
- Bây giờ chúng ta in ra thì sẽ dùng lệnh này `db.flightData.find()`
```
{ "_id" : ObjectId("6026642a6ca27285a6a01810"), "departureAirport" : "MUC", "arrivalAirport" : "SFO", "aircraft" : "Airbus A380", "distance" : 12000, "intercontinental" : true }
```
Dùng lệnh này kết quả show ra sẽ không đẹp nên chúng ta dùng lệnh này `db.flightData.find().pretty()` để nó format kết quả ra dạng json
```
{
    "_id" : ObjectId("6026642a6ca27285a6a01810"),
    "departureAirport" : "MUC",
    "arrivalAirport" : "SFO",
    "aircraft" : "Airbus A380",
    "distance" : 12000,
    "intercontinental" : true
}
```

## So sánh json và bson
- Mongo dùng bson, bson nhanh hơn và chiếm ít dung lượng hơn, nó sẽ nhận json rồi chuyển thành bson

- Khi insert phần key có thể bỏ cái `"` này đi miễn là key không có dấu cách

- bạn có thể tự thêm `_id` vào nhưng các cái _id nó phải khác nhau nếu trùng mongo sẽ không đồng ý

## CRUD
- Insert
    + insertOne(data, option): insert 1 document
    + insertMany(data, option): insert nhiều document có thể đưa 1 array vào
```
    db.flightData.insertMany([
... {
    ... "departureAirport": "Muc",
    ... "arrivalAirport": "SFO",
    ... "aircraft": "Airbus A380",
    ... "distance": 12000,
    ... "intercontinental": true
    ... },
    ... {
    ... "departureAirport": "LHR",
    ... "arrivalAirport": "TXL",
    ... "aircraft": "Airbus A320",
    ... "distance":950,
    ... "intercontinental": false
    ... }
... ])
```

- Read
    + find(filter, option): tìm nhiều kết quả `db.flightData.find({intercontinental: true}).pretty()` 
    + findOne(filter, option): tìm 1 kết quả thôi `db.flightData.find({distance: {$gt:12000}}).pretty()` 

- Update
    + updateOne(filter, data, options): update 1 document thôi `db.flightData.updateOne({_id:ObjectId("aaA"}, {$set:{delayed: true}})`
    + updateMany(filter, data, options): update nhiều document `db.flightData.updateMany({},{$set:{marker: "toDelete"}})` cái lệnh này vì filter để rỗng nên nó sẽ update cả collection
    + update: gần giống updateMany nhưng nó không cần thêm cái operator set và nó sẽ overwrite toàn bộ cái document đó bằng data trong cái ngoặc thứ 2 `db.flightData.updateMany({},{marker: "toDelete"})`
    + replaceOne(filter, data, options): thay thế luôn cái document đó

- Delete
    + deleteOne(filter, option): xóa 1 cái document đi `db.flightData.deleteOne({departureAirport:"TXL"})`
    + deleteMany(filter, option): xóa nhiều cái document đi `db.flightData.deleteMany({marker: "toDelete"})`

## Find
lệnh find trả về chúng ta 1 cursor để chúng ta có thể loop qua các kết quả nếu nó quá dài
```
db.passengers.find().forEach((passengerData) => {printjson(passengerData)})
```
`db.passengers.find()` trả về 1 cursor object sau đó chúng ta dùng hàm `forEach` với cái cursor đó để in ra từng cái data 1. Nếu bình thường thì cursor object sẽ in ra 20 cái đầu tiên thôi. Ở lệnh này nó sẽ trả ra hết và in ra từng cái 1 

Tìm hành khách có sở thích là sport
```
db.passengers.findOne({hobbies: "sport"})
```
mongo đủ thông minh để tìm trong từng array 1

## Projection
nó là kiểu lựa chọn các trường bạn muốn in ra chứ không phải là lấy ra hết
```
db.passengers.find({},{name: 1, _id: 0}).pretty()
```

Câu lệnh ở trên là chỉ lấy name thôi bỏ id và age

## embedded document
Nó kiểu như là trong 1 document có 1 document con nữa (max là 100 document). và 1 document max dung lượng là 16mb
```
db.flightData.updateMany({}, {
                                $set: 
                                {
                                    status: 
                                    {
                                        description: "on-time", 
                                        lastUpdated: "1 hour ago", 
                                        details: {
                                                responsible:"thanh"
                                        }
                                    }
                                }
                            }
                        )
```

Tìm 1 bản ghi responsible là thanh
```
db.flightData.find({"status.details.responsible": "thanh"}).pretty()

## Arrays
```
db.passengers.updateOne({name: "Albert Twostone"}, {$set: {hobbies: ["cooking", "sport"]}})
```
