---
name: hdc-opendata
description: สืบค้นและดึงรายงานจาก HDC / MOPH Open Data API (opendata.moph.go.th) — ~970 รายงาน 50+ หมวด เช่น คัดกรองความดัน เบาหวาน ANC EPI ทันตกรรม KPI ตัวชี้วัด. Use when the user asks for Thai MOPH / HDC health data, กระทรวงสาธารณสุข, รายงาน HDC, ข้อมูลรายจังหวัด, opendata.moph.go.th, or names an s_* source table.
---

# HDC Open Data

API เปิดสาธารณะ ไม่มี token: `https://opendata.moph.go.th/api`
ใช้สคริปต์ในโฟลเดอร์นี้เสมอ อย่ายิง API ตรง (จัดการ 403/429/paging ให้แล้ว) — ไฟล์ละ endpoint รันเดี่ยวได้

รันด้วย `node` หรือ `bun` ก็ได้ ผลเหมือนกัน (งานติดเน็ต ไม่ติด runtime) — ไม่มีทั้งคู่ให้
**ขออนุมัติผู้ใช้ก่อน ห้ามติดตั้งเงียบ** แล้วค่อย `irm bun.sh/install.ps1|iex` (Windows)
หรือ `curl -fsSL https://bun.sh/install | bash` (mac/Linux)

## ตำแหน่ง workspace และ artifacts (ข้อบังคับ)

- ไฟล์ผลลัพธ์ที่สร้างทุกชนิด (HTML, XLSX, JSON, CSV, รูปภาพ และไฟล์รายงานชั่วคราว) ต้องอยู่ใน `<WORKSPACE>/artifacts/` เสมอ
- `<WORKSPACE>` คือโฟลเดอร์โปรเจกต์ของผู้ใช้ที่กำลังทำงานนี้ ให้ระบุพาธเต็มก่อนรันคำสั่ง และใช้เป็นโฟลเดอร์ทำงานตลอด แม้ skill จะติดตั้งอยู่ที่อื่น
- ห้ามสร้าง `artifacts/` ภายในโฟลเดอร์ติดตั้ง skill ทั้ง `.claude/skills/hdc-opendata/` และโฟลเดอร์ skill แบบ global ห้ามเปลี่ยนโฟลเดอร์ทำงานเข้าไปใน skill เพื่อรันสคริปต์
- กำหนด `SKILL_DIR` เป็นพาธเต็มของโฟลเดอร์ที่มี `SKILL.md` นี้ ตัวอย่างทั้งหมดด้านล่างต้องรันจาก `<WORKSPACE>` และเรียกสคริปต์ผ่าน `"$SKILL_DIR/scripts/..."` (PowerShell: `$SKILL_DIR = '<พาธเต็มของโฟลเดอร์ skill>'`; Bash: `SKILL_DIR='<พาธเต็มของโฟลเดอร์ skill>'`) ส่วน `data/` ที่มาพร้อม skill หมายถึงไฟล์ตารางอ้างอิงภายใน skill
- สร้าง `<WORKSPACE>/artifacts/` ก่อนใช้การเปลี่ยนทาง stdout ลงไฟล์ สคริปต์ HTML/XLSX สร้างโฟลเดอร์ผลลัพธ์ให้เอง โดยพาธเริ่มต้น `artifacts/` อ้างอิงจากโฟลเดอร์ทำงาน
- สคริปต์ HTML/XLSX ปฏิเสธพาธที่ออกนอก `artifacts/` และการใช้โฟลเดอร์ skill เป็น workspace หากตัวเรียกสคริปต์เปลี่ยนโฟลเดอร์ทำงานไม่ได้ ให้กำหนดตัวแปรสภาพแวดล้อม `HDC_WORKSPACE` เป็นพาธเต็มของ workspace ที่ใช้งานจริง
- ก่อนส่งลิงก์ไฟล์ให้ผู้ใช้ ตรวจสอบว่าพาธเต็มของไฟล์ผลลัพธ์อยู่ภายใน `<WORKSPACE>/artifacts/`

## ขั้นตอน

ดึงรายงานจาก API ล้วน ไม่มีการต่อฐานข้อมูล เดินตามลำดับ อย่าข้าม
**หาหมวด -> หาตารางในหมวด -> อ่าน schema -> ดึงข้อมูล -> เอา schema มาเป็นหัวตารางตอนนำเสนอ**
`data/` เป็น lookup ที่เอาไปประกอบกับรายงานที่ดึงมา (รหัส -> ชื่อ) ไม่ใช่แหล่งข้อมูลรายงาน

**1. หาตาราง — `get-category.mjs`** ค้นจาก `data/reports.csv` ที่ทำไว้ล่วงหน้า (API ไม่มี search endpoint)

