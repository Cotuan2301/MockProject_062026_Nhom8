# Thiết kế API & Database - SC_025 LOC History

## 1. Thiết kế Cơ sở dữ liệu (Database Schema)

Để lưu trữ lịch sử thay đổi LOC, chúng ta sẽ tạo model `ResidentCareLevelHistory` (có thể thuộc app `medical` hoặc `residents` tùy vào kiến trúc hiện tại, ưu tiên `medical` vì liên quan đến đánh giá sức khỏe và LOC).

### Bảng: `medical_residentcarelevelhistory`

| Cột | Kiểu dữ liệu (Django) | Thuộc tính | Ràng buộc |
| --- | --- | --- | --- |
| `id` | `BigAutoField` | Primary Key | |
| `resident` | `ForeignKey` | Khóa ngoại tới model `Resident` | `on_delete=models.CASCADE` |
| `date` | `DateTimeField` | Thời gian xảy ra thay đổi | `auto_now_add=True` |
| `action` | `CharField` | Loại hành động thay đổi | Choices: `CONFIRMED`, `OVERRIDDEN` |
| `previous_tier` | `CharField` | Mức độ trước đó (có thể null nếu là lần đầu) | `max_length=50`, `null=True`, `blank=True` |
| `new_tier` | `CharField` | Mức độ mới (sau khi thay đổi) | `max_length=50` |
| `actor` | `ForeignKey` | Người thực hiện (User/Staff) | `on_delete=models.SET_NULL`, `null=True` |
| `note` | `TextField` | Lý do thay đổi / Ghi đè | `blank=True`, `null=True` |

> *Ghi chú:* Bảng này mang tính chất Audit (bất biến - immutable), sau khi tạo bản ghi thì không được phép sửa đổi/xóa trừ trường hợp đặc biệt bởi admin hệ thống.

## 2. Thiết kế API Endpoints

### 2.1. API Lấy danh sách Lịch sử LOC
- **Endpoint:** `GET /api/medical/residents/{resident_id}/loc-history/`
- **Mục đích:** Lấy danh sách lịch sử thay đổi LOC của một cư dân, sắp xếp theo thời gian giảm dần.
- **Quyền truy cập:** Các role được phép xem hồ sơ y tế (Ví dụ: DON, Billing Administrator, Nurse).
- **Tham số (Query Params):**
  - `page`: Số trang (phân trang).
  - `limit`: Số lượng bản ghi mỗi trang.
- **Response thành công (200 OK):**
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 3,
      "date": "2026-04-05T10:00:00Z",
      "action": "Confirmed",
      "previous_tier": "Level 3",
      "new_tier": "Level 3",
      "actor_name": "Anna Lee, RN",
      "note": "No change - reassessment v3"
    },
    {
      "id": 2,
      "date": "2026-01-08T14:30:00Z",
      "action": "Confirmed",
      "previous_tier": "Level 2",
      "new_tier": "Level 3",
      "actor_name": "Anna Lee, RN",
      "note": "Suggested tier accepted"
    },
    {
      "id": 1,
      "date": "2025-11-02T09:15:00Z",
      "action": "Overridden",
      "previous_tier": "Level 1",
      "new_tier": "Level 2",
      "actor_name": "Denise Carter, DON",
      "note": "Post-fall mobility decline - raised to Level 2"
    }
  ]
}
```

### 2.2. API Xuất báo cáo (Export/Print)
- **Endpoint:** `GET /api/medical/residents/{resident_id}/loc-history/export/`
- **Mục đích:** Tải xuống file báo cáo (PDF/CSV) chứa thông tin lịch sử LOC.
- **Quyền truy cập:** DON, Billing Administrator.
- **Tham số (Query Params):**
  - `format`: `pdf` hoặc `csv` (Mặc định `pdf`).
- **Response thành công (200 OK):**
  - File đính kèm dưới dạng stream data.
  - Header: `Content-Disposition: attachment; filename="loc_history_{resident_id}.pdf"`
- **Response thất bại (500 Internal Server Error):**
```json
{
  "error": "Export failed. Please try again later."
}
```

---
*Tài liệu này là kết quả của Bước 2.2 trong quy trình.*
