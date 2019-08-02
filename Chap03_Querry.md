# Query
## Find
### Định nghĩa
Phương thức find được sử dụng để thực hiện các truy vấn trong MongoDB. Truy vấn trả về một tập hợp con các document trong một collection. 
Những document được trả về được xác định bởi đối số đầu tiên cần tìm.

1 empty query document trả về toàn bộ document trong collection

Khi bạn thêm các yêu cầu tìm kiếm vào thì nó sẽ giới hạn các document trả ra
```
db.users.find({"age" : 27})
```

Chỉ lấy user có tuổi là 27

### Chọn key để trả về
- Để chọn key nào sẽ được trả ra ta làm như nào
```
db.users.find({}, {"username" : 1, "email" : 1})
```

object id sẽ auto được trả ra dù như nào đi nữa
- Để chọn key không trả ra ta làm như sau
```
db.users.find({}, {"fatal_weakness" : 0})
```

## Query criteria
### Query conditional

- `$lt`: less than
- `$lte`: less than equal
- `$gt`: greater than
- `$gte`: greater than equal

```
db.users.find({"age" : {"$gte" : 18, "$lte" : 30}})
```
lấy user lớn hơn 18 tuổi và bé hơn 30 tuổi

```
> start = new Date("01/01/2007")
> db.users.find({"registered" : {"$lt" : start}})
```
tìm được cả bằng thời gian nhé

### OR query
Có 2 cách để làm truy vấn OR 
- `$in`
- `$or`

#### $in

```
db.raffle.find({"ticket_no" : {"$in" : [725, 542, 390]}})
```

tìm những document có ticket_no có giá trị 725, 542, 390

`$in` linh hoạt có thể search nhiều kiểu dữ liệu
```
db.users.find({"user_id" : {"$in" : [12345, "joe"]})
```

#### $nin
`$nin` là not in ngược lại của in và vẫn có những tính năng như vậy

#### $or
```
db.raffle.find({"$or" : [{"ticket_no" : 725}, {"winner" : true}]})
```
nó sẽ tìm các document có ticket_no là 725 hoặc winner là true cho phép tìm nhiều giá trị hơn in

#### $not
- LÀ 1 metaconditional đặt ở đầu mọi cái condition khác
```
db.users.find({"id_num" : {"$not" : {"$mod" : [5, 1]}}})
```
mod sẽ in ra các số 1,6,11,16 là thêm not vào thì nó sẽ tìm những số không phải những số đó

#### Conditional Semantics (Vị trí)
`$lt` nằm trong document còn `$inc` nằm ngoài document
```
db.users.find({"age" : {"$lt" : 30, "$gt" : 20}})
```
Có thể cho nhiều condition vào 1 key nhưng không thể cho nhiều update vào 1 key

1 vài meta - operator nằm ngoài operator như `$and`, `$or` và `$nor`
```
db.users.find({"$and" : [{"x" : {"$lt" : 1}}, {"x" : 4}]})
```

## Truy vấn loại cụ thể

### null
có 3 bản ghi
```
db.c.find()
{ "_id" : ObjectId("4ba0f0dfd22aa494fd523621"), "y" : null }
{ "_id" : ObjectId("4ba0f0dfd22aa494fd523622"), "y" : 1 }
{ "_id" : ObjectId("4ba0f148d22aa494fd523623"), "y" : 2 }
```
- Cú pháp query document có y là null
```
db.c.find({"z" : {"$in" : [null], "$exists" : true}})
```

### regular expression
Mongo cho phép tìm kiếm biểu thức chính quy
```
db.users.find({"name" : /joe/i})
```

## Querying Arrays
Chúng ta có bản ghi như này
```
db.food.insert({"fruit" : ["apple", "banana", "peach"]})
```
Chúng ta chỉ cần match 1 phần tử trong fruit thôi thì chúng ta cũng có thể in ra cả mảng rồi
```
db.food.find({"fruit" : "banana"})
```
Kết quả
```
{ "_id" : ObjectId("5d43e514bf5d0bc34d2fa58b"), "fruit" : [ "apple", "banana", "peach" ] }
```

### $all

```
> db.food.insert({"_id" : 1, "fruit" : ["apple", "banana", "peach"]})
> db.food.insert({"_id" : 2, "fruit" : ["apple", "kumquat", "orange"]})
> db.food.insert({"_id" : 3, "fruit" : ["cherry", "banana", "apple"]})
```

Khi thêm $all vào ngoài document mongodb sẽ in ra toàn bộ những document match với điều kiện của chúng ta
```
db.food.find({fruit : {$all : ["apple", "banana"]}})
```

Kết quả

```
{"_id" : 1, "fruit" : ["apple", "banana", "peach"]}
{"_id" : 3, "fruit" : ["cherry", "banana", "apple"]}
 ```
 
