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

