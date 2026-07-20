# Business Requirements Document (BRD)
## Ticket: SC_024 - LOC Classification Result

### 1. Giới thiệu & Mục tiêu (Overview & Objectives)
Tính năng **LOC (Level of Care) Classification Result** cho phép Điều dưỡng (Nurse) hoặc Người đánh giá (Assessor) xem trước phân loại mức độ chăm sóc được hệ thống gợi ý dựa trên điểm số đánh giá ADL (Activities of Daily Living) từ hồ sơ Đánh giá ban đầu (Initial Assessment). Người dùng có thể xác nhận (Confirm) gợi ý này hoặc ghi đè (Override) trong các trường hợp đặc biệt, làm căn cứ để đưa ra mức phí chăm sóc hàng ngày (Estimated Daily Rate) và thiết lập Kế hoạch chăm sóc (Care Plan) tiếp theo.

### 2. User Stories & Acceptance Criteria (AC)

**User Story:**
> *Với tư cách là một Điều dưỡng viên (Nurse/RN), tôi muốn xem kết quả tính toán phân loại LOC dựa trên điểm ADL của bệnh nhân, để tôi có thể chốt (Confirm) hoặc điều chỉnh (Override) mức độ chăm sóc, từ đó hệ thống có thể áp dụng mức phí (Daily Rate) phù hợp.*

**Acceptance Criteria (AC):**
1. **Hiển thị Tổng điểm ADL (ADL Score):** Hệ thống tự động tổng hợp điểm từ 8 hoạt động (Bed Mobility, Transfer, Locomotion, Dressing, Eating, Toilet Use, Personal Hygiene, Bathing). Mỗi hoạt động từ 0-4 điểm. Tổng điểm tối đa là 32.
2. **Gợi ý Mức độ LOC (Suggested LOC):** Dựa vào tổng điểm ADL, hệ thống gợi ý mức LOC theo công thức (Hardcoded reference):
   - **Level 1 (0-8):** Independent (Độc lập)
   - **Level 2 (9-16):** Limited Assist. (Hỗ trợ giới hạn)
   - **Level 3 (17-24):** Extensive Assist. (Hỗ trợ diện rộng)
   - **Level 4 (25-32):** Total Assistance (Hỗ trợ toàn diện)
3. **Bảng phân tích (ADL Item Breakdown):** Hiển thị danh sách 8 hoạt động, điểm số từng mục và nguồn đánh giá (VD: Initial Assessment v3).
4. **Chi phí ước tính (Estimated Daily Rate):** Hệ thống tự động ánh xạ mức LOC được gợi ý/chọn với bảng giá `LOC Rate Table` để hiển thị phí hàng ngày (Read-only).
5. **Thao tác Xác nhận (Confirm/Override):**
   - Nút **Confirm LOC**: Chốt mức LOC hệ thống gợi ý.
   - Nút **Override**: Mở modal cho phép chọn mức LOC khác và BẮT BUỘC nhập lý do ghi đè.
   - Nút **View LOC History**: Chuyển hướng sang màn hình lịch sử LOC (SC_025).
6. **Lịch sử thao tác (Audit Log):** Hiển thị log của hành động ở cuối trang (Người xác nhận, thời gian, hành động, bước tiếp theo).

### 3. Cấu trúc Dữ liệu & Thiết kế Database (Data Models)
*(Sẽ được triển khai tại `apps/medical/models.py` và `apps/billing/models.py`)*

* **`medical.Assessment`** (Bảng đánh giá hiện tại hoặc mở rộng):
  - Ghi nhận chi tiết điểm ADL (`adl_bed_mobility`, `adl_transfer`, v.v.).
  - `total_adl_score` (Integer)

* **`medical.LOCClassification`** (Bảng lưu trữ kết quả phân loại - Mới):
  - `assessment` (ForeignKey -> Assessment): Liên kết với bài đánh giá gốc.
  - `calculated_score` (Integer): Tổng điểm tại thời điểm phân loại.
  - `suggested_loc` (CharField): Mức LOC hệ thống đề xuất (Level 1,2,3,4).
  - `final_loc` (CharField): Mức LOC cuối cùng được chốt.
  - `is_overridden` (BooleanField): Cờ đánh dấu có bị ghi đè hay không.
  - `override_reason` (TextField, null=True, blank=True): Lý do ghi đè.
  - `confirmed_by` (ForeignKey -> User): Người xác nhận.
  - `confirmed_at` (DateTimeField, auto_now_add=True): Thời điểm chốt.
  - `status` (CharField): Trạng thái (Pending, Confirmed).

* **`billing.LOCRate`** (Bảng giá cấu hình):
  - `loc_level` (CharField): Mã Level.
  - `daily_rate` (DecimalField): Giá tiền/ngày.

### 4. Luật Kiểm soát Truy cập (RBAC) & Luật Bất biến (Immutability)

**Luật Bất biến (Immutability - BR-05 Chart Lock):**
* Sau khi người dùng nhấn **Confirm LOC** hoặc **Override** thành công, bản ghi `LOCClassification` sẽ bị KHÓA (Chart Lock).
* Không ai được phép sửa đổi trực tiếp dữ liệu đã chốt. Bất kỳ sự thay đổi nào về sau đều phải thông qua quy trình Đánh giá lại (Reassessment), tạo ra một version mới.

**Role-Based Access Control (RBAC):**
* **Nurse / Assessor / Doctor**: Có quyền View bảng điểm và thực hiện hành động Confirm/Override.
* **Admin / Manager**: Có quyền xem (View-only), có thể điều chỉnh cấu hình bảng giá `LOCRate` ở hệ thống backend.
* **Người dùng không có quyền (Unauthorized)**: Nếu bị khóa quyền hoặc không được phân công, sẽ chỉ nhìn thấy màn hình ở trạng thái Read-Only, các nút "Confirm", "Override" sẽ bị vô hiệu hóa hoặc ẩn đi.

### 5. Chuẩn tuân thủ HIPAA
* Thông tin bệnh nhân (Robert Hayes) và chi tiết bệnh án (điểm ADL) là dữ liệu PHI (Protected Health Information).
* Mọi hành động thao tác (Confirm, Override) phải được log lại chi tiết (Thời gian, ID người dùng, nội dung thay đổi) để phục vụ mục đích kiểm toán (Audit Trail) trong chuẩn HIPAA. Tên và vai trò của người thao tác hiển thị rõ ở dòng log cuối màn hình.
