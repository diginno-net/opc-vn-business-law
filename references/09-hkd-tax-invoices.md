# 09 — Thuế hộ kinh doanh và hóa đơn điện tử

> **Phạm vi:** HKD/cá nhân kinh doanh tại Việt Nam, kỳ 2026; phần TNCN dưới đây dành cho **cá nhân cư trú**. Bản gốc thu thập 29/10, đối chiếu bổ sung 30/10/2026. **VERIFIED_SOURCE_TEXT / VALIDITY_UNCONFIRMED**: đã đọc điều khoản chỉ ra, chưa khóa toàn bộ sửa đổi đến ngày sử dụng; xem [hồ sơ nguồn](<08-sources.md>). Không phải công cụ quyết toán, tư vấn cá biệt hoặc quyền thao tác hóa đơn thật.

## 1. Chốt dữ liệu trước khi trả lời

Hỏi tối đa 5 nhóm, ưu tiên phần thiếu liên quan câu hỏi:

1. **Chủ thể và kỳ:** HKD/cá nhân hay công ty; cư trú hay không; năm/kỳ, ngày bắt đầu kinh doanh và phương pháp đang áp dụng.
2. **Hoạt động:** hàng hóa, dịch vụ, xây dựng, cho thuê, nội dung số; bán trong nước/xuất khẩu; bên mua là cơ sở kinh doanh hay người tiêu dùng.
3. **Doanh thu:** tất cả kênh, địa điểm, doanh thu giao dịch trước phí; chiết khấu/giảm giá/trả lại, khoản sàn giữ và tiền thực chuyển. Không lấy riêng payout ngân hàng làm doanh thu.
4. **Chứng từ:** báo cáo đơn, giao hàng/nghiệm thu/thu tiền, hoàn/hủy, khấu trừ/nộp thay, sổ và chi phí hợp lệ.
5. **Hóa đơn:** đã đăng ký loại nào, mã/không mã/máy tính tiền; giao dịch nào, ngày nào, trạng thái gửi/khai; lỗi ban đầu hay trả hàng/chấm dứt sau đó.

Tách bốn kết luận: **GTGT — TNCN — thông báo/kê khai — hóa đơn**. [CLI TNDN](<../scripts/so_sanh_thue.py>) chỉ dành DN theo [05](<05-tax.md>), không tính TNCN HKD dù có cùng các con số 15%/17%/20%.

## 2. Ngưỡng và phương pháp thuế: không dùng bảng cũ một cách máy móc

Nguồn: [NĐ68/2026/NĐ-CP](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-68-2026-nd-cp-469047.htm), Điều 3–6; **đọc cùng** [NĐ141/2026/NĐ-CP](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-141-2026-nd-cp-469455.htm), Điều 1 khoản 1, Điều 3. NĐ141 thay cụm “500 triệu đồng” bằng “01 tỷ đồng” tại các vị trí được liệt kê, áp dụng từ **01/01/2026**; không phải thay mọi con số trong mọi văn bản.

| Tổng doanh thu năm và phạm vi phù hợp | Hướng phân loại, trước miễn/giảm khác |
|---|---|
| **≤1 tỷ** | NĐ68 Điều 3 khoản 1: không chịu GTGT; Điều 4 khoản 1: cá nhân cư trú không phải nộp TNCN kinh doanh. **Không suy thành hết nghĩa vụ thông báo, sổ/chứng từ hoặc mọi nghĩa vụ hóa đơn.** |
| **>1 tỷ đến ≤3 tỷ** | Điều 4 khoản 5 điểm a–b: nhánh TNCN theo doanh thu tính thuế hoặc lựa chọn theo thu nhập tính thuế. Kiểm phương pháp đã chọn và điều kiện thực tế. |
| **>3 tỷ** | Điều 4 khoản 5 điểm b, d: nhánh theo thu nhập; đang theo doanh thu mà hết năm thực tế vượt 3 tỷ thì chuyển từ năm tiếp theo theo đúng điểm d. Không tự đổi phương pháp giữa kỳ hoặc áp cổng doanh thu kỳ trước của TNDN DN. |

