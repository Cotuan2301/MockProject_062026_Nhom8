# Giao diện UI/UX Design (SC_024 - LOC Classification)

## 1. Cấu trúc Layout Tổng thể (Layout Structure)
Giao diện kế thừa layout chuẩn của hệ thống (Django template `base.html` hoặc `dashboard.html`), bao gồm:
* **Sidebar (Left):** Menu điều hướng (Dashboard, Residents, Care Planning, eMAR...).
* **Topbar (Top):** Thanh tìm kiếm, thông báo, User Profile (Anna Lee - Nurse).
* **Main Content Area:** Khu vực hiển thị nội dung chính của LOC Classification.

## 2. Phân rã Component (Block Breakdown)

### 2.1. Page Header (Tiêu đề trang)
* **Breadcrumb:** `Residents > {Resident Name} > LOC`
* **Title:** `LOC Classification Result — {Resident Name}` (Thẻ `<h1>` font đậm, hiện đại).
* **Subtitle:** `From Assessment v{Version} · {Date}` (Màu xám nhạt text-gray-500).

### 2.2. Info Cards (Grid 2 cột trên Desktop, 1 cột trên Mobile)
* **Card 1 (ADL Score):** 
  - Khối chữ nhật bo góc, đổ bóng nhẹ (shadow-sm).
  - Nội dung: Số điểm cực lớn (vd: **20 / 32**) ở trung tâm.
* **Card 2 (Suggested LOC):**
  - Khối chữ nhật bo góc, màu nền thay đổi động theo Level (Dynamic Background):
    - Level 1: Nền xanh lá nhạt (bg-green-100).
    - Level 2: Nền xanh dương nhạt (bg-blue-100).
    - Level 3: Nền vàng nhạt (bg-yellow-100).
    - Level 4: Nền đỏ nhạt (bg-red-100).
  - Nội dung: Tên level (vd: **Level 3 — Extensive Assistance**).

### 2.3. ADL Item Breakdown (Bảng chi tiết)
* Bảng hiển thị 8 tiêu chí ADL. Sử dụng thẻ `<table>` với class của Tailwind/Bootstrap (vd: `table-auto w-full`).
* Cột: `Activity` (Canh trái), `Score` (Canh giữa, in đậm), `Source` (Canh trái, chữ xám).
* Hàng có hiệu ứng hover đổi màu nền (`hover:bg-gray-50`).

### 2.4. LOC Level Reference (Khối tham chiếu - Fixed)
* Sử dụng Flexbox hoặc Grid (4 cột) để hiển thị 4 block màu tương ứng với 4 level.
* Mỗi block chứa thông tin: Tên Level, Khoảng điểm, Phân loại. Trực quan hóa giúp User đối chiếu dễ dàng.

### 2.5. Estimated Daily Rate (Khối chi phí)
* Card đơn giản hiển thị số tiền tương ứng với Level. Text màu nhấn mạnh (Primary Color).

### 2.6. Action Bar & Modals (Nút thao tác)
* **Khu vực Nút:**
  - Nút **Confirm LOC**: Button primary (màu xanh/màu chủ đạo của app), có icon dấu tick.
  - Nút **Override**: Button secondary (outline), có icon cây bút.
  - Link **View LOC History**: Thẻ `<a>` màu xanh, có icon mũi tên `->`.
* **Modal Override:**
  - Khi bấm Override, popup modal hiện lên.
  - Chứa Select box chọn Level mới.
  - Chứa Textarea nhập `override_reason` (Bắt buộc - Required).
  - Nút Submit & Cancel.

### 2.7. Audit Log (Footer)
* Khối text chữ nhỏ, màu xám ở dưới cùng.
* Hiển thị log của hành động gần nhất: `Confirmed by: {User} · {Date} · Action: {Action Detail}`.

## 3. Responsive & Interactive Design
* **Mobile/Tablet:** Khối Info Cards chuyển thành xếp chồng (stack vertically). Bảng ADL Breakdown có thể cuộn ngang (`overflow-x-auto`).
* **Micro-interactions:** Hiệu ứng hover vào các nút bấm, hiệu ứng mờ nền khi mở Modal.
* **Loading State:** Thêm spinner mờ màn hình khi bấm nút Confirm/Override để chờ API phản hồi.

## 4. Xử lý RBAC & Trạng thái Khóa (Chart Lock)
Trong Django Template, sử dụng cấu trúc `{% if %}` để render:
* **Trường hợp bị Khóa (Confirmed):**
  - Ẩn hoàn toàn nút **Confirm LOC** và **Override**.
  - Hiển thị badge trạng thái `[ ĐÃ XÁC NHẬN ]`.
* **Trường hợp không có quyền (View-only Role):**
  - Ẩn các nút thao tác.
  - Bảng biểu và điểm số vẫn hiển thị bình thường.