chúng ta có thể thấy không quan trọng thứ tự



### Slice operator

- Lấy 10 comment đầu
```
db.blog.posts.findOne(criteria, {"comments" : {"$slice" : 10}})
```

- Lấy 10 comment cuối
```
db.blog.posts.findOne(criteria, {"comments" : {"$slice" : -10}})
``

- Lấy 10 comment từ comment số 24 trở đi
```
db.blog.posts.findOne(criteria, {"comments" : {"$slice" : [23, 10]}})
```

Khi trả về kết quả vẫn sẽ có title và content đi cùng với comment

- Lấy comment với giá trị cụ thể
```
db.blog.posts.find({"comments.name" : "bob"}, {"comments.$" : 1})

{
 "_id" : ObjectId("4b2d75476cc613d5ee930164"),
 "comments" : [
 {
 "name" : "bob",
 "email" : "bob@example.com",
 "content" : "good post."
 }
 ]
}
```

- Chúng ta có 4 bản ghi 
```
{"x" : 5}
{"x" : 15}
{"x" : 25}
{"x" : [5, 25]}
```

Chúng ta query như này
```
> db.test.find({"x" : {"$gt" : 10, "$lt" : 20}})
```

nó sẽ trả về
```
{"x" : 15}
{"x" : [5, 25]}
```
Cái này `{"x" : [5, 25]}` vì 5 bé hơn 20 và 25 lớn hơn 10 dị nhỉ
Để sửa lại chúng ta phải dùng lệnh này

```
db.test.find({"x" : {"$elemMatch" : {"$gt" : 10, "$lt" : 20}})
```

### Query Embedded document
- Chúng ta có bản ghi
```
{
 "name" : {
 "first" : "Joe",
 "last" : "Schmoe"
 },
 "age" : 45
}
```

```
> db.people.find({"name.first" : "Joe", "name.last" : "Schmoe"})
```
### Where
- Where chỉ là cách cuối cùng bạn làm để query thôi nha
```
db.foo.find({"$where" : function () {
... for (var current in this) {
... for (var other in this) {
... if (current != other && this[current] == this[other]) {
... return true;
... }
... }
... }
... return false;
... }});
```

### ServerSide javascript
Bạn phải rất cẩn thận với bảo mật khi thực thi JavaScript trên máy chủ. Nếu được thực hiện không chính xác, 
JavaScript phía máy chủ dễ bị tấn công tiêm chích tương tự như các cuộc tấn công xảy ra trong cơ sở dữ liệu quan hệ. 
Tuy nhiên, bằng cách tuân theo các quy tắc nhất định xung quanh việc chấp nhận đầu vào, 
bạn có thể sử dụng JavaScript một cách an toàn. Ngoài ra, bạn có thể tắt thực thi JavaScript hoàn toàn bằng cách chạy mongod
với tùy chọn --noscripting.


### Cusor
Cơ sở dữ liệu trả về kết quả từ tìm bằng cách sử dụng một con trỏ. Việc triển khai các con trỏ phía máy khách thường cho phép bạn 
kiểm soát rất nhiều về đầu ra cuối cùng của một truy vấn. Bạn có thể giới hạn số lượng kết quả, bỏ qua một số kết quả, 
sắp xếp kết quả theo bất kỳ tổ hợp phím nào theo bất kỳ hướng nào và thực hiện một số thao tác mạnh mẽ khác.

Để tạo một con trỏ với shell, đặt một số document vào một collection, thực hiện truy vấn trên chúng và gán kết quả cho một biến cục bộ 
(các biến được xác định bằng "var" là cục bộ). Ở đây, chúng tôi tạo ra một collection rất đơn giản và truy vấn nó, 
lưu trữ các kết quả trong biến con trỏ:


```
> for(i=0; i<100; i++) {
... db.collection.insert({x : i});
... }
> var cursor = db.collection.find();
```

Ưu điểm của việc này là bạn có thể nhìn vào một kết quả tại một thời điểm. Nếu bạn lưu trữ kết quả trong một biến toàn cục 
hoặc không có biến nào cả, trình bao MongoDB sẽ tự động lặp lại và hiển thị một vài tài liệu đầu tiên. 
Đây là những gì tôi đã thấy cho đến thời điểm này, và đó thường là hành vi bạn muốn thấy những gì trong một collection 
nhưng không phải để lập trình thực tế với shell.

```
> while (cursor.hasNext()) {
... obj = cursor.next();
... // do stuff
... }
```
cái này để chạy trong vòng lặp


### Skip Limit
#### Limit
chỉ cho in ra 3 cái thôi nếu không đủ thì không in ra
```
> db.c.find().limit(3)
```

#### Skip
skip 3 cái đầu rồi làm in từ đó về sau

