Theo **NĐ68 Điều 4 khoản 5 điểm d**, phương pháp TNCN theo thu nhập phải ổn định **02 năm liên tục** kể từ năm đầu áp dụng. Có vài hóa đơn chi phí không có nghĩa được mỗi kỳ tự chọn cách rẻ hơn.

### TNCN: hai cơ sở khác nhau

[Luật109/2025/QH15 Điều 7 khoản 2–4](https://congbao.chinhphu.vn/van-ban/luat-so-109-2025-qh15-468671.htm), đọc cùng [Luật09/2026/QH16 Điều 1, Điều 5 khoản 2](https://congbao.chinhphu.vn/van-ban/luat-so-09-2026-qh16-469536.htm) và NĐ68 đã sửa:

- **Theo doanh thu:** khoản 3 Điều 7 Luật109 dùng phần doanh thu vượt ngưỡng; NĐ68 Điều 4 khoản 3 quy định phân bổ mức trừ giữa ngành/địa điểm nhưng **tổng mức trừ chỉ một lần cho toàn bộ hoạt động thuộc khoản này trong năm**, không nhân ngưỡng theo cửa hàng/sàn. Tỷ lệ tùy ngành, không mặc định 1,5%.
- **Theo thu nhập:** thu nhập tính thuế xác định từ doanh thu trừ chi phí theo luật; mức 15% cho nhánh trên ngưỡng đến 3 tỷ, 17% cho trên 3 đến 50 tỷ, 20% cho trên 50 tỷ (Luật109 Điều 7 khoản 2). Không lấy lợi nhuận tự khai làm thu nhập tính thuế đã xác nhận.
- **Chi phí:** NĐ68 Điều 6 khoản 1–2 yêu cầu thực tế liên quan kinh doanh, hóa đơn/chứng từ và điều kiện thanh toán; có khoản không được trừ. Đọc đủ điều này và hướng dẫn tương ứng trước nhận chi phí; chi phí không chứng từ không tự hợp lệ.
- **Cho thuê bất động sản (trừ lưu trú)** có nhánh riêng tại Luật109 Điều 7 khoản 4 và NĐ68 Điều 4 khoản 4. Không đưa vào nhánh lựa chọn phổ thông chỉ vì doanh thu dưới 3 tỷ. Không gộp nội dung số, đại lý hoặc cá nhân không cư trú vào tỷ lệ của hàng hóa thông thường.

### GTGT: cơ sở độc lập với TNCN

NĐ68 Điều 3 khoản 2 dẫn Luật GTGT và văn bản hướng dẫn cho tỷ lệ/cơ sở trực tiếp. **Không lấy mức trừ doanh thu của TNCN trừ tiếp cho GTGT**, không dùng tỷ lệ TNDN hoặc TNCN làm tỷ lệ GTGT; kiểm loại hàng/dịch vụ, diện không chịu thuế và chính sách giảm GTGT theo đúng kỳ riêng. Tài liệu này không lập bảng đủ mọi thuế suất GTGT năm 2026.

### Doanh thu đa kênh và sàn

NĐ68 Điều 5 khoản 1: doanh thu gồm toàn bộ khoản bán hàng/gia công/dịch vụ và khoản được hưởng theo quy định, không phụ thuộc đã thu tiền; loại trừ chiết khấu thương mại, giảm giá hàng bán và hàng bị trả lại theo điều này. Phí sàn/ads/thuế sàn giữ là những dòng đối soát khác, không tự giảm doanh thu thành tiền nhận ròng.

**Quy trình đối soát đề xuất, không phải biểu mẫu pháp định:** doanh thu giao dịch → giảm giá/trả lại có chứng từ → phân ngành/kênh → cộng doanh thu cùng người nộp thuế → đối chiếu thuế đã nộp thay → xác định phần còn khai/nộp hoặc xử lý nộp thừa. Tránh cả nộp trùng cùng khoản đã nộp thay lẫn kết luận “sàn giữ thuế là xong”.

**NĐ252/2026/NĐ-CP Điều 74 khoản 1, khoản 3 điểm d** quy định hiệu lực 01/07/2026 và thay NĐ117/2025. Vì vậy, phần khấu trừ/nộp thay sau mốc này phải đối chiếu NĐ252, thông tư quản lý thuế tương ứng và chứng từ sàn; không dùng riêng NĐ117 hoặc quy trình đầu năm làm mặc định cả năm. Đợt này chỉ kiểm các điều khoản thủ tục được chỉ ra trong [hồ sơ nguồn](<08-sources.md>), chưa khóa toàn bộ cơ chế quyết toán/hoàn và biểu mẫu cập nhật; thiếu nguồn thì trả việc cần kiểm, không bịa thủ tục.

### Thông báo doanh thu và ưu đãi

- NĐ68 Điều 8 khoản 1 điểm a (đã sửa ngưỡng bởi NĐ141): nhánh doanh thu đến ngưỡng vẫn thông báo doanh thu thực tế, mốc **31/01 năm sau**; vượt trong năm phải kiểm nhánh khai từ quý vượt. **NĐ252 Điều 10 khoản 9** tiếp tục dẫn thời hạn HKD theo NĐ68; **Điều 11 khoản 1** loại nhánh HKD dưới ngưỡng khỏi quy tắc chung không phải nộp hồ sơ khai thuế. Không suy “không nộp thuế = không báo doanh thu”.
- **Mẫu sau 01/07/2026:** TT89/2026/TT-BTC Điều 99 khoản 1, khoản 4 điểm đ và khoản 5 có hiệu lực từ mốc này, bãi bỏ **một phần** Điều 4 TT18 và thay 6 mẫu; không bãi bỏ toàn bộ TT18. Đọc cùng **QĐ2551/QĐ-BTC ngày 15/09/2026** đính chính tên mẫu, gồm `01/XSBHDCMG-CNKD`, `01/BK-XSBHDCMG`, và Điều 100 về chuyển tiếp. Trước chọn mẫu/lịch cho hồ sơ cụ thể phải kiểm cả Luật Quản lý thuế108/2025, NĐ252 và sửa đổi liên quan; tài liệu này không cung cấp bộ mẫu kê khai đã xác nhận đầy đủ.
- [NQ198/2025/QH15 Điều 10 khoản 6–7](https://xaydungchinhsach.chinhphu.vn/nghi-quyet-198-2025-qh15-ve-mot-so-co-che-chinh-sach-dac-biet-phat-trien-kinh-te-tu-nhan-119250517191622422.htm): chấm dứt phương pháp khoán và thu/nộp lệ phí môn bài từ **01/01/2026**. Không tự xóa nghĩa vụ còn nợ của kỳ cũ.
- [NQ43/2026/QH16 Điều 1 khoản 1, Điều 2](https://vanban.chinhphu.vn/?classid=1&docid=219330&orggroupid=1&pageid=27160): giảm **30% số TNCN phải nộp** kỳ 2026 và 2027 từ kinh doanh của cá nhân cư trú có doanh thu từng năm không quá **10 tỷ**; hiệu lực 24/08/2026. Không giảm GTGT, không đổi thuế suất luật định. **Chưa xác minh nghị định hướng dẫn cuối cùng**, không dùng dự thảo để khẳng định cách khấu trừ/hoàn hay tự ngừng kê khai.

## 3. Ai dùng hóa đơn điện tử, có phải máy tính tiền không?

Căn cứ [NĐ254/2026/NĐ-CP](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-254-2026-nd-cp-469957.htm), Điều 4 khoản 1, Điều 6–7, Điều 43–44; [TT91/2026/TT-BTC](https://congbao.chinhphu.vn/van-ban/thong-tu-so-91-2026-tt-btc-470171.htm). Hai văn bản quy định hiệu lực **01/07/2026**; NĐ254 Điều 43 khoản 2 chấm dứt NĐ123/2020, NĐ70/2025 và Điều 1 NĐ41/2022. Kiểm chuyển tiếp, không dùng NĐ70 như căn cứ duy nhất cho giao dịch sau mốc này.

1. **Ngưỡng:** NĐ254 Điều 6 khoản 1 điểm d: HKD/cá nhân kinh doanh doanh thu năm **trên 1 tỷ** hoặc bán tài sản phải đăng ký quyền sở hữu/quyền sử dụng phải áp dụng HĐĐT có mã hoặc từ máy tính tiền theo quy định. **Đúng 1 tỷ không phải “trên 1 tỷ”**; vẫn kiểm ngoại lệ giao dịch và đăng ký tự nguyện.
2. **Máy tính tiền:** điểm c xác định nhóm bán/cung cấp trực tiếp cho người tiêu dùng theo ngành liệt kê. Cũng tại điểm c, đã đăng ký HĐĐT theo điểm a/b thì **không bắt buộc đăng ký lại HĐĐT từ máy tính tiền**. Vì thế không kết luận “mọi hộ bán lẻ đều phải mua máy/phần mềm mới”.
3. **Không thuộc diện bắt buộc:** điểm d cho đăng ký theo nhu cầu; cấp theo từng lần phát sinh phải đúng đối tượng/điều kiện khoản 2, không mặc định mọi hộ nhỏ đều xin được một hóa đơn miễn thủ tục.
4. **Ngoại lệ:** Điều 7 có các nhánh không phải sử dụng HĐĐT, gồm HKD/cá nhân có thu nhập cho thuê bất động sản; nội dung số giải trí/trò chơi/phim/ảnh/nhạc/quảng cáo số cho tổ chức, cá nhân nước ngoài (khoản 2); đại lý xổ số/bảo hiểm/đa cấp đã được doanh nghiệp khấu trừ thuế theo điều kiện khoản 3. Đọc đúng phạm vi, không mở rộng sang mọi dịch vụ xuất khẩu hoặc mọi người bán trên sàn.
5. **Vượt ngưỡng:** NĐ141 Điều 1 khoản 2 sửa NĐ68 Điều 8 khoản 5 điểm c có mốc đăng ký **30 ngày từ ngày cuối kỳ tính thuế có doanh thu lũy kế vượt 1 tỷ** cho nhánh mới kinh doanh/năm trước chưa vượt. Trước áp dụng cho hồ sơ cụ thể, đối chiếu quy định đăng ký và chuyển tiếp sau 01/07 tại NĐ254/TT91 và tình trạng đăng ký hiện có; không đếm máy móc từ ngày phát sinh một đơn hàng.

## 4. Khách không lấy hóa đơn, bán hàng qua sàn và thời điểm lập

- **Khách không lấy:** với người bán/giao dịch thuộc diện lập, Điều 4 khoản 1 NĐ254 không trao quyền bỏ hóa đơn chỉ vì khách từ chối. **Phụ lục NĐ254 mục 4 điểm b** quy định người tiêu dùng không cung cấp thông tin thì thể hiện “Bán cho người tiêu dùng”, có trường hợp đặc thù tại mục 9; không bắt mọi khách lẻ cung cấp mã số thuế/giấy tờ tùy thân. Cơ sở kinh doanh mua hàng có nhánh thông tin riêng tại mục 4 điểm a.
- **Bán hàng hóa:** Điều 9 khoản 1: thời điểm chuyển quyền sở hữu/quyền sử dụng, không phụ thuộc đã thu tiền. Hàng xuất khẩu có quy tắc riêng gắn thông quan; không áp một mốc giao hàng nội địa cho mọi đơn xuất khẩu.
- **Cung cấp dịch vụ:** Điều 9 khoản 2: hoàn thành cung cấp; thu tiền trước/trong khi cung cấp thì thời điểm thu tiền, trừ tiền đặt cọc bảo đảm hợp đồng theo quy định. Không gọi mọi tiền trả trước là đặt cọc để trì hoãn hóa đơn.
- **Nhiều lần giao/bàn giao:** khoản 3 yêu cầu lập theo khối lượng, giá trị mỗi lần tương ứng. **Ngoại lệ theo ngành/đối soát** nằm tại khoản 4; bán hàng trên sàn không tự làm mọi đơn được gộp một hóa đơn cuối tháng. Không chờ sàn payout mới xuất nếu không có căn cứ riêng.
- **Loại hóa đơn và đầu vào:** Điều 8 khoản 1–2 phân biệt hóa đơn GTGT và hóa đơn bán hàng theo đối tượng/phương pháp. HĐĐT từ máy tính tiền không tự trở thành hóa đơn GTGT khấu trừ; bên mua phải kiểm loại và điều kiện khấu trừ/chi phí theo luật thuế riêng. Không cam kết “có mã là khấu trừ được VAT”.

## 5. Sai hóa đơn: phân nhánh thay vì hủy hàng loạt

Căn cứ **TT91 Điều 10** (và Điều 24 chuyển tiếp cho hóa đơn lịch sử):

| Tình huống | Hướng xử lý theo điều khoản; kiểm hồ sơ trước thao tác |
|---|---|
| Hóa đơn thường sai tên/địa chỉ/số tiền bằng chữ/nội dung thuộc điểm a, không sai các chỉ tiêu loại trừ | Khoản 1 điểm a: thông báo người mua và cơ quan thuế theo mẫu, không phải lập lại. Không áp nhánh nhẹ này cho sai MST/số tiền/thuế suất. |
| Hóa đơn thường sai MST, hàng hóa, số tiền, thuế suất/tiền thuế hoặc nội dung thuộc điểm b | Khoản 1 điểm b: điều chỉnh hoặc thay thế; đọc yêu cầu văn bản thỏa thuận/thông báo, trường hợp ngoại lệ và thông tin dẫn hóa đơn gốc. |
| Hóa đơn **máy tính tiền đã lập sai** hoặc bán tài sản thuộc diện đăng ký sở hữu/sử dụng | Khoản 1 điểm c: **thay thế**, trừ trường hợp được dẫn tại điểm c.2 khoản 5. Không mở quyền chọn điều chỉnh/thay thế phổ thông cho mọi lỗi máy tính tiền. |
| Trả lại hàng, hoặc dịch vụ đã xuất theo thu tiền rồi hủy/chấm dứt theo phạm vi quy định | Khoản 5 điểm c.1–c.4: nhánh điều chỉnh, hồ sơ và ngoại lệ tương ứng; khác với hóa đơn sai ngay khi lập. **Không suy “máy tính tiền luôn thay thế” cho trả hàng.** |

Khoản 6 điểm a quy định cách xử lý khi tiếp tục phát hiện sai sau lần đầu; điểm b có nhánh chỉ điều chỉnh cho hóa đơn không có ký hiệu mẫu/ký hiệu/số theo quy định. **Khoản 6 điểm d chỉ nêu kỳ kê khai cho hóa đơn điều chỉnh thuộc khoản 5**, không áp chung mọi lỗi ban đầu. Cần kiểm quy định khai bổ sung của kỳ/hồ sơ riêng.

Đầu ra chỉ là phương án và danh sách chứng từ. Không đăng nhập nhà cung cấp, phát hành/điều chỉnh/hủy hóa đơn thật hoặc hứa “không bị phạt”. Hạn và chế tài cần kiểm văn bản quản lý thuế/xử phạt áp dụng, tình tiết và trạng thái hồ sơ; chưa có căn cứ thì chuyển người hành nghề/cơ quan thuế, không tự tạo hạn phổ quát.

## 6. Checklist bàn giao một câu hỏi

- **Đã xác nhận:** chủ thể/kỳ, nguồn đã đọc, doanh thu có chứng từ, loại/đăng ký hóa đơn, nhánh luật phù hợp.
- **Chưa xác nhận:** dữ liệu còn thiếu, tính hợp lệ chi phí, khấu trừ/nộp thay, chuỗi sửa đổi và thủ tục chưa khóa.
- **Việc tiếp:** đối soát dữ liệu, mở đúng điều khoản của kỳ, người chịu trách nhiệm duyệt, hồ sơ cần giữ và bước xử lý dự kiến.

Thông tin tham khảo, không phải tư vấn pháp lý/thuế/kế toán; kiểm văn bản gốc và hỏi người hành nghề trước quyết định/kê khai.
