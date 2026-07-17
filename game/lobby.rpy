# =============================================================================
# LOBBY — ศูนย์บัญชาการของเกม (Hub กลางเชื่อมทุกด่าน)
# =============================================================================
# หน้าที่ของไฟล์นี้:
#   - หน้า Lobby หลัง/ระหว่างภารกิจ: Inventory, External Learning Connection,
#     Mission & Stage Progression, SDG Knowledge และ Achievement Database
#   - แผงข้อมูลและปุ่มทั้งหมดวาดด้วยโค้ด (code-native UI) โดยอ่านค่าจริงจาก
#     ระบบกลางใน sustainability_core.rpy จึงไม่มีข้อมูลรางวัล/ความคืบหน้าคลาดเคลื่อน
#
# ตำแหน่ง asset ที่ใช้:
#   - พื้นหลัง Lobby : images/lobby/lobby_command_center.png
#   - ตัวละครหลัก   : images/lobby/main_character.png
# =============================================================================

## ภาพพื้นหลังและตัวละครของ Lobby (มี fallback: หากไฟล์รูปหายเกมยังเปิดได้
## โดยแสดงพื้นสีเข้มแทน เพื่อไม่ให้ runtime error)
init python:
    if renpy.loadable("images/lobby/lobby_command_center.png"):
        renpy.image(
            "mk lobby command center",
            Transform("images/lobby/lobby_command_center.png", xysize=(1920, 1080)),
        )
    else:
        renpy.image(
            "mk lobby command center",
            Transform(Solid("#0b1220"), xysize=(1920, 1080)),
        )

    if renpy.loadable("images/lobby/main_character.png"):
        renpy.image("mk lobby main character", "images/lobby/main_character.png")
    else:
        renpy.image("mk lobby main character", Null())


init -7 python:
    MK_LOBBY_STAGES = ("rama4", "nextopia", "lumpini")

    MK_LOBBY_MODULES = {
        "inventory": {
            "number": "01",
            "title": "INVENTORY DATABASE MANAGEMENT",
            "subtitle": "คลังไอเทมและหลักฐานการเรียนรู้",
            "accent": "#22d3ee",
        },
        "connections": {
            "number": "02",
            "title": "EXTERNAL LEARNING CONNECTION SYSTEM",
            "subtitle": "สถานที่จริงและเครือข่ายภาครัฐ",
            "accent": "#60a5fa",
        },
        "progress": {
            "number": "03",
            "title": "MISSION & STAGE PROGRESSION SYSTEM",
            "subtitle": "ติดตามภารกิจ การตัดสินใจ และ Carbon HP",
            "accent": "#4ade80",
        },
        "knowledge": {
            "number": "04",
            "title": "SDG KNOWLEDGE DATABASE SYSTEM",
            "subtitle": "ฐานความรู้ SDG และการลดคาร์บอน",
            "accent": "#facc15",
        },
        "achievements": {
            "number": "05",
            "title": "ACHIEVEMENT & SUSTAINABILITY DATABASE",
            "subtitle": "Badge, Meow Coin และ Eco Score",
            "accent": "#ef4444",
        },
    }

    MK_SDG_SUMMARIES = (
        ("SDG 1", "ยุติความยากจนทุกรูปแบบ"),
        ("SDG 2", "ยุติความหิวโหยและส่งเสริมเกษตรกรรมยั่งยืน"),
        ("SDG 3", "สร้างหลักประกันสุขภาพและความเป็นอยู่ที่ดี"),
        ("SDG 4", "การศึกษาที่มีคุณภาพ เท่าเทียม และเรียนรู้ตลอดชีวิต"),
        ("SDG 5", "ความเท่าเทียมทางเพศและการเสริมพลังทุกคน"),
        ("SDG 6", "น้ำสะอาดและสุขาภิบาลที่จัดการอย่างยั่งยืน"),
        ("SDG 7", "พลังงานสะอาดที่ทุกคนเข้าถึงได้"),
        ("SDG 8", "งานที่มีคุณค่าและการเติบโตทางเศรษฐกิจ"),
        ("SDG 9", "อุตสาหกรรม นวัตกรรม และโครงสร้างพื้นฐานที่ยืดหยุ่น"),
        ("SDG 10", "ลดความเหลื่อมล้ำภายในและระหว่างประเทศ"),
        ("SDG 11", "เมืองและชุมชนปลอดภัย ยืดหยุ่น และยั่งยืน"),
        ("SDG 12", "การผลิตและการบริโภคที่รับผิดชอบ"),
        ("SDG 13", "รับมือการเปลี่ยนแปลงสภาพภูมิอากาศ"),
        ("SDG 14", "อนุรักษ์และใช้ประโยชน์จากทะเลอย่างยั่งยืน"),
        ("SDG 15", "ปกป้องระบบนิเวศบนบกและความหลากหลายทางชีวภาพ"),
        ("SDG 16", "สังคมสงบสุข ยุติธรรม และสถาบันที่เข้มแข็ง"),
        ("SDG 17", "หุ้นส่วนความร่วมมือเพื่อบรรลุเป้าหมาย"),
    )

    def mk_lobby_snapshot():
        try:
            return mk_progress_snapshot()
        except Exception:
            s = renpy.store
            return {
                "coins": int(getattr(s, "mk_meow_coins", 0)),
                "eco_score": int(getattr(s, "mk_eco_score", 0)),
                "badges": list(getattr(s, "mk_sdg_badges", [])),
                "inventory": list(getattr(s, "mk_inventory", [])),
                "completed_stages": [],
                "decisions": {},
                "stage_hp": {},
            }

    def mk_lobby_stage_row(stage_id):
        config = mk_stage_config(stage_id)
        decision = mk_get_stage_decision(stage_id)
        return {
            "id": stage_id,
            "title": config["title"] if config else stage_id.upper(),
            "sdg": config["sdg"] if config else "",
            "badge": config["badge"] if config else "-",
            "completed": mk_has_completed_stage(stage_id),
            "rewarded": mk_has_stage_reward(stage_id),
            "decision": decision,
            "start_hp": mk_get_stage_start_hp(stage_id),
            "current_hp": mk_get_stage_current_hp(stage_id),
        }

    def mk_lobby_inventory_rows():
        rows = []
        for item in mk_lobby_snapshot().get("inventory", []):
            if isinstance(item, dict):
                rows.append({
                    "id": str(item.get("id", "ITEM")),
                    "type": str(item.get("type", "mission_item")),
                    "name": str(item.get("name", item.get("badge", "Mission Item"))),
                    "stage": str(item.get("stage_id", "-")),
                })
            else:
                rows.append({"id": str(item), "type": "mission_item", "name": str(item), "stage": "-"})
        return rows


