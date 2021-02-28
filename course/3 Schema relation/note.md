## Data type
- Text
- Boolean 
- Number: có interger (int32), numberLong(int64), numberDecimal(floating 12.99)
- ObjectID: để tạo ra 1 đoạn id độc nhất
- ISODate: lưu date
- Timestamp:
- Embedded Document
- Arrays

## Lookup
Để tìm các cái field giống nhau giữa các collections

```
db.books.aggregate([{$lookup: {from: "authors", localField: "authors", foreignField: "_id", as: "creator"}}])
```

tìm ở bảng author xem những giá trị nào ở trường authors trùng với giá trị ở trường _id thì lôi ra dưới tên là creator


## Schema validiation
ở đây chúng ta tạo ra 1 collection thủ công và tạo validiator cho nó
đầu vào phải là dạng object, với các trường yêu cầu phải có là title text creator và comments
Sau đó chúng ta specify các yêu cầu về kiểu dữ liệu trong từng trường
```
db.createCollection('posts', { 
    validator: {
        $jsonSchema: {
            bsonType: 'object',
            required: ['title', 'text', 'creator', 'comments'],
            properties: {
                title: {
                    bsonType: 'string',
                    description: 'must be a string and is required'
                },
                text: {
                    bsonType: 'string',
                    description: 'must be a string and is required'
                },
                creator: {
                    bsonType: 'objectId',
                    description: 'must be an objectid and is required'
                },
                comments: {
                    bsonType: 'array',
                    description: 'must be an array and is required',
                    items: {
                        bsonType: 'object',
                        required: ['text', 'author'],
                        properties: {
                            text: {
                                bsonType: 'string',
                                description: 'must be a string and is required'
                            },
                            author: {
                                bsonType: 'objectId',
                                description: 'must be an objectid and is required'
                            }
                        }
                    }
                }
            }
        }
    }
});
```

Nếu muốn thay đổi thì chúng ta sẽ sử dụng lệnh này
collMod có nghĩa là collection modified
```
db.runCommand({
    collMod: 'posts',
    validator: {
        $jsonSchema: {
            bsonType: 'object',
            required: ['title', 'text', 'creator', 'comments'],
            properties: {
                title: {
                    bsonType: 'string',
                    description: 'must be a string and is required'
                },
                text: {
                    bsonType: 'string',
                    description: 'must be a string and is required'
                },
                creator: {
                    bsonType: 'objectId',
                    description: 'must be an objectid and is required'
                },
                comments: {
                    bsonType: 'array',
                    description: 'must be an array and is required',
                    items: {
                        bsonType: 'object',
                        required: ['text', 'author'],
                        properties: {
                            text: {
                                bsonType: 'string',
                                description: 'must be a string and is required'
                            },
                            author: {
                                bsonType: 'objectId',
                                description: 'must be an objectid and is required'
                            }
                        }
                    }
                }
            }
        }
    },
    validationAction: 'warn'
});
```
