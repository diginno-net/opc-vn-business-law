# 08 — Nguồn chính thức và quy trình cập nhật

## Nguồn nên tra

| Mục đích | Địa chỉ | Ghi chú |
|---|---|---|
| Văn bản pháp luật đang hiệu lực | https://vbpl.vn | Cơ sở dữ liệu quốc gia về pháp luật (Bộ Tư pháp) |
| Bản gốc, công báo | https://vanban.chinhphu.vn | PDF/DOC gốc, số công báo |
| Dự thảo luật | https://duthaoonline.quochoi.vn | Trạng thái, lần dự thảo, toàn văn |
| Chính sách, tin chính thống | https://xaydungchinhsach.chinhphu.vn | Giải thích chính sách mới |
| Thuế | https://gdt.gov.vn · https://mof.gov.vn | Văn bản thuế, hướng dẫn kê khai |
| Đăng ký doanh nghiệp | https://dangkykinhdoanh.gov.vn | Hồ sơ, biểu mẫu, tra cứu |
| Bảo hiểm xã hội | https://baohiemxahoi.gov.vn | Biểu mẫu, lịch đóng |
| Chứng khoán (nếu là CTCP đại chúng) | https://ssc.gov.vn | Báo cáo, công bố thông tin |

## Quy trình kiểm chứng một điều luật

1. Tra **số hiệu** trên `vbpl.vn` → xem "Hiệu lực hiện tại", "Văn bản sửa đổi, bổ sung".
2. Mở bản gốc trên `vanban.chinhphu.vn` → đối chiếu **điều, khoản, điểm**.
3. Kiểm tra **ngày ban hành vs ngày hiệu lực**.
4. Nếu là dự thảo: xem `duthaoonline.quochoi.vn` → xác định **lần dự thảo** và ngày.
5. Ghi nguồn + ngày truy cập vào câu trả lời.

## Quy trình cập nhật skill

Khi có văn bản mới:

1. Cập nhật `references/00-legal-status.md` (bảng trạng thái là nguồn sự thật).
2. Sửa file chuyên đề bị ảnh hưởng (`01`–`07`).
3. Cập nhật `CHANGELOG.md`, tăng `version` trong `SKILL.md` (semver).
4. Chạy kiểm tra:
   ```bash
   python3 scripts/so_sanh_thue.py --self-test
   ```
5. Kiểm tra link trong file này (không có link chết).
6. Nếu thay đổi lớn: cập nhật `evals/evals.json` và chạy lại thử nghiệm.

## Lịch rà soát đề xuất

| Tần suất | Việc |
|---|---|
| Hàng tháng | Tin thuế mới, thông tư, nghị định |
| Hàng quý | Dự thảo luật, tiến trình Quốc hội |
| 6 tháng | Rà soát toàn bộ `00-legal-status.md`, kiểm tra link |
| Khi có luật mới | Cập nhật ngay, tăng version |

## Ghi công và giấy phép

- Nội dung: **CC BY 4.0** — được dùng, sửa, chia sẻ, kể cả thương mại, với điều kiện ghi công "Diginno — opc-vn-business-law" và giữ disclaimer.
- Script: **MIT**.
- Chi tiết: `LICENSE`.

## Miễn trừ trách nhiệm

Xem `DISCLAIMER.md`. Nội dung trong skill này là thông tin tham khảo, không phải tư vấn pháp lý/thuế/kế toán, không tạo quan hệ luật sư – khách hàng, không bảo đảm tính đầy đủ hoặc cập nhật. Người dùng tự chịu trách nhiệm với quyết định của mình.