transform mk_lobby_card_hover:
    on idle:
        alpha 0.94
    on hover:
        alpha 1.0
        linear 0.12 zoom 1.015
    on idle:
        linear 0.12 zoom 1.0


screen mk_lobby_module_button(module_id, xpos_value, ypos_value, width_value=520, height_value=174):
    $ module = MK_LOBBY_MODULES[module_id]

    button:
        xpos xpos_value
        ypos ypos_value
        xsize width_value
        ysize height_value
        background Solid("#061522eb")
        hover_background Solid("#0b2638f5")
        padding (28, 22)
        action Show("mk_lobby_module_screen", module_id=module_id)
        at mk_lobby_card_hover

        fixed:
            add Solid(module["accent"], xsize=8, ysize=height_value - 44) xpos 0 ypos 0
            text module["number"]:
                xpos 30
                ypos 2
                size 45
                color module["accent"]
                bold True
            text module["title"]:
                xpos 112
                ypos 3
                xmaximum width_value - 150
                size 24
                color "#f8fafc"
                bold True
            text module["subtitle"]:
                xpos 112
                ypos 78
                xmaximum width_value - 150
                size 22
                color "#cbd5e1"


screen mk_lobby_dashboard():
    tag mk_lobby
    modal True

    $ snapshot = mk_lobby_snapshot()
    $ completed_count = len(snapshot.get("completed_stages", []))
    $ decision_count = len(snapshot.get("decisions", {}))

    add "mk lobby command center"
    add Solid("#020b16a0")

    # Native 282x434 transparent artwork. Its centre column stays clear of all
    # side modules and ends above the Live Mission Database panel.
    add "mk lobby main character":
        xpos 960
        xanchor 0.5
        ypos 282

    frame:
        xpos 38
        ypos 28
        xsize 1844
        ysize 132
        background Solid("#061522ee")
        padding (32, 20)

        fixed:
            text "MEOW KHIAO SUSTAINABILITY COMMAND":
                xpos 0
                ypos 0
                size 42
                color "#86efac"
                bold True
            text "ระบบฐานข้อมูลภารกิจและการเรียนรู้เพื่ออนาคตที่ยั่งยืน":
                xpos 2
                ypos 60
                size 23
                color "#cbd5e1"

            frame:
                xpos 1155
                ypos 0
                xsize 620
                ysize 88
                background Solid("#0b2638e8")
                padding (18, 12)
                hbox:
                    xalign 0.5
                    spacing 22
                    vbox:
                        text "MEOW COIN" size 16 color "#fcd34d" bold True
                        text "{:,}".format(snapshot.get("coins", 0)) size 30 color "#ffffff" bold True
                    vbox:
                        text "ECO SCORE" size 16 color "#86efac" bold True
                        text "{:,}".format(snapshot.get("eco_score", 0)) size 30 color "#ffffff" bold True
                    vbox:
                        text "SDG BADGES" size 16 color "#67e8f9" bold True
                        text "{} / 3".format(len(snapshot.get("badges", []))) size 30 color "#ffffff" bold True
                    vbox:
                        text "MISSIONS" size 16 color "#86efac" bold True
                        text "{} / 3".format(completed_count) size 30 color "#ffffff" bold True

    use mk_lobby_module_button("inventory", 48, 188, 535, 174)
    use mk_lobby_module_button("connections", 48, 382, 535, 194)
    use mk_lobby_module_button("progress", 48, 596, 535, 194)

    use mk_lobby_module_button("knowledge", 1337, 188, 535, 242)
    use mk_lobby_module_button("achievements", 1337, 452, 535, 242)

    frame:
        xpos 625
        ypos 760
        xsize 670
        ysize 240
        background Solid("#061522e8")
        padding (30, 24)

        vbox:
            xalign 0.5
            spacing 14
            text "LIVE MISSION DATABASE":
                xalign 0.5
                size 30
                color "#67e8f9"
                bold True
            text "บันทึกการตัดสินใจแล้ว  {} / 3 ด่าน".format(decision_count):
                xalign 0.5
                size 24
                color "#e2e8f0"
            text "ภารกิจสำเร็จ  {} / 3    |    รางวัลถูกบันทึกแบบรับครั้งเดียว".format(completed_count):
                xalign 0.5
                size 22
                color "#cbd5e1"
            bar:
                xalign 0.5
                xsize 560
                ysize 20
                value StaticValue(completed_count, 3)
                left_bar Solid("#22c55e")
                right_bar Solid("#1e293b")

    textbutton "MAIN MENU":
        xpos 1580
        ypos 956
        xminimum 292
        yminimum 76
        background Solid("#3f1d2dea")
        hover_background Solid("#881337")
        padding (24, 15)
        text_size 26
        text_color "#fecdd3"
        text_bold True
        action MainMenu(confirm=True)

    key "K_ESCAPE" action MainMenu(confirm=True)


