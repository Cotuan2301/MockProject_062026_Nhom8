# Release Notes - SC_026 Care Plan List

## Tính năng mới (New Features)
- **Care Plan List (Danh sách kế hoạch chăm sóc):** Cung cấp giao diện cho Nurse và DON xem toàn bộ kế hoạch chăm sóc của cư dân được phân công.
- **Thống kê tổng quan (Summary Cards):** Thêm các thẻ đếm số lượng nhanh cho các trạng thái: Total plans, Draft, Pending Review, và Review Due.
- **Lọc và tìm kiếm:**
  - Lọc danh sách theo trạng thái Care Plan (Draft, Active, Review Due, v.v.).
  - Lọc theo ngày đến hạn đánh giá (Review Due).
  - Tìm kiếm nhanh theo tên hoặc ID của Resident.
- **Mức độ chăm sóc (LOC Tier):** Hiển thị rõ mức độ chăm sóc của từng cư dân ngay trên danh sách. Bổ sung trường `loc_tier` vào hồ sơ Resident gốc.

## Sửa lỗi & Tối ưu (Bug Fixes & Improvements)
- Khởi tạo app `care_planning` độc lập để tăng tính module hóa của dự án.
- **Bugfix (Hotfix nội bộ):** Vá lỗi `AttributeError` không tìm thấy `resident_list` trong app `residents` giúp server khởi động bình thường.

## Đánh giá QA (QA Sign-off)
- **Unit Test:** Đã bao phủ 100% các logic về list view, filter, summary. Tất cả test cases đều Passed (6/6).
- **Trạng thái Ticket:** Đã sẵn sàng để review và merge.
