# Indexing
## Giới thiệu
Một database index tương tự như một mục lục của 1 cuốn sách. Thay vì xem qua toàn bộ cuốn sách, cơ sở dữ liệu sẽ sử dụng một phím tắt và 
chỉ cần nhìn vào một danh sách đã được sắp xếp và trỏ đến nội dung, cho phép nó truy vấn nhanh hơn.

Một truy vấn không sử dụng chỉ mục được gọi là quét bảng (thuật ngữ được kế thừa từ cơ sở dữ liệu quan hệ), 
điều đó có nghĩa là máy chủ phải xem qua toàn bộ cuốn sách để tìm kết quả truy vấn. 
Quá trình này về cơ bản là những gì bạn làm nếu bạn đang tìm kiếm thông tin trong một cuốn sách không có mục lục:
bạn bắt đầu ở trang 1 và đọc toàn bộ. Nói chung, bạn muốn tránh làm cho máy chủ thực hiện quét bảng vì nó rất chậm đối với các bộ sưu tập lớn.

Việc tạo index cũng có mặt không tốt tức là nó giúp cho việc truy vấn nhanh hơn nhưng cũng làm cho việc thêm sửa xóa lâu hơn.

Để chọn trường nào để tạo chỉ mục, hãy xem qua các truy vấn và truy vấn phổ biến cần nhanh và cố gắng tìm một bộ khóa chung từ các khóa đó. Ví dụ, trong ví dụ trên, chúng tôi đã truy vấn "username". Nếu đó là một truy vấn đặc biệt phổ biến hoặc đang trở thành nút cổ chai, tạo index "username" sẽ là một lựa chọn tốt. Tuy nhiên, nếu đây là một truy vấn bất thường hoặc một truy vấn chỉ được thực hiện bởi các quản trị viên đã không quan tâm đến việc mất bao lâu, thì đó không phải là một lựa chọn tốt về chỉ mục.

```
db.users.ensureIndex({"username" : 1})
```

Mỗi Index lấy giá trị của username là khóa và chứa giá trị là địa chỉ vật lý của thông tin Document lưu trên ổ đĩa. Ví dụ khi truy vấn là tìm user100, MongoDB sẽ gọi INDEXES['user100'] và lấy ra địa chỉ trỏ đến Document từ đó có thông tin của Document và trả về.
```
{
    ...
    "user100" => 0x0c965148
    "user101" => 0xf51f818e
    "user102" => 0x00fd7934
    ...
}
```
## Giới thiệu Compound Indexes

Compound Indexes rất hữu ích nếu truy vấn của bạn có nhiều hướng sắp xếp hoặc có nhiều tiêu chí cần. Một Compound Indexes là một index trên nhiều lĩnh vực.

```
db.users.ensureIndex({"age" : 1, "username" : 1})
```
1 Compound Indexes bao gồm tuổi và tên người dùng và trỏ đến vị trí của tài liệu trên đĩa (được biểu thị bằng số thập lục phân, có thể bỏ qua)
```
[21, "user999977"] -> 0x9b3160cf
[21, "user999954"] -> 0xfe039231
[21, "user999902"] -> 0x719996aa
```

## Sử dụng Compound Indexes
- Để sắp xếp các index theo nhiều hướng khác nhau, chúng ta cần để như này
```
{"age": 1, "username": -1}
```

- Nếu cần 1 cái `{"age": 1, "username": 1}` như này, chúng ta cần tạo 1 tập index khác

### Implicit indexes
Compound index có thể thực hiện nhiệm vụ đôi nhiệm vụ và hành động như các indexes khác cho các truy vấn khác nhau. Nếu chúng ta có một indexes về {"tuổi": 1, "tên người dùng": 1}, thì trường "age" được sắp xếp giống hệt như cách bạn có nếu chỉ có chỉ số {"age": 1}. Do đó, Compound index có thể được sử dụng theo cách một chỉ mục trên {"age": 1}.


## How $-Operators Use Indexes

### Inefficient operators
- `$exist`:  nonexistent fields được lưu giống null fields nên mongo sẽ phải kiểm tra từng document 1 xem nó là null hay nonexistent

- `$ne`: cũng phải scan cả index để check

- `$not` và `$nin` cũng thường dùng table scan

### Range
- Khi chúng ta để index có thứ tự là ` {"age" : 1, "username" : 1}`, bây giờ chúng ta làm 1 câu truy vấn như này

`db.users.find({"age" : 47, "username":{"$gt" : "user5", "$lt" : "user8"}})`

Mongo sẽ tìm age = 47 trước rồi tìm những user nằm trong khoảng sau

