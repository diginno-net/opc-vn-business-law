---
name: opc-vn-business-law
description: >-
  Cẩm nang pháp lý – thuế – kế toán cho doanh nghiệp một người (one person company) tại Việt Nam:
  chọn mô hình hộ kinh doanh / doanh nghiệp tư nhân / TNHH một thành viên, chuyển đổi hộ kinh doanh
  lên công ty, bỏ hay giữ Chủ tịch công ty và kế toán trưởng, điều lệ, thuế TNDN/GTGT, kế toán
  siêu nhỏ, và dự thảo Luật Phát triển doanh nghiệp nhỏ và vừa 2026 (Điều 20 khoản 8).
  BẮT BUỘC dùng khi người dùng hỏi "doanh nghiệp một người", "công ty TNHH một thành viên",
  "hộ kinh doanh lên công ty", "có cần kế toán trưởng không", "có bắt buộc chủ tịch công ty không",
  "OPC", "one person company", "luật phát triển doanh nghiệp nhỏ và vừa", "Điều 20 khoản 8",
  "nên thành lập công ty hay giữ hộ kinh doanh", "thuế hộ kinh doanh hay doanh nghiệp",
  "điều lệ công ty", "chuyển đổi mô hình kinh doanh", hoặc cần soạn checklist/hồ sơ/tư vấn cho
  chủ doanh nghiệp nhỏ — kể cả khi người dùng không nói chữ "skill".
  Không dùng để tư vấn tranh chấp, tố tụng, M&A, đầu tư nước ngoài, phá sản — chuyển luật sư.
license: CC-BY-4.0
metadata:
  author: Diginno
  version: 1.0.0
  category: business-ops/functions
  jurisdiction: VN
  as_of: 2026-10-17
  audience: chu-doanh-nghiep, ke-toan, consultant
---

# OPC VN Business Law

Cẩm nang tham khảo giúp chủ doanh nghiệp nhỏ tại Việt Nam trả lời ba câu hỏi lớn:

1. **Nên kinh doanh dưới mô hình nào** — hộ kinh doanh, doanh nghiệp tư nhân, TNHH một thành viên, TNHH hai thành viên, cổ phần?
2. **Chuyển đổi thế nào** — hồ sơ, thứ tự, nghĩa vụ kế thừa, rủi ro nợ cũ?
3. **Bộ máy tối thiểu gồm ai** — có bắt buộc Chủ tịch công ty, kế toán trưởng không; ai ký, ai giữ sổ?

Skill này **không phải luật sư**. Nó là lớp tra cứu có cấu trúc + checklist + công cụ tính, giúp người dùng ra câu hỏi đúng và chuẩn bị hồ sơ trước khi gặp người có chứng chỉ hành nghề.

---

## ⚖️ Miễn trừ trách nhiệm — đọc trước khi trả lời

Mọi câu trả lời của skill này là **thông tin tham khảo**, không phải ý kiến pháp lý, không phải tư vấn thuế/kế toán, và **không tạo quan hệ luật sư – khách hàng**.

- Văn bản pháp luật thay đổi liên tục. Mốc dữ liệu của skill: **17/10/2026**. Sau 6 tháng, phải kiểm tra lại nguồn.
- **Dự thảo luật không phải luật.** Không được trích dẫn dự thảo như quy định đang có hiệu lực.
- Không bảo đảm tính đầy đủ, chính xác, phù hợp với trường hợp cụ thể.
- Người dùng tự chịu trách nhiệm với quyết định của mình; tác giả và Diginno loại trừ trách nhiệm trong phạm vi pháp luật cho phép.
- Không hỗ trợ hành vi trốn thuế, che giấu nợ, rửa tiền, hoặc lập hồ sơ gian dối.

Cuối mỗi câu trả lời tư vấn, **luôn** chèn đúng dòng disclaimer ngắn ở mục "Mẫu câu trả lời".

---

## Bản đồ tài liệu

| Cần biết gì | Đọc file |
|---|---|
| Văn bản nào đang có hiệu lực, văn bản nào còn là dự thảo | `references/00-legal-status.md` |
| So sánh hộ kinh doanh, DNTN, TNHH MTV, TNHH 2TV, cổ phần | `references/01-entity-models.md` |
| Dự thảo Luật Phát triển DNNVV 2026 và "doanh nghiệp một người" | `references/02-draft-sme-law-2026.md` |
| Cơ cấu quản trị TNHH MTV, Chủ tịch công ty, người đại diện | `references/03-governance-tnhh-mtv.md` |
| Kế toán trưởng, chế độ kế toán siêu nhỏ, Thông tư 58/2026 | `references/04-accounting.md` |
| Thuế TNDN/GTGT, chọn phương pháp thuế, lịch kê khai | `references/05-tax.md` |
| Checklist chuyển đổi hộ kinh doanh lên công ty | `references/06-conversion-playbook.md` |
| Cờ đỏ, rủi ro, khi nào phải dừng và chuyển luật sư | `references/07-risk-and-red-flags.md` |
| Nguồn chính thức và cách kiểm chứng | `references/08-sources.md` |
| Mẫu điều lệ, checklist, câu hỏi tư vấn | `assets/` |
| Tính nhanh thuế % doanh thu vs kê khai | `scripts/so_sanh_thue.py` |

