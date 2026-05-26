---
name: clean
description: Làm sạch file .xlsx — backup, normalize dữ liệu, tô vàng ô thiếu Website/Email, ghi change log
---

## Khi nào dùng
Khi người dùng yêu cầu: "làm sạch file", "clean data", "xử lý file leads", `/clean`

## Xác định file input

Nếu `$ARGUMENTS` là tên file .xlsx → dùng file đó làm input, không hỏi thêm.

Nếu `$ARGUMENTS` trống:
1. Dùng `Glob` tìm tất cả `*.xlsx` trong thư mục project
2. Loại bỏ file có `_backup_` hoặc `_cleaned` trong tên
3. Không tìm thấy → báo lỗi và dừng
4. Chỉ 1 file → hiển thị tên, hỏi xác nhận trước khi tiếp tục
5. Nhiều file → hiển thị danh sách đánh số, hỏi người dùng chọn:

```
Tìm thấy các file có thể xử lý:
  1. leads_Q1.xlsx
  2. leads_Q2.xlsx

Bạn muốn clean file nào? (nhập số)
```

## Thực thi
Sau khi xác định file input, gọi agent `cleaner` để thực thi toàn bộ pipeline theo logic trong `.claude/agents/cleaner.md`.

## Cách dùng
```
/clean
/clean leads.xlsx
/clean leads.xlsx --output leads_cleaned.xlsx
```