ngược lại nếu chúng ta để index như này  ` {"username" : 1, "age" : 1}.` thì nó sẽ tìm user trong khoảng trước rồi mới tìm age sau 


### Or
Khi viết bài này, MongoDB chỉ có thể sử dụng một index cho mỗi truy vấn. Đó là, nếu bạn tạo một index trên {"x": 1} và một index khác trên {"y": 1} và sau đó thực hiện truy vấn trên {"xOr": 123, "y": 456}, MongoDB sẽ sử dụng một trong những index bạn đã tạo, không sử dụng cả hai. Ngoại lệ duy nhất cho quy tắc này là "$Or". "$Or" có thể sử dụng một chỉ mục cho mỗi $ hoặc mệnh đề, dưới dạng $ hoặc tạo trước hai truy vấn và sau đó hợp nhất các kết quả


## Indexing Object và Arrays

### Indexing embedded docs
Với 1 dãy document có dạng như này
```
{
 "username" : "sid",
     "loc" : {
     "ip" : "1.2.3.4",
     "city" : "Springfield",
     "state" : "NY"
     }
}
```
Chúng ta có thể đặt index như này
```
> db.users.ensureIndex({"loc.city" : 1})
```
**Lưu ý**:
Tạo index cho cái loc sẽ chỉ giúp cho việc truy vấn với cái loc đấy thôi chứ không giúp truy vấn cái loc.city nhanh

### Indexing an array
Không thể tạo index cho cả 1 mảng mà chỉ có thể tạo index cho phần tử trong mảng chính vì vậy index của mảng sẽ rất tốn dung lượng

Các index của mảng cũng không có khái niệm gì về số thứ tự cả
document array tạo index multikey index
### Multikey Index

Nếu bất kỳ document nào có trường array cho khóa được tạo index, index ngay lập tức được gắn cờ là multikey index. Bạn có thể xem liệu một index có giống nhau từ đầu ra của explain() hay không: nếu sử dụng một multikey index, trường "isMultikey" sẽ true Khi một index đã được gắn cờ là multikey, nó không bao giờ có thể không được multikey, ngay cả khi tất cả các tài liệuchứa các mảng trong lĩnh vực đó được loại bỏ. Cách duy nhất để không giống nhau là thả và tái tạo nó.

Các multikey index có thể chậm hơn một chút so với các chỉ mục không đa điểm.

## Index Cardinality

Nói chung, tính đa dạng một lĩnh vực càng lớn, chỉ số trên lĩnh vực đó càng hữu ích. Điều này là do chỉ mục có thể nhanh chóng thu hẹp không gian tìm kiếm thành tập kết quả nhỏ hơn nhiều. Đối với trường cardinality thấp, một chỉ mục thường không thể loại bỏ càng nhiều kết quả khớp càng tốt.


## Khi nào không nên dùng index

Index hợp với lấy 1 lượng nhỏ document vì nó cần tới 2 bước:
  + Tìm index entry
  + Theo cái index entry đấy truy ra document
  
Trong khi table scan chỉ cần 1 bước truy ra cả bảng vậy những query mà lấy ra cả bảng hoặc hơn 1 nửa bảng thì không nên dùng index

nếu một truy vấn trả về 30% hoặc nhiều hơn bộ sưu tập, hãy bắt đầu xem xét các index hoặc table scancó nhanh hơn không.

Bạn có thể yêu cầu mongo chạy theo cách bình thường 
```
db.entries.find({"created_at" : {"$lt" : hourAgo}}).hint({"$natural" : 1})
```

## Types of Indexes

### Unique Indexes
Unique Indexes đảm bảo rằng mỗi giá trị sẽ chỉ xuất hiện 1 lần 
```
db.users.ensureIndex({"username" : 1}, {"unique" : true})
```

nếu trùng nhau sẽ báo lỗi
```
> db.users.insert({username: "bob"})
> db.users.insert({username: "bob"})
E11000 duplicate key error index: test.users.$username_1 dup key: { : "bob" }
```

### Compound unique indexes
Compound unique indexes cho phép có 2 key giống nhau nhưng không có 2 cặp key giống nhau
```
> db.users.insert({"username" : "bob"})
> db.users.insert({"username" : "bob", "age" : 23})
> db.users.insert({"username" : "fred", "age" : 23})
```

### Sparse Index
Là 1 kiểu unique nhưng cho phép null tồn tại ở nhiều dòng 
```
db.ensureIndex({"email" : 1}, {"unique" : true, "sparse" : true})
```

## Index Administration

- Tạo index `ensureIndex`
- Tất cả thông tin về index được lưu ở `system.indexes collection`
- 

































