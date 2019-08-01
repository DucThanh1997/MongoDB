## Các khái niệm cơ bản 

### Định nghĩa các thành phần của mongodb
Document là đơn vị dữ liệu cơ bản cho MongoDB và gần tương đương với một hàng trong hệ thống quản lý cơ sở dữ liệu quan hệ 
(nhưng okke hơn nhiều).
• Tương tự, một collection có thể được coi là một bảng có lược đồ động.
• Một phiên bản MongoDB duy nhất có thể lưu trữ nhiều cơ sở dữ liệu độc lập, mỗi database
trong đó có thể nhiều collection.
• Mỗi tài liệu có một khóa đặc biệt, "_id", là duy nhất trong một bộ sưu tập.
• MongoDB đi kèm với trình bao JavaScript đơn giản nhưng mạnh mẽ, rất hữu ích cho việc quản trị các phiên bản MongoDB và thao tác dữ liệu.

![image](https://user-images.githubusercontent.com/45547213/62197520-2cdcf080-b3aa-11e9-8bde-2189523c047a.png)

Cái hay là:

- 1 doucment không cần thiết phải có đủ cái này cái kia ví dụ ở dòng đầu tiên của collection User có name và age đến dòng thứ 2 lại không có
age đấy là sự khác nhau giữa mongo và mysql. Tính flexibility hay người ta còn nói collection trong mongo có Dynamic Schemas (lược đồ động)

- Có case sensitive và type sensitive, 
```
{"foo" : 3}
{"foo" : "3"}
```

Khác nhau nha

```
{"foo" : 3}
{"Foo" : 3}
```

cũng khác nhau nha

### Quy ước đặt tên cho collection
bộ sưu tập được phân biệt bởi tên. Tên bộ sưu tập có thể là bất kỳ chuỗi UTF-8 nào, với một vài hạn chế:
• Chuỗi trống ("") không phải là tên bộ sưu tập hợp lệ.
• Tên bộ sưu tập có thể không chứa ký tự \0 (ký tự null) vì cái này mô tả sự kết thúc của một tên bộ sưu tập.
• Bạn không nên tạo bất kỳ bộ sưu tập nào bắt đầu với `system`., Tiền tố dành riêng chobộ sưu tập nội bộ. 
Ví dụ: bộ sưu tập system.users chứa cơ sở dữ liệu người dùng, 
và bộ sưu tập system.namespaceschứa thông tin về tất cả các bộ sưu tập cơ sở dữ liệu.
• Bộ sưu tập do người dùng tạo không được chứa ký tự dành riêng $ trong tên. Các trình điều khiển khác nhau có sẵn 
cho cơ sở dữ liệu hỗ trợ sử dụng $ trong tên bộ sưu tập vì một số bộ sưu tập do hệ thống tạo có chứa nó. 
Bạn không nên sử dụng $ trong tên trừ khi bạn đang truy cập một trong những bộ sưu tập này.

#### Subcollection
Một quy ước để tổ chức các bộ sưu tập là sử dụng các bộ sưu tập con được đặt tên được phân tách bằng dấu. character. 
Ví dụ: một ứng dụng chứa blog có thể có một bộ sưu tập có tên blog.posts và một bộ sưu tập riêng có tên blog.authors. 
Cái này dành cho mục đích tổ chức chỉ có mối quan hệ giữa bộ sưu tập blog (nó thậm chí không tồn tại) và trẻ em của nó.

Mặc dù các bộ sưu tập con không có bất kỳ thuộc tính đặc biệt nào, chúng rất hữu ích và được tích hợp vào nhiều công cụ MongoDB:

• GridFS, một giao thức để lưu trữ các tệp lớn, sử dụng các bộ lọc con để lưu trữ siêu dữ liệu của tệp
tách biệt với các đoạn nội dung (xem Chương 6 để biết thêm thông tin về GridFS).
• Hầu hết các trình điều khiển cung cấp một số đường cú pháp để truy cập vào một bộ sưu tập con của một
bộ sưu tập. Ví dụ: trong vỏ cơ sở dữ liệu, db.blog sẽ cung cấp cho bạn bộ sưu tập blog và db.blog.posts sẽ cung cấp cho bạn bộ sưu tập blog.posts.

Subcollections là một cách tuyệt vời để tổ chức dữ liệu trong MongoDB và việc sử dụng chúng rất được khuyến khích.



## Database
## Quy ước đặt tên
• Chuỗi rỗng ("") không phải là tên cơ sở dữ liệu hợp lệ.
• Tên cơ sở dữ liệu không thể chứa bất kỳ ký tự nào trong số này: /, \,., ", *, <,>,:, |,?, $, (Một khoảng trắng) hoặc \ 0 (ký tự null).
Về cơ bản, thường là với ASCII chữ và số.
• Tên cơ sở dữ liệu phân biệt chữ hoa chữ thường, ngay cả trên các hệ thống tệp không phân biệt chữ hoa chữ thường. Để giữ
những điều đơn giản, cố gắng chỉ sử dụng các ký tự chữ thường.
• Tên cơ sở dữ liệu được giới hạn tối đa 64 byte.

## CRUD cơ bản
### Create
- Tạo 1 object javascript
```
post = {"title" : "My Blog Post",
... "content" : "Here's my blog post.",
... "date" : new Date()}
{
 "title" : "My Blog Post",
 "content" : "Here's my blog post.",
 "date" : ISODate("2012-08-24T21:12:09.982Z")
}
```
- Insert vào collection
```
db.blog.insert(post)
```

### Find
Lúc này object bạn tạo được save vào rồi, chúng ta sẽ dùng find hoặc findOne để tìm nó
- `Find`: in ra 20 bản ghi match các điều kiện
- `findOne`: in ra 1 bản ghi thôi

### Update
- Đầu tiên chỉnh sửa object post, add thêm thuộc tính comment vào
```
post.comments = []
```

- update lại
```
db.blog.update({title : "My Blog Post"}, post)
``` 

### Xóa
```
db.blog.remove({title : "My Blog Post"})
```

## Data types
- Null
```
{"x" : null}
```
- boolean
```
{"x" : true}
```
- Number
```
{"x" : 3.14}
```
- String
```
{"x" : "foobar"}
```

- date lưu dưới dạng milliseconds. Khi gọi tạo 1 date mới cho object chúng ta sẽ phải gọi `new Date()` chứ không phải mỗi `Date()` không
```
{"x" : new Date()}
```

- regular expression
```
{"x" : /foobar/i}
```

- array 
```
{"x" : ["a", "b", "c"]}
```

- embedded document
```
{"x" : {"foo" : "bar"}}
```

- object id
```
{"x" : ObjectId()}
```
![image](https://user-images.githubusercontent.com/45547213/62261367-44b28400-b43f-11e9-900a-3acfaf50271b.png)


- binary data
- code
```
{"x" : function() { /* ... */ }}
```







































