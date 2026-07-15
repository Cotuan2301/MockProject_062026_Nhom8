# Yêu Cầu Nghiệp Vụ (BRD) - SC_025 LOC History

## 1. Thông tin chung
- **Ticket ID:** SC_025
- **Tên tính năng:** LOC History (Lịch sử thay đổi Level of Care)
- **Người thực hiện:** Senior BA / Senior Research
- **Vai trò người dùng:** DON (Director of Nursing), Billing Administrator

## 2. User Story
"As a DON or Billing Administrator, I want to view the history of LOC changes and overrides for a resident, so that I can audit rate adjustments and ensure regulatory compliance."

## 3. Phân tích chức năng (Business Rules)
Dựa trên User Story và các Acceptance Criteria (AC), hệ thống cần cung cấp các chức năng sau:

### 3.1. Hiển thị danh sách lịch sử LOC
- **Vị trí hiển thị:** Tab "LOC" trong màn hình Resident Profile.
- **Dữ liệu hiển thị:**
  - Bảng danh sách các cấp độ chăm sóc (LOC) trong quá khứ.
  - Các trường dữ liệu yêu cầu theo AC: Start Date, End Date, Daily Rate, User authorized.
  - *(Lưu ý từ UI Mockup)* Giao diện hiện tại đang thể hiện các cột: Date, Action (Confirmed/Overridden), Previous Tier, New Tier, Actor, Note. Cần đảm bảo database cung cấp đủ các trường này để map với UI và AC.
- **Sắp xếp:** Mặc định sắp xếp theo thời gian mới nhất (Newest first).

### 3.2. Đánh dấu thủ công (Manual Override)
- **Luật bất biến (Business Rule):** Khi một bản ghi LOC được tạo ra do ghi đè thủ công (manual override), hệ thống phải lưu vết trạng thái này.
- **Hiển thị:** Cần có một dấu hiệu nhận biết (icon, badge - ví dụ: text "Overridden" theo UI mockup) trên bảng lịch sử LOC.
- **Hành động:** Cho phép người dùng click vào dấu hiệu/dòng dữ liệu đó để xem chi tiết lý do ghi đè (override reason/note).

### 3.3. Xuất báo cáo (Print/Export)
- **Hành động:** Cung cấp nút "Print/Export" trong giao diện lịch sử LOC.
- **Kết quả:** Hệ thống tạo và tải xuống báo cáo kiểm toán định dạng PDF hoặc CSV chứa danh sách lịch sử thay đổi LOC của cư dân.
- **Xử lý ngoại lệ (Error Handling):** Trong trường hợp server timeout hoặc lỗi không thể tạo file, hệ thống không được crash. Thay vào đó, giữ nguyên giao diện hiện tại và hiển thị thông báo lỗi (toast error message): *"Export failed. Please try again later."*

## 4. Luồng Dữ Liệu (Data Flow)
1. User truy cập Resident Profile -> Tab LOC.
2. Frontend gọi API lấy danh sách `resident_care_level_history`.
3. Backend truy vấn database, trả về danh sách đã được sắp xếp giảm dần theo thời gian.
4. User click Export:
   - Frontend gửi yêu cầu tải file.
   - Backend tổng hợp dữ liệu, generate file PDF/CSV và stream về cho client.
   - Nếu có lỗi, Backend trả về HTTP status error (ví dụ 500), Frontend catch lỗi và hiển thị toast message.

## 5. Dữ liệu liên quan (Models / Tables)
Dựa vào các từ khóa: `assessments`, `assessment_metrics`, `assessment_details`, `care_levels`, `resident_care_level_history`, `care_plans`.
Bảng chính được sử dụng cho tính năng này là `resident_care_level_history`, dự kiến bao gồm:
- ID
- Resident ID
- Date / Start Date / End Date
- Action (Confirmed / Overridden)
- Previous Tier / New Tier
- Actor (User ID người thực hiện)
- Note (Lý do thay đổi/ghi đè)
- Daily Rate (nếu có lưu lịch sử giá tại thời điểm thay đổi)

---
*Tài liệu này được sinh ra từ Bước 1 trong quy trình chuẩn (usage.md). Vui lòng xem xét và phản hồi (Duyệt) để chuyển sang Bước 2 (Thiết kế hệ thống).*
