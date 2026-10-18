# OPC VN Business Law

**Skill tham khảo pháp lý – thuế – kế toán cho doanh nghiệp một người tại Việt Nam.**

Dành cho chủ hộ kinh doanh, freelancer, người mới thành lập công ty, kế toán dịch vụ và consultant — những người cần trả lời nhanh:

- Nên kinh doanh dưới mô hình nào?
- Chuyển hộ kinh doanh lên công ty cần gì?
- Có bắt buộc Chủ tịch công ty, kế toán trưởng không?
- Dự thảo Luật Phát triển DNNVV 2026 có gì mới, đã áp dụng được chưa?
- Chọn thuế theo % doanh thu hay kê khai?

> ⚠️ **Đây là tài liệu tham khảo, không phải tư vấn pháp lý.** Đọc `DISCLAIMER.md` trước khi dùng. Luôn kiểm tra văn bản gốc và hỏi luật sư/kế toán hành nghề trước khi quyết định.

---

## Nội dung

| File | Nội dung |
|---|---|
| `SKILL.md` | Hướng dẫn cho AI: quy trình, nguyên tắc, mẫu câu trả lời, disclaimer |
| `references/00-legal-status.md` | **Nguồn sự thật** về văn bản nào đang hiệu lực, văn bản nào là dự thảo |
| `references/01-entity-models.md` | So sánh hộ kinh doanh, DNTN, TNHH MTV, TNHH 2TV, cổ phần |
| `references/02-draft-sme-law-2026.md` | Dự thảo Luật Phát triển DNNVV 2026, Điều 20 khoản 8 |
| `references/03-governance-tnhh-mtv.md` | Chủ tịch công ty, Giám đốc, người đại diện, điều lệ |
| `references/04-accounting.md` | Kế toán trưởng, Thông tư 58/2026, chế độ kế toán siêu nhỏ |
| `references/05-tax.md` | Thuế TNDN/GTGT, chọn phương pháp, lịch kê khai |
| `references/06-conversion-playbook.md` | 12 bước chuyển đổi hộ kinh doanh |
| `references/07-risk-and-red-flags.md` | Rủi ro, cờ đỏ, khi nào chuyển luật sư |
| `references/08-sources.md` | Nguồn chính thức, quy trình cập nhật |
| `assets/` | Checklist, mẫu điều lệ, bộ câu hỏi tư vấn |
| `scripts/so_sanh_thue.py` | Tính nhanh thuế % doanh thu vs kê khai |
| `evals/evals.json` | Bộ kiểm thử gợi ý cho skill |

## Cài đặt

### Cách 1 — Copy thư mục

Sao chép thư mục này vào nơi agent đọc skill:

| Agent | Thư mục |
|---|---|
| Claude Code | `~/.claude/skills/opc-vn-business-law/` |
| Codex | `~/.codex/skills/opc-vn-business-law/` |
| OpenCode | `~/.config/opencode/skills/opc-vn-business-law/` |
| Harness khác | thư mục `skills/` của harness đó |

Giữ nguyên cấu trúc thư mục (SKILL.md phải nằm ở gốc).

### Cách 2 — Clone từ Git

```bash
git clone https://github.com/diginno-net/opc-vn-business-law.git ~/.claude/skills/opc-vn-business-law
```

> Repo: https://github.com/diginno-net/opc-vn-business-law

### Kiểm tra

```bash
python3 scripts/so_sanh_thue.py --self-test
```

## Cách dùng

Nói với agent bằng ngôn ngữ tự nhiên:

- "Tôi đang là hộ kinh doanh bán hàng online, doanh thu 6 tỷ/năm. Có nên lên công ty TNHH một thành viên?"
- "Công ty TNHH một thành viên có bắt buộc Chủ tịch công ty không?"
- "Doanh nghiệp siêu nhỏ có cần kế toán trưởng không?"
- "Dự thảo Luật Phát triển DNNVV 2026 có gì mới về doanh nghiệp một người?"
- "So sánh giúp tôi thuế theo % doanh thu và kê khai, doanh thu 8 tỷ, lợi nhuận 1,2 tỷ."
- "Soạn checklist chuyển đổi hộ kinh doanh lên công ty cho tôi."

Agent sẽ đọc `SKILL.md`, mở file chuyên đề tương ứng, và trả lời theo mẫu có disclaimer.

## Cộng đồng & dịch vụ

- **Tự động hóa cho bớt việc** — nhóm Facebook cho chủ doanh nghiệp/vận hành: https://www.facebook.com/groups/tudonghoachobotviec/
- **OpenCode VN** — nhóm Facebook cho người build agent/skill: https://www.facebook.com/groups/opencode.io.vn/
- **YouTube**: https://www.youtube.com/@nguyenngothuong
- **Training AI 1:1 cho doanh nghiệp** — làm trên quy trình thật, bàn giao workflow chạy được. Chi tiết: [PROMO.md](PROMO.md).

Nội dung pháp lý/kinh doanh đăng chủ yếu ở nhóm Tự động hóa; nhóm OpenCode dành cho build agent/skill.

## Phạm vi

**Có:** chọn mô hình, chuyển đổi, quản trị công ty một người, kế toán siêu nhỏ, thuế cơ bản, checklist hồ sơ, dự thảo luật 2026.

**Không:** tranh chấp, tố tụng, M&A, đầu tư nước ngoài, phá sản, ngành nghề có điều kiện phức tạp, tối ưu thuế xuyên biên giới. Những việc này cần luật sư/kế toán hành nghề.

## Trạng thái dữ liệu

- Mốc cập nhật: **17/10/2026**.
- Dự thảo Luật Phát triển DNNVV: **chưa phải luật**, dự kiến hiệu lực 01/7/2027.
- Thông tư 58/2026/TT-BTC: đã có hiệu lực từ 01/7/2026.
- Sau 6 tháng, kiểm tra lại `references/00-legal-status.md` và nguồn chính thức.

## Miễn trừ trách nhiệm (tóm tắt)

Nội dung là thông tin tham khảo, không phải tư vấn pháp lý/thuế/kế toán, không tạo quan hệ luật sư – khách hàng, không bảo đảm tính đầy đủ hoặc cập nhật. Người dùng tự chịu trách nhiệm với quyết định của mình. Tác giả và Diginno loại trừ trách nhiệm trong phạm vi pháp luật cho phép. Xem `DISCLAIMER.md`.

## Giấy phép

- Nội dung: **CC BY 4.0** — dùng, sửa, chia sẻ, kể cả thương mại, với điều kiện ghi công và giữ disclaimer.
- Script: **MIT**.

Ghi công đề xuất:

> Dựa trên skill `opc-vn-business-law` của Diginno (CC BY 4.0).

## Đóng góp

1. Kiểm tra `references/00-legal-status.md` trước khi sửa.
2. Cập nhật file chuyên đề + `CHANGELOG.md` + `version`.
3. Chạy `python3 scripts/so_sanh_thue.py --self-test`.
4. Mở pull request mô tả văn bản/nguồn thay đổi.

## Phiên bản

- **1.0.2** — 18/10/2026 — cập nhật link repo public, giữ nguyên nội dung pháp lý.
- **1.0.1** — 17/10/2026 — bổ sung Điều 4, đủ 12 khoản Điều 20, Điều 33–35 sau đối chiếu OCR.
- **1.0.0** — 17/10/2026 — bản đầu tiên.
