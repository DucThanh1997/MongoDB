# Replica set
là tạo 1 cái mongodb mà nó sẽ là bản sao của cái mongodb chính phòng khi mongodb chính bị down.
Khi viết vào mongodb chính thì nó sẽ chuyển sang cái mongodb rep sau 1 khoảng thời gian

# Sharding
Là tạo nhiều mongodb chứa từng phần data mỗi thứ chứa 1 ít dữ liệu

Client khi đọc database sẽ viết sẽ đi vào `mongos` và mongos sẽ đọc shard key để xem cái data mà thằng này muốn ở shard nào