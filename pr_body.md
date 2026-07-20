# Pull Request

**Title:** `feat(care_planning): implement SC_026 Care Plan List`

## 📝 Mô tả (Description)
Pull Request này hiện thực hóa **Ticket SC_026 (Care Plan List)**, cho phép Nurse và DON (Director of Nursing) xem danh sách các kế hoạch chăm sóc của cư dân được phân công. Tính năng này giúp nhận diện nhanh chóng các Care Plan cần cập nhật, đang chờ đánh giá (Pending Review), hoặc đã đến hạn (Review Due).

## 🚀 Các thay đổi chính (Key Changes)
- **Database & Models:**
  - Khởi tạo app `care_planning` mới hoàn toàn độc lập.
  - Khởi tạo bảng `CarePlan` tại `apps/care_planning/models.py`.
  - Cập nhật bảng `Resident` trong `apps/residents/models.py` thêm trường `loc_tier`.
  - Migrate cơ sở dữ liệu để áp dụng thay đổi.
- **REST APIs / Views:**
  - `GET /care-planning/care-plans/`: (CarePlanListView) Lấy danh sách Care Plan hỗ trợ lọc (status, review) và search. Đồng thời tính toán dữ liệu cho các thẻ thống kê Summary Cards.
- **Giao diện (UI):**
  - Bổ sung màn hình `care_plan_list.html` nằm trong app `care_planning`.
  - Bảng dữ liệu hiển thị rõ ràng LOC, Trạng thái (được đánh dấu màu sắc/badge) và ngày tháng.
- **Tài liệu & Test:**
  - Bổ sung Unit Tests tại `apps/care_planning/tests.py` (Covered 6/6 test cases đạt 100%).
  - Cập nhật [Config.md](docs/release/SC_026/config.md) và [Release.md](docs/release/SC_026/release.md).
  - Log lại thông tin thay đổi vào `change_history.md`.

## 📸 Ảnh chụp màn hình / UI Mockup (Nếu có)
*(Developer có thể chèn ảnh chụp màn hình tính năng Care Plan List tại đây)*

## 📋 Checklist kiểm tra (QA Checklist)
- [x] Code đã tuân thủ Naming Conventions của dự án.
- [x] Đã xử lý logic filter và search theo đúng UI design.
- [x] Các test cases đã pass 100% (`python manage.py test apps.care_planning`).
- [x] Không có xung đột (conflicts) với nhánh `dev`.
- [x] Đã cập nhật tài liệu phát hành (Release Note).

## 🔗 Liên kết (Related Links)
- **Ticket:** SC_026
- **Tài liệu tham khảo:** [Bước 2.1 UI Design](docs/design/SC_026/ui_design.md), [Bước 2.2 API Design](docs/design/SC_026/api_design.md)
