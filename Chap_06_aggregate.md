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

## Group
Group cho phép bạn nhóm các document dựa trên các trường nhất định và kết hợp các giá trị của chúng.

Ví dụ: Chúng ta có collection của học sinh, và chúng ta muốn tổ chức học sinh theo nhóm dựa trên `grade`. Chúng ta sẽ group theo grade

`• {"$group" : {"_id" : "$grade"}}`


### Các toán tử
- `"$sum"` : tổng
```
> db.sales.aggregate(
... {
... "$group" : {
... "_id" : "$country",
... "totalRevenue" : {"$sum" : "$revenue"}
... }
... })
```

- `"$avg"` : trung bình
```
> db.sales.aggregate(
... {
... "$group" : {
... "_id" : "$country",
... "totalRevenue" : {"$average" : "$revenue"},
... "numSales" : {"$sum" : 1}
... }
... })
```

## Unwind
Unwinding biến mỗi trường của một mảng thành một document riêng biệt. Ví dụ: nếu chúng tôi có một blog có các bình luận, chúng tôi có thể sử dụng thư giãn để biến mỗi bình luận thành tài liệu của riêng mình.

Rất ôkke nếu bạn muốn trả về một số subdocuments nhất định từ một truy vấn: `$Unwind` các subdocuments và sau đó `$match` những subdocuments bạn muốn

```
> db.blog.aggregate({"$project" : {"comments" : "$comments"}},
... {"$unwind" : "$comments"},
... {"$match" : {"comments.author" : "Mark"}})
```

## $sort
Sắp xếp 1 trường hay nhiều trường đều được
```
db.employees.aggregate(
... {
...   "$project" : {
...      "compensation" : {
...         "$add" : ["$salary", "$bonus"]
...      },
...      "name" : 1
...      }
...   },
...   {
...      "$sort" : {"compensation" : -1, "name" : 1}
...})

```

## Sử dụng pipeline
Cố gắng lọc ra càng nhiều document (và càng nhiều field từ các document) càng tốt ở đầu pipeline của bạn trước khi thực hiện bất kỳ hoạt động "$ project", "$ group" hoặc "$ unwind" nào. Khi pipeline không được sử dụng dữ liệu trực tiếp từ collection, các index không còn có thể được sử dụng để giúp lọc và sắp xếp. Các pipeline tổng hợp sẽ cố gắng sắp xếp lại các hoạt động cho bạn, nếu có thể, để sử dụng các chỉ mục.

MongoDB sẽ không cho phép một aggreation duy sử dụng nhiều hơn một phần bộ nhớ của hệ thống: nếu nó tính toán rằng một aggreation đã sử dụng hơn 20% bộ nhớ, thì aggreation đó sẽ đơn giản là lỗi. Việc cho phép đầu ra được dẫn đến một bộ sưu tập (sẽ giảm thiểu lượng bộ nhớ cần thiết) được lên kế hoạch cho tương lai.

Nếu bạn có thể nhanh chóng giảm kích thước tập kết quả bằng "$match" chọn lọc, bạn có thể sử dụng đường ống cho các aggreation thời gian thực. Vì các pipeline cần bao gồm nhiều document hơn và trở nên phức tạp hơn, nên ít có khả năng bạn có thể nhận được kết quả thời gian thực từ họ.


## Map reduce
MapReduce là một công cụ mạnh mẽ và linh hoạt để tổng hợp dữ liệu. Nó có thể giải quyết một số vấn đề quá phức tạp để diễn đạt bằng cách sử dụng khung tổng hợp Ngôn ngữ truy vấn của ngôn ngữ.MapReduce sử dụng JavaScript làm ngôn ngữ truy vấn của nó, vì vậy nó có thể diễn đạt logic phức tạp tùy ý. Tuy nhiên, sức mạnh này có giá: MapReduce có xu hướng khá chậm và không nên được sử dụng để phân tích dữ liệu thời gian thực.

MapReduce có thể dễ dàng song song trên nhiều máy chủ. Nó phân tách một vấn đề, gửi các phần của nó đến các máy khác nhau và cho phép mỗi máy giải quyết một phần của vấn đề. Khi tất cả các máy đã hoàn thành, chúng hợp nhất tất cả các phần của giải pháp lại thành một giải pháp đầy đủ.

## Aggregation Commands
### count
đếm số lượng document trong collection
```
> db.foo.count()
0
> db.foo.insert({"x" : 1})
> db.foo.count()
```

### distinct
Loại bỏ các bản ghi có cùng tên cho vào thành 1 cái và thường đi cùng với group
```
> db.runCommand({"distinct" : "people", "key" : "age"})
```

```
{"name" : "Ada", "age" : 20}
{"name" : "Fred", "age" : 35}
{"name" : "Susan", "age" : 60}
{"name" : "Andy", "age" : 35}
```

### group
Trên có nói rồi. Gộp nhiều bản ghi lại theo 1 điều kiện nào đó






































