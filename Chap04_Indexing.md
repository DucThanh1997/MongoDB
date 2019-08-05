# Indexing
A database index is similar to a book’s index. Instead of looking through the whole book,
the database takes a shortcut and just looks at an ordered list that points to the content,
which allows it to query orders of magnitude faster.

A query that does not use an index is called a table scan (a term inherited from relational
databases), which means that the server has to “look through the whole book” to find
a query’s results. This process is basically what you’d do if you were looking for infor‐
mation in a book without an index: you start at page 1 and read through the whole thing.
In general, you want to avoid making the server do table scans because it is very slow
for large collections.

Một chỉ mục cơ sở dữ liệu tương tự như một chỉ mục cuốn sách. Thay vì xem qua toàn bộ cuốn sách, cơ sở dữ liệu sẽ sử dụng một phím tắt và 
chỉ nhìn vào một danh sách được sắp xếp trỏ đến nội dung, cho phép nó truy vấn các đơn đặt hàng có cường độ nhanh hơn.

Một truy vấn không sử dụng chỉ mục được gọi là quét bảng (thuật ngữ được kế thừa từ cơ sở dữ liệu quan hệ), 
điều đó có nghĩa là máy chủ phải xem qua toàn bộ cuốn sách để tìm kết quả truy vấn. 
Quá trình này về cơ bản là những gì bạn làm nếu bạn đang tìm kiếm thông tin trong một cuốn sách không có chỉ mục:
bạn bắt đầu ở trang 1 và đọc toàn bộ. Nói chung, bạn muốn tránh làm cho máy chủ thực hiện quét bảng vì nó rất chậm đối với các bộ sưu tập lớn.
