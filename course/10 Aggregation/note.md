## Aggregation
- Nó là find nhưng nó sẽ tạo 1 pipeline các step với nhau để tạo ra 1 find
```
db.persons.aggregate([ {$match: {gender:"female"}} ]).pretty()
```
cũng khá giống filter

## Group
- Group giúp chúng ta gộp kết quả match lại thành 1 kiểu document khác

```
db.persons.aggregate([
    { $match: {gender: 'female' }},
    { $group: {_id: {state: "$location.state"}, totalPersons: {$sum: 1}}}
]).pretty()
```
Kết quả sẽ là
```
{ "_id" : { "state" : "noord-brabant" }, "totalPersons" : 14 }
{ "_id" : { "state" : "burdur" }, "totalPersons" : 2 }
{ "_id" : { "state" : "la réunion" }, "totalPersons" : 2 }
{ "_id" : { "state" : "isère" }, "totalPersons" : 3 }
{ "_id" : { "state" : "sachsen-anhalt" }, "totalPersons" : 10 }
{ "_id" : { "state" : "schaffhausen" }, "totalPersons" : 5 }
{ "_id" : { "state" : "central" }, "totalPersons" : 2 }
{ "_id" : { "state" : "val-de-marne" }, "totalPersons" : 3 }
{ "_id" : { "state" : "yvelines" }, "totalPersons" : 2 }
```
nó đếm số người trong state lại rồi cộng lại và in ra

Nếu chúng ta muốn sort keeys quả theo totalPersons thì làm như này
```
db.persons.aggregate([
    { $match: {gender: 'female' }}, // không
    { $group: {_id: {state: "$location.state"}, totalPersons: {$sum: 1}}}, // cái dấu $ giúp mongo biết đây là 1 /// trường
    { $sort: {totalPersons: -1}}
]).pretty()
```

## Projection
là cái để định nghĩa đầu ra  có những trường nào và thêm các trường cần thiết vào
```
db.person.aggregate([
    {
        $project: {
            _id: 0, // không lấy _id
            gender: 1, // lấy gender
            fullName: {    // lấy fullName
                $concat: [ // nối các đoạn string lại với nhau
                    {
                        $toUpper: { // in hoa
                            $substrCP: ['$name.first', 0, 1] // lấy chữ cái đầu của trường first
                        } 
                    },
                    {
                        $substrCP: [ // lấy phần còn lại của của trường name.first
                            '$name.first', 
                            1,
                            { $subtract: [{ $strLenCP: '$name.first' }, 1]} // $subtract là trừ đi len của str - 1
                        ]
                    },
                    ' ',
                    {
                        $toUpper: { 
                            $substrCP: ['$name.last', 0, 1] // lấy chữ cái đầu của trường last
                        }
                    },
                    {
                        $substrCP: [ // lấy phần còn lại của của trường name.last
                            '$name.last', 
                            1,
                            { $subtract: [{ $strLenCP: '$name.last' }, 1]} // $subtract là trừ đi len của str - 1
                        ]
                    },
                ]
            }
        }
    },
    {$group: { _id: { birthYear: { $isoWeekYear: "$birthdate" } }, numPersons: { sum: 1}}}, 
    // cái này group cái đồng birthdate lại rồi đếm số người sinh ra của từng năm và $isoWeekYear là để lấy năm trong cái birthdate ra
    {$sort: { numPersons: -1}} //sort cái numPerson mới ra
])
```


```
db.people.aggregate([
    { $group: { _id: { age: "$age"}, allHobbies: { $push: "$hobbies"}}} // đẩy các array hobbies vào 1 array chính
]).pretty()
```


- Hàm $unwind dùng để split ra toàn bộ các phần tử trong array
Ví dụ Maria có 2 phần tử thì nó sẽ được unwind ra thành 2 collections với lệnh này
```
db.people.aggregate([ {$unwind: "$hobbies"}, ]).pretty()
```

```
{
        "_id" : ObjectId("6033db5a94cdd55b3b8011e7"),
        "name" : "Maria",
        "hobbies" : "Cooking",
        "age" : 29,
        "examScores" : [
                {
                        "difficulty" : 3,
                        "score" : 75.1
                },
                {
                        "difficulty" : 8,
                        "score" : 44.2
                },
                {
                        "difficulty" : 6,
                        "score" : 61.5
                }
        ]
}
{
        "_id" : ObjectId("6033db5a94cdd55b3b8011e7"),
        "name" : "Maria",
        "hobbies" : "Skiing",
        "age" : 29,
        "examScores" : [
                {
                        "difficulty" : 3,
                        "score" : 75.1
                },
                {
                        "difficulty" : 8,
                        "score" : 44.2
                },
                {
                        "difficulty" : 6,
                        "score" : 61.5
                }
        ]
}
```

Vậy nếu chúng ta bh không muốn đẩy từng array vào 1 nữa mà đẩy toàn bộ các phần tử vào trong 1 array thì sẽ dùng $unwind như này
```
db.people.aggregate([
    {$unwind: "$hobbies"}
    { $group: { _id: { age: "$age"}, allHobbies: { $push: "$hobbies"}}} // đẩy các array hobbies vào 1 array chính
]).pretty()
```
nhưng mà chúng ta sẽ nên để là addToSet thay vì push ví nó sẽ làm cho chúng ta add những phần tử trùng vào 1 array

## $slice 
```
db.people.aggregate([
    { $project: { _id: 0, examScore:{$slice: ["$examScores", 1]}}}            
])
```
- $slice là cái để bóc tách phần tử từ array ra ở đây chúng ta lấy phần tử đầu tiên của examScore

- Nếu là `{$slice: ["$examScores", 1, 3]}` thì chúng ta sẽ lấy 3 phần tử từ phần tử thứ nhất

## $size
- Để lấy số lượng phần tử của array
```
db.friends.aggregate([
    {$project: { _id: 0, numScores: { $size: "$examScores"}}}
]).pretty()
```

## Filter
```
db.people.aggregate([
    {
        $project: { 
            _id: 0,
            scores: { // tạo 1 trường mới 
                $filter: {   // filter dùng đề tạo các điều kiện để lọc trong projection
                    input: '$examScores', // đầu vào là field có tên là examScore
                    as: 'sc', // đặt tên
                    cond: { $gt: ["$$sc.score", 70]}  // condition, bình thường chỉ cần 1 cái $ nhưng trong trường hợp này cần 2 cái $$
                }
            }
        }
    }
]).pretty()
```

## Bucket 
```
db.persons.aggregate([
    {
        $bucket: {
            groupBy: '$dob.age', // chọn trường để group
            boundaries: [18, 30, 40, 50, 60, 120] // phân vùng cno ra
            output: {
                numPersons: { $sum: 1 }, // trả ra số lượng người trong phân vùng
                averageAge: { $avg: "$dob.age" } // cùng độ tuổi trung bình của họ
            }
        }
    }
]).pretty()
```

Nếu muốn nó auto tạo boundaries

```
db.persons.aggregate([
    {
        $bucketAuto: {
            groupBy: '$dob.age',
            buckets: 5, // auto chia ra thành 5 phần
            output: {
                numPersons: { $sum: 1 },
                averageAge: { $avg: '$dob.age' }
            }
        }
    }
])
```


- Bucket là cái để lấy dữ liệu xong chia nhỏ nó ra kiểu phân tích ấy