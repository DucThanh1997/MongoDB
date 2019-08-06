# Capped Collections
## Định nghĩa
- Là 1 dạng collection đặc biệt. Như dạng collection bình thường data cứ thế tăng dần lên còn ở capped collection. Khi tạo bạn set cho nó 1 dung
lượng nhất định.

- Vậy câu hỏi đặt ra là khi full thì nó sẽ thêm document mới vào kiểu gì? Nó như thế lày, khi capped collection full bộ nhớ và bạn muốn thêm 
document mới vào, capped collection sẽ xóa document cũ nhất đi để giải phóng bộ nhớ để thêm document mới nhất vào

- Nó không có những thuộc tính như sửa xóa document để duy trì tính nhất quán về vị trí của document

- dữ liệu được ghi tuần tự trên một phần cố định của đĩa. Điều này làm cho chúng có xu hướng thực hiện ghi nhanh trên đĩa quay, đặc biệt là 
nếu chúng có thể được cung cấp đĩa riêng (để không bị gián đoạn bởi các bộ sưu tập khác ghi ngẫu nhiên).
