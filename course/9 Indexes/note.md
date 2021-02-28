## Index là gì
Là nó chọn 1 trường rồi sắp xếp theo thứ tự alphabet ấy, khi query thì sẽ nhanh hơn nhưng nó sẽ làm chậm 1 phần update và insert. Việc đánh index như kiểu bạn tạo 1 cái mục lục ý thay vì ngày xưa bạn tìm kiếm mà ko có mục lục

- cách thêm 1 index vào `db.contacts.createIndex({"dob.age": 1})`

## Hiểu rõ về giới hạn của index
Nếu bạn query như này `db.contacts.explain("executionStats").find({"dob.age":{$gt:20}})` khi đánh index thì sẽ tốn tầm 8ms còn khi không đánh là 4ms. Tại sao vậy??

Bản thân cái collection trả về 5000 bản ghi tức là toàn bộ số record trong collection. Vậy thì khi mà đánh index nó sẽ tìm ở địa chỉ ở trong index rồi vào collection tìm địa chỉ ở trong index rồi vào collection lấy cứ lặp đi lặp lại như thế còn khi không có index nó vào collection và bê nguyên tất cả ra nên nó nhanh hơn là vậy.

**Đây là điều cần lưu ý khi đánh index**

## Compound Indexes
Là cái để bạn tạo 1 index nhưng có nhiều hơn 1 trường
```
db.contacts.dropIndex({"dob.age":1,gender:1})
```
Thường dùng để tối giản thời gian querry khi query 2 trường trở lên

Ngoài ra nó còn dùng để sort cho nhanh nữa

## Partial Index
Là nó chỉ đánh index những cái mà match cái filter đề ra thôi

Có 1 case như này ví dụ khi chúng ta có 2 user 1 người có email 1 người không có
```
{
    "_id" : ObjectId("602d1ee58f6e664f90bbc98d"),
    "name" : "Max",
    "email" : "max@test.com"
}
{   "_id" : ObjectId("602d1ee58f6e664f90bbc98e"), 
    "name" : "Manu" 
}
```
Nếu chúng ta add index là email và index là unique vẫn sẽ add được thôi nhưng nếu bh mà bạn add thêm 1 thằng user vào nữa và thằng user này ko có email thì nó sẽ báo lỗi là trùng index key unique vì có 2 thằng ko có email.

Để fix điều này chúng ta add index như sau
```
db.users.createIndex({email: 1}, {unique: true, partialFilterExpression: {email: {$exist: true}}})
```

nó sẽ chỉ đánh index những document mà có email thôi hiểu chưa

## TimetoLive index
nó sẽ auto xóa doc sau 1 khoảng thời gian nhất định và nó chỉ được đặt trên trường date mà thôi
```
db.sessions.createIndex({createdAt: 1}, {expireAfterSeconds: 10})
```

## Covered Query
```
db.customers.insertMany([{name: "Max", age: 29, salary: 3000}, {name: "Manu", age: 30, salary: 4000}])
```
add 1 index name vào

bây giờ nếu bạn query và bỏ projection vào chỉ lấy mỗi name thì nó sẽ nhanh hơn rât nhiều vì nó bỏ đi được cái bước bốc address vào trong database để lôi cái document ra  

## Reject Plan
Mongo sẽ so sánh các index với nhau, nếu có khoảng 1tr bản ghi thì nó chỉ lấy 1000 thôi với câu query đấy thằng nào lấy được xong sớm hơn thì thằng đấy sẽ thắng mấy thằng kia bị rejected còn nếu mà nó win thì nó sẽ được cache lại. Tất nhiên nó sẽ chỉ cache lại 1 thời gian, và khi mà
- có thêm index mới được add vào
- mongo restart
- collection add thêm 1k document mới

## Using Multi-key Index
Multikey là đặt index vào các field có kiểu dữ liệu là array và object, mongo sẽ pull hết các element trong arrray ra và đặt index cho chúng nên multikey index sẽ phình rất to

## Text index
Nó là 1 kiểu đặc biệt của multi-key index
```
{
    "_id" : ObjectId("602d35288f6e664f90bbc993"),
    "title" : "A book",
    "description" : "This is an awesome book about a young artist!"
}
{
    "_id" : ObjectId("602d35288f6e664f90bbc994"),
    "title" : "Red T-shirt",
    "description" : "This T-shirt is red and it's pretty awesome"
}
```
ví dụ chúng ta có case như này, chúng ta sẽ đặt text index cho dễ search `db.products.createIndex({description: "text"})`

Text index sẽ loại bỏ các từ như this, is rồi mấy từ linh tinh nó sẽ lưu những từ keyword là chính. Cái này giống như regular expression nhưng nó nhanh hơn rất nhiều
```
db.product.find({$text: {$search: "book"}}).pretty()

db.product.find({$text: {$search: "red book"}}).pretty()

db.products.find({$text: {$search: "\"awesome book\""}}).pretty() // nếu bạn muốn search 1 cụm từ awesome book
```

Nếu bạn muốn sắp xếp cái nào trùng nhiều hơn
```
db.products.find({$text: {$search: "awesome t-shirt"}}, {score: {$meta: "textScore"}}).sort({score: {$meta: "textScore"}}).pretty()
```

Kết quả sẽ ra như này
```
{
    "_id" : ObjectId("602d35288f6e664f90bbc994"),
    "title" : "Red T-shirt",
    "description" : "This T-shirt is red and it's pretty awesome",
    "score" : 1.7999999999999998
}
{
    "_id" : ObjectId("602d35288f6e664f90bbc993"),
    "title" : "A book",
    "description" : "This is an awesome book about a young artist!",
    "score" : 0.625
}
```

ta search 2 chữ awesome và t-shirt thì ở cái document đầu tiên nó có cả 2

Chúng ta có thể gộp nhiều text index vào với nhau
```
db.products.createIndex({description: "text", title: "text"})
```

Index bạn có thể configure 2 thứ default language để loại các từ như kiểu is, are, and và weight để tính score''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''/