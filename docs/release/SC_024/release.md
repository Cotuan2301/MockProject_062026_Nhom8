# Release Note: SC_024 - LOC Classification Result

## Tóm tắt (Summary)
Bản phát hành này tích hợp tính năng **LOC Classification Result**, cho phép hệ thống tự động tính toán, gợi ý và lưu trữ cấp độ chăm sóc (Level of Care - LOC) dựa vào tổng điểm ADL của bệnh nhân từ Initial Assessment.

## Các tính năng mới (New Features)
- **Tính điểm Tự động:** Tự động quy đổi tổng điểm ADL (0-32) ra các cấp độ LOC từ Level 1 đến Level 4.
- **Xác nhận LOC:** Chức năng cho phép Điều dưỡng/Assessor "Confirm" mức LOC được hệ thống gợi ý. Kích hoạt luật bất biến **BR-05 Chart Lock**, đóng băng bản ghi không cho sửa đổi nếu không có đánh giá lại.
- **Ghi đè (Override):** Cho phép người dùng chọn mức LOC khác (kèm lý do bắt buộc) trong các trường hợp đặc biệt.
- **Audit Log (HIPAA):** Ghi nhận chi tiết lịch sử xác nhận, ghi đè (thời gian, người thực hiện, hành động) hiển thị tại Footer.
- **UI/UX Update:** Bổ sung giao diện thẻ động màu sắc theo mức LOC, khóa giao diện (hiển thị Read-only) khi hồ sơ đã được chốt.

## Các thay đổi cơ sở dữ liệu (Database Migrations)
Các models mới đã được thêm và migrate vào Database:
- `medical.Assessment` (Khởi tạo structure gốc)
- `medical.LOCClassification` (OneToOne với Assessment)
- `medical.LOCClassificationHistory` (Log Audit HIPAA)
- `billing.LOCRate` (Bảng giá Level of Care)
