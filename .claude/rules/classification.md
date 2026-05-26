---
description: Quy tắc phân loại type/service cho công ty xây dựng Đức — áp dụng khi chạy /classify hoặc chỉnh sửa tagger
globs:
  - ".claude/agents/tagger.md"
  - "src/tags.py"
alwaysApply: false
---

# Rules: Type & Service Classification

## Format ghi vào cột Note / Category
```
type, service
```
Ví dụ: `Consultant, Structural` | `Contractor, Infra` | `Developer, Building`

Nếu không xác định được: `n.a, n.a`

---

## TYPE — Danh sách và dấu hiệu nhận biết

### Developer
Chủ đầu tư / phát triển dự án, mua đất, bán/cho thuê.
Từ khóa: project developer, real estate developer, Projektentwickler.
**Không** gán nếu chỉ thi công cho chủ đầu tư khác.

### Contractor
Nhận hợp đồng thi công, xây dựng, lắp đặt.
Từ khóa: construction, installation, EPC, fit-out, execution, fabrication, turnkey.
**Không** gán nếu chủ yếu tư vấn thiết kế.

### Consultant
Tư vấn kỹ thuật, thiết kế, quản lý dự án — không thi công.
Từ khóa: engineering, consulting, design, planning, advisory, Ingenieurbüro, Planungsbüro.
**Mặc định** cho đơn vị tư vấn kỹ thuật chưa rõ hơn.

### General Planner
Điều phối toàn bộ thiết kế đa bộ môn.
Từ khóa: Generalplanung, general planning, alle Leistungsphasen HOAI, điều phối kiến trúc + kết cấu + MEP.
Ưu tiên hơn `Consultant` nếu có vai trò điều phối tổng thể.

### Freelancer
Cá nhân hành nghề độc lập hoặc văn phòng 1–2 người.
Từ khóa: self-employed, freiberuflich, independent consultant.
**Không** dùng cho công ty tư vấn thông thường dù website nhỏ.

### Housing Association
Quản lý / cung cấp nhà ở xã hội, hợp tác xã.
Từ khóa: Genossenschaft, Wohnungsbaugesellschaft, municipal housing.
Phân biệt với `Developer`: thiên về quản lý lâu dài, không phải thương mại hóa.

### Prefab Manufacturer
Sản xuất cấu kiện đúc sẵn tại nhà máy.
Từ khóa: Fertigteile, Betonfertigteile, Betonwerk, Produktion.
**Không** dùng nếu chỉ lắp dựng prefab ngoài công trường.

### Steel Manufacturer
Sản xuất thép thô / thép hình / cấu kiện thép tại nhà máy.
Từ khóa: Stahlhersteller, Stahlwerk, cán thép tại nhà máy.
**Không** dùng cho thi công kết cấu thép tại công trường.

### Software Company
Sản phẩm chính là phần mềm ngành xây dựng.
Từ khóa: BIM software, CAD, ERP, SaaS, demo, trial, pricing page.

---

## Thứ tự ưu tiên TYPE khi bị chồng lấn
1. Software Company
2. Housing Association
3. Developer
4. Prefab Manufacturer
5. Steel Manufacturer
6. General Planner
7. Contractor
8. Consultant
9. Freelancer

---

## SERVICE — Danh sách và dấu hiệu nhận biết

| Service | Từ khóa chính |
|---------|--------------|
| Architectural | Architektur, architectural design, concept design, master planning |
| Structural | Tragwerksplanung, structural engineering, Statik, concrete/steel structure |
| MEP | TGA, Haustechnik, mechanical, electrical, plumbing, HVAC, sanitary |
| Civil | Tiefbau, civil engineering, drainage, water, sewer, earthworks |
| Geotechnical | Geotechnik, Bodenmechanik, soil investigation, foundation engineering |
| Energy Consulting | Energieberatung, Energieeffizienz, GEG, EnEV, energy performance |
| Scan to BIM | Laserscanning, Scan to BIM, point cloud, Punktwolke |
| Timber Construction | Holzbau, Holzrahmenbau, timber engineering, CLT |
| Steel Construction | Stahlbau, steel construction, steel frame (thi công, không phải sản xuất) |
| Facade | Fassadenbau, Fassadenplanung, facade engineering, curtain wall |
| Infra | Infrastruktur, Verkehrswegebau, Brückenbau, Straßenbau, Tunnelbau |
| Building | Nhà ở, văn phòng, khách sạn, mixed-use (khi không rõ discipline cụ thể) |
| Industrial | Nhà máy, kho, logistics, production facility |
| Data Center | Rechenzentrum, Datacenter, Tier certification |

## Thứ tự ưu tiên SERVICE khi nhiều service cùng lúc
1. Scan to BIM, Energy Consulting, Facade, Geotechnical
2. Timber Construction, Steel Construction
3. Structural, MEP, Civil
4. Architectural
5. Infra
6. Building, Industrial, Data Center

## Nguồn đọc để xác định type/service (theo thứ tự ưu tiên)
1. Services / Leistungen trên website
2. Portfolio / Projects / Referenzen
3. About / Company profile
4. LinkedIn / Xing
5. Tên công ty (chỉ gợi ý, không dùng làm căn cứ chính)

## Lưu ý quan trọng
- `Architectural` là **service**, không phải type
- Văn phòng kiến trúc → `Consultant, Architectural` hoặc `Freelancer, Architectural`
- Không dùng `Architect` làm type
- Nếu không xác định được rõ → `n.a, n.a`
