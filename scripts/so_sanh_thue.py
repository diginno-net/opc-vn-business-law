#!/usr/bin/env python3
"""So sánh nhanh thuế TNDN: tỷ lệ % doanh thu vs kê khai trên lợi nhuận.

Chỉ so sánh thuế TNDN. KHÔNG tính GTGT, lệ phí môn bài, ưu đãi,
hay việc mất quyền khấu trừ GTGT đầu vào.

Ví dụ:
    python3 so_sanh_thue.py --doanh-thu 8000000000 --loi-nhuan 1200000000 --ty-le 1.5

    python3 so_sanh_thue.py --doanh-thu 8e9 --loi-nhuan 1.2e9 --ty-le 0.015 --json
    python3 so_sanh_thue.py --self-test

Giấy phép: MIT. Nội dung tham khảo, không phải tư vấn thuế.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass


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


def chuan_hoa_ty_le(value: float) -> float:
    """Nhận 1.5 (nghĩa là 1,5%) hoặc 0.015; trả về dạng thập phân."""
    if value <= 0:
        raise ValueError("Tỷ lệ phải lớn hơn 0")
    if value > 1:
        value = value / 100.0
    if value >= 1:
        raise ValueError("Tỷ lệ không hợp lệ (phải < 100%)")
    return value


def tinh(doanh_thu: float, loi_nhuan: float, ty_le: float, thue_suat: float) -> KetQua:
    if doanh_thu <= 0:
        raise ValueError("Doanh thu phải lớn hơn 0")
    if loi_nhuan < 0:
        raise ValueError("Lợi nhuận không được âm (nhập 0 nếu lỗ)")
    if loi_nhuan > doanh_thu:
        raise ValueError("Lợi nhuận không thể lớn hơn doanh thu")

    ty_le = chuan_hoa_ty_le(ty_le)
    if not (0 < thue_suat <= 1):
        raise ValueError("Thuế suất phải trong khoảng (0, 1]")

    thue_doanh_thu = doanh_thu * ty_le
    thue_loi_nhuan = loi_nhuan * thue_suat
    bien = loi_nhuan / doanh_thu if doanh_thu else 0.0
    hoa_von = ty_le / thue_suat
    chenh = thue_loi_nhuan - thue_doanh_thu

    if abs(chenh) < 1:
        khuyen_nghi = "Hai cách gần như tương đương về thuế TNDN; chọn theo mức độ đơn giản và khả năng khấu trừ GTGT."
    elif chenh < 0:
        khuyen_nghi = "Kê khai trên lợi nhuận có lợi hơn về thuế TNDN (nhớ kiểm tra GTGT đầu vào)."
    else:
        khuyen_nghi = "Cách tính theo % doanh thu có lợi hơn về thuế TNDN (nhưng thường mất khấu trừ GTGT đầu vào)."

    gia_dinh = (
        f"Giả định: doanh thu {doanh_thu:,.0f} đ; lợi nhuận trước thuế {loi_nhuan:,.0f} đ; "
        f"tỷ lệ % doanh thu {ty_le*100:.2f}%; thuế suất TNDN {thue_suat*100:.0f}%. "
        "Chưa tính GTGT, lệ phí môn bài, ưu đãi, chi phí không được trừ."
    )
    disclaimer = (
        "Thông tin tham khảo, không phải tư vấn thuế. Tỷ lệ % và thuế suất phải đối chiếu "
        "văn bản thuế hiện hành tại thời điểm kê khai."
    )

    return KetQua(
        doanh_thu=doanh_thu,
        loi_nhuan=loi_nhuan,
        ty_le_doanh_thu=ty_le,
        thue_suat=thue_suat,
        thue_theo_doanh_thu=thue_doanh_thu,
        thue_theo_loi_nhuan=thue_loi_nhuan,
        bien_loi_nhuan=bien,
        bien_hoa_von=hoa_von,
        chenh_lech=chenh,
        khuyen_nghi=khuyen_nghi,
        gia_dinh=gia_dinh,
        disclaimer=disclaimer,
    )


def in_ket_qua(k: KetQua) -> None:
    print("=== SO SÁNH THUẾ TNDN ===")
    print(f"Doanh thu:                    {k.doanh_thu:>15,.0f} đ")
    print(f"Lợi nhuận trước thuế:         {k.loi_nhuan:>15,.0f} đ")
    print(f"Biên lợi nhuận:               {k.bien_loi_nhuan*100:>14.2f} %")
    print(f"Tỷ lệ % doanh thu:            {k.ty_le_doanh_thu*100:>14.2f} %")
    print(f"Thuế suất TNDN:               {k.thue_suat*100:>14.0f} %")
    print("-" * 52)
    print(f"Thuế theo % doanh thu:        {k.thue_theo_doanh_thu:>15,.0f} đ")
    print(f"Thuế theo lợi nhuận:          {k.thue_theo_loi_nhuan:>15,.0f} đ")
    print(f"Chênh lệch (kê khai - %DT):   {k.chenh_lech:>15,.0f} đ")
    print(f"Biên hòa vốn:                 {k.bien_hoa_von*100:>14.2f} %")
    print("-" * 52)
    print(f"Khuyến nghị: {k.khuyen_nghi}")
    print(f"\n{k.gia_dinh}")
    print(f"\n⚠️  {k.disclaimer}")


def self_test() -> int:
    k = tinh(8_000_000_000, 1_200_000_000, 0.015, 0.20)
    assert abs(k.thue_theo_doanh_thu - 120_000_000) < 1
    assert abs(k.thue_theo_loi_nhuan - 240_000_000) < 1
    assert abs(k.bien_hoa_von - 0.075) < 1e-9
    assert "% doanh thu" in k.khuyen_nghi  # 1,5% x 8 tỷ = 120tr < 20% x 1,2 tỷ

    k2 = tinh(8_000_000_000, 1_200_000_000, 1.5, 0.20)  # percent form
    assert abs(k2.ty_le_doanh_thu - 0.015) < 1e-12

    k3 = tinh(1_000_000_000, 100_000_000, 0.05, 0.20)
    assert k3.chenh_lech < 0
    assert "lợi nhuận" in k3.khuyen_nghi

    for bad in [
        lambda: tinh(0, 0, 0.01, 0.2),
        lambda: tinh(100, -1, 0.01, 0.2),
        lambda: tinh(100, 200, 0.01, 0.2),
        lambda: tinh(100, 10, 0, 0.2),
        lambda: tinh(100, 10, 0.01, 0),
    ]:
        try:
            bad()
        except ValueError:
            pass
        else:
            raise AssertionError("Phải ném ValueError")

    print("Self-test OK")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="So sánh thuế TNDN: % doanh thu vs kê khai")
    p.add_argument("--doanh-thu", type=float, help="Doanh thu năm (đồng)")
    p.add_argument("--loi-nhuan", type=float, help="Lợi nhuận trước thuế (đồng)")
    p.add_argument("--ty-le", type=float, default=1.5, help="Tỷ lệ %% trên doanh thu (vd 1.5 hoặc 0.015)")
    p.add_argument("--thue-suat", type=float, default=0.20, help="Thuế suất TNDN (vd 0.20)")
    p.add_argument("--json", action="store_true", help="Xuất JSON")
    p.add_argument("--self-test", action="store_true", help="Chạy kiểm tra nội bộ")
    args = p.parse_args(argv)

    if args.self_test:
        return self_test()

    if args.doanh_thu is None or args.loi_nhuan is None:
        p.error("Cần --doanh-thu và --loi-nhuan (hoặc dùng --self-test)")

    try:
        k = tinh(args.doanh_thu, args.loi_nhuan, args.ty_le, args.thue_suat)
    except ValueError as e:
        print(f"Lỗi: {e}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(asdict(k), ensure_ascii=False, indent=2))
    else:
        in_ket_qua(k)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