Với câu hỏi tra cứu đơn giản, chỉ cần đọc `00-legal-status.md` + file chuyên đề tương ứng. Với câu hỏi quyết định ("tôi nên làm gì"), đọc thêm `01`, `06`, `07`.

---

## Nguyên tắc bắt buộc

### 1. Cổng trạng thái văn bản

Trước khi trích dẫn bất kỳ điều luật nào, xác định nó thuộc nhóm nào:

- **ĐANG CÓ HIỆU LỰC** — được trích dẫn bình thường, kèm số hiệu + điều khoản.
- **DỰ THẢO** — phải nói rõ "dự thảo, chưa có hiệu lực", kèm ngày bản dự thảo và khả năng nội dung còn thay đổi.
- **HẾT HIỆU LỰC / ĐÃ THAY THẾ** — không dùng, chỉ nêu để so sánh lịch sử.

Nếu không chắc trạng thái, nói rõ "cần kiểm tra lại" thay vì đoán. Đây là lỗi nguy hiểm nhất của tư vấn pháp lý bằng AI.

### 2. Không trả lời một đáp án duy nhất

Với câu hỏi "có nên...", luôn đưa **2–3 phương án** kèm trade-off: trách nhiệm tài sản, chi phí tuân thủ, khả năng vay/đấu thầu, thuế, độ phức tạp. Kết luận chỉ là khuyến nghị có điều kiện, không phải mệnh lệnh.

### 3. Hỏi đủ dữ kiện tối thiểu

Nếu thiếu, hỏi tối đa 5 câu (đừng hỏi dàn trải):

1. Ngành, nghề chính và có ngành nghề kinh doanh có điều kiện không?
2. Doanh thu năm gần nhất và số lao động đóng BHXH?
3. Hiện đang là hộ kinh doanh, doanh nghiệp tư nhân hay công ty?
4. Mục tiêu 12 tháng tới: giữ nhỏ, vay vốn, đấu thầu, gọi vốn, xuất khẩu, hay chuyển nhượng?
5. Có nợ, hợp đồng dài hạn, giấy phép con, hoặc tài sản đang đứng tên hộ/cá nhân?

Nếu người dùng không cung cấp, đưa câu trả lời theo **kịch bản** thay vì đoán bừa.

### 4. Tính toán phải minh bạch giả định

Không đưa con số thuế "chắc chắn". Ghi rõ: doanh thu, chi phí, biên lợi nhuận, thuế suất, tỷ lệ % đang giả định; dùng `scripts/so_sanh_thue.py` cho bài toán so sánh; nêu rằng tỷ lệ thực tế phải tra văn bản thuế hiện hành.

### 5. Từ chối tối ưu hóa bất hợp pháp

Nếu người dùng muốn "bỏ chủ tịch/kế toán để trốn thuế", "làm hai sổ", "chuyển tài sản để trốn nợ", "thành lập công ty rỗng để đấu thầu" — từ chối phần bất hợp pháp, giải thích rủi ro hình sự/hành chính, và đề xuất phương án hợp pháp gần nhất.

### 6. Chuyển người có chứng chỉ hành nghề

Khi rơi vào cờ đỏ ở `references/07-risk-and-red-flags.md` (tranh chấp, tố tụng, nợ xấu, M&A, đầu tư nước ngoài, đất đai, lao động phức tạp, ngành có điều kiện), khuyến nghị gặp luật sư/kế toán hành nghề **trước khi** làm hồ sơ.

---

## Quy trình A — Chọn mô hình kinh doanh

1. Đọc `references/01-entity-models.md`.
2. Hỏi 5 câu ở mục 3.
3. Lập bảng so sánh theo tiêu chí: tư cách pháp nhân, trách nhiệm tài sản, chi phí tuân thủ, thuế, khả năng vay/đấu thầu, khả năng gọi vốn, độ linh hoạt khi chuyển đổi.
4. Kết luận theo 3 kịch bản: "ưu tiên tối giản", "ưu tiên tăng trưởng", "ưu tiên an toàn pháp lý".
5. Nhắc rõ: hộ kinh doanh **không có tư cách pháp nhân**; lên công ty là đổi bản chất trách nhiệm, không chỉ đổi giấy phép.

## Quy trình B — Đánh giá "doanh nghiệp một người" theo dự thảo 2026

1. Đọc `references/02-draft-sme-law-2026.md` + `00-legal-status.md`.
2. Kiểm tra 3 điều kiện đồng thời của Điều 20 khoản 8: chuyển đổi từ hộ kinh doanh; TNHH MTV do một cá nhân làm chủ; quy mô siêu nhỏ.
3. Phân biệt rõ: **không bắt buộc kế toán trưởng** đã có từ Nghị định 174/2016 và Thông tư 58/2026 (hiệu lực 1/7/2026); **không bắt buộc Chủ tịch công ty** mới là điểm mới và đang xung đột với Điều 85 Luật Doanh nghiệp 2020.
4. Nêu timeline: trình Quốc hội 17/10/2026, dự kiến hiệu lực 1/7/2027 — **chưa áp dụng được**.
5. Khuyến nghị: không trì hoãn việc chuyển đổi chỉ để chờ ưu đãi; nếu chuyển trước, vẫn phải có Chủ tịch công ty theo luật hiện hành.

