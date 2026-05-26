---
name: contact
description: Tìm contact person cấp cao (CEO, Managing Director, Owner) cho từng công ty — mỗi người một dòng trong file Excel
---

## Khi nào dùng
Khi người dùng yêu cầu: "tìm contact person", "tìm người liên hệ", "find contacts", `/contact`

## Xác định file input

Nếu `$ARGUMENTS` là tên file .xlsx → dùng file đó làm input, không hỏi thêm.

Nếu `$ARGUMENTS` trống:
1. Dùng `Glob` tìm tất cả `*_cleaned.xlsx` trong thư mục (ưu tiên file đã qua clean)
2. Nếu không có `_cleaned.xlsx` → tìm tất cả `*.xlsx`, loại trừ file có `_backup_` trong tên
3. Không tìm thấy → báo lỗi và dừng
4. Chỉ 1 file → hiển thị tên, hỏi xác nhận trước khi tiếp tục
5. Nhiều file → hiển thị danh sách đánh số, hỏi người dùng chọn

## Thực thi
Sau khi xác định file input, gọi agent `contact-finder` để tìm contact persons theo logic trong `.claude/agents/contact-finder.md`.

## Cách dùng
```
/contact
/contact leads_cleaned.xlsx
```
