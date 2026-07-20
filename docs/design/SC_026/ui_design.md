# UI/UX Design - SC_026 Care Plan List

## 1. Tổng quan giao diện (Overview)
Màn hình Care Plan List hiển thị danh sách các kế hoạch chăm sóc của những cư dân được phân công cho điều dưỡng. Giao diện được thiết kế theo phong cách hiện đại, sạch sẽ và tối ưu hóa để người dùng có thể dễ dàng quản lý, nhận diện các đầu việc cần làm (Draft, Pending, Review Due).

## 2. Bố cục (Layout)
- **Sidebar (Trái):** Hệ thống menu điều hướng với mục **Care Planning** đang được active.
- **Top Bar (Trên cùng):** Logo hệ thống (NHMS), chuông thông báo, hỗ trợ, thông tin người dùng (VD: Anna Lee - Nurse).
- **Vùng Nội dung chính (Main Content):** 
  - Khu vực Header (Tiêu đề và số lượng).
  - Thanh công cụ (Bộ lọc, Tìm kiếm, Các nút thao tác).
  - Thẻ tóm tắt (Summary Cards).
  - Bảng dữ liệu chính (Data Table).

## 3. Thành phần chi tiết (Components)

### 3.1. Header & Actions
- **Title:** "Care Plans" (Typography: H1, Bold, Màu sắc: Dark Gray / Đen).
- **Subtitle:** "24 plans across your assigned residents" (Typography: Body 2, Màu sắc: Text Muted / Xám nhạt).
- **Thanh tìm kiếm (Search Box):** Có icon kính lúp (magnifying glass). Chiếm tỷ lệ khoảng 30% chiều rộng của thanh filter.
- **Dropdowns (Status, Review):** Nền trắng, viền xám nhạt, có mũi tên xổ xuống.
- **Nút "Board":** Nút outline, viền xám, nền trắng.
- **Nút "+ New Care Plan":** Nút Primary (Màu xanh dương đậm: `#1d4ed8` hoặc tương tự), chữ trắng, bo góc (border-radius: 6px).

### 3.2. Summary Cards
Gồm 4 thẻ được phân bổ đều nhau trên 1 hàng, có hiệu ứng hover hoặc đổ bóng nhẹ (box-shadow).
- **Total plans:** Icon chồng tài liệu màu xanh dương nhạt. Nền icon tròn xanh dương.
- **Draft:** Icon giấy nháp màu xám. Nền icon tròn xám nhạt.
- **Pending Review:** Icon đồng hồ cát hoặc thời gian màu vàng cam. Nền icon vàng nhạt.
- **Review Due:** Icon báo thức màu cam đậm. Nền icon cam nhạt.
*Cấu trúc mỗi thẻ:* Icon bên trái, bên phải là Tiêu đề (chữ nhỏ) và Số lượng (chữ to, in đậm).

### 3.3. Data Table (Bảng dữ liệu)
Thiết kế dạng bảng kẻ ngang (horizontal borders) không có đường kẻ dọc, nền dòng chẵn/lẻ hoặc hover qua đổi màu xám nhạt (hover effect).

**Cấu hình hiển thị cột:**
- **Resident:** In đậm tên (VD: **Susan Wright**), nối với mã phòng bằng dấu chấm (· 114B).
- **LOC Tier:** Hiển thị dạng Badge viền tròn (Pill shape).
  - Tier 1: Nền xanh lá nhạt, chữ xanh lá đậm.
  - Tier 2: Nền xanh dương nhạt, chữ xanh dương đậm.
  - Tier 3: Nền vàng nhạt, chữ vàng đậm.
  - Tier 4: Nền đỏ/hồng nhạt, chữ đỏ đậm.
- **Status:** Hiển thị dạng Badge.
  - `Needs Update`: Nền đỏ nhạt, chữ đỏ (`#dc2626`).
  - `Review Due`: Nền vàng/cam nhạt.
  - `Active`: Nền xanh lá nhạt.
  - `Pending Review`: Nền vàng nhạt.
  - `Draft`: Nền xám nhạt.
- **Last Review:** Dạng Text bình thường (`YYYY-MM-DD`). Nếu trống hiển thị `--`.
- **Next Review:** Ngày dự kiến. Nếu quá hạn hiển thị chữ "overdue" màu xanh dương hoặc đỏ tùy mức độ cảnh báo (Theo wireframe là chữ màu xanh dương). Cột này có icon Sort (mũi tên lên/xuống).
- **Assigned:** Dạng Text bình thường (Tên nhân sự).
- **Hành động:** Chữ "View" màu xanh dương, đậm, có gạch chân khi hover.

## 4. Tương tác (Interactions)
- **Click "+ New Care Plan":** Chuyển hướng tới màn hình tạo mới Care Plan.
- **Click "View":** Chuyển hướng tới màn hình Care Plan Detail của dòng tương ứng.
- **Hover row:** Toàn bộ dòng của bảng sẽ sáng lên (highlight) để người dùng dễ nhìn.
- **Search/Filter:** Khi gõ từ khóa hoặc chọn filter, bảng dữ liệu bên dưới tự động reload lại (Ajax hoặc Reload page) để hiển thị danh sách tương ứng.

## 5. Responsive
- Màn hình Tablet (iPad): Ẩn bớt sidebar hoặc chuyển sidebar thành dạng icon thu gọn. Các Summary Cards có thể co thành 2 hàng x 2 cột.
- Cột trong Data Table: Cần cuộn ngang (horizontal scroll) nếu màn hình quá hẹp.
