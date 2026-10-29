# Changelog

## 1.1.0 — 2026-10-29 (đã cập nhật trên main)

- **Trạng thái:** mã nguồn và tài liệu đã được gộp vào `main` ngày 29/10/2026 qua [PR #1](https://github.com/diginno-net/opc-vn-business-law/pull/1). Chưa tạo tag/GitHub Release 1.1.0; gói tải trong Releases vẫn là 1.0.2. Dùng repo `main` để lấy bản cập nhật này.
- **Mốc kiểm chứng pháp lý:** 28/10/2026, không phải ngày merge; chỉ rà soát trong phạm vi thuế/kế toán nêu dưới đây.

- **Đính chính:** ví dụ 8 tỷ cũ dùng 20% mặc định; phép tính 17% là 204 triệu và biên hòa vốn 8,82% **trước miễn/giảm**, không xác nhận doanh nghiệp được dùng phương pháp % doanh thu. Sửa chiều kết luận hòa vốn trong tài liệu.
- CLI mặc định `danh-gia`, tách doanh thu kỳ hiện tại với doanh thu căn cứ năm trước; không kết luận khi thiếu dữ kiện/ngoại lệ. Sàng lọc điều kiện % doanh thu <=3 tỷ, khả năng xác định chi phí/thu nhập và nhánh kiểm miễn <=1 tỷ.
- **Thay đổi tương thích:** mô phỏng phải ghi `--che-do mo-phong` cùng hai tỷ lệ tường minh. Chỉ nhận phân số thập phân (0.015, 0.17); bỏ cách nhập 1.5 và hai giá trị mặc định. Giữ `--loi-nhuan` làm alias cho `--thu-nhap-tinh-thue` giả định.
- Chặn đầu vào/kết quả NaN/Infinity; không gắn phương pháp TNDN với quyền khấu trừ GTGT. Không tự tính số thực nộp sau ưu đãi; cảnh báo NQ43/2026 và phần hướng dẫn chưa xác minh.
- Bổ sung TT99, phạm vi/lựa chọn TT133 và kỳ áp dụng TT58. Sửa thông tin môn bài từ 2026, lương chủ TNHH MTV cá nhân và thu nhập sau hoàn thành nghĩa vụ TNDN.
- Thêm regression test stdlib, eval CLI tự động và rubric câu trả lời có cơ chế nhận điểm/bằng chứng; không coi test số học là benchmark tư vấn pháp lý.
- Phạm vi rà soát pháp lý **một phần** ngày 28/10; không tuyên bố cập nhật toàn bộ luật, hiệu lực TT133 hoặc nghị định hướng dẫn NQ43 cuối cùng.
- Đóng gói theo danh sách nguồn công khai, không di chuyển `.git` hay xóa cả `dist`; ZIP đầy đủ có test/eval, `.skill` chỉ chứa runtime/tài liệu cài agent.
- Kiểm bổ sung theo legal-docs-vn: tải đủ 10 phần TT99; kiểm hình TT46 Điều 3/7 sửa Điều 10 TT133; bổ sung TT58 Điều 11 chuyển số dư. Không biến việc chưa tìm được hướng dẫn riêng năm dương lịch 2026 thành khẳng định không có quy tắc chuyển sổ.

## 1.0.2 — 2026-10-18

- Cập nhật link repo public (`diginno-net/opc-vn-business-law`) trong README.
- Không thay đổi nội dung pháp lý.


## 1.0.1 — 2026-10-17

- Đối chiếu OCR 27 trang văn bản gốc: khớp 99,7%, không thiếu trang, không có dữ liệu nhạy cảm.
- Bổ sung `references/02-draft-sme-law-2026.md`: tiêu chí DNNVV (Điều 4), bảng đủ 12 khoản Điều 20, Điều 33–35.
- Không thay đổi kết luận pháp lý; chỉ bổ sung độ phủ.


## 1.0.0 — 2026-10-17

Bản phát hành đầu tiên.

- Skill `opc-vn-business-law`: cẩm nang pháp lý – thuế – kế toán cho doanh nghiệp một người tại Việt Nam.
- 9 tài liệu tham khảo: trạng thái pháp lý, mô hình kinh doanh, dự thảo Luật Phát triển DNNVV 2026, quản trị TNHH MTV, kế toán siêu nhỏ, thuế, playbook chuyển đổi, rủi ro, nguồn.
- Bộ công cụ: checklist chuyển đổi, mẫu điều lệ tối giản, bộ câu hỏi tư vấn 30 phút.
- Script `so_sanh_thue.py` (thuế % doanh thu vs kê khai) + self-test.
- Disclaimer tiếng Việt và tiếng Anh; giấy phép CC BY 4.0 (nội dung) + MIT (script).
- Bộ eval gợi ý cho kiểm thử skill.
- `PROMO.md`: mời cộng đồng (2 nhóm Facebook + YouTube) và CTA dịch vụ Training AI 1:1.
- `scripts/audit_public.sh`: quét secret/PII/đường dẫn và kiểm tra bên trong gói.
- `scripts/package_skill.sh`: đóng gói `.skill` sạch (loại `.git`, `launch/`, `evals/`).
- Phạm vi quảng cáo đợt này: chỉ nhóm Tự động hóa cho bớt việc; nhóm OpenCode để dành cho nội dung build agent/skill.

Nguồn chính: Cổng thông tin Quốc hội (duthaoonline.quochoi.vn), Công báo Chính phủ, Luật Doanh nghiệp 2020, Luật Kế toán 2015, Nghị định 174/2016/NĐ-CP, Thông tư 58/2026/TT-BTC, Nghị định 80/2021/NĐ-CP, Luật Thuế TNDN 67/2025/QH15.

Mốc dữ liệu: 17/10/2026.
