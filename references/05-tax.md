# 05 — Thuế cho doanh nghiệp một người

> Thuế là lĩnh vực thay đổi nhanh nhất trong skill này. Mọi con số dưới đây là **mốc tham khảo tại 17/10/2026**; phải kiểm tra văn bản thuế hiện hành trước khi kê khai.

## Thuế thu nhập doanh nghiệp (TNDN)

Luật Thuế TNDN 67/2025/QH15 (hiệu lực 01/10/2025):

| Doanh thu năm | Thuế suất |
|---|---|
| ≤ 3 tỷ đồng | **15%** |
| Trên 3 tỷ đến ≤ 50 tỷ đồng | **17%** |
| Trên 50 tỷ đồng | **20%** |

- Doanh thu làm căn cứ xác định thuế suất là doanh thu của kỳ tính thuế **trước liền kề**.
- Doanh nghiệp mới thành lập chưa có doanh thu kỳ trước: áp dụng theo hướng dẫn của Chính phủ (kiểm tra nghị định hiện hành).
- Công thức chung: **thu nhập chịu thuế = doanh thu − chi phí được trừ + thu nhập khác**; thuế = thu nhập chịu thuế × thuế suất (sau ưu đãi, nếu có).

Lưu ý:

- Chi phí phải có hóa đơn, chứng từ hợp lệ và phục vụ hoạt động sản xuất kinh doanh.
- Một số khoản chi bị giới hạn (quảng cáo, tiếp khách, lương... theo luật).
- Ưu đãi theo ngành/địa bàn/khu công nghiệp có điều kiện riêng.

## Thuế giá trị gia tăng (GTGT)

Hai phương pháp:

| Phương pháp | Cách tính | Phù hợp |
|---|---|---|
| **Khấu trừ** | Thuế đầu ra − thuế đầu vào được khấu trừ | Doanh nghiệp có hóa đơn đầu vào đầy đủ, doanh thu lớn |
| **Trực tiếp** | Doanh thu × tỷ lệ % (theo ngành) | Quy mô nhỏ, không đủ điều kiện khấu trừ |

- Doanh nghiệp đáp ứng điều kiện được chọn phương pháp khấu trừ; phương pháp trực tiếp áp dụng cho một số đối tượng theo luật.
- Tỷ lệ % trực tiếp khác nhau theo ngành (phân phối, dịch vụ, sản xuất, xây dựng...). **Phải tra biểu tỷ lệ hiện hành.**
- Hộ kinh doanh có ngưỡng doanh thu miễn thuế GTGT/TNCN — ngưỡng này đang thay đổi theo lộ trình 2025–2026, phải kiểm tra trước khi tính.

## Lệ phí môn bài

- Mức theo vốn điều lệ/doanh thu (bậc), thường từ 1–3 triệu đồng/năm với doanh nghiệp; hộ kinh doanh mức thấp hơn.
- Doanh nghiệp mới thành lập thường được miễn năm đầu.
- Doanh nghiệp chuyển đổi từ hộ kinh doanh được miễn 3 năm theo Nghị định 80/2021/NĐ-CP (Điều 18).
- Mức và diện miễn có thể đã thay đổi — tra cứu trước khi nộp.

## Thuế thu nhập cá nhân (TNCN) của chủ doanh nghiệp

- Nếu chủ sở hữu làm việc và nhận lương: phần lương là chi phí được trừ (nếu hợp lý, có hợp đồng, chứng từ) và chịu thuế TNCN theo biểu lũy tiến.
- Lợi nhuận chia cho chủ sở hữu: thu nhập từ đầu tư vốn, thường chịu thuế TNCN 5% (kiểm tra quy định hiện hành).
- Không được coi tiền rút từ công ty là "tiền cá nhân" mà không có căn cứ; có thể bị coi là chia lợi nhuận/trả thu nhập và bị truy thu.

## So sánh phương pháp thuế — dùng script

Bài toán: nên chọn thuế theo **tỷ lệ % doanh thu** hay **kê khai trên lợi nhuận**?

