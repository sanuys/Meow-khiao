# วิธีการโคลน Github และดาวน์โหลด Ren'Py

1. เตรียมเครื่องมือ
   - ติดตั้ง Git จาก https://git-scm.com/downloads
   - ดาวน์โหลด Ren'Py จาก https://www.renpy.org/latest.html

2. โคลน repository เกม
   - เปิด Terminal หรือ Command Prompt
   - รันคำสั่ง:
     ```bash
     git clone <https://github.com/sanuys/Meow-khiao.git>
     ```
   - เข้าไปยังโฟลเดอร์เกม:
     ```bash
     cd <ชื่อโฟลเดอร์>
     ```

3. ดาวน์โหลดและติดตั้ง Ren'Py
   - แตกไฟล์ Ren'Py ที่ดาวน์โหลดมา
   - เปิดโฟลเดอร์ Ren'Py
   - รันโปรแกรม Ren'Py Launcher

4. เล่นเกม "Meow khiao"
   - ใน Ren'Py Launcher คลิก "Launch Project" หรือเลือกโฟลเดอร์เกม
   - เลือกโปรเจกต์ "Meow khiao" แล้วกดเล่น

5. หมายเหตุ
   - หากไม่แน่ใจ URL ของ Github ให้ไปที่หน้า repository และคัดลอกลิงก์จากปุ่ม "Code"
   - ถ้าเกมมีไฟล์เพิ่มเติม ให้แน่ใจว่าได้ดาวน์โหลดและวางไว้ในโฟลเดอร์โปรเจกต์ก่อนรัน
  
## 🛠️ Third-Party Libraries & Open Source Credits

**"มินิเกมจับจังหวะดนตรี (Rhythm Game Mini-game)"** สำหรับภารกิจพื้นที่ Landmark สวนลุมพินีและถนนพระราม 4 ทีมผู้พัฒนาได้นำระบบ Core Framework มาพัฒนาต่อยอดจากโครงการ Open Source ดังนี้:

### 🎵 Ren'Py Rhythm Game Framework
* **ผู้พัฒนาต้นฉบับ:** RuolinZheng08
* **ลิงก์โครงการต้นฉบับ:** [GitHub - RuolinZheng08/renpy-rhythm](https://github.com/RuolinZheng08/renpy-rhythm.git)
* **สิทธิ์การใช้งาน (License):** MIT License
* **การนำมาประยุกต์ใช้และพัฒนาต่อยอดในโปรเจกต์นี้:**
    1. นำระบบ Core Engine (`00-renpy-rhythm`) มาใช้เป็นตัวขับเคลื่อนตำแหน่งโน้ตและระบบหน้าจอมินิเกม
    2. ออกแบบและปรับปรุงสไตล์หน้าจอผู้ใช้งาน (User Interface & Graphics) ใหม่ทั้งหมดเพื่อให้สอดคล้องกับธีมหลักของเกม Meow Khiao
    3. สร้างไฟล์แผนที่โน้ตจับจังหวะดนตรี (`.beatmap.txt`) ขึ้นมาใหม่ด้วยตนเอง เพื่อให้ตรงกับจังหวะของบทเพลงที่ใช้ประกอบฉากปราบอสูรคาร์บอน
    4. เขียนสคริปต์ Python เพิ่มเติมเพื่อเชื่อมต่อและส่งค่าคะแนนกลับเข้าสู่เนื้อเรื่องหลัก (Story Interaction) เพื่อใช้คำนวณผลกระทบต่อสิ่งแวดล้อมภายในเกม

---

