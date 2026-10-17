# Hướng dẫn duy trì & phát hành

Tài liệu dành cho người duy trì skill. Trước khi phát hành, chạy qua checklist bên dưới.

## 1. Trước khi publish — checklist

- [ ] `SKILL.md` có `name`, `description`, `license`, `metadata.version`, `metadata.as_of`.
- [ ] `references/00-legal-status.md` đúng mốc thời gian; không còn văn bản hết hiệu lực bị ghi là "đang áp dụng".
- [ ] Mọi tuyên bố pháp lý có nguồn; dự thảo được đánh dấu rõ.
- [ ] `DISCLAIMER.md` có tiếng Việt + tiếng Anh; xuất hiện trong `SKILL.md` và `README.md`.
- [ ] Không có dữ liệu nội bộ: tên khách, số liệu sống, giá nội bộ, chiến lược kinh doanh, token, đường dẫn máy cá nhân.
- [ ] `python3 scripts/so_sanh_thue.py --self-test` chạy OK.
- [ ] `CHANGELOG.md` khớp version.
- [ ] Không có link chết trong `references/08-sources.md`.

Kiểm tra nhanh:

```bash
bash scripts/audit_public.sh
```

Script sẽ quét secret/token, đường dẫn máy, email/số điện thoại, tên hệ thống nội bộ, và kiểm tra bên trong file zip/.skill (không có `.git`, `dist`, file lạ). Bước soát tên khách/nhân sự vẫn phải làm thủ công theo danh sách nội bộ — **không lưu danh sách đó trong repo**.

Sau khi đóng gói, chạy lại audit; chỉ phát hành khi PASS.

## 2. Chốt đích publish

Trước khi tạo repo/release, xác nhận:

- **Repo:** `diginno-net/opc-vn-business-law` (public) — hoặc repo khác do người duyệt chọn.
- **License:** CC BY 4.0 (nội dung) + MIT (script).
- **Tên hiển thị:** OPC VN Business Law.
- **Mô tả ngắn:** "Skill tham khảo pháp lý – thuế – kế toán cho doanh nghiệp một người tại Việt Nam."

Không tạo repo trùng. Kiểm tra `git remote -v` trước khi push.

## 3. Phát hành bản đầu

```bash
cd opc-vn-business-law
git init
git add .
git commit -m "feat: opc-vn-business-law v1.0.0"
git branch -M main
git remote add origin https://github.com/diginno-net/opc-vn-business-law.git
git push -u origin main

bash scripts/package_skill.sh   # tao .skill, loai .git/launch/evals
bash scripts/build_dist.sh      # tao .zip, loai .git/launch
gh release create v1.0.0 dist/opc-vn-business-law-v1.0.0.zip \
  --title "v1.0.0" \
  --notes "Bản đầu tiên: mô hình doanh nghiệp một người, chuyển đổi hộ kinh doanh, dự thảo Luật Phát triển DNNVV 2026, kế toán siêu nhỏ, thuế."
```

Nếu chưa có `gh`, tạo release thủ công và đính kèm file zip trong `dist/`.

## 4. Gói phát hành

Hai script đóng gói:

- `scripts/package_skill.sh` → `dist/opc-vn-business-law.skill` (không có `.git`, `launch/`, `evals/`).
- `scripts/build_dist.sh` → `dist/opc-vn-business-law-v<version>.zip` (không có `.git`, `launch/`; có `evals/`).

Sau khi đóng gói, chạy `bash scripts/audit_public.sh` và chỉ phát hành khi PASS.

Nội dung zip giữ nguyên cấu trúc thư mục, có `SKILL.md` ở gốc.

## 5. Sau khi publish

- Ghim issue mẫu: báo lỗi pháp lý, đề xuất cập nhật, câu hỏi.
- Ghi rõ trong README: "Không phải tư vấn pháp lý; không trả lời câu hỏi cá nhân qua issue."
- Lịch rà soát: hàng tháng (thuế), hàng quý (dự thảo luật), 6 tháng (toàn bộ).
- Khi có luật mới: cập nhật `00-legal-status.md` trước, tăng version, release mới.
- Không hứa SLA trả lời.

## 6. Truyền thông đề xuất

- Bài giới thiệu: "Vì sao 'không cần kế toán trưởng' không phải là tin mới" — dùng đúng insight trong `references/02-draft-sme-law-2026.md`.
- Demo 3 prompt mẫu (chọn mô hình, kiểm tra Chủ tịch, so sánh thuế).
- Kèm disclaimer ngay trong bài, không chỉ trong repo.

## 7. Dữ liệu không đưa vào bản công khai

- Số liệu tài chính nội bộ, giá dịch vụ, chiến lược bán.
- Tên khách hàng, hợp đồng, hồ sơ thật.
- Đường dẫn máy cá nhân, token, API key.
- `launch/` là nháp nội bộ (bài đăng, CTA, kế hoạch); không commit, không đóng gói, không publish khi chưa duyệt.

## 8. Rollback

Nếu phát hiện nội dung sai hoặc lộ thông tin:

1. Sửa hoặc xoá file trong repo.
2. Release bản vá (patch version).
3. Ghi rõ trong `CHANGELOG.md`.
4. Nếu đã chia sẻ zip: thu hồi link, thông báo bản thay thế.
