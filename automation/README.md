# Tự động cập nhật nội dung tiếng Pháp

Đây là bước khởi tạo **an toàn**, chưa tự sinh bài mới hoặc sửa website.

- Workflow chạy mỗi ngày khoảng 08:15 giờ Việt Nam (GitHub Actions có thể chạy trễ).
- Kiểm tra tệp `index032.html` tồn tại và đọc được.
- Không sửa `index.html`, không ghi đè `index032.html`.
- Để tự sinh từ vựng, truyện và động từ, cần bổ sung nguồn tạo nội dung, bộ kiểm tra trùng lặp/chất lượng, và cơ chế xuất bản. Không đưa API key trực tiếp vào repository; sử dụng GitHub Actions Secrets.

Sau khi kiểm tra và thống nhất nguồn tạo nội dung, có thể mở rộng workflow để cập nhật các tệp JSON và tạo pull request tự động trước khi xuất bản.
