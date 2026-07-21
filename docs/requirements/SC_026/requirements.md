# Business Requirement Document (BRD) - SC_026 Care Plan List

## 1. Thông tin chung
- **Mã Ticket:** SC_026
- **Tên tính năng:** Care Plan List
- **Mô-đun:** Care Planning
- **Vai trò người dùng:** Nurse, DON (Director of Nursing)

## 2. User Story
"As a Nurse or DON, I want to view the list of care plans by resident, status, and review date, so that I can quickly identify which care plans need to be created, reviewed, approved, or updated."

## 3. Acceptance Criteria
1. **Truy cập danh sách:** Given the Nurse or DON has access to the Care Planning module, When the user opens the Care Plan List screen, Then the system displays care plans with resident name, LOC, care plan status, last updated date, and next review date.
2. **Lọc theo trạng thái:** Given care plans exist in different statuses, When the user filters by status, Then the system displays only the care plans matching the selected status.
3. **Tìm kiếm:** Given the user searches by resident name or resident ID, When matching records are found, Then the system displays the related care plans in the list.
4. **Xem chi tiết:** Given a care plan is selected from the list, When the user clicks the record, Then the system opens the Care Plan Detail screen for that resident.

## 4. Đặc tả giao diện (Wireframe & UI Elements)
Dựa trên wireframe được cung cấp, màn hình Care Plan List bao gồm các thành phần sau:

### 4.1. Tiêu đề và thông tin chung
- **Breadcrumb:** Care Planning > List
- **Page Title:** Care Plans
- **Subtitle:** Hiển thị tổng số kế hoạch chăm sóc trong các cư dân được phân công (VD: "24 plans across your assigned residents")

### 4.2. Vùng điều khiển (Controls)
- **Thanh tìm kiếm (Search box):** Text input với placeholder "Search residents..." dùng để tìm kiếm theo tên hoặc ID cư dân.
- **Bộ lọc Trạng thái (Status filter):** Dropdown list cho phép lọc theo trạng thái (Mặc định: "All"). Các trạng thái bao gồm: Needs Update, Review Due, Active, Pending Review, Draft.
- **Bộ lọc Ngày đánh giá (Review filter):** Dropdown list cho phép lọc theo tình trạng đánh giá (Mặc định: "All").
- **Nút "Board":** Nút chức năng chuyển đổi chế độ xem.
- **Nút "+ New Care Plan":** Nút chính để tạo kế hoạch chăm sóc mới (nút Primary).

### 4.3. Thẻ thống kê (Summary Cards)
- **Total plans:** Tổng số kế hoạch chăm sóc.
- **Draft:** Số lượng kế hoạch đang ở trạng thái nháp.
- **Pending Review:** Số lượng kế hoạch đang chờ đánh giá/duyệt.
- **Review Due:** Số lượng kế hoạch đến hạn đánh giá.

### 4.4. Bảng dữ liệu (Data Table)
Bảng hiển thị danh sách kế hoạch chăm sóc với các cột (theo thứ tự từ trái sang phải):
1. **Resident:** Tên cư dân và số phòng/ID (VD: Susan Wright · 114B). Có in đậm tên.
2. **LOC Tier:** Mức độ chăm sóc (VD: Tier 1, Tier 2, Tier 3, Tier 4) - Hiển thị dạng badge với màu sắc phân biệt.
3. **Status:** Trạng thái của care plan (VD: Needs Update, Review Due, Active, Pending Review, Draft) - Hiển thị dạng badge với màu sắc tương ứng trạng thái.
4. **Last Review:** Ngày đánh giá lần cuối (Định dạng: YYYY-MM-DD hoặc "--" nếu chưa có).
5. **Next Review:** Ngày dự kiến đánh giá tiếp theo (Định dạng: YYYY-MM-DD). Hiển thị text "overdue" (màu khác biệt) nếu đã quá hạn. Cột này cho phép sắp xếp (Sortable).
6. **Assigned:** Tên nhân viên được phân công phụ trách bản kế hoạch (VD: Anna Lee).
7. **Action:** Liên kết "View" để chuyển hướng mở chi tiết kế hoạch chăm sóc của cư dân đó.
