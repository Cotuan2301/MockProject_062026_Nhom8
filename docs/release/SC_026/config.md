# Configuration & Deployment Notes - SC_026

## 1. Yêu cầu môi trường (Environment Variables)
- Không có biến môi trường (Environment Variables) mới nào được thêm vào trong Ticket này. Hệ thống vẫn sử dụng các biến cũ từ file `.env`.

## 2. Các thay đổi về Cấu hình Hệ thống (System Config)
- **Cập nhật `INSTALLED_APPS`:** Đã thêm app `apps.care_planning` vào danh sách `INSTALLED_APPS` trong `config/settings.py`. Quá trình triển khai không cần can thiệp thủ công vì file `settings.py` đã được commit.
- **Cập nhật `ROOT_URLCONF`:** Đã định tuyến endpoint `/care-planning/` trong `config/urls.py`.

## 3. Hướng dẫn Triển khai (Deployment Steps)
Khi kéo (pull) mã nguồn mới về môi trường Staging/Production, bắt buộc chạy các lệnh sau để đồng bộ hóa cơ sở dữ liệu:

```bash
# 1. Kích hoạt môi trường ảo (nếu có)
# source venv/bin/activate 

# 2. Áp dụng thay đổi cơ sở dữ liệu (Schema update)
python manage.py migrate

# 3. Thu thập file tĩnh (nếu triển khai production)
python manage.py collectstatic --noinput

# 4. Khởi động lại service (Gunicorn/Uvicorn hoặc systemctl)
# sudo systemctl restart gunicorn
```

## 4. Tác động tới CSDL (Database Impact)
- Tạo mới bảng `care_planning_careplan`.
- Thêm cột `loc_tier` vào bảng `residents_resident` (Có dữ liệu mặc định là "Tier 1"). Lệnh migrate sẽ tự động xử lý.
