# The script of the game goes in this file.

# -----------------------------------------------
# ประกาศตัวละคร
# -----------------------------------------------
define e       = Character("Director",    color="#2a23a3")
define catlord = Character("catlord",     image="catlord.png", color="#15d815")
define m       = Character("Meow Khiao",  color="#32CD32")
define c       = Character("อสูรคาร์บอน", color="#FF0000")

# -----------------------------------------------
# ตัวแปรเกม
# -----------------------------------------------
default carbon_monster_hp = 3

# -----------------------------------------------
# 1. ฟังก์ชัน Python สำหรับตรวจสอบการลากวาง
# -----------------------------------------------
init python:
    def trash_dropped(drags, drop):
        if not drop:
            return None
        return drop.drag_name

# -----------------------------------------------
# 2. Screen สำหรับมินิเกมลากขยะ
# -----------------------------------------------
screen trash_sorting_minigame(trash_item, trash_image):

    draggroup:

        # ถังสีเหลือง (รีไซเคิล)
        drag:
            drag_name "yellow_bin"
            child "bin_yellow.png"
            draggable False
            xpos 100 ypos 500

        # ถังสีเขียว (อินทรีย์)
        drag:
            drag_name "green_bin"
            child "bin_green.png"
            draggable False
            xpos 400 ypos 500

        # ถังสีแดง (อันตราย)
        drag:
            drag_name "red_bin"
            child "bin_red.png"
            draggable False
            xpos 700 ypos 500

        # ถังสีน้ำเงิน (ทั่วไป)
        drag:
            drag_name "blue_bin"
            child "bin_blue.png"
            draggable False
            xpos 1000 ypos 500

        # ขยะ (สิ่งที่ต้องลาก)
        drag:
            drag_name trash_item
            child trash_image
            droppable False
            dragged trash_dropped
            xpos 550 ypos 200


# ===============================================
# เริ่มต้นเกม — บทนำ (Bastian / Director)
# ===============================================
label start:

    scene scene_galaxy
    play music "Sovereigns_of_the_Bamboo_Sky.mp3" fadeout 1

    e "ในกาแล็กซี่อันห่างไกล....!"

    scene scene_antherworld

    e "มีดาวเคราะห์ดวงหนึ่งที่ปกครองโดยเผ่าพันธ์ุแมวทรงภูมิปัญญา..."

    scene scene_meowgod

    e "พวกเขาคือเผ่าพันธ์ 'Bastian' ผู้สืบเชื้อสายมาจากแมวโบราณที่ถือครองพลังวิเศษและความรู้ลึกลับมากมาย"

    scene scene_citysimulation

    e "พวกเขาได้สร้างโลกจำลองที่เจริญรุ่งเรืองและมีเทคโนโลยีที่ล้ำสมัยที่สุดในกาแล็กซี่... โดยโลกจำลองนี้ถูกตั้งชื่อว่า 'Meowkhiao' 
    ซึ่งเป็นเมืองที่ถอดแบบมาจากกรุงเทพมหานครในยุคปัจจุบัน"
    
    scene scene_experiment

    e "เพื่อใช้เป็นสนามทดสอบสำหรับการทดลองทางวิทยาศาสตร์เพื่อแก้ไขปัญหาสิ่งแวดล้อมที่เกิด 'Carbon Monster'"

    scene scene_goals

    e "โดยมีเป้าหมายเพื่อสร้างสังคมที่ยั่งยืน และ ทำให้โลกนี้กลายเป็น Net Zero ภายในปี 2050"

    jump intro


# ===============================================
# บทนำ — catlord อธิบายภารกิจ
# ===============================================
label intro:

    stop music fadeout 1
    play music "Temple_in_the_Stars.mp3"

    scene scene_operatorroom
    show lord happy at center

    catlord "ยินดีต้อนรับสู่... แมวอาสาดิจิทัล!"

    scene scene_map
    show lord happy at left

    catlord "ตอนนี้โลก(กรุงเทพมหานคร)กำลังถูก 'อสูรคาร์บอนที่แสนชั่วร้าย' รุกรานอย่างรุุนแรง!"

    scene scene_trash
    show lord happy at left

    catlord "มลพิษกำลังทำลายเมืองของเรา..."

    scene carbonmon
    show lord happy at left

    catlord "นั่นจึงเป็นเหตุผลที่ท่านถูกเรียกตัวมาที่นี่เพื่อช่วยพวกเราชาว 'Bastian' ต่อสู้กับอสูรคาร์บอน!"
    catlord "พลังชีวิตของอสูรคาร์บอนจะขึ้นอยู่กับ carbon footprint ของดาวดวงนี้"

    scene scene_sdg
    show lord happy at left

    catlord "ภารกิจของท่านคือการพิชิต 17 ด่าน SDGs เพื่อช่วยลด carbon footprint และเอาชนะอสูรคาร์บอน!"

    scene carbonmonster
    show lord happy at left

    catlord "ปราบอสูรคาร์บอนให้ได้ และกอบกู้สยามให้กลับมาเขียวขจีอีกครั้ง!"

    scene scene_operatorroom
    show lord command at center

    catlord "ท่านพร้อมหรือยัง?"

    jump gameplay_start