screen mk_lobby_module_screen(module_id):
    modal True
    zorder 300

    $ module = MK_LOBBY_MODULES[module_id]
    $ snapshot = mk_lobby_snapshot()
    $ stage_rows = [mk_lobby_stage_row(stage_id) for stage_id in MK_LOBBY_STAGES]

    add Solid("#020617d8")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1740
        ysize 960
        background Solid("#061522fa")
        padding (42, 34)

        fixed:
            add Solid(module["accent"], xsize=10, ysize=104) xpos 0 ypos 0
            text module["number"]:
                xpos 34
                ypos 0
                size 58
                color module["accent"]
                bold True
            text module["title"]:
                xpos 145
                ypos 2
                size 36
                color "#f8fafc"
                bold True
            text module["subtitle"]:
                xpos 147
                ypos 58
                size 23
                color "#cbd5e1"

            textbutton "ปิดหน้าต่าง":
                xpos 1430
                ypos 5
                xminimum 215
                yminimum 68
                background Solid("#1e293b")
                hover_background Solid("#334155")
                padding (22, 13)
                text_size 24
                text_color "#ffffff"
                action Hide("mk_lobby_module_screen")

            viewport:
                xpos 0
                ypos 130
                xsize 1650
                ysize 745
                scrollbars "vertical"
                mousewheel True
                draggable True
                pagekeys True

                vbox:
                    xfill True
                    spacing 18

                    if module_id == "inventory":
                        $ inventory_rows = mk_lobby_inventory_rows()
                        if inventory_rows:
                            text "รายการทั้งหมด {} ชิ้น".format(len(inventory_rows)) size 27 color "#67e8f9" bold True
                            for item in inventory_rows:
                                frame:
                                    xfill True
                                    background Solid("#0b2638e8")
                                    padding (26, 20)
                                    hbox:
                                        spacing 28
                                        text item["id"].upper() size 24 color "#22d3ee" bold True xminimum 330
                                        text item["name"] size 26 color "#ffffff" bold True xminimum 620
                                        text "TYPE  " + item["type"] size 21 color "#cbd5e1" xminimum 330
                                        text "STAGE  " + item["stage"].upper() size 21 color "#86efac"
                        else:
                            text "ยังไม่มีไอเทมใน Inventory" size 32 color "#e2e8f0" bold True
                            text "ชนะ minigame ของแต่ละด่านเพื่อรับ SDG Badge และบันทึกลงฐานข้อมูล" size 25 color "#cbd5e1"

                    elif module_id == "connections":
                        text "แต่ละด่านเชื่อมการเรียนรู้ในเกมกับสถานที่จริงและหน่วยงานที่เกี่ยวข้อง" size 26 color "#e2e8f0"
                        for row in stage_rows:
                            $ info = stage_learning_info(row["id"])
                            if info:
                                frame:
                                    xfill True
                                    background Solid("#0b2638e8")
                                    padding (28, 22)
                                    vbox:
                                        spacing 10
                                        text info["stage_title"] + "  |  " + info["sdg_title"] size 29 color module["accent"] bold True
                                        text "สถานที่จริง: " + info["local_title"] size 23 color "#ffffff" bold True
                                        text info["local_description"] size 22 color "#cbd5e1"
                                        text "หน่วยงาน: " + info["agency"] size 23 color "#86efac" bold True
                                        text info["policy_title"] size 24 color "#fcd34d" bold True
                                        text info["policy_description"] size 22 color "#e2e8f0"
                                        if info["policy_url"]:
                                            textbutton info["policy_link_label"]:
                                                xminimum 560
                                                yminimum 64
                                                background Solid("#0e7490")
                                                hover_background Solid("#0891b2")
                                                padding (22, 12)
                                                text_size 23
                                                text_color "#ffffff"
                                                text_bold True
                                                action OpenURL(info["policy_url"])
                                        if info.get("policy_link_notice"):
                                            text info["policy_link_notice"]:
                                                xmaximum 1500
                                                size 21
                                                color "#fca5a5"
                                                bold True
                                                line_spacing 4

                    elif module_id == "progress":
                        for row in stage_rows:
                            frame:
                                xfill True
                                background Solid("#0b2638e8")
                                padding (28, 22)
                                vbox:
                                    spacing 10
                                    hbox:
                                        spacing 24
                                        text row["title"] size 31 color "#86efac" bold True xminimum 580
                                        text ("MISSION COMPLETE" if row["completed"] else "IN PROGRESS") size 25 color ("#4ade80" if row["completed"] else "#fbbf24") bold True
                                    text row["sdg"] size 23 color "#67e8f9"
                                    if row["decision"]:
                                        text "Sustainability Decision: " + row["decision"].get("choice_title", "-") size 23 color "#ffffff"
                                        text "Carbon Monster HP  {:,} -> {:,}".format(row["start_hp"], row["current_hp"]) size 24 color "#fda4af" bold True
                                    else:
                                        text "ยังไม่ได้ทำ Sustainability Decision" size 23 color "#cbd5e1"

                    elif module_id == "knowledge":
                        frame:
                            xfill True
                            background Solid("#102019e8")
                            padding (28, 22)
                            vbox:
                                spacing 12
                                text "SUSTAINABLE DEVELOPMENT GOALS" size 31 color "#86efac" bold True
                                text "SDG คือเป้าหมายการพัฒนาที่ยั่งยืน 17 ข้อของสหประชาชาติ เป็นกรอบร่วมเพื่อพัฒนาคน สังคม เศรษฐกิจ และสิ่งแวดล้อมไปพร้อมกันภายในปี 2030" size 23 color "#e2e8f0"
                                text "NET ZERO" size 27 color "#67e8f9" bold True
                                text "ภาวะที่ก๊าซเรือนกระจกที่ปล่อยออกมาสมดุลกับปริมาณที่ลดหรือกำจัดออก โดยให้ความสำคัญกับการลดการปล่อยจริงก่อนการชดเชย" size 22 color "#cbd5e1"
                                text "CARBON FOOTPRINT" size 27 color "#67e8f9" bold True
                                text "ปริมาณก๊าซเรือนกระจกจากกิจกรรม ผลิตภัณฑ์ หรือองค์กร เมื่อคำนวณตลอดขอบเขตที่กำหนดและแปลงเป็นคาร์บอนไดออกไซด์เทียบเท่า" size 22 color "#cbd5e1"
                                text "CARBON CREDIT" size 27 color "#67e8f9" bold True
                                text "หน่วยที่รับรองการลดหรือกักเก็บก๊าซเรือนกระจก โดยทั่วไปหนึ่งเครดิตแทนหนึ่งตันคาร์บอนไดออกไซด์เทียบเท่า ต้องตรวจสอบมาตรฐานและไม่ใช้แทนการลดการปล่อยโดยตรง" size 22 color "#cbd5e1"

                        text "สรุปเป้าหมายทั้ง 17 ข้อ" size 30 color "#facc15" bold True
                        for sdg_code, sdg_summary in MK_SDG_SUMMARIES:
                            frame:
                                xfill True
                                background Solid("#0b2638d8")
                                padding (24, 16)
                                hbox:
                                    spacing 28
                                    text sdg_code size 25 color "#facc15" bold True xminimum 150
                                    text sdg_summary size 23 color "#f8fafc"

                    elif module_id == "achievements":
                        frame:
                            xfill True
                            background Solid("#2c230be8")
                            padding (30, 22)
                            hbox:
                                spacing 50
                                vbox:
                                    text "MEOW COIN BALANCE" size 23 color "#fcd34d" bold True
                                    text "{:,}".format(snapshot.get("coins", 0)) size 52 color "#ffffff" bold True
                                vbox:
                                    text "ECO SCORE" size 23 color "#86efac" bold True
                                    text "{:,}".format(snapshot.get("eco_score", 0)) size 52 color "#ffffff" bold True
                                vbox:
                                    text "SUSTAINABILITY BADGES" size 23 color "#67e8f9" bold True
                                    text "{} / 3".format(len(snapshot.get("badges", []))) size 52 color "#ffffff" bold True
                                vbox:
                                    text "REWARD RULE" size 23 color "#86efac" bold True
                                    text "SDG Badge + {:,} Coin + {:,} Eco ต่อด่าน".format(MK_STAGE_REWARD_COINS, MK_STAGE_REWARD_ECO_SCORE) size 26 color "#ffffff" bold True

                        for row in stage_rows:
                            frame:
                                xfill True
                                background Solid("#0b2638e8")
                                padding (28, 20)
                                hbox:
                                    spacing 25
                                    text row["badge"] size 30 color "#fcd34d" bold True xminimum 190
                                    text row["title"] size 27 color "#ffffff" bold True xminimum 540
                                    text ("REWARD CLAIMED" if row["rewarded"] else "LOCKED") size 25 color ("#4ade80" if row["rewarded"] else "#94a3b8") bold True xminimum 300
                                    text (("+{:,} COIN • +{:,} ECO SCORE".format(MK_STAGE_REWARD_COINS, MK_STAGE_REWARD_ECO_SCORE)) if row["rewarded"] else "ชนะด่านเพื่อรับรางวัล") size 23 color "#cbd5e1"

                        text "ฐานข้อมูลนี้แสดงสถานะจริงเท่านั้น ไม่มีปุ่มรับรางวัลซ้ำ" size 22 color "#94a3b8"

    key "K_ESCAPE" action Hide("mk_lobby_module_screen")


label mk_lobby_start:
    $ save_name = "Meow Khiao Sustainability Lobby"
    window hide
    call screen mk_lobby_dashboard
    return
