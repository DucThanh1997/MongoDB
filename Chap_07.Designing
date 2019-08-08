# Normalization versus Denormalization
Có nhiều cách biểu diễn dữ liệu và một trong những vấn đề quan trọng nhất là bạn nên bình thường hóa dữ liệu của mình đến mức nào. Chuẩn hóa là chia dữ liệu thành nhiều bộ sưu tập với các tham chiếu giữa các bộ sưu tập. Mỗi phần dữ liệu nằm trong một bộ sưu tập mặc dù nhiều tài liệu có thể tham chiếu nó. Do đó, để thay đổi dữ liệu, chỉ có một tài liệu phải được cập nhật. Tuy nhiên, MongoDB không có phương tiện tham gia, vì vậy việc thu thập tài liệu từ nhiều bộ sưu tập sẽ yêu cầu nhiều truy vấn.

Sự không chuẩn hóa ngược lại với chuẩn hóa: nhúng tất cả dữ liệu vào một tài liệu. Thay vì các tài liệu có chứa các tham chiếu đến một bản sao dữ liệu rõ ràng, nhiều tài liệu có thể có các bản sao của dữ liệu. Điều này có nghĩa là nhiều tài liệu cần được cập nhật nếu thông tin thay đổi nhưng tất cả dữ liệu liên quan có thể được tìm nạp bằng một truy vấn duy nhất.

Quyết định khi nào bình thường hóa và khi nào không chuẩn hóa có thể khó khăn: thông thường, việc chuẩn hóa làm cho việc viết nhanh hơn và việc không chuẩn hóa làm cho việc đọc nhanh hơn. Vì vậy, bạn cần tìm ra những gì đánh đổi có ý nghĩa cho ứng dụng của bạn.
