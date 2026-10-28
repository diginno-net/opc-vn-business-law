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

Chạy từ **repo clone hoặc gói ZIP đầy đủ**. Gói `.skill` chỉ để cài agent, không chứa bộ eval/kiểm thử phát triển.

```bash
python3 scripts/so_sanh_thue.py --self-test
python3 -m unittest discover -s tests -v
python3 scripts/run_evals.py
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

## Tính thuế: kiểm điều kiện trước, mô phỏng sau

Từ **1.1.0**, CLI mặc định sàng lọc điều kiện, không còn tự dùng 1,5%/20%. Đây là thay đổi giao diện có chủ đích để tránh trả số sai khi thiếu dữ kiện. Phạm vi đánh giá: doanh nghiệp thành lập theo pháp luật Việt Nam, kỳ 2026; không phải công cụ tính thuế hộ kinh doanh hoặc quyết toán tự động.

```bash
# Chỉ có doanh thu/lợi nhuận: trả thiếu dữ kiện, không kết luận chọn cách nộp.
python3 scripts/so_sanh_thue.py --doanh-thu 8e9 --loi-nhuan 1.2e9 --json

# Sàng lọc: doanh thu căn cứ là năm trước đã xác định/quy đổi đúng NĐ320.
python3 scripts/so_sanh_thue.py --doanh-thu 8e9 --doanh-thu-can-cu 8e9 \
  --nganh dich-vu --xac-dinh-chi-phi khong --ngoai-le khong --json
# Không đạt nhánh % doanh thu <=3 tỷ; không sinh bảng chọn phương pháp.

# Phép tính giả định thuần túy, không chứng minh quyền áp dụng hay số thực nộp:
python3 scripts/so_sanh_thue.py --che-do mo-phong --doanh-thu 8e9 \
  --thu-nhap-tinh-thue 1.2e9 --ty-le 0.015 --thue-suat 0.17 --json
# 120 triệu so với 204 triệu trước miễn/giảm; biên hòa vốn 8,82%.
```

- Tỷ lệ nhập **thập phân duy nhất**: 1,5% → `0.015`, 17% → `0.17`; cách nhập cũ `1.5` bị từ chối, không đoán định dạng.
- `--thu-nhap-tinh-thue` là thu nhập **giả định** trước ưu đãi; `--loi-nhuan` là alias tương thích, không tự chuyển lợi nhuận kế toán thành căn cứ thuế.
- Cần biết ngành, doanh thu căn cứ, khả năng xác định chi phí/thu nhập và ngoại lệ. Doanh nghiệp mới/chưa loại trừ ngoại lệ phải kiểm riêng, không tự gán thuế suất.
- Có nhánh kiểm miễn ngưỡng 1 tỷ và cảnh báo giảm số thuế theo NQ43/2026; **chưa tính miễn/giảm**, chưa xác minh đầy đủ nghị định hướng dẫn cuối cùng. 204 triệu không phải cam kết số thực nộp.
- GTGT được đánh giá độc lập với TNDN. Chọn TT58/TT133/TT99 cũng không tự tạo quyền chọn phương pháp thuế.

Xem `references/05-tax.md` về nguồn/điều kiện, `evals/README.md` về cách chấm. Unit test và eval CLI chạy tự động; rubric câu trả lời cần người hoặc mô hình chấm bằng chứng, không suy test script xanh thành tư vấn pháp lý đúng toàn diện.

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

- **Thuế/kế toán rà soát một phần ngày 28/10/2026**; không phải xác nhận hiệu lực toàn bộ tài liệu. Nội dung mô hình/quản trị/dự thảo khác giữ mốc 17/10/2026 và phải kiểm lại trước dùng.
- Dự thảo Luật Phát triển DNNVV: **chưa phải luật theo hồ sơ 17/10**, dự kiến hiệu lực 01/7/2027; cần kiểm tiến trình mới trước trích dẫn.
- TT58/2026: hiệu lực 01/7/2026, áp dụng năm tài chính bắt đầu từ/sau ngày đó. TT99/2025: hiệu lực 01/01/2026; DNNVV có quyền lựa chọn, không mặc nhiên thay TT133.
- Đã kiểm trực quan TT46 Điều 3 sửa Điều 10 TT133 và TT99 Điều 2/31; chưa khóa toàn bộ chuỗi sửa đổi trên VBPL hoặc nghị định hướng dẫn NQ43 cuối cùng. Xem giới hạn tại `references/00-legal-status.md` và `references/08-sources.md`.
- Kiểm văn bản hiện hành ở mỗi lần tư vấn thuế; không chờ hết 6 tháng mới kiểm.

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
3. Chạy đủ ba lệnh ở mục **Kiểm tra**; với câu trả lời skill, chấm rubric riêng theo hướng dẫn eval.
4. Mở pull request mô tả văn bản/nguồn thay đổi.

## Phiên bản

- **1.1.0** — 28/10/2026 — bản sửa local: kiểm điều kiện thuế trước mô phỏng, bỏ mặc định tỷ lệ, bổ sung TT99 và nguồn miễn/giảm 2026, regression test và rubric. Chưa phát hành release.
- **1.0.2** — 18/10/2026 — cập nhật link repo public, giữ nguyên nội dung pháp lý.
- **1.0.1** — 17/10/2026 — bổ sung Điều 4, đủ 12 khoản Điều 20, Điều 33–35 sau đối chiếu OCR.
- **1.0.0** — 17/10/2026 — bản đầu tiên.
