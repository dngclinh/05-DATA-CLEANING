---
description: Schema chuẩn 12 cột cho file Excel output — áp dụng mọi lúc khi đọc/ghi dữ liệu trong project này
alwaysApply: true
---

# Rules: Output Schema

## Thứ tự cột bắt buộc (12 cột)

```
Company Name | Street | City | Zip | Website | Phone | E-Mail | Contact Person | Position | Contact Email | Contact Phone | Note / Category
```

4 cột contact (`Contact Person | Position | Contact Email | Contact Phone`) được điền bởi `/contact`. Mỗi contact person = 1 dòng riêng; toàn bộ dữ liệu công ty được copy lại trên dòng đó.

## Quy tắc giá trị thiếu

- Bất kỳ ô nào trống (kể cả chỉ có khoảng trắng) → điền `n.a`
- Không để ô trống trong file output

## Quy tắc format từng cột

| Cột | Quy tắc |
|-----|---------|
| **Company Name** | Giữ nguyên tên đầy đủ theo hồ sơ chính thức |
| **E-Mail** | Lowercase toàn bộ; xóa obfuscation (`[@]` → `@`, `[.]` → `.`) |
| **Contact Email** | Lowercase; chỉ email cá nhân — không dùng email chung (info@, kontakt@) |
| **Phone** | International format qua `phonenumbers` lib (ví dụ: `+49 30 12345678`) |
| **Contact Phone** | Cùng format với Phone |
| **Website** | Domain chính thức, không trailing slash |
| **City / Street / Zip** | Tách đúng từng trường, không gộp vào một ô |
| **Note / Category** | Format: `type, service` (ví dụ: `Consultant, Structural`) hoặc `n.a, n.a` |

Strip tất cả khoảng trắng thừa đầu/cuối mỗi ô.

## Highlight vàng (#FFD966)

Tô nền vàng nếu:
- Cột **Website** = `n.a`
- Cột **E-Mail** = `n.a`

Các cột khác nếu thiếu: chỉ điền `n.a`, **không** highlight.

## Cấu trúc file output

- **Sheet 1 "Data"**: dữ liệu đã làm sạch, đúng thứ tự 12 cột, yellow highlight
- **Sheet 2 "Deleted Data"**: log các ô bị xóa nội dung thực
  - Cột: `# | Row | Company Name | Field | Old Value | New Value | Highlighted`
  - Chỉ ghi khi ô từng có nội dung thực → bị mất thành `n.a`
  - Cột `Highlighted` = `yes` nếu ô đó thuộc Website hoặc E-Mail
  - Trong vận hành bình thường sheet này rỗng (safety net)