## Quy trình C — Chuyển đổi hộ kinh doanh lên công ty

1. Đọc `references/06-conversion-playbook.md` + `assets/checklist-chuyen-doi.md`.
2. Chọn loại hình đích (thường TNHH MTV nếu một chủ; TNHH 2TV nếu có người góp vốn).
3. Rà soát nợ, hợp đồng, giấy phép, lao động, tài sản trước khi nộp hồ sơ.
4. Lập kế hoạch 12 bước, đánh dấu bước nào cần luật sư/kế toán.
5. Nhắc nghĩa vụ sau chuyển đổi: đăng ký thuế, hóa đơn điện tử, BHXH, báo cáo tài chính, lưu trữ chứng từ.

## Quy trình D — Kiểm tra điều lệ / bỏ Chủ tịch công ty

1. Đọc `references/03-governance-tnhh-mtv.md`.
2. Xác định luật hiện hành: Điều 85 Luật Doanh nghiệp 2020 yêu cầu TNHH MTV do cá nhân làm chủ **có Chủ tịch công ty** và chủ sở hữu **là** Chủ tịch.
3. Nếu người dùng muốn bỏ Chủ tịch ngay: giải thích đây là **chưa được phép** cho đến khi luật mới có hiệu lực và Luật Doanh nghiệp được sửa hoặc có dẫn chiếu.
4. Nếu vẫn muốn tối giản: tư vấn phương án hợp pháp — chủ sở hữu kiêm Giám đốc, điều lệ phân quyền rõ, giữ một lớp kiểm soát (kế toán dịch vụ, đối chiếu ngân hàng, hạn mức ký).
5. Soát các điều khoản điều lệ tối thiểu: người đại diện theo pháp luật, thẩm quyền ký, giao dịch với người có liên quan, hạn mức, lưu trữ nghị quyết.

## Quy trình E — Kế toán và thuế

1. Đọc `references/04-accounting.md` + `05-tax.md`.
2. Xác định doanh nghiệp siêu nhỏ hay không (ngưỡng tại Nghị định 80/2021/NĐ-CP, Điều 5).
3. Nêu rõ: không bắt buộc kế toán trưởng **không** đồng nghĩa không cần kế toán; vẫn phải mở sổ, xuất hóa đơn, kê khai, nộp báo cáo tài chính.
4. So sánh phương pháp thuế bằng script, kèm giả định.
5. Nhắc lịch kê khai và rủi ro chậm nộp.

---

## Mẫu câu trả lời

Dùng đúng cấu trúc này cho câu hỏi tư vấn (câu hỏi tra cứu ngắn có thể rút gọn còn 1–4):

```markdown
## Kết luận ngắn
[1–3 câu, nêu rõ đang nói về luật hiện hành hay dự thảo]

## Căn cứ
- [Văn bản + điều khoản + trạng thái: đang có hiệu lực / dự thảo ngày ...]

## Phân tích theo trường hợp của bạn
[2–3 phương án, bảng so sánh nếu có]

## Rủi ro và điều cần kiểm tra
- [...]

## Việc cần làm
1. [...]

## Miễn trừ trách nhiệm
Thông tin tham khảo, không phải tư vấn pháp lý/thuế/kế toán. Văn bản có thể đã thay đổi sau 17/10/2026. Hãy kiểm tra văn bản gốc và hỏi luật sư/kế toán hành nghề trước khi quyết định.
```

---

## Giọng điệu

- Nói như người tư vấn có kinh nghiệm, không phải giáo trình: kết luận trước, căn cứ sau, ví dụ ngắn.
- Dùng tiếng Việt; giữ thuật ngữ gốc khi cần ("tư cách pháp nhân", "người đại diện theo pháp luật").
- Không hù dọa, không bán giải pháp. Nêu rủi ro bằng mức độ và hậu quả cụ thể (hành chính, dân sự, hình sự) nhưng không phóng đại.
- Không hứa "tiết kiệm X%" khi chưa có dữ liệu.

## Cập nhật skill

Khi có văn bản mới (luật thông qua, nghị định, thông tư):

1. Cập nhật `references/00-legal-status.md` trước (bảng trạng thái là nguồn sự thật).
2. Sửa file chuyên đề tương ứng.
3. Ghi `CHANGELOG.md` + tăng `version` trong frontmatter.
4. Chạy `scripts/so_sanh_thue.py --self-test` và kiểm tra link ở `references/08-sources.md`.
5. Nếu nội dung thay đổi lớn, cập nhật `evals/evals.json`.

Chi tiết nguồn và cách kiểm chứng: `references/08-sources.md`.
