---
name: classify
description: Enrich thông tin contact còn thiếu và gán tag type/service cho công ty bằng cách đọc website
---

## Khi nào dùng
Khi người dùng yêu cầu: "gán tag", "classify", "phân loại công ty", `/classify`

## Xác định file input

Nếu `$ARGUMENTS` là tên file .xlsx → dùng file đó làm input, không hỏi thêm.

Nếu `$ARGUMENTS` trống:
1. Dùng `Glob` tìm tất cả `*_cleaned.xlsx` trong thư mục (ưu tiên file đã qua clean)
2. Nếu không có `_cleaned.xlsx` → tìm tất cả `*.xlsx`, loại trừ file có `_backup_` trong tên
3. Không tìm thấy → báo lỗi và dừng
4. Chỉ 1 file → hiển thị tên, hỏi xác nhận trước khi tiếp tục
5. Nhiều file → hiển thị danh sách đánh số, hỏi người dùng chọn:

```
Tìm thấy các file có thể phân loại:
  1. leads_Q1_cleaned.xlsx
  2. leads_Q2_cleaned.xlsx

Bạn muốn classify file nào? (nhập số)
```

## Thực thi
Sau khi xác định file input, gọi agent `tagger` để thực thi toàn bộ enrich + classify theo logic trong `.claude/agents/tagger.md`.

## Cách dùng
```
/classify
/classify leads_cleaned.xlsx
```
