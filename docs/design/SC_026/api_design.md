# API & Database Schema Design - SC_026 Care Plan List

## 1. Database Schema

Dựa trên yêu cầu của tính năng Care Plan List, cấu trúc dữ liệu chủ yếu liên quan đến Model `CarePlan`. Mối quan hệ với các bảng khác bao gồm `Resident` (Cư dân) và `User` (Nhân viên y tế).

### 1.1. Model `CarePlan` (Thuộc App `care_planning`)

**Các trường dữ liệu (Fields):**
- `id` (UUID hoặc AutoField): Khóa chính.
- `resident` (ForeignKey to `Resident`): Cư dân được lập kế hoạch chăm sóc. Liên kết này để lấy tên và ID, phòng của cư dân (Resident details).
- `status` (CharField, Choices): Trạng thái của Care Plan.
  - Các giá trị (Choices): `draft` (Draft), `pending_review` (Pending Review), `active` (Active), `review_due` (Review Due), `needs_update` (Needs Update).
- `last_review_date` (DateField, null=True, blank=True): Ngày đánh giá lần cuối.
- `next_review_date` (DateField, null=True, blank=True): Ngày dự kiến đánh giá tiếp theo.
- `assigned_to` (ForeignKey to `User`, null=True): Nhân viên (Nurse/DON) được phân công phụ trách.
- `created_at` (DateTimeField, auto_now_add=True): Ngày tạo.
- `updated_at` (DateTimeField, auto_now=True): Ngày cập nhật cuối.

*Lưu ý: Mức độ chăm sóc (LOC Tier) thường được lấy từ thông tin của `Resident` thông qua quan hệ, hoặc là một phần của hệ thống Assessment.*

### 1.2. Mối quan hệ bổ trợ (Relationships)
- **`Resident` Model:** Chứa các thông tin về `first_name`, `last_name`, `room_number`, và liên kết tới mức độ `loc_tier` (Mức độ chăm sóc hiện tại).
- **`User` Model:** Thông tin nhân sự y tế.

## 2. API Design

Ứng dụng có thể sử dụng Django Templates trực tiếp hoặc cung cấp RESTful APIs để Front-end (React/Vue/Vanilla JS) gọi. Dưới đây là thiết kế REST API nếu sử dụng dạng SPA hoặc Ajax calls.

### 2.1. API Lấy danh sách Care Plans
- **Endpoint:** `GET /api/care-planning/care-plans/`
- **Mục đích:** Lấy danh sách Care Plan, hỗ trợ phân trang (pagination), tìm kiếm (search), lọc (filter) và sắp xếp (sorting).
- **Query Parameters:**
  - `search` (string): Tìm kiếm theo tên cư dân (vd: "Susan") hoặc ID cư dân.
  - `status` (string): Lọc theo trạng thái (vd: `active`, `draft`).
  - `review` (string): Lọc theo trạng thái đánh giá (vd: `all`, `due`).
  - `ordering` (string): Sắp xếp. (vd: `next_review_date`, `-next_review_date`).
  - `page`, `page_size`: Phân trang.
- **Response Format (200 OK):**
```json
{
  "count": 24,
  "next": "http://api.../care-plans/?page=2",
  "previous": null,
  "results": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "resident": {
        "id": 1,
        "name": "Susan Wright",
        "room": "114B",
        "loc_tier": "Tier 2"
      },
      "status": "needs_update",
      "last_review_date": "2026-03-30",
      "next_review_date": "2026-07-03",
      "is_overdue": true,
      "assigned_to": {
        "id": 101,
        "name": "Anna Lee"
      }
    }
    // ...
  ]
}
```

### 2.2. API Lấy thống kê số lượng (Summary Cards)
- **Endpoint:** `GET /api/care-planning/care-plans/summary/`
- **Mục đích:** Trả về số liệu cho các thẻ thống kê phía trên của giao diện.
- **Query Parameters:** Tương tự API Danh sách để số liệu thống kê thay đổi theo điều kiện (hoặc mặc định chỉ lấy của User hiện tại).
- **Response Format (200 OK):**
```json
{
  "total_plans": 24,
  "draft": 5,
  "pending_review": 3,
  "review_due": 2
}
```

## 3. Quyền truy cập (Permissions)
- Chức năng chỉ khả dụng cho các User thuộc nhóm (Roles): **Nurse**, **DON (Director of Nursing)**.
- Người dùng chỉ thấy các Care Plan của những cư dân mà mình được phân công (Assigned), trừ khi là DON có quyền xem toàn hệ thống.
