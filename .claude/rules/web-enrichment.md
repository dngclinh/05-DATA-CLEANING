---
description: Quy tắc truy cập website để enrich thông tin contact và phân loại công ty — áp dụng khi chạy /classify
globs:
  - ".claude/agents/tagger.md"
alwaysApply: false
---

# Rules: Web Enrichment

## Điều kiện xử lý một row

Chỉ xử lý row khi `Website` != `n.a` **VÀ** ít nhất một trong:
- `Note / Category` == `n.a, n.a` hoặc trống → cần classify
- Bất kỳ field nào trong `Phone | E-Mail | Street | City | Zip` == `n.a` → cần enrich

Row đã có đủ data và đã classify → bỏ qua.

## Bước 1: Enrich contact info

Truy cập theo thứ tự ưu tiên — dừng khi đã điền đủ các field còn thiếu:

1. `/impressum` hoặc `/impressum.html` ← **ưu tiên cao nhất** (công ty Đức bắt buộc có địa chỉ + phone + email ở đây)
2. `/kontakt` hoặc `/contact`
3. Homepage — đọc footer

| Field | Quy tắc lấy |
|-------|-------------|
| **Phone** | Số đầu tiên tìm thấy, ưu tiên số có mã vùng |
| **E-Mail** | Email liên hệ chung (`info@`, `kontakt@`) — ưu tiên hơn email cá nhân |
| **Street** | Tên đường + số nhà |
| **City** | Thành phố |
| **Zip** | Mã bưu chính (5 chữ số Đức) |

Chỉ điền khi tìm thấy giá trị rõ ràng. Giữ `n.a` nếu không tìm thấy — **không suy đoán**.

**Lưu ý:** `/impressum` thường chứa thêm thông tin services → đọc luôn để hỗ trợ bước classify.

## Bước 2: Classify type/service

Truy cập theo thứ tự:

1. `/services` hoặc `/leistungen`
2. `/about` hoặc `/ueber-uns` hoặc `/unternehmen`
3. `/projects` hoặc `/referenzen` hoặc `/portfolio`

Áp dụng `.claude/rules/classification.md` để xác định `type` và `service`.
Ghi kết quả vào `Note / Category`: `type, service`.

Nếu không xác định được → ghi `n.a, n.a`.

## Xử lý lỗi

Website không load (timeout, 403, 404, connection error):
- Giữ nguyên các field contact đang là `n.a`
- Ghi `n.a, n.a` vào `Note / Category` nếu chưa classify
- Tiếp tục row tiếp theo — **không retry**

## Nguyên tắc chung

- Thà ghi `n.a` còn hơn điền sai — không suy diễn khi bằng chứng yếu
- Đọc Services/Leistungen và Portfolio **trước** About khi classify
- Lưu file sau mỗi 5 công ty để tránh mất dữ liệu
