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
### Limitation
Có 1 vài giới hạn trong querry. Giá trị của query phải là constant. Ví dụ như này sẽ fail
```
db.stock.find({"in_stock" : "this.num_sold"}) // doesn't work
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
```
db.users.find({"user_id" : {"$in" : [12345, "joe"]})
```

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

`$in` tối ưu hơn `$or`

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

- Conditional sẽ nằm ở trong còn cái lệnh modifier sẽ nằm ở ngoài

- Trong khi nhiều condittional có thể dùng trên 1 key nhưng modifier thì không được
```
{"$inc" : {"age" : 1}, "$set" : {age : 40}}
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

- Nếu bạn viết như này nó sẽ trả ra các hàm mà y bị thiếu
```
{ "_id" : ObjectId("4ba0f0dfd22aa494fd523621"), "y" : null }
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

Nếu bạn muốn querry kiểu phải match cả array thì mới in ra
```
db.food.find({"fruit" : ["apple", "banana", "peach"]})
```

Hoặc nếu bạn muốn querry những thằng là peach ở vị trí số 2
```
db.food.find({"fruit.2" : "peach"})
```

### seize
Muốn tìm các loại fruit có array size là 3 thì làm như này
```
> db.food.find({"fruit" : {"$size" : 3}})
```

**Lưu ý**: thằng size này không kết hợp được với các thằng condition kahcs như là `$gt`



### Slice operator

- Lấy 10 comment đầu
```
db.blog.posts.findOne(criteria, {"comments" : {"$slice" : 10}})
```

- Lấy 10 comment cuối
```
db.blog.posts.findOne(criteria, {"comments" : {"$slice" : -10}})
```

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

Tuy nhiên sử dụng cách querry trên phải match cả cái bản ghi embed nên chúng ta sẽ query như ở dưới đây cho tiện

```
> db.people.find({"name.first" : "Joe", "name.last" : "Schmoe"})
```

Bây giờ nếu thằng name có nhiều key hơn nhưng nó vẫn có thể match những thằng có first và last như hình trên


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
```
db.c.find().skip(3)
```

### Tránh bỏ qua nhiều
Sử dụng bỏ qua cho một số lượng nhỏ các tài liệu là tốt. Đối với một số lượng lớn kết quả, bỏ qua có thể chậm, vì nó phải tìm và sau đó loại bỏ tất cả các kết quả bị bỏ qua. Hầu hết các cơ sở dữ liệu giữ nhiều siêu dữ liệu hơn trong chỉ mục để giúp bỏ qua, nhưng MongoDB chưa hỗ trợ điều này, vì vậy nên bỏ qua các bước lớn. 


### Advanced Query option
Có 2 kiểu là query là wrapped và plain
- wrapped
```
var cursor = db.foo.find({"foo" : "bar"})
```
- plain
```
var cursor = db.foo.find({"foo" : "bar"}).sort({"x" : 1})
```

### Getting consistent result
Bây giờ, khi chúng tôi thực hiện tìm kiếm, con trỏ bắt đầu trả về kết quả từ đầu bộ sưu tập và di chuyển sang phải. Chương trình của bạn lấy 100 tài liệu đầu tiên và xử lý chúng. Khi bạn lưu chúng trở lại cơ sở dữ liệu, thông thường nó sẽ bị chuyển xuống cuối.

Bây giờ chương trình của chúng tôi tiếp tục lấy các lô tài liệu. Khi đến cuối, nó sẽ trả lại các tài liệu được di dời một lần nữa (Hình 4-4)!

Giải pháp cho vấn đề này là snapshot truy vấn của bạn. Nếu bạn thêm tùy chọn, truy vấn sẽ được chạy bằng cách duyệt qua chỉ mục "_id", điều này đảm bảo rằng bạn sẽ chỉ trả về mỗi tài liệu một lần. Ví dụ: thay vì db.foo.find (), bạn sẽ chạy:

```
> db.foo.find ().snapshot()
```

### database command
Có một loại truy vấn rất đặc biệt gọi là lệnh cơ sở dữ liệu. Chúng ta đã nói đến việc tạo, cập nhật, xóa và tìm tài liệu. Các lệnh cơ sở dữ liệu thực hiện mọi thứ khác, từ các nhiệm vụ quản trị như tắt máy chủ và sao chép cơ sở dữ liệu để đếm các tài liệu trong bộ sưu tập và thực hiện tổng hợp.

Các lệnh được đề cập trong suốt văn bản này, vì chúng hữu ích cho việc thao tác, quản trị và giám sát dữ liệu. Ví dụ, việc thả bộ sưu tập được thực hiện thông qua lệnh "thả" cơ sở dữ liệu:

```
db.runCommand({"drop" : "test"});
{
 "nIndexesWas" : 1,
 "msg" : "indexes dropped for collection",
 "ns" : "test.test",
 "ok" : true
}
```

#### Cách hoạt động

database command luôn trả về document chứa khóa "ok". Nếu "ok" là 1, lệnh đã thành công; và nếu nó là 0, lệnh không thành công vì một số lý do. Nếu "ok" là 0 thì một khóa bổ sung sẽ xuất hiện, "errmsg". Giá trị của "errmsg" là một chuỗi giải thích tại sao lệnh thất bại. Ví dụ, hãy để Lôi thử chạy lại lệnh thả, trên bộ sưu tập đã bị loại bỏ trong phần trước:

```
> db.runCommand({"drop" : "test"});
{ "errmsg" : "ns not found", "ok" : false }
```

Các lệnh trong MongoDB được triển khai như một loại truy vấn đặc biệt được thực hiện trên $ cmd collection. runCommand chỉ cần lấy một tài liệu lệnh và thực hiện truy vấn tương đương, vì vậy lệnh gọi thả của chúng ta trở thành như sau:
```
db.$cmd.findOne({"drop" : "test"});
```


















