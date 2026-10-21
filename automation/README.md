# Tự động xuất bản bài tiếng Pháp hằng ngày (không API key)

Sau khi merge PR vào nhánh `main`, GitHub Actions chạy theo lịch mỗi ngày khoảng **08:15 Việt Nam** (có thể trễ) hoặc chạy thủ công từ tab Actions.

- **Nguồn nội dung:** `automation/content-queue.json` gồm 14 bài gốc chuẩn bị sẵn; mỗi ngày phát hành thêm một bài bắt đầu từ **22/10/2026**.
- **Tác vụ:** `automation/publish.py` kiểm tra dữ liệu và cập nhật `automation/published.json`; workflow commit khi có thay đổi.
- **Trang đọc mới:** `daily.html`, truy cập qua GitHub Pages.
- **An toàn:** Không sửa `index032.html`, `index.html` hoặc các tệp phiên bản khác.
- **Không dùng AI API:** Hệ thống phát hành nội dung được biên soạn trước, không tự sáng tác vô hạn. **Sau 14 ngày phải bổ sung nội dung vào hàng đợi**; khi hết, workflow không tạo nội dung mới.
- **Đổi ngày để thử cục bộ:** `CONTENT_DATE=2026-10-22 python3 automation/publish.py`.

**Điều kiện:** GitHub Actions phải được bật, quyền Workflow permissions cho phép ghi (`Read and write permissions`), và GitHub Pages xuất bản từ nhánh `main` (hoặc thiết lập Pages tương ứng). Nếu nhánh được bảo vệ không cho bot push, cần điều chỉnh workflow sang pull request.

Đường dẫn học: `https://trungbh408.github.io/hoctiengphap/daily.html`.