```bash
node "$SKILL_DIR/scripts/get-category.mjs" search คัดกรอง ความดัน   # AND ทุกคำ -> source_table,report_name,category
node "$SKILL_DIR/scripts/get-category.mjs"                          # ลิสต์หมวดทั้งหมด + สรุปจำนวนสดจาก API
node "$SKILL_DIR/scripts/get-category.mjs" <cat_id>                 # ลิสต์รายงานในหมวด
node "$SKILL_DIR/scripts/get-category.mjs" build                    # สร้าง data/reports.csv ใหม่ (~30s)
node "$SKILL_DIR/scripts/get-category.mjs" url s_epi_p1_6            # URL รายงานบน HDC (default hdc.moph.go.th/plk, เปลี่ยนด้วย env HDC_BASE)
```

ถ้าได้หลายตาราง **เอารายชื่อมาถามผู้ใช้ก่อน อย่าเดา** — ชื่อคล้ายกันแต่นิยามคนละเรื่อง
(`s_ht_screen_pop_age` คัดกรองแยกกลุ่มอายุ vs `s_ht_screen_risk` เฉพาะกลุ่มเสี่ยง)

**2. อ่านนิยามคอลัมน์ — `get-schema.mjs`** จำเป็นเสมอ ชื่อคอลัมน์เป็น `pop_group3`/`result_group3` ล้วนๆ ตีความเองไม่ได้
คำอธิบายที่ได้คือหัวตารางของขั้น 4/5 ด้วย — ส่งชื่อตารางไปให้สคริปต์ แล้วมันไปดึง schema เอง

```bash
node "$SKILL_DIR/scripts/get-schema.mjs" s_ht_screen_pop_age
```

**3. ดึงข้อมูล — `get-data.mjs`** ปีงบประมาณไทย (≥2560) + จังหวัด (ชื่อไทยหรือรหัส) วน offset ให้ครบอัตโนมัติ

**ผู้ใช้ไม่บอกปี/จังหวัด → ไม่ต้องถาม** ละไว้ได้เลย default = ปีงบปัจจุบัน + พิษณุโลก (65)

```bash
node "$SKILL_DIR/scripts/get-data.mjs" s_ht_screen_pop_age                > artifacts/data.json  # = ปีงบนี้ + พิษณุโลก
node "$SKILL_DIR/scripts/get-data.mjs" s_ht_screen_pop_age csv            > artifacts/data.csv   # ข้ามปี/จังหวัดไปสั่ง csv ได้เลย
node "$SKILL_DIR/scripts/get-data.mjs" s_ht_screen_pop_age 2568 พิษณุโลก > artifacts/data.json
node "$SKILL_DIR/scripts/get-data.mjs" s_ht_screen_pop_age 2568 65 csv   > artifacts/data.csv   # แปลง csv ฝั่งเรา ไม่ใช่ type:csv ของ API
```

**4. นำเสนอผู้ใช้ — `make-report.mjs`** เขียน HTML (ตาราง sort/กรองได้ + กราฟแท่ง Chart.js จาก CDN) แล้วเปิด Chrome ให้เอง

**ทำ HTML เฉพาะเมื่อผู้ใช้สั่ง** (ขอรายงาน/dashboard/หน้าเว็บ/กราฟ/"เปิดให้ดู") ไม่สั่ง = ตอบในแชท อย่าสร้างไฟล์เอง
ถ้าข้อมูลยาวเกินพ่นลงแชท ให้สรุปแล้วเสนอ 1 บรรทัดว่า **จะแสดงเป็น dashboard ไหม** (อย่าถามว่า "ทำ HTML ให้ไหม" — ผู้ใช้ไม่ได้สนใจว่าเป็นไฟล์อะไร)
**ตำแหน่งไฟล์ให้ทำตามหัวข้อ ตำแหน่ง workspace และ artifacts ด้านบน**

```bash
node "$SKILL_DIR/scripts/get-data.mjs" s_ht_screen | node "$SKILL_DIR/scripts/make-report.mjs" s_ht_screen "คัดกรองความดัน · พิษณุโลก · ปีงบ 2569"
node "$SKILL_DIR/scripts/make-report.mjs" s_ht_screen artifacts/data.json ht.html "ชื่อรายงาน" --no-open   # -> artifacts/ht.html ไม่เปิด Chrome
node "$SKILL_DIR/scripts/get-data.mjs" s_ht_screen csv > artifacts/ht.csv            # json/csv ดิบก็ลง artifacts/ เหมือนกัน
```

- รวมรายอำเภอให้อัตโนมัติจาก `areacode` 4 หลักแรก (กราฟเป็นระดับอำเภอ ตารางยังเป็นราย hospcode)
- เลือกคอลัมน์ที่จะพล็อตได้จาก dropdown — ตรวจเองว่าคอลัมน์ไหนเป็นตัวเลข
- **ใส่ชื่อตาราง (`s_xxx`) เป็น argument = หัวตารางเป็นคำอธิบายไทยจาก schema** ไม่ใส่ = ได้ `pt_all_q1` ดิบๆ ที่ผู้ใช้อ่านไม่ออก
  (ชื่อคอลัมน์จริงอยู่ใน tooltip ของหัวตาราง · ดึง schema ไม่ได้ก็ไม่ล้ม ตกกลับไปใช้ชื่อดิบ)