```bash
python3 scripts/so_sanh_thue.py \
  --doanh-thu 8000000000 \
  --loi-nhuan 1200000000 \
  --ty-le 0.015 \
  --thue-suat 0.20
```

Script sẽ tính:

- Thuế theo % doanh thu.
- Thuế theo kê khai (lợi nhuận × thuế suất).
- Biên lợi nhuận hòa vốn.
- Khuyến nghị sơ bộ + giả định + disclaimer.

**Công thức hòa vốn:** nếu tỷ lệ % doanh thu là `r` và thuế suất TNDN là `t`, hai cách bằng nhau khi:

```
biên lợi nhuận = r / t
```

Ví dụ: r = 1,5%, t = 20% → biên hòa vốn = 7,5%. Nếu biên lợi nhuận thực tế cao hơn 7,5%, kê khai trên lợi nhuận thường có lợi hơn (về TNDN).

**Nhưng đừng quên GTGT:** phương pháp trực tiếp thường **không được khấu trừ GTGT đầu vào**. Với ngành nhập hàng bán lại (đầu vào lớn, biên mỏng), kê khai + khấu trừ thường có lợi hơn nhiều, dù TNDN tính ra cao hơn.

## Lịch kê khai tham khảo

| Loại | Tần suất | Ghi chú |
|---|---|---|
| GTGT | Hàng tháng hoặc hàng quý | Doanh nghiệp nhỏ thường được chọn quý |
| TNDN tạm nộp | Hàng quý | Tạm nộp theo lợi nhuận ước tính |
| Quyết toán TNDN | Hàng năm | Trong 90 ngày kể từ kết thúc năm tài chính |
| TNCN | Hàng tháng/quý + quyết toán | Tùy số lượng lao động |
| Lệ phí môn bài | Đầu năm | Nộp trước 30/01 (kiểm tra hiện hành) |
| BHXH | Hàng tháng | Khi có lao động thuộc đối tượng |

Lịch cụ thể có thể thay đổi; luôn kiểm tra thông báo của cơ quan thuế.

## Hóa đơn điện tử

- Doanh nghiệp phải sử dụng hóa đơn điện tử khi bán hàng/cung cấp dịch vụ (trừ trường hợp được miễn).
- Đăng ký mẫu hóa đơn, chữ ký số với cơ quan thuế trước khi sử dụng.
- Hóa đơn phải phản ánh đúng giao dịch; lập hóa đơn khống là hành vi bị xử lý nghiêm (hành chính, thậm chí hình sự).

## Cờ đỏ về thuế — dừng lại, hỏi chuyên gia

- Đề nghị "làm hai sổ", "ẩn doanh thu", "xuất hóa đơn khống".
- Chuyển tài sản sang công ty mới để né nợ/thuế.
- Dùng chi phí không có chứng từ để giảm lợi nhuận.
- Kê khai sai loại hình/ngành nghề để hưởng ưu đãi.
- Giao dịch với bên liên quan không có hợp đồng, giá không thị trường.

Các hành vi này có thể dẫn đến truy thu, phạt, cấm hành nghề, hoặc trách nhiệm hình sự. Skill này **không hỗ trợ** các phương án đó.

## Checklist thuế cho công ty mới

- [ ] Đăng ký thuế, xác nhận phương pháp tính GTGT.
- [ ] Đăng ký hóa đơn điện tử, chữ ký số.
- [ ] Xác định nghĩa vụ lệ phí môn bài và diện miễn.
- [ ] Thiết lập lịch kê khai, phân công người phụ trách.
- [ ] Lưu chứng từ, hóa đơn, biên bản.
- [ ] Rà soát ưu đãi (ngành, địa bàn, DNNVV, chuyển đổi từ hộ kinh doanh).
- [ ] Kiểm tra nghĩa vụ TNCN/BHXH nếu có lao động.

> Nội dung tham khảo, không phải tư vấn thuế. Thuế suất, tỷ lệ %, ngưỡng miễn và lịch kê khai phải đối chiếu văn bản hiện hành tại thời điểm kê khai.
