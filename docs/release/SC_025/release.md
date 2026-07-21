# Release Note - SC_025 LOC History

## Tổng quan
Ticket **SC_025** hoàn thành việc hiển thị lịch sử thay đổi mức độ chăm sóc (Level of Care - LOC) của cư dân, giúp phục vụ cho việc kiểm toán và theo dõi.

## Các tính năng (Features)
- Thêm màn hình danh sách lịch sử LOC tại Resident Profile -> Tab LOC.
- Hỗ trợ hiển thị rõ thao tác (Confirmed/Overridden), trạng thái trước và sau khi thay đổi, người thực hiện và ghi chú.
- Thêm API xuất danh sách lịch sử LOC ra file CSV (`/api/medical/residents/<id>/loc-history/export/`).
- Đã được unit test bao phủ (coverage).

## Known Issues / Limitations
- File export hiện tại sử dụng định dạng CSV. Nếu người dùng yêu cầu khắt khe về format đẹp, sẽ cần cập nhật thư viện PDF generation trong tương lai.
- UI mockups đang tạm link cứng (placeholder) ở các tab chưa phát triển.

## Checklist
- [x] Đã migrate database.
- [x] Đã hoàn thiện giao diện người dùng theo thiết kế.
- [x] Đã viết testcase và chạy pass.
