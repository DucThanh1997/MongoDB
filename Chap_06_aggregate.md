# The Aggregation Framework
## Definition 
Nó là 1 cái framework kiểu dạng như là pipeline ấy

Cho phép truyển đổi và tổng hợp dữ liệu chỉ trong 1 câu lệnh 

Ví dụ Chúng ta có 1 blog và chúng ta sẽ làm tìm xem ai là tác giả tích cực nhất
B1: Lấy hết tên của tác giả từ các bài viết ra
B2: Group by lại rồi count
B3: Sort giảm dần
B4: Limit top 5 file

```
> db.articles.aggregate({"$project" : {"author" : 1}},
... {"$group" : {"_id" : "$author", "count" : {"$sum" : 1}}},
... {"$sort" : {"count" : -1}},
... {"$limit" : 5})
```

Kết quả:
```
{
   "result" : [
     {
         "_id" : "R. L. Stine",
         "count" : 430
     },
     {
         "_id" : "Edgar Wallace",
         "count" : 175
     },
     {
         "_id" : "Nora Roberts",
         "count" : 145
     },
     {
         "_id" : "Erle Stanley Gardner",
         "count" : 140
     },
     {
         "_id" : "Agatha Christie",
         "count" : 85
     }
    ],
   "ok" : 1
}
```

# Pipeline Operations
Mỗi 1 toán tử nhận đầu vào là các document (chưa được xử lý hoặc đã được xử lý) rồi biến đổi hoặc tổng hợp. Sau đó toán tử này pass kết quả sang 1 toán tử khác hoặc nếu đó đã là toán tử cuối cùng rồi thì chúng ta sẽ chuyển kết quả ra màn hình

### $match
`$match` filter các document (đưa ra các điều kiện)

Ví dụ bạn chỉ muốn tìm các user ở bang oregon
```
 {$match : {"state" : "OR"}}
```

match cũng có thể kết hợp được với `lt, gt , lte, gte`

- Bạn nên đặt $match ở đầu aggreate vì nó giúp chúng ta loại bỏ được các document 1 cách nhanh chóng trước khi chúng ta biến đổi và tổng hợp

### $project
- Giúp chúng ta chọn trường nào sẽ in ra, trường nào không, sửa tên trường và làm 1 vài cái hay ho nữa. 

Ví dụ: Bình thường chúng ta không thể bỏ trường `_id` nhưng ở đây với `$project` chúng ta có thể loại bỏ chungs đi 
```
> db.users.aggregate({"$project" : {"userId" : "$_id", "_id" : 0}})
{
 "result" : [
 {
 "userId" : ObjectId("50e4b32427b160e099ddbee7")
 },
 {
 "userId" : ObjectId("50e4b32527b160e099ddbee8")
 }
 ...
 ],
 "ok" : 1
}
```

#### Pipeline expressions
Ngoài các tính năng vừa đề cập ở trên `$project` còn có thêm `$expression` cho phép chúng ta gộp nhiều chữ hay biến thành 1 giá trị

- Mathetical expresion: 
```
> db.employees.aggregate(
... {
... "$project" : {
... "totalPay" : {
... "$add" : ["$salary", "$bonus"]
... }
... }
... })
```

"$add" : [expr1[, expr2, ..., exprN]]

"$subtract" : [expr1, expr2]

"$multiply" : [expr1[, expr2, ..., exprN]]

"$divide" : [expr1, expr2]

- Date expressions:
Nhiều Aggregation dựa trên thời gian: Điều gì đã xảy ra tuần trước?
Tháng trước? So với năm ngoái? Do đó, Aggregation có một tập hợp các biểu thức có thể được sử dụng để trích xuất thông tin ngày theo những cách hữu ích hơn:

`"$year", "$month", "$week", "$dayOfMonth", "$dayOfWeek", "$dayOfYear", "$hour", "$minute", and "$second".`

Ví dụ
```
> db.employees.aggregate(
... {
... "$project" : {
... "hiredIn" : {"$month" : "$hireDate"}
... }
... })
```

- String expressions
      + `"$substr" : [expr, startOffset, numToReturn]`: cắt chuỗi
      + `"$concat : [expr1[, expr2, ..., exprN]]`: ghép chuỗi
 ```
 db.employees.aggregate(
... {
... "$project" : {
... "email" : {
... "$concat" : [
... {"$substr" : ["$firstName", 0, 1]},
... ".",
... "$lastName",
... "@example.com"
... ]
... }
... }
... })
```

- Logical expressions
      + `"$cmp" : [expr1, expr2]`: COMPARE
      + `"$strcasecmp" : [string1, string2]`: so sánh chuỗi
      + `"$eq"/"$ne"/"$gt"/"$gte"/"$lt"/"$lte" : [expr1, expr2]`: so sánh nhỏ lớn hơn bằng
      + `"$or" : [expr1[, expr2, ..., exprN]]`: toán tử OR
      + 









































