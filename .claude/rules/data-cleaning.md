---
description: Quy tắc normalize dữ liệu Excel — áp dụng khi chỉnh sửa normalizer, excel_handler, hoặc tags
globs:
  - "src/normalizer.py"
  - "src/excel_handler.py"
  - "src/tags.py"
alwaysApply: false
---

# Rules: Data Cleaning & Normalization

## Template chuẩn đầu ra
Thứ tự cột bắt buộc:
```
Company Name | Street | City | Zip | Website | Phone | E-Mail | Contact Person | Position | Contact Email | Contact Phone | Note / Category
```

Cột `Contact Person | Position | Contact Email | Contact Phone` được điền bởi `/contact` (sau bước clean + classify). Mỗi contact person = 1 dòng riêng; dữ liệu công ty được copy lại.

## Quy tắc điền dữ liệu thiếu
- Bất kỳ ô nào trống (kể cả khoảng trắng) → điền `n.a`
- Không để ô trống trong file output

## Quy tắc chuẩn hóa format
- **Company Name**: giữ nguyên tên đầy đủ theo hồ sơ chính thức
- **E-Mail**: viết thường toàn bộ (`INFO@example.com` → `info@example.com`)
- **Phone**: giữ định dạng dễ đọc, thống nhất trong file
- **Website**: ưu tiên domain chính thức
- **City / Street / Zip**: tách đúng trường, không gộp nhiều trường vào một ô
- Strip tất cả khoảng trắng thừa đầu/cuối mỗi ô

## Highlight vàng
Tô nền `#FFD966` cho ô nếu:
- Cột **Website** có giá trị `n.a`
- Cột **E-Mail** có giá trị `n.a`

Các cột khác nếu thiếu: chỉ điền `n.a`, không highlight.

## Output
- Sheet 1 "Data": dữ liệu đã làm sạch, đúng thứ tự cột
- Sheet 2 "Deleted Data": ghi lại ô có nội dung thực bị xóa/mất
- Backup file gốc trước khi xử lý

## Deleted Data log (Sheet 2 "Deleted Data")
Cột: `# | Row | Company Name | Field | Old Value | New Value | Highlighted`
- Chỉ ghi khi ô từng có nội dung thực (không phải ô trống) → bị mất/xóa thành n.a
- Trong vận hành bình thường sheet này sẽ rỗng (safety net phát hiện lỗi)
- Cột `Highlighted` = `yes` nếu ô đó thuộc cột Website hoặc E-Mail
