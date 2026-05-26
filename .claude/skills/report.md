---
name: report
description: Tạo báo cáo thống kê file leads — coverage Website/Email, breakdown type/service, contact person stats
---

## Khi nào dùng
Khi người dùng yêu cầu: "báo cáo", "thống kê", "report leads", `/report`

## Thực thi
Đọc file .xlsx (ưu tiên `*_cleaned.xlsx`) và tạo báo cáo thống kê.

Nếu `$ARGUMENTS` là tên file .xlsx → dùng file đó.
Nếu `$ARGUMENTS` trống → tự tìm file `*_cleaned.xlsx` trong thư mục làm việc.

## Báo cáo gồm

| Chỉ số | Mô tả |
|--------|-------|
| Total leads | Tổng số công ty |
| Website coverage | Có / thiếu website |
| E-Mail coverage | Có / thiếu email |
| Đã phân loại | Note/Category != `n.a, n.a` |
| Breakdown type | Số lượng theo từng type |
| Breakdown service | Số lượng theo từng service |
| Contact person | Số công ty đã / chưa có contact |

## Cách dùng
```
/report
/report leads_cleaned.xlsx
```
