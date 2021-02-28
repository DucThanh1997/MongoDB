## Method, Filter, Operator
```
db.mycollection.find({age:32})
```
- `db` để access db hiện tại
- `myCollection` để access vào 1 collection
- `find` là method
- `{age:32}` là filter

- Operator có nhiều kiểu
    + Query Selector: dùng để locate data `$eq`
    + Projection Operator: điều chỉnh data trả ra `$`
    + Update Operator: chỉnh sửa data `$set`
    + Aggregation Operator

- Query Selector và Projection Operator

db.movies.find trả về 1 cursor để chúng ta xem các cái document match với filter còn findOne chỉ để match với 1 cái duy nhất

## Comparison Operator
- Tìm các movie có thời lượng bằng 60 dùng `$eq` equal
```
db.movies.find({runtime: {$eq: 60}})
```

- Tìm các movie có thời lượng khác 60 dùng `$eq` not equal
```
db.movies.find({runtime: {$ne: 60}})
```

- Tìm các movie có thời lượng thấp hơn 40 dùng `$lt` lower than
```
db.movies.find({runtime: {$lt: 40}})
```

- Ngoài ra còn có kiểu `$lte` là thấp hơn bằng tức là như này <= tương tự với `$gte` là >=

## Query embedded field
- Muốn filter cái trường embedded thì chúng ta làm như này
```
db.movies.find({"rating.average":{$gt: 7}})
```

- Muốn filter trong 1 array thì cứ dùng bình thường còn nếu mà muốn chỉ có mình nó thôi thì dùng như này
```
db.movies.find({"genres": [Drama]})
```
thì nó sẽ chỉ tìm cái phim nào có đúng genres chứa array chỉ có drama thôi


```
db.movies.find({"runtime": {$in:[30,42]}})
```
tìm những bộ phim có thời lượng là 30 hoặc 42 ngược lại với $nin là tìm những bộ phim không có thời lượng là 30 và 42



## Logical Operator
- `$or` với operator `$or` chúng ta sẽ đưa các chỉ tiêu vào trong 1 array và để ở ngoài 1 cái key operator `$or`
```
db.movies.find({$or: [{"rating.average": {$lt: 5}}, {"rating.average": {$gt: 9.3}}]}).pretty()
```

- `$nor` là ngược lại của or

- `$and` với operator `$and` chúng ta sẽ đưa các chỉ tiêu vào trong 1 array và để ở ngoài 1 cái key operator `$and`
```
db.movies.find({$and: [{"genres": "Drama"}, {"rating.average": {$gt: 9.3}}]}).count()
```
viết như này cũng được nhưng sai
```
db.movies.find({"rating.average": {$gt: 9.3}, "genres": "Drama"}).count()
```
Tại sao?? nếu chúng ta search 2 tiêu chí trên cùng field giả dụ như này
```
db.movies.find({"genres": "Drama", "genres": "Horror"}).count()
```
thì thực chất nó chỉ tìm kiếm cái genres là horror thôi cái tiêu chí đầu bị tiêu chí sau ghi đè rồi (javascript nó vậy)
nên nếu muốn search 2 tiêu chí trên cùng 1 field thì phải dùng `$and`

- `$not` kiểu như là khác ấy
```
db.movies.find({rutime: {$not: {$eq: 60}}}).count()
```

## Element Operator
- `$exist` tìm những document có field nào đó 
```
db.users.find({age: {$exist: true}})
```
Cái này tìm các user có trường age nhưng nó cũng tìm cả các trường có null để tránh nó ra thì
```
db.users.find({age: {$exist: true, $ne: null}})
```

- `$type` tìm những doc mà field có type theo yêu cầu
```
db.users.find({phone: {$type: ["double", "string"]}})
```

## Evaluation Operator
- `$regex` rgular expression đó
```
db.movies.find({summary: {$regex: /musical/}})
```

tìm những doc mà có summary chứa musical 

- `$expr` so sánh các field trong document rồi lấy ra các cái mà thỏa mãn yêu cầu mình đặt ra
```
db.sales.find({$expr: {$gt: ["$volume", "$target"]}})
```
Ở đây là lấy các document mà giá trị của volume lớn hơn giá trị của target

```
db.sales.find({$expr: {$gt: [{$cond: {if: {gte: ["$volume", "$target"]}, then {$subtract: ["$volume", 10]}, else: "$volume"}}, "$target"]}}).pretty()
```

## Querry Array deep dive
Chúng ta có 1 collection như này
```
{
    "_id" : ObjectId("602a3ee1e46cd413653d661b"),
    "name" : "Max",
    "hobbies" : [
        {
                "title" : "Sports",
                "frequency" : 3
        },
        {
                "title" : "Cooking",
                "frequency" : 6
        }
    ],
    "phone" : 675
}
```

Nếu muốn tìm thằng document mà có title Sport thì làm như này
```
db.users.find({"hobbies.title": "Sports"}).pretty()
```

### $size
- $size tìm những document có field là array và có size = 3
```
db.users.find({hobbies: {$size: 3}})
``` 

### Array Query Selector
```
db.movies.find({genre: {$all: ["action", thriller"]}}).pretty()
```
cái này tìm chính xác những movie có genre là như action và thriller nhưng nó ko care về vị trí có thể là thriller và action cũng được


### $elemMatch
trong hobbie thì nó có 1 array vậy làm sao để tìm 1 element mà chỉ match trong đó không thôi.
Ví dụ bây giờ chúng ta muốn tìm 1 người mà có sở thích là sport với frequency là 3.
Nếu dùng lệnh này
```
db.users.find({$and: [{"hobbies.title: "Sports"}, {"hobbies.frequency":{$gte: 3}}]}).pretty()
```
Kết quả trả ra sẽ sai vì nó sẽ tìm frequency ở cả những hobbie khác trong array để match chứ không chỉ mỗi frequency của thằng Sports, để làm điều này elemMatch xuất hiện

```
db.users.find({hobbies: {$elemMatch: {title: "Sports", frequency: {$gte: 3}}}})
```

## Understanding Cursor
Khi mà bạn query ở trong find thì bạn có thể nhận về 10000 hoặc 1 triệu bản ghi nhưng thực sự bạn ko cần phải xem từng cái 1 và việc fetch 10000 hoặc 1 triệu bản ghi về rất nặng.

Vì vậy find đưa chúng ta 1 cursor, nó trỏ cho chúng ta 20 bản ghi đầu và cho phép chúng ta trỏ đến 20 bản ghi tiếp theo và tiếp theo

### Sort
```
db.movies.find().sort({"rating.average": -1, runtime: -1}).pretty()
```

cái này dùng để sort

### Skip, limit
```
db.movies.find().sort({"rating.average": -1, runtime: -1}).skip(10).limit(10).pretty()
```

- skip dùng để bỏ qua. Ở ví dụ trên ta bỏ qua 10 thằng

- limit để giới hạn số lượng trả về

