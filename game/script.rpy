# =============================================================================
# script.rpy — จุดเริ่มเกม (label start) + ฉากเปิดเรื่อง
# =============================================================================
# ลำดับการไหลของเกมทั้งหมด:
#   start (ฉากเปิดจักรวาล) -> intro (ห้องบัญชาการ CATLOARD)
#   -> rama4_pre_minigame_story -> nz_mission (ด่านที่ 1 ใน rama4.rpy)
#   -> nextopia_start (ด่านที่ 2) -> lumpini_start (ด่านที่ 3) -> Lobby
#
# เพลงประกอบฉากเปิด: audio/1-RAMA_4_ROAD/
# ภาพฉากเปิด: images/story/1-RAMA_4_ROAD/ (ประกาศนามแฝงใน screens.rpy)
# =============================================================================

## ประกาศตัวละครทั้งหมดของเกม (สี = สีชื่อผู้พูดในกล่องข้อความ)
define e = Character("Director", color="#2a23a3")                    # ผู้บรรยาย
define CATLOARD = Character("CATLOARD", image="lord", color="#15d815")  # ผู้นำเผ่าแมว (ด่าน 1)
define PROF_NEXT = Character("PROF.NEXT", color="#15d815")           # ผู้ดูแลด่าน NEXTOPIA
define LUMI = Character("LUMI", color="#15d815")                     # ผู้ดูแลด่าน Lumpini


## เกมเริ่มที่นี่
label start:

    scene galaxy
    play music "audio/1-RAMA_4_ROAD/Sovereigns_of_the_Bamboo_Sky.mp3" fadeout 1

    e "ในกาแล็กซี่อันห่างไกล....!"

    scene antherworld

    e "มีดาวเคราะห์ดวงหนึ่งที่ปกครองโดยเผ่าพันธ์ุแมวผู้ทรงภูมิปัญญา..."

    scene meowgod

    e "พวกเขาคือ 'Bastian' ผู้สืบเชื้อสายมาจากแมวโบราณที่มีพลังวิเศษและความรู้ลึกลับ"

    scene citysimulation

    e "พวกเขาได้โลกจำลองที่เจริญรุ่งเรืองและมีเทคโนโลยีที่ล้ำสมัย
    ถอดแบบมาจากกรุงเทพมหานครในยุคปัจจุบัน"

    scene experiment

    e "เพื่อใช้เป็นสนามทดสอบสำหรับการทดลองทางวิทยาศาสตร์และการแก้ไขปัญหาสิ่งแวดล้อม"

    scene goals

    e "โดยมีเป้าหมายเพื่อสร้างสังคมที่ยั่งยืน และ ทำให้โลกนี้เป็น Net Zero ภายในปี 2050"

    # scene carbonmonster

    # e "แต่พวกเขาก็ต้องเผชิญกับความท้าทายมากมายมลพิษทางอากาศและการเปลี่ยนแปลง
    # สภาพภูมิอากาศอย่างรุนแรง"

    # e "และการปรากฏตัวของ 'Carbon Monster' สัตว์ประหลาดที่เกิดจากมลพิษทางอากาศ
    # และคาร์บอนที่สะสมในชั้นบรรยากาศ"

    jump intro
    return

label intro:

    stop music fadeout 1
    play music "audio/1-RAMA_4_ROAD/Temple_in_the_Stars.mp3"

    # แสดงฉากห้องบัญชาการผ่านนามแฝงภาพที่ประกาศไว้ใน screens.rpy
    scene operatorroom

    # อารมณ์ของตัวละครถูกผูกกับไฟล์ใน images/characters/
    # ผ่านนามแฝงภาพแท็ก "lord" ใน screens.rpy
    show lord happy at center

    # บทสนทนาแนะนำภารกิจ
    CATLOARD "ยินดีต้อนรับสู่... แมวอาสาดิจิทัล!"

    scene map
    show lord happy at left

    CATLOARD "ตอนนี้กรุงเทพมหานครกำลังถูกร 'อสูรคาร์บอน' รุกราน"

    scene trash
    show lord happy at left

    CATLOARD "มลพิษกำลังทำลายเมืองของเรา..."

    scene carbonmon
    show lord happy at left

    CATLOARD "พลังชีวิตของอสูรคาร์บอนจะขึ้นอยู่กับ carbon footprint ของดาวดวงนี้"

    scene sdg
    show lord happy at left

    CATLOARD "ภารกิจของคุณคือการพิชิต 17 ด่าน SDGs เพื่อช่วยลด carbon footprint และเอาชนะอสูรคาร์บอน!"

    scene carbonmonster
    show lord happy at left

    CATLOARD "ปราบอสูรคาร์บอนให้ได้ และกอบกู้สยามให้กลับมาเขียวขจีอีกครั้ง!"

    scene operatorroom
    show lord command at center

    CATLOARD "เจ้าพร้อมหรือยัง?"

    # หน้า command จบแล้วจึงเล่าเรื่อง RAMA 4 ROAD ตอนที่ 1-6 ตามลำดับ
    # ก่อนเข้าสู่ Sustainability Decision และมินิเกม
    call rama4_pre_minigame_story

    # จบช่วงอินโทร -> กระโดดเข้าสู่ระบบเกม Net Zero (ด่านที่ 1 ใน rama4.rpy)
    jump nz_mission
