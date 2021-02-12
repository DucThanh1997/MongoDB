## MongoDB là gì
- 1 database chứa nhiều collection và trong 1 collection có nhiều document, mỗi document ko có 1 định dạng cụ thể
- Các collection ko có quan hệ với nhau

## Khởi động mongoShell
- Vào cmd gõ mongo
- Gõ `use Shop` nếu mà chưa có thì nó sẽ tạo mà có rồi thì nó vào luôn
- Gõ `db.products.insertOne({name: "A book", price: 12.99})` để insert 1 document vào collection product với các key là name và price
- Gõ `db.products.find({}).pretty()` để show ra các document mà mình đã thêm vào