# Thiết kế Giao diện (UI/UX) - SC_025 LOC History

## 1. Tổng quan
- **Vị trí:** Tab "LOC" nằm trong màn hình hồ sơ cư dân (Resident Profile).
- **Mục đích:** Hiển thị danh sách lịch sử các thay đổi cấp độ chăm sóc (Level of Care - LOC) của một cư dân, hỗ trợ xuất báo cáo.

## 2. Các thành phần giao diện

### 2.1. Bảng danh sách lịch sử (Data Table)
Bảng lịch sử LOC sẽ bao gồm các cột sau:
- **Date (Ngày):** Có thể sắp xếp (sortable), mặc định là giảm dần (mới nhất xếp trước). Hiển thị định dạng MM/DD/YYYY.
- **Action (Hành động):** Hiển thị các hành động thay đổi LOC (VD: Confirmed, Overridden). Dữ liệu này được hiển thị dưới dạng văn bản có màu xanh lam, có thể click hoặc hover để xem chi tiết nếu cần.
- **Previous Tier (Cấp độ trước đó):** Trạng thái LOC trước khi thay đổi, hiển thị dạng badge (VD: Level 1 màu xanh lá, Level 2 màu xanh dương, Level 3 màu vàng).
- **New Tier (Cấp độ mới):** Trạng thái LOC sau khi thay đổi, hiển thị dạng badge tương tự Previous Tier.
- **Actor (Người thực hiện):** Tên người và chức danh (VD: Anna Lee, RN; Denise Carter, DON).
- **Note (Ghi chú):** Lý do thay đổi hoặc ghi đè (VD: "No change - reassessment v3", "Suggested tier accepted", "Post-fall mobility decline - raised to Level 2").

### 2.2. Trạng thái Ghi đè (Override Indicator)
- Theo yêu cầu (AC), những bản ghi có thao tác ghi đè thủ công (manual override) cần có dấu hiệu nhận biết.
- Trong giao diện, cột **Action** sẽ hiển thị chữ **Overridden**.
- Người dùng có thể đọc lý do cụ thể ở cột **Note**.
- *Tùy chọn bổ sung:* Có thể hiển thị thêm một icon nhỏ cảnh báo bên cạnh chữ Overridden.

### 2.3. Báo cáo & Xuất dữ liệu (Print/Export)
- Có một nút **"Print/Export"** đặt phía trên cùng hoặc dưới cùng của bảng danh sách.
- Khi người dùng click:
  - Hiển thị Toast thông báo trạng thái "Đang xuất file...".
  - Nếu thành công, trình duyệt tự động tải xuống file PDF/CSV.
  - Nếu thất bại (server timeout, lỗi generate), hiển thị **Toast Error**: *"Export failed. Please try again later."* và giữ nguyên giao diện không bị gián đoạn.

### 2.4. Khung Audit Log (Thông tin phụ)
- Giao diện có một box thông tin (Alert/Note) hiển thị dòng chữ:
  *"Every LOC confirm/override event is immutable and timestamped (audit log).*
  *DON-only view — Nurse sees current tier on Profile Overview."*

## 3. Responsive & Accessibility
- **Responsive:** Bảng dữ liệu có khả năng cuộn ngang (horizontal scroll) trên các thiết bị màn hình nhỏ.
- **Màu sắc:** Tuân thủ hệ thống màu của dự án (màu badge Level 1, 2, 3 đã được định nghĩa ở SC_024).

---
*Tài liệu này là kết quả của Bước 2.1 trong quy trình.*
