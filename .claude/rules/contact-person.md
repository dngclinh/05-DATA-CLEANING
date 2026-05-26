---
description: Quy tắc tìm và ghi contact person vào file Excel — áp dụng khi chạy /contact
globs:
  - ".claude/agents/contact-finder.md"
alwaysApply: false
---

# Rules: Contact Person

## Điều kiện xử lý một công ty

Chỉ xử lý khi:
- `Website` != `n.a`
- `Contact Person` == `n.a` (chưa tìm contact)

Gom các rows theo `Company Name` — mỗi công ty chỉ xử lý 1 lần (dùng dòng đầu tiên làm đại diện).

## Nguồn tìm kiếm (theo thứ tự ưu tiên)

**Trên website công ty:**
1. `/team` hoặc `/our-team`
2. `/management` hoặc `/geschaeftsfuehrung` / `/geschäftsführung`
3. `/vorstand`
4. `/ueber-uns` hoặc `/about` hoặc `/unternehmen` (tìm section leadership)
5. Homepage (footer hoặc section giới thiệu ban lãnh đạo)

**Google search (nếu website không đủ):**
- `"[Company Name]" Geschäftsführer`
- `"[Company Name]" CEO`
- Đọc snippet — nếu tên + chức vụ rõ ràng → lấy trực tiếp, không cần click

## Chức vụ được chấp nhận (senior only)

✅ **Lấy:** CEO, CFO, CTO, COO, Geschäftsführer, Inhaber, Eigentümer, Gesellschafter, Director, Direktor, Manager, Leiter, Head of [...], Partner, Vorstand, Founder, Co-Founder

❌ **Bỏ qua:** nhân viên thông thường, trợ lý, intern, Sachbearbeiter

Tối đa 3–7 contacts mỗi công ty, ưu tiên chức vụ cao nhất trước.

## Cách ghi vào file (mỗi contact = 1 dòng)

**Tìm được N contacts:**
- Contact 1 → cập nhật dòng gốc của công ty (4 ô: Contact Person, Position, Contact Email, Contact Phone)
- Contact 2..N → chèn dòng mới ngay bên dưới, copy toàn bộ dữ liệu công ty (Company Name, Street, City, Zip, Website, Phone, E-Mail, Note / Category), chỉ thay 4 ô contact

**Không tìm được ai:**
- Giữ nguyên dòng gốc, 4 ô contact giữ `n.a`

## Quy tắc điền 4 cột contact

| Cột | Quy tắc |
|-----|---------|
| **Contact Person** | Tên đầy đủ |
| **Position** | Chức vụ dịch sang **tiếng Anh** theo bảng dịch trong `agents/contact-finder.md` (ví dụ: Geschäftsführer → Managing Director) |
| **Contact Email** | Email cá nhân (`firstname@domain`) — **không** dùng `info@`, `kontakt@` |
| **Contact Phone** | Số trực tiếp nếu có, `n.a` nếu không tìm được |

- Contact Email → lowercase
- Chỉ điền khi tìm thấy — điền `n.a` cho field nào không có
- Không suy đoán, không điền khi bằng chứng không rõ ràng

Lưu file sau mỗi 5 công ty (tính theo số công ty, không phải số dòng).
