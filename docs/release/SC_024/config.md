# Cấu hình Môi trường (SC_024 - LOC Classification)

Không có cấu hình biến môi trường (ENV) hay Port mới nào được thêm vào trong ticket này. Các cấu hình kết nối Database (SSMS 22/SQLite) và URL cơ bản tiếp tục sử dụng từ file `.env` chung của dự án.

## Dữ liệu phụ thuộc (Dependencies)
Cần đảm bảo file `setup_dummy_data.py` được chạy 1 lần ở môi trường Dev/Staging để nạp các thông số bảng giá (LOC Rate) và bản ghi test:
```bash
python setup_dummy_data.py
```