- แปลงรหัสเป็นชื่อให้แล้ว (`areacode`→ตำบล ม.x, `hospcode`→ชื่อหน่วยบริการ, กราฟ→ชื่ออำเภอ) รหัสเดิมดูได้จาก tooltip
- ทำกราฟเองนอกสคริปต์นี้ก็ได้ แต่ **ซีรีส์เดียวห้ามใส่ legend** และห้ามแกน y สองแกน

**5. ขอ xlsx — `to-xlsx.mjs`** เขียน ZIP+OOXML เอง **ไม่ต้องลงอะไรเลย** มี node ก็พอ

**ห้ามใช้ skill xlsx ที่เป็น python และห้าม `npm i exceljs`** — skill นี้ต้องรันได้บนเครื่อง รพ.
ที่ไม่มี python ไม่มีเน็ต ลง lib ไม่ได้ อะไรที่ต้องติดตั้งก่อน = พังที่ปลายทาง

```bash
node "$SKILL_DIR/scripts/get-data.mjs" s_ht_screen | node "$SKILL_DIR/scripts/to-xlsx.mjs" s_ht_screen ht.xlsx "ชื่อชีต"   # -> artifacts/ht.xlsx
```

- **รหัสถูกเขียนเป็นข้อความเสมอ** (`inlineStr`) — นี่คือเหตุผลเดียวที่ต้องใช้ xlsx แทน csv
  เพราะ Excel เปิด csv แล้วตัด 0 นำหน้าทิ้ง `07574` → `7574` รหัสหน่วยบริการเพี้ยนทั้งไฟล์เงียบๆ
- เลขคงเป็นเลข, `null`/`''` เป็นช่องว่าง, ตรึงแถวหัวตารางให้แล้ว, ใส่ `s_xxx` ได้เหมือน make-report
- ถ้าจำเป็นต้องส่ง csv จริงๆ `get-data.mjs ... csv` เติม BOM (U+FEFF) ให้แล้ว (ไม่มี BOM = Excel อ่านไทยเป็นขยะ)
  แต่ยังต้องบอกผู้ใช้ให้ import ผ่าน Data > From Text ตั้งคอลัมน์รหัสเป็น Text — **ห้ามเงียบ** csv ไม่มีชนิดคอลัมน์ 0 นำหน้าหายอยู่ดี

**ตารางชื่อ — `data/areacode.csv` + `data/hospcode.csv`** (พิษณุโลกเท่านั้น) API ไม่มีชื่อเลย ทุกรายงานเป็นรหัสล้วน
ดัมพ์จาก HOSxP ในเครื่อง ไม่มีไฟล์ก็ยังรันได้ แค่โชว์เป็นรหัส — **อย่าเดาชื่อเอง**

`areacode.csv` = `code,amphoe,tambon` แถวละระดับอำเภอ (`xxxx00`) กับตำบล (`xxxxxx`) แต่ละแถวมีชื่ออำเภอกำกับครบ
**หมู่ที่ไม่ได้อยู่ในไฟล์** เพราะเป็น 2 หลักท้ายของ areacode อ่านตรงๆ ได้ 100% — ตารางหมู่บ้านในฐาน
(`thaiaddress_sub_hcode`) ครอบคลุมแค่ ~92% และ `area_name` ปนชื่อตำบลกับชื่อหมู่บ้าน ใช้เป็น lookup ไม่ได้

ไฟล์หายหรืออยากได้จังหวัดอื่น -> ดัมพ์เองจาก HOSxP ใน SQL query window: `thaiaddress` (กรอง `chwpart`=รหัสจังหวัด, `codetype` 2=อำเภอ 3=ตำบล) -> `code,amphoe,tambon` และตาราง `hospcode` -> `hospcode,name` เติมบรรทัดหัวตารางเอง สคริปต์ข้ามบรรทัดแรกเสมอ (ครั้งเดียว ไม่เกี่ยวกับการดึงรายงาน)

## ข้อควรรู้

- **ได้ทีละจังหวัด** — API บังคับ `province` หลายจังหวัดต้องวนเรียก
- **ข้อมูลระดับ hospcode** (รายสถานบริการ) ต้อง sum เองถ้าต้องการระดับจังหวัด/อำเภอ — `areacode` = รหัส มท. 8 หลัก (จังหวัด 2 + อำเภอ 2 + ตำบล 2 + หมู่บ้าน 2)
- **`b_year` คือปีงบประมาณ** (ต.ค.–ก.ย.) ไม่ใช่ปีปฏิทิน
- **ถ้าขึ้น `!` บน stderr อย่าเงียบ** — `ไม่มีข้อมูล` = ปี/จังหวัดผิด หรือรายงานยังไม่เปิดผ่าน API, `total ไม่ตรง` = ข้อมูลไม่ครบ ห้ามเอาไปสรุป
- **ค่า 0 ไม่ได้แปลว่าไม่มีข้อมูล** — อาจเป็นหน่วยบริการที่ยังไม่ส่ง ดู `date_com` ประกอบ
- search ไม่เจอทั้งที่ควรเจอ = index เก่า -> `node "$SKILL_DIR/scripts/get-category.mjs" build`
- self-check: `for f in get-data make-report to-xlsx; do node "$SKILL_DIR/scripts/$f.mjs" --check; done`
