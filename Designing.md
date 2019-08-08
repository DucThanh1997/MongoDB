# Normalization versus Denormalization
Có nhiều cách biểu diễn dữ liệu và một trong những vấn đề quan trọng nhất là bạn nên Normalization dữ liệu của mình đến mức nào. Normalization là chia dữ liệu thành nhiều collection với các tham chiếu giữa các bộ sưu tập. Mỗi phần dữ liệu nằm trong một collection mặc dù nhiều document có thể tham chiếu nó. Do đó, để thay đổi dữ liệu, chỉ có một tài liệu phải được cập nhật. Tuy nhiên, MongoDB không có join, vì vậy việc thu thập tài liệu từ nhiều collection sẽ yêu cầu nhiều truy vấn.

Denormalization ngược lại với Normalization: nhúng tất cả dữ liệu vào một document. Thay vì các document có chứa các tham chiếu đến một bản sao dữ liệu rõ ràng, nhiều document có thể có các bản sao của dữ liệu. Điều này có nghĩa là nhiều tài liệu cần được cập nhật nếu thông tin thay đổi nhưng tất cả dữ liệu liên quan có thể được tìm nạp bằng một truy vấn duy nhất.

Quyết định khi nào Normalization và khi nào Denormalization có thể khó khăn: thông thường, Normalization làm cho việc viết nhanh hơn và việc Denormalization làm cho việc đọc nhanh hơn. Vì vậy, bạn cần tìm ra những gì đánh đổi có ý nghĩa cho ứng dụng của bạn.

![image](https://user-images.githubusercontent.com/45547213/62681205-58cc2780-b9e3-11e9-9203-2ab668d2f23d.png)

