# LLD & API Design Document (SC_024)

## 1. Database Schema Design (Django Models)

### Bảng `billing.LOCRate` (Biểu phí theo LOC)
Lưu trữ cấu hình giá tiền tương ứng với từng cấp độ chăm sóc.
* `loc_level`: `CharField` (VD: 'Level 1', 'Level 2', 'Level 3', 'Level 4'), Unique.
* `daily_rate`: `DecimalField` (max_digits=10, decimal_places=2)

### Bảng `medical.Assessment` (Bổ sung nếu chưa hoàn chỉnh)
* `total_adl_score`: `IntegerField`
* *(Các trường điểm ADL thành phần...)*

### Bảng `medical.LOCClassification`
Lưu trữ kết quả phân loại dựa trên 1 Assessment.
* `assessment`: `OneToOneField(Assessment, on_delete=CASCADE, related_name='loc_classification')`
* `calculated_score`: `IntegerField` (Tổng điểm ADL lúc tính toán)
* `suggested_loc`: `CharField(max_length=20)` (Mức hệ thống tính)
* `final_loc`: `CharField(max_length=20)` (Mức cuối cùng được chốt)
* `is_overridden`: `BooleanField(default=False)`
* `override_reason`: `TextField(null=True, blank=True)`
* `confirmed_by`: `ForeignKey(User, on_delete=SET_NULL, null=True)`
* `confirmed_at`: `DateTimeField(null=True)`
* `status`: `CharField` (choices: 'Pending', 'Confirmed')

### Bảng `medical.LOCClassificationHistory` (HIPAA Audit Log)
Lịch sử thao tác trên bảng LOCClassification.
* `loc_classification`: `ForeignKey(LOCClassification, on_delete=CASCADE)`
* `action`: `CharField` (VD: 'Confirmed', 'Overridden')
* `action_by`: `ForeignKey(User, on_delete=SET_NULL, null=True)`
* `action_at`: `DateTimeField(auto_now_add=True)`
* `details`: `TextField` (Ghi chú lý do hoặc thông tin level bị thay đổi)

---

## 2. API Design & URL Routing

**Base URL**: `/medical/api/assessments/<assessment_id>/loc/`

### 2.1 GET `/` (Retrieve LOC Result)
* **Quyền hạn:** `@permission_required('medical.view_locclassification')`
* **Mô tả:** Lấy thông tin gợi ý LOC hiện tại dựa trên điểm ADL của Assessment, kèm tỷ giá từ `LOCRate` và lịch sử xác nhận.
* **Response (200 OK):**
```json
{
    "assessment_id": 1,
    "total_adl_score": 20,
    "breakdown": [...],
    "suggested_loc": "Level 3",
    "loc_rate": 248.00,
    "status": "Pending",
    "final_loc": null,
    "history": []
}
```

### 2.2 POST `/confirm/` (Xác nhận LOC)
* **Quyền hạn:** `@permission_required('medical.change_locclassification')`
* **Mô tả:** Xác nhận mức LOC do hệ thống gợi ý. Kích hoạt **BR-05 Chart Lock**.
* **Payload:** Không cần (lấy gợi ý hiện hành).
* **Luật xử lý:**
  - Nếu `status == 'Confirmed'`, trả về lỗi `400 Bad Request` (Đã khóa).
  - Cập nhật `final_loc = suggested_loc`, `status = 'Confirmed'`, `confirmed_by = request.user`.
  - Ghi 1 bản ghi vào `LOCClassificationHistory`.

### 2.3 POST `/override/` (Ghi đè LOC)
* **Quyền hạn:** `@permission_required('medical.change_locclassification')`
* **Mô tả:** Chọn một mức LOC khác, kích hoạt **BR-05 Chart Lock**.
* **Payload:**
```json
{
    "override_loc": "Level 4",
    "override_reason": "Bệnh nhân cần hỗ trợ nhiều hơn do biến chứng."
}
```
* **Luật xử lý:**
  - Bắt buộc có `override_reason` (Nếu rỗng trả về `400 Bad Request`).
  - Nếu `status == 'Confirmed'`, trả về lỗi `400 Bad Request` (Đã khóa).
  - Cập nhật `final_loc = override_loc`, `is_overridden = True`, `override_reason = ...`, `status = 'Confirmed'`.
  - Ghi log vào `LOCClassificationHistory`.

---

## 3. UI/UX Component & Template Structure (Tùy chọn)
* Sử dụng thẻ `disabled` hoặc `read-only` trên các nút Confirm/Override nếu User không có quyền, hoặc nếu `status == 'Confirmed'`.
* Modal Override sử dụng form để nhập lý do (thẻ `<textarea required>`).