# ===============================================
# เริ่มเกมจริง — Meow Khiao vs อสูรคาร์บอน
# ===============================================
label gameplay_start:

    m "ในที่สุดก็มาถึงถนนพระราม 4... ที่นี่ขยะเกลื่อนกลาดไปหมดเลย!"
    c "ฮ่าๆๆ! ขยะพวกนี้แหละคือแหล่งพลังงานชั้นยอดของข้า!"
    m "เราต้องรีบแยกขยะให้ถูกต้อง ช่วยฉันลากขยะไปทิ้งให้ถูกถังทีนะ!"

    jump tutorial_1


# -----------------------------------------------
# ด่านที่ 1 — ขวดพลาสติกใส (PET)
# -----------------------------------------------
label tutorial_1:

    m "ชิ้นแรก! {b}ขวดพลาสติกใส (PET){/b} ลากไปทิ้งถังไหนดี?"

    call screen trash_sorting_minigame("plastic", "plastic_bottle.png")

    if _return == "yellow_bin":
        $ carbon_monster_hp -= 1
        m "ถูกต้อง! ขวดพลาสติกใสต้องทิ้งถังสีเหลืองเพื่อไปรีไซเคิล"
        c "อ๊ากก! พลังงานขยะของข้าลดลงไปแล้ว!"
    else:
        m "ผิดถังแล้วเมี้ยว! ขวดพลาสติกต้องทิ้งถังสีเหลืองนะ"
        c "ฮ่าๆๆ พลังของข้าแข็งแกร่งขึ้น!"

    jump tutorial_2


# -----------------------------------------------
# ด่านที่ 2 — แกนแอปเปิ้ล
# -----------------------------------------------
label tutorial_2:

    m "ชิ้นต่อไป... {b}แกนแอปเปิ้ล{/b} ลากไปทิ้งเลย!"

    call screen trash_sorting_minigame("apple", "apple.png")

    if _return == "green_bin":
        $ carbon_monster_hp -= 1
        m "เยี่ยมมาก! เศษอาหารทิ้งถังสีเขียวเพื่อไปทำปุ๋ยหมัก"
        c "กรอดดด... พลังงานของข้าหายไปอีกแล้ว!"
    else:
        m "ไม่ได้นะ! แกนแอปเปิ้ลย่อยสลายได้ ต้องทิ้งถังสีเขียว"
        c "อร่อยเลย! ขอบใจสำหรับพลังงาน!"

    jump tutorial_3


# -----------------------------------------------
# ด่านที่ 3 — ถ่านไฟฉายเก่า
# -----------------------------------------------
label tutorial_3:

    m "ชิ้นสุดท้าย! {b}ถ่านไฟฉายเก่า{/b} อันตรายนะเนี่ย!"

    call screen trash_sorting_minigame("battery", "battery_old.png")

    if _return == "red_bin":
        $ carbon_monster_hp -= 1
        m "เก่งมาก! ขยะอันตรายต้องทิ้งถังสีแดงเพื่อนำไปกำจัดอย่างถูกวิธี"
        c "ม่ายยยยย! พลังงานขยะของข้าหมดแล้ววว!"
    else:
        m "อันตราย! ถ่านไฟฉายมีสารพิษ ต้องทิ้งถังสีแดงเท่านั้นนะ"
        c "พลังความสกปรกจงเจริญ!"

    if carbon_monster_hp <= 0:
        jump victory
    else:
        jump game_over


# -----------------------------------------------
# ชนะ
# -----------------------------------------------
label victory:

    c "ฝากไว้ก่อนเถอะ เจ้าแมวอาสาดิจิทัล!"
    m "เย้! เรากำจัดอสูรคาร์บอนสำเร็จแล้ว!"
    return


# -----------------------------------------------
# แพ้
# -----------------------------------------------
label game_over:

    c "ฮ่าๆๆ! กรุงเทพฯ จะต้องจมอยู่ใต้กองขยะของข้า!"
    m "เมี๊ยว... เราจัดการขยะพลาดไป อสูรคาร์บอนเลยชนะ"
    return
