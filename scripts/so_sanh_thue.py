#!/usr/bin/env python3
"""Sàng lọc điều kiện TNDN hoặc mô phỏng trước miễn/giảm (không quyết toán).

Tỷ lệ luôn là số thập phân: 1,5% nhập 0.015; 17% nhập 0.17.
Không tính GTGT, miễn/giảm, chuyển lỗ hoặc xác nhận phân loại ngành.
Nguồn/phạm vi hỗ trợ: references/05-tax.md. Python 3.10+, stdlib.
Giấy phép MIT. Thông tin tham khảo, không phải tư vấn thuế.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
import math
import sys

# NĐ320/2025 Điều12(4), không phải tỷ lệ TNCN/GTGT của hộ kinh doanh.
TY_LE_NGANH = {
    'hang-hoa': .003,
    'san-xuat': .012,
    'dich-vu': .015,
    'cho-thue-dai-ly': .04,
    'noi-dung-so': .04,
    'khac': .005,
}
DISCLAIMER = (
    'Thông tin tham khảo, không phải tư vấn thuế. Chỉ sàng lọc sơ bộ cho doanh nghiệp '
    'thành lập theo pháp luật Việt Nam trong kỳ 2026; không áp dụng cho hộ kinh doanh. '
    'Kiểm văn bản hiện hành và hỏi kế toán hành nghề trước khi kê khai.'
)


@dataclass
class KetQua:
    doanh_thu: float
    loi_nhuan: float
    ty_le_doanh_thu: float
    thue_suat: float
    thue_theo_doanh_thu: float
    thue_theo_loi_nhuan: float
    bien_loi_nhuan: float
    bien_hoa_von: float
    chenh_lech: float
    khuyen_nghi: str
    gia_dinh: str
    disclaimer: str
    che_do: str = 'mo-phong'


def kiem_tra_so(value: float, label: str, *, cho_phep_khong: bool = False) -> None:
    if not math.isfinite(value) or value < 0 or (not cho_phep_khong and value == 0):
        raise ValueError(f'{label} phải là số hữu hạn ' + ('không âm' if cho_phep_khong else 'lớn hơn 0'))


def chuan_hoa_ty_le(value: float) -> float:
    """Chỉ nhận phân số thập phân, không đoán 1 là 1% hay 100%."""
    if not math.isfinite(value) or not 0 < value < 1:
        raise ValueError('Tỷ lệ phải là số thập phân trong (0, 1): 1,5% nhập 0.015')
    return value


def thue_suat_theo_doanh_thu(doanh_thu_can_cu: float) -> float:
    """Thuế suất phổ thông trước miễn/giảm; chỉ gọi sau khi loại ngoại lệ.

    Căn cứ là doanh thu kỳ trước đã xác định/annualize theo Điều11 NĐ320,
    không phải tự động lấy doanh thu năm đang tính. Không xét miễn <=1 tỷ ở đây.
    """
    kiem_tra_so(doanh_thu_can_cu, 'Doanh thu căn cứ', cho_phep_khong=True)
    if doanh_thu_can_cu <= 3e9:
        return .15
    return .17 if doanh_thu_can_cu <= 50e9 else .20


def tinh(doanh_thu: float, loi_nhuan: float, ty_le: float, thue_suat: float) -> KetQua:
    """Mô phỏng thuần số học. loi_nhuan là thu nhập tính thuế giả định.

    Không khẳng định quyền lựa chọn phương pháp; lợi nhuận kế toán thực tế
    cần điều chỉnh chi phí không được trừ, miễn thuế và chuyển lỗ trước khi dùng.
    """
    kiem_tra_so(doanh_thu, 'Doanh thu')
    kiem_tra_so(loi_nhuan, 'Thu nhập giả định', cho_phep_khong=True)
    ty_le = chuan_hoa_ty_le(ty_le)
    thue_suat = chuan_hoa_ty_le(thue_suat)
    thue_dt = doanh_thu * ty_le
    thue_ln = loi_nhuan * thue_suat
    bien = loi_nhuan / doanh_thu
    hoa_von = ty_le / thue_suat
    chenh = thue_ln - thue_dt
    if not all(math.isfinite(x) for x in (thue_dt, thue_ln, bien, hoa_von, chenh)):
        raise ValueError('Kết quả vượt giới hạn số hữu hạn; kiểm lại dữ liệu')
    if math.isclose(thue_ln, thue_dt, rel_tol=1e-12, abs_tol=.01):
        ket_luan = 'Hai số thuế mô phỏng gần như bằng nhau.'
    elif chenh < 0:
        ket_luan = 'Thuế trên thu nhập giả định nhỏ hơn thuế theo % doanh thu.'
    else:
        ket_luan = 'Thuế trên thu nhập giả định lớn hơn thuế theo % doanh thu.'
    return KetQua(
        doanh_thu, loi_nhuan, ty_le, thue_suat, thue_dt, thue_ln, bien, hoa_von, chenh,
        ket_luan + ' Không suy ra quyền lựa chọn phương pháp hoặc số phải nộp.',
        'Mô phỏng trước miễn/giảm, không phải quyết toán. Thu nhập tính thuế là giả định, '
        'không mặc nhiên bằng lợi nhuận kế toán. GTGT phải xét độc lập; '
        'mô phỏng không xác nhận ngành, kỳ tính thuế hay điều kiện pháp lý.'
        + (' Nếu xét kỳ 2026–2027, doanh thu không quá 10 tỷ cần kiểm NQ43/2026/QH16; '
           'chưa xác minh đầy đủ hướng dẫn cuối cùng, chưa áp giảm 30%.' if doanh_thu <= 10e9 else ''),
        DISCLAIMER,
    )


def danh_gia(args: argparse.Namespace) -> dict:
    """Sàng lọc phạm vi hẹp; mọi số so sánh đều là mô phỏng trước ưu đãi."""
    canh_bao = [
        'Chỉ xét sơ bộ doanh nghiệp Việt Nam, kỳ 2026, không phải hộ kinh doanh; '
        'không xác nhận doanh thu căn cứ đã đúng hoặc phân loại ngành hợp lệ.',
        'Doanh thu căn cứ phải xác định theo NĐ320 Điều11: năm trước liền kề, '
        'gồm doanh thu tài chính/thu nhập khác, quy đổi kỳ dưới 12 tháng khi áp dụng. '
        'Doanh nghiệp mới hoặc chưa xác định căn cứ: chuyển kế toán kiểm tra.',
        'Chưa tính miễn/giảm, chuyển lỗ, ưu đãi doanh nghiệp mới hoặc thu nhập đặc thù; '
        'không dùng kết quả như số thuế thực nộp.',
        'Phương pháp TNDN không tự quyết định quyền khấu trừ GTGT; phải xét GTGT độc lập.',
    ]
    if args.doanh_thu <= 10e9:
        canh_bao.append(
            'NQ43/2026/QH16 giảm 30% số thuế phải nộp kỳ 2026–2027 có điều kiện; '
            'chưa xác minh đầy đủ hướng dẫn cuối cùng, không tự áp giảm hoặc đổi thuế suất.'
        )
    missing = [name for name, value in (
        ('doanh_thu_can_cu', args.doanh_thu_can_cu), ('nganh', args.nganh),
        ('xac_dinh_chi_phi', args.xac_dinh_chi_phi), ('ngoai_le', args.ngoai_le),
    ) if value is None]
    result = dict(
        che_do='danh-gia', trang_thai='thieu_du_kien', doanh_thu=args.doanh_thu,
        doanh_thu_can_cu=args.doanh_thu_can_cu, thue_suat=None, ty_le_doanh_thu=None,
        so_sanh=None, du_kien_thieu=missing, canh_bao=canh_bao, disclaimer=DISCLAIMER,
    )
    if args.ngoai_le == 'co':
        result['trang_thai'] = 'can_chuyen_chuyen_gia'
        canh_bao.append('Có ngoại lệ/liên kết/thu nhập đặc thù hoặc chưa được loại trừ: không tự gán thuế suất.')
        return result
    if missing:
        return result
    result['thue_suat'] = thue_suat_theo_doanh_thu(args.doanh_thu_can_cu)
    if args.doanh_thu_can_cu <= 1e9:
        result['trang_thai'] = 'can_kiem_tra_mien_thue'
        canh_bao.append('Kiểm miễn TNDN theo NĐ141/2026 Điều2; thuế suất trước miễn không phải số phải nộp.')
    elif args.doanh_thu_can_cu > 3e9 or args.xac_dinh_chi_phi == 'co':
        result['trang_thai'] = 'khong_du_dieu_kien'
        canh_bao.append('Không đạt nhánh % doanh thu NĐ320 Điều12(4): căn cứ <=3 tỷ và không xác định chi phí/thu nhập.')
    else:
        result['trang_thai'] = 'du_dieu_kien_so_bo'
        result['ty_le_doanh_thu'] = TY_LE_NGANH[args.nganh]
        canh_bao.append('Phân loại ngành cần đối chiếu: dịch vụ có ngoại lệ 4%; không gộp mọi phần mềm/AI vào nội dung số.')
        if args.loi_nhuan is not None:
            result['so_sanh'] = asdict(tinh(args.doanh_thu, args.loi_nhuan,
                                           result['ty_le_doanh_thu'], result['thue_suat']))
            canh_bao.append('Thu nhập đưa vào so sánh chỉ là giả định kịch bản; nếu thực tế xác định được chi phí/thu nhập thì phải đánh giá lại điều kiện.')
    return result


def in_ket_qua(k: KetQua) -> None:
    print('=== MÔ PHỎNG TNDN TRƯỚC MIỄN/GIẢM ===')
    print(f'Doanh thu: {k.doanh_thu:,.0f} đ; thu nhập giả định: {k.loi_nhuan:,.0f} đ')
    print(f'Tỷ lệ doanh thu: {k.ty_le_doanh_thu * 100:g}%; thuế suất giả định: {k.thue_suat * 100:g}%')
    print(f'Thuế theo % doanh thu: {k.thue_theo_doanh_thu:,.0f} đ')
    print(f'Thuế trên thu nhập giả định: {k.thue_theo_loi_nhuan:,.0f} đ')
    print(f'Biên hòa vốn: {k.bien_hoa_von * 100:.2f}%')
    print(k.khuyen_nghi)
    print(k.gia_dinh)
    print(k.disclaimer)


def self_test() -> int:
    k = tinh(8e9, 1.2e9, .015, .17)
    checks = [math.isclose(k.thue_theo_loi_nhuan, 204e6),
              math.isclose(k.bien_hoa_von, .015 / .17),
              thue_suat_theo_doanh_thu(3e9 + 1) == .17]
    for value in (math.nan, math.inf, 1.5):
        try:
            chuan_hoa_ty_le(value)
        except ValueError:
            continue
        raise AssertionError('Tỷ lệ không hợp lệ phải bị từ chối')
    if not all(checks):
        raise AssertionError('Sai regression số học/thuế suất')
    print('Self-test OK (số học, không xác nhận nghĩa vụ thuế)')
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description='Sàng lọc TNDN kỳ 2026 hoặc mô phỏng trước ưu đãi; không quyết toán')
    p.add_argument('--che-do', choices=['danh-gia', 'mo-phong'], default='danh-gia')
    p.add_argument('--doanh-thu', type=float, help='Doanh thu kỳ hiện tại, đồng')
    p.add_argument('--loi-nhuan', '--thu-nhap-tinh-thue', dest='loi_nhuan', type=float,
                   help='Thu nhập tính thuế GIẢ ĐỊNH trước ưu đãi; không tự lấy lợi nhuận kế toán')
    p.add_argument('--doanh-thu-can-cu', type=float, help='Doanh thu kỳ trước đã xác định/quy đổi đúng quy định; DN mới cần kiểm riêng')
    p.add_argument('--nganh', choices=TY_LE_NGANH)
    p.add_argument('--xac-dinh-chi-phi', choices=['co', 'khong'], help='Có xác định được chi phí/thu nhập thực tế?')
    p.add_argument('--ngoai-le', choices=['co', 'khong'], help='Có liên kết, thu nhập đặc thù, DN mới hoặc ngoại lệ chưa loại trừ?')
    p.add_argument('--ty-le', type=float, help='Chỉ mô phỏng: phân số thập phân, 1,5%% nhập 0.015')
    p.add_argument('--thue-suat', type=float, help='Chỉ mô phỏng: phân số thập phân, 17%% nhập 0.17')
    p.add_argument('--json', action='store_true')
    p.add_argument('--self-test', action='store_true')
    args = p.parse_args(argv)
    if args.self_test:
        return self_test()
    if args.doanh_thu is None:
        p.error('Cần --doanh-thu (hoặc --self-test)')
    try:
        kiem_tra_so(args.doanh_thu, 'Doanh thu')
        if args.loi_nhuan is not None:
            kiem_tra_so(args.loi_nhuan, 'Thu nhập giả định', cho_phep_khong=True)
        if args.doanh_thu_can_cu is not None:
            kiem_tra_so(args.doanh_thu_can_cu, 'Doanh thu căn cứ', cho_phep_khong=True)
        if args.che_do == 'mo-phong':
            if any(x is not None for x in (args.doanh_thu_can_cu, args.nganh, args.xac_dinh_chi_phi, args.ngoai_le)):
                p.error('Mô phỏng không nhận cờ đánh giá điều kiện; dùng --che-do danh-gia riêng')
            if any(x is None for x in (args.loi_nhuan, args.ty_le, args.thue_suat)):
                p.error('Mô phỏng cần --thu-nhap-tinh-thue, --ty-le và --thue-suat tường minh')
            k = tinh(args.doanh_thu, args.loi_nhuan, args.ty_le, args.thue_suat)
            if args.json:
                print(json.dumps(asdict(k), ensure_ascii=False, allow_nan=False, indent=2))
            else:
                in_ket_qua(k)
        else:
            if args.ty_le is not None or args.thue_suat is not None:
                p.error('Không override tỷ lệ trong đánh giá; dùng --che-do mo-phong cho số giả định')
            result = danh_gia(args)
            if args.json:
                print(json.dumps(result, ensure_ascii=False, allow_nan=False, indent=2))
            else:
                print('Trạng thái:', result['trang_thai'])
                if result['du_kien_thieu']:
                    print('Thiếu:', ', '.join(result['du_kien_thieu']))
                for warning in result['canh_bao']:
                    print('-', warning)
                if result['so_sanh']:
                    in_ket_qua(KetQua(**result['so_sanh']))
                else:
                    print(DISCLAIMER)
    except ValueError as exc:
        print(f'Lỗi: {exc}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
