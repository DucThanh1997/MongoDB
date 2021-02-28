- `insert` không được recommend bằng `insertOne` và `insertMany` vì nó ko tiện bằng dù nó chấp nhận cả truyền vào mảng lẫn truyền vào 1 phần tử

- trong `insertMany` nếu có 1 cái fail thì nó sẽ cancel toàn bộ tiến trình insert, nếu muốn nó tiếp tục thì phải specify như này
```
db.hobbies.insertMany([{_id: "yoga", name: "yoga"}, {_id: "sports", name: "sports}], {ordered: false})
```
sự khác biệt ở đây nằm ở cái tùy chỉnh ordered là false, nếu cái insert yoga đầu tiên bị fail thì nó vẫn sẽ tiếp tục insert cái sport tiếp theo

- Write concern:  `{w: 1, j: undefined, wtimeout: 200}` 
    + w là số instance mà record sẽ được ghi vào
    + j là journal, journal như 1 cái to-do-list ấy, nó sẽ chứa những việc cần làm mà chưa làm xong của mongo vào đó, nếu trong trường hợp mà mongo server down khi nó restart trở lại nó sẽ nhìn vào đấy để tiếp tục công việc, 1 phương án backup khá hay, nếu set j là undefined thì bạn sẽ ko đưa nó vào journal
    + wtimeout là timeout cho quá trình ghi

```
db.person.insertOne({name: "Michael", age: 41}, {writeConcern: {w: 1, j: true}})
```

- cách để import 1 file vào
```
mongoimport '.\course\5 Create\9.1 tv-shows.json.json' -d movieData -c movies --jsonArray --drop
```
đầu tiên là điền path của file import sau đó là `-d ten_database`

tiếp theo là `-c ten_collection` rồi nói với mongo là trong file này là 1 đoạn array chứa các json bằng option `--jsonArrray` tiếp đó là `--drop` sẽ xóa collection movieData đi nếu nó có rồi và tạo lại 1 cái mới sau đó import vào

đây là result trả ra
```
2021-02-15T11:35:47.294+0700    connected to: mongodb://localhost/
2021-02-15T11:35:47.296+0700    dropping: movieData.movies
2021-02-15T11:35:47.410+0700    240 document(s) imported successfully. 0 document(s) failed to import.
```