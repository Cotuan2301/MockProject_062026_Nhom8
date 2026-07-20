⚙️ Cài đặt thêm thư viện:

- pip install python-dotenv (Đọc file .env)
- pip freeze > requirements.txt (Tự động ghi các phiên bản thư viện vào file requirements.txt)

---
**Lưu ý về Tính năng e-Signature & Upload (Step 2 - Admission Form):**
- Tính năng Ký điện tử được xây dựng **100% bằng HTML5 Canvas và Vanilla Javascript thuần**, hoàn toàn không sử dụng hay cài đặt thêm bất kỳ thư viện ngoài (như SignaturePad.js) hay package `pip` nào.
- Tuy nhiên, vì Database có sự thay đổi (thêm các cột `verification_method`, `consent_signature`, `consent_file` vào bảng `Admission`), nên khi clone code về máy khác, bạn **bắt buộc phải chạy lệnh Migration**:
  `python manage.py migrate`
