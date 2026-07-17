# =============================================================================
# nextopia.rpy — ด่านที่ 2: NEXTOPIA (SDG 4) — Hidden-Object Missions
# =============================================================================
# เนื้อเรื่อง + มินิเกมหาวัตถุ (hidden object) 5 เกม สลับกับซีนเนื้อเรื่องตามลำดับ:
#   ซีน 16-24 / เกม 1 / ซีน 25-27 / เกม 2 / ซีน 28-31 / เกม 3 /
#   ซีน 32-35 / เกม 4 / ซีน 36-37 / เกม 5 / ซีน 38 / บทสรุป 3 ภาพ
# ผ่านแต่ละเกมจะลด Carbon Monster HP ลง 20% ของ HP หลัง Sustainability Decision
# (ครบ 5 เกม HP = 0 พอดี)
#
# ตำแหน่ง asset ที่ใช้:
#   - ภาพเนื้อเรื่อง/บทสรุป : images/story/2-NEXTOPIA/ (นามแฝงใน screens.rpy)
#   - ฉากมินิเกม 5 ฉาก     : minigames/2-NEXTOPIA/images/scenes/
#   - ภาพ tutorial          : minigames/2-NEXTOPIA/images/tutorial/
#   - เพลงประกอบด่าน (BGM)  : audio/2-NEXTOPIA/Nextopia_BGM.mp3
#   - วิดีโอสรุป            : videos/2-NEXTOPIA/NEXTOPIA.ogv (ผ่าน learning_connections.rpy)

define NEXTOPIA_BGM_FILE = "audio/2-NEXTOPIA/Nextopia_BGM.mp3"

image nextopia black = Solid("#020617")
image nextopia tutorial background = Transform(
    "minigames/2-NEXTOPIA/images/tutorial/nextopia_hidden_tutorial_bg.png",
    xysize=(1920, 1080),
)
image nextopia_conclusion_1 = Transform("images/story/2-NEXTOPIA/conclusion_1.png", xysize=(1920, 1080))
image nextopia_conclusion_2 = Transform("images/story/2-NEXTOPIA/conclusion_2.png", xysize=(1920, 1080))
image nextopia_conclusion_3 = Transform("images/story/2-NEXTOPIA/conclusion_3.png", xysize=(1920, 1080))

default nextopia_hidden_game_id = "waste"
default nextopia_hidden_found = []
default nextopia_hidden_time = 0
default nextopia_hidden_lives = 4
default nextopia_hidden_hint_target = None
default nextopia_hidden_feedback = ""
default nextopia_completed_games = []
default nextopia_accessibility_completions = []
default nextopia_stage_start_hp = 30000
default nextopia_stage_current_hp = 30000
default nextopia_last_hp_result = None
default nextopia_reward_record = None


init -5 python:
    NEXTOPIA_STAGE_ID = "nextopia"
    NEXTOPIA_GAME_ORDER = (
        "waste",
        "food",
        "nature",
        "energy",
        "knowledge",
    )

    def nextopia_stage_bgm_is_playing():
        """Return True when the NEXTOPIA stage loop owns the music channel."""
        playing = renpy.music.get_playing(channel="music")
        if not playing:
            return False

        current_path = str(playing).replace("\\", "/").lower()
        target_path = str(renpy.store.NEXTOPIA_BGM_FILE).replace("\\", "/").lower()
        return current_path == target_path or current_path.endswith("/" + target_path)

    def nextopia_play_stage_bgm():
        """Start the one NEXTOPIA BGM without restarting an active loop."""
        bgm_path = renpy.store.NEXTOPIA_BGM_FILE
        if not renpy.loadable(bgm_path):
            return False
        if nextopia_stage_bgm_is_playing():
            return True

        renpy.music.play(
            bgm_path,
            channel="music",
            loop=True,
            fadeout=0.35,
            fadein=0.35,
        )
        return True

    def nextopia_stop_stage_bgm():
        """Release the music channel before the post-stage video section."""
        renpy.music.stop(channel="music", fadeout=0.35)

    # Coordinates are authored for the project's 1920x1080 virtual canvas.
    # The source images are transformed to that exact runtime size by the
    # screen, so hotspots are deterministic on every supported desktop size.
    NEXTOPIA_HIDDEN_GAMES = {
        "waste": {
            "number": 1,
            "title": "WASTE TO WONDER",
            "subtitle": "ค้นหาวัสดุที่เปลี่ยนขยะให้เป็นงานสร้างสรรค์",
            "scene": "minigames/2-NEXTOPIA/images/scenes/waste_to_wonder_scene.png",
            "time": 78,
            "accent": "#86efac",
            "targets": (
                {"id": "glass_bottle", "name": "ขวดแก้วแบบเติมซ้ำ", "x": 665, "y": 485, "w": 115, "h": 220},
                {"id": "cat_mosaic", "name": "แผ่นโมเสกรูปแมว", "x": 1050, "y": 540, "w": 220, "h": 220},
                {"id": "art_card", "name": "การ์ดศิลปะจากวัสดุเหลือใช้", "x": 1180, "y": 735, "w": 285, "h": 190},
                {"id": "paint_jar", "name": "โหลตกแต่งนำกลับมาใช้ใหม่", "x": 820, "y": 820, "w": 205, "h": 245},
                {"id": "cat_doll", "name": "ตุ๊กตาแมวทำมือ", "x": 1570, "y": 520, "w": 205, "h": 285},
            ),
        },
        "food": {
            "number": 2,
            "title": "FOOD RESCUE",
            "subtitle": "ค้นหาองค์ประกอบของระบบฟาร์มอาหารเมือง",
            "scene": "minigames/2-NEXTOPIA/images/scenes/food_rescue_scene.png",
            "time": 72,
            "accent": "#67e8f9",
            "targets": (
                {"id": "climate_sensor", "name": "เซนเซอร์สภาพแวดล้อม", "x": 965, "y": 150, "w": 140, "h": 175},
                {"id": "grow_light", "name": "ไฟปลูกพืช LED", "x": 1450, "y": 130, "w": 380, "h": 145},
                {"id": "farm_robot", "name": "หุ่นยนต์ตรวจแปลงผัก", "x": 990, "y": 525, "w": 275, "h": 225},
                {"id": "water_filter", "name": "ระบบกรองน้ำหมุนเวียน", "x": 690, "y": 655, "w": 250, "h": 365},
                {"id": "seedling_tray", "name": "ถาดต้นกล้าพร้อมปลูก", "x": 1160, "y": 780, "w": 585, "h": 235},
            ),
        },
        "nature": {
            "number": 3,
            "title": "HARMONIOUS NATURE",
            "subtitle": "ค้นหาเครื่องมือฟื้นฟูระบบนิเวศทางทะเล",
            "scene": "minigames/2-NEXTOPIA/images/scenes/harmonious_nature_scene.png",
            "time": 74,
            "accent": "#60a5fa",
            "targets": (
                {"id": "plastic_bottle", "name": "ขวดพลาสติกหลงเหลือ", "x": 750, "y": 820, "w": 245, "h": 165},
                {"id": "ghost_net", "name": "อวนประมงที่ถูกทิ้ง", "x": 935, "y": 745, "w": 510, "h": 240},
                {"id": "capture_basket", "name": "ตะกร้าดักจับขยะลอยน้ำ", "x": 1350, "y": 515, "w": 325, "h": 220},
                {"id": "smart_valve", "name": "วาล์วควบคุมน้ำอัจฉริยะ", "x": 1625, "y": 720, "w": 290, "h": 330},
                {"id": "coral_rack", "name": "ชั้นอนุบาลปะการัง", "x": 1070, "y": 260, "w": 250, "h": 325},
            ),
        },
        "energy": {
            "number": 4,
            "title": "COLLECTIVE CLEAN ENERGY",
            "subtitle": "ค้นหาระบบผลิตและแบ่งปันพลังงานสะอาด",
            "scene": "minigames/2-NEXTOPIA/images/scenes/collective_clean_energy_scene.png",
            "time": 76,
            "accent": "#bef264",
            "targets": (
                {"id": "energy_columns", "name": "เสาพลังงานจลน์คู่", "x": 740, "y": 65, "w": 300, "h": 590},
                {"id": "pedal_pad", "name": "แท่นพลังงานจากจักรยาน", "x": 910, "y": 835, "w": 450, "h": 240},
                {"id": "microgrid_node", "name": "โหนดเครือข่ายพลังงานชุมชน", "x": 1380, "y": 165, "w": 355, "h": 370},
                {"id": "energy_kiosk", "name": "จอแสดงผลพลังงาน", "x": 1380, "y": 505, "w": 365, "h": 545},
                {"id": "flywheel", "name": "เครื่องกำเนิดไฟฟ้าแบบฟลายวีล", "x": 640, "y": 635, "w": 320, "h": 320},
            ),
        },
        "knowledge": {
            "number": 5,
            "title": "FUTURE KNOWLEDGE",
            "subtitle": "เชื่อมองค์ความรู้ทั้งห้าให้เป็นอนาคตเดียวกัน",
            "scene": "minigames/2-NEXTOPIA/images/scenes/future_knowledge_scene.png",
            "time": 82,
            "accent": "#c084fc",
            "targets": (
                {"id": "recycle_emblem", "name": "องค์ความรู้เศรษฐกิจหมุนเวียน", "x": 625, "y": 560, "w": 235, "h": 225},
                {"id": "seed_heart", "name": "องค์ความรู้อาหารและสุขภาวะ", "x": 1260, "y": 305, "w": 230, "h": 225},
                {"id": "ocean_emblem", "name": "องค์ความรู้การดูแลมหาสมุทร", "x": 1545, "y": 530, "w": 260, "h": 245},
                {"id": "energy_emblem", "name": "องค์ความรู้พลังงานสะอาด", "x": 875, "y": 320, "w": 215, "h": 190},
                {"id": "learning_tablet", "name": "คลังการเรียนรู้แบบเปิด", "x": 1025, "y": 785, "w": 290, "h": 205},
            ),
        },
    }


    def nextopia_hidden_reset(game_id):
        game = NEXTOPIA_HIDDEN_GAMES[game_id]
        s = renpy.store
        s.nextopia_hidden_game_id = game_id
        s.nextopia_hidden_found = []
        s.nextopia_hidden_time = int(game["time"])
        s.nextopia_hidden_lives = 4
        s.nextopia_hidden_hint_target = None
        s.nextopia_hidden_feedback = "ค้นหาวัตถุจากรายการด้านซ้าย แล้วคลิกที่วัตถุในฉาก"


    def nextopia_hidden_find(target_id, target_name):
        s = renpy.store
        if target_id in s.nextopia_hidden_found:
            return
        s.nextopia_hidden_found = list(s.nextopia_hidden_found) + [target_id]
        s.nextopia_hidden_hint_target = None
        s.nextopia_hidden_feedback = "ค้นพบแล้ว: " + target_name
        renpy.restart_interaction()


    def nextopia_hidden_hover(target_name):
        renpy.store.nextopia_hidden_feedback = "ตรวจสอบ: " + target_name
        renpy.restart_interaction()


    def nextopia_hidden_unhover():
        renpy.store.nextopia_hidden_feedback = "ค้นหาวัตถุจากรายการด้านซ้าย"
        renpy.restart_interaction()


    def nextopia_hidden_miss():
        s = renpy.store
        game = NEXTOPIA_HIDDEN_GAMES[s.nextopia_hidden_game_id]
        if len(s.nextopia_hidden_found) >= len(game["targets"]):
            return
        s.nextopia_hidden_lives = max(0, int(s.nextopia_hidden_lives) - 1)
        s.nextopia_hidden_feedback = "ยังไม่ใช่วัตถุเป้าหมาย — พลังค้นหาลดลง 1 หน่วย"
        renpy.restart_interaction()


    def nextopia_hidden_tick():
        s = renpy.store
        if s.nextopia_hidden_time > 0:
            s.nextopia_hidden_time = max(0, int(s.nextopia_hidden_time) - 1)
            renpy.restart_interaction()


    def nextopia_hidden_show_hint():
        s = renpy.store
        game = NEXTOPIA_HIDDEN_GAMES[s.nextopia_hidden_game_id]
        remaining = [item for item in game["targets"] if item["id"] not in s.nextopia_hidden_found]
        if not remaining:
            return
        s.nextopia_hidden_hint_target = remaining[0]["id"]
        s.nextopia_hidden_time = max(1, int(s.nextopia_hidden_time) - 8)
        s.nextopia_hidden_feedback = "คำใบ้กำลังเน้นเป้าหมาย 2 วินาที — หักเวลา 8 วินาที"
        renpy.restart_interaction()


    def nextopia_hidden_hide_hint():
        renpy.store.nextopia_hidden_hint_target = None
        renpy.restart_interaction()


    def nextopia_prepare_stage_run():
        """Start a fresh five-step battle without repeating the stage tax."""
        s = renpy.store
        get_start = getattr(s, "mk_get_stage_start_hp", None)
        reset_battle = getattr(s, "mk_reset_stage_battle", None)

        start_hp = int(get_start(NEXTOPIA_STAGE_ID)) if callable(get_start) else 30000
        if callable(reset_battle):
            current_hp = int(reset_battle(NEXTOPIA_STAGE_ID, clear_steps=True))
        else:
            current_hp = start_hp

        s.nextopia_stage_start_hp = max(1, start_hp)
        s.nextopia_stage_current_hp = max(0, min(start_hp, current_hp))
        s.nextopia_completed_games = []
        s.nextopia_accessibility_completions = []
        s.nextopia_last_hp_result = None


    def nextopia_sync_stage_hp():
        s = renpy.store
        get_start = getattr(s, "mk_get_stage_start_hp", None)
        get_current = getattr(s, "mk_get_stage_current_hp", None)
        if callable(get_start):
            s.nextopia_stage_start_hp = max(1, int(get_start(NEXTOPIA_STAGE_ID)))
        if callable(get_current):
            s.nextopia_stage_current_hp = max(0, int(get_current(NEXTOPIA_STAGE_ID)))
        return s.nextopia_stage_current_hp


    def nextopia_register_win(game_id, assisted=False):
        """Apply exactly one fifth of post-decision HP for a unique clear."""
        s = renpy.store
        start_hp = max(1, int(s.nextopia_stage_start_hp))
        previous_hp = max(0, int(s.nextopia_stage_current_hp))

        if game_id in s.nextopia_completed_games:
            return {
                "is_new": False,
                "start_hp": start_hp,
                "previous_hp": previous_hp,
                "current_hp": previous_hp,
                "damage": 0,
                "completed_steps": len(s.nextopia_completed_games),
            }

        s.nextopia_completed_games = list(s.nextopia_completed_games) + [game_id]
        if assisted and game_id not in s.nextopia_accessibility_completions:
            s.nextopia_accessibility_completions = list(s.nextopia_accessibility_completions) + [game_id]

        complete_step = getattr(s, "mk_complete_stage_step", None)
        if callable(complete_step):
            core_result = complete_step(NEXTOPIA_STAGE_ID, game_id, total_steps=5)
            current_hp = int(core_result["current_hp"])
            damage = int(core_result["damage"])
            completed_steps = int(core_result["completed_steps"])
        else:
            completed_steps = min(5, len(s.nextopia_completed_games))
            current_hp = int(round(start_hp * ((5 - completed_steps) / 5.0)))
            damage = max(0, previous_hp - current_hp)

        if completed_steps >= 5:
            current_hp = 0
            set_hp = getattr(s, "mk_set_stage_current_hp", None)
            if callable(set_hp):
                set_hp(NEXTOPIA_STAGE_ID, 0)

        s.nextopia_stage_current_hp = current_hp
        result = {
            "is_new": True,
            "start_hp": start_hp,
            "previous_hp": previous_hp,
            "current_hp": current_hp,
            "damage": damage,
            "completed_steps": completed_steps,
            "assisted": bool(assisted),
        }
        s.nextopia_last_hp_result = result
        return result


    def nextopia_grant_rewards():
        s = renpy.store
        grant = getattr(s, "mk_grant_stage_rewards", None)
        if callable(grant):
            return grant(NEXTOPIA_STAGE_ID)
        # Never mint a local fallback reward: the shared claim ledger is the
        # authority that keeps stage results, Achievement, and old saves in sync.
        return {
            "new_reward": False,
            "coins_awarded": 0,
            "eco_score_awarded": 0,
            "badge": "SDG 4",
            "badge_name": "การศึกษาที่มีคุณภาพ",
            "coin_balance": int(getattr(s, "mk_meow_coins", 0)),
            "eco_score_balance": int(getattr(s, "mk_eco_score", 0)),
        }


transform nextopia_next_pulse:
    alpha 0.86
    linear 0.8 alpha 1.0
    linear 0.8 alpha 0.86
    repeat


transform nextopia_hint_pulse:
    alpha 0.18
    linear 0.35 alpha 0.58
    linear 0.35 alpha 0.18
    repeat


# -----------------------------------------------------------------------------
# Three-page tutorial shown immediately after Sustainability Decision.
# Text stays code-native so Thai copy remains crisp and easy to maintain.
# -----------------------------------------------------------------------------

screen _legacy_nextopia_minigame_tutorial_page(page=0):
    tag nextopia_tutorial
    modal True

    $ decision_hp = max(1, int(mk_get_stage_start_hp("nextopia")))

    add "nextopia tutorial background"
    add Solid("#020617b9")

    frame:
        xpos 52
        ypos 24
        xsize 1816
        ysize 112
        background Solid("#03111cf2")
        padding (30, 10)

        hbox:
            xfill True
            yalign 0.5

            vbox:
                spacing 2
                text "NEXTOPIA DISCOVERY TUTORIAL" size 42 color "#67e8f9" bold True
                text "คู่มือภารกิจค้นหาวัตถุเพื่อการเรียนรู้ SDG 4" size 26 color "#dbeafe"

            text "PAGE  [page + 1] / 3":
                xalign 1.0
                yalign 0.5
                size 28
                color "#a7f3d0"
                bold True

    frame:
        xpos 70
        ypos 148
        xsize 1780
        ysize 762
        background Solid("#020817ed")
        padding (34, 26)

        if page == 0:
            vbox:
                xfill True
                spacing 20

                text "1  ภารกิจของคุณ":
                    xalign 0.5
                    size 42
                    color "#86efac"
                    bold True

                text "สำรวจฉากและค้นหาวัตถุเป้าหมายให้ครบ 5 ชิ้นในแต่ละภารกิจ":
                    xalign 0.5
                    size 29
                    color "#ffffff"
                    text_align 0.5

                hbox:
                    xalign 0.5
                    spacing 20

                    frame:
                        xsize 540
                        ysize 510
                        background Solid("#06283be8")
                        padding (26, 24)
                        vbox:
                            spacing 15
                            text "ค้นหาให้ครบ" size 34 color "#67e8f9" bold True xalign 0.5
                            text "อ่าน TARGET CHECKLIST ทางซ้าย แล้วสำรวจวัตถุที่ซ่อนอยู่ในฉาก" size 27 color "#e2e8f0" text_align 0.5 xalign 0.5 line_spacing 3
                            null height 8
                            frame:
                                xfill True
                                background Solid("#0f172ae8")
                                padding (20, 16)
                                vbox:
                                    spacing 9
                                    text "FOUND  0 / 5" size 30 color "#ffffff" bold True xalign 0.5
                                    text "เป้าหมายที่ค้นพบจะถูกตีกรอบ และถูกทำเครื่องหมายในรายการ" size 24 color "#bfdbfe" text_align 0.5 xalign 0.5 line_spacing 3

                    frame:
                        xsize 540
                        ysize 510
                        background Solid("#123122e8")
                        padding (26, 24)
                        vbox:
                            spacing 13
                            text "5 ภารกิจต่อเนื่อง" size 34 color "#86efac" bold True xalign 0.5
                            text "1  Waste to Wonder" size 25 color "#ffffff"
                            text "2  Food Rescue" size 25 color "#ffffff"
                            text "3  Harmonious Nature" size 25 color "#ffffff"
                            text "4  Collective Clean Energy" size 25 color "#ffffff"
                            text "5  Future Knowledge" size 25 color "#ffffff"
                            text "เนื้อเรื่องจะดำเนินต่อระหว่างแต่ละภารกิจ" size 24 color "#bbf7d0" text_align 0.5 xalign 0.5 line_spacing 3

                    frame:
                        xsize 540
                        ysize 510
                        background Solid("#301b46e8")
                        padding (26, 24)
                        vbox:
                            spacing 15
                            text "ลดพลังอสูรคาร์บอน" size 34 color "#d8b4fe" bold True xalign 0.5
                            text "HP หลัง Sustainability Decision" size 25 color "#e2e8f0" xalign 0.5
                            text "{:,}".format(decision_hp) size 58 color "#fda4af" bold True xalign 0.5
                            bar:
                                value StaticValue(decision_hp, decision_hp)
                                xalign 0.5
                                xsize 430
                                ysize 32
                                left_bar Solid("#ef4444")
                                right_bar Solid("#1e293b")
                            text "ชัยชนะแต่ละภารกิจลด HP 20%\nเมื่อผ่านครบ 5 ภารกิจ HP จะเหลือ 0" size 26 color "#ffffff" text_align 0.5 xalign 0.5 line_spacing 4

        elif page == 1:
            vbox:
                xfill True
                spacing 22

                text "2  วิธีค้นหาและควบคุม":
                    xalign 0.5
                    size 42
                    color "#67e8f9"
                    bold True

                hbox:
                    xalign 0.5
                    spacing 24

                    frame:
                        xsize 828
                        ysize 588
                        background Solid("#06283bea")
                        padding (32, 26)
                        vbox:
                            spacing 15
                            text "เลือกวัตถุในฉาก" size 35 color "#67e8f9" bold True
                            text "เมาส์ / สัมผัส" size 28 color "#86efac" bold True
                            text "เล็งวัตถุที่ตรงกับรายการ แล้วคลิกหรือแตะหนึ่งครั้ง" size 25 color "#e2e8f0" line_spacing 3
                            text "คีย์บอร์ด" size 28 color "#86efac" bold True
                            text "กด Tab หรือ Shift+Tab เพื่อย้ายโฟกัส แล้วกด Enter เพื่อเลือก" size 25 color "#e2e8f0" line_spacing 3
                            text "คอนโทรลเลอร์" size 28 color "#86efac" bold True
                            text "ใช้ D-pad หรือ Left Stick เลื่อนโฟกัส แล้วกด A เพื่อเลือก" size 25 color "#e2e8f0" line_spacing 3
                            frame:
                                xfill True
                                background Solid("#0f172ae8")
                                padding (18, 14)
                                text "กรอบเรืองแสงขณะ Hover หรือ Focus ช่วยบอกตำแหน่งที่กำลังตรวจสอบ" size 23 color "#bfdbfe" text_align 0.5 xalign 0.5 line_spacing 3

                    frame:
                        xsize 828
                        ysize 588
                        background Solid("#102f2bea")
                        padding (32, 26)
                        vbox:
                            spacing 15
                            text "อ่านสถานะระหว่างเล่น" size 35 color "#86efac" bold True

                            hbox:
                                spacing 18
                                frame:
                                    xsize 358
                                    background Solid("#0f172ae8")
                                    padding (18, 14)
                                    vbox:
                                        text "TIME" size 27 color "#fcd34d" bold True xalign 0.5
                                        text "เวลาที่เหลือ" size 24 color "#ffffff" xalign 0.5
                                frame:
                                    xsize 358
                                    background Solid("#0f172ae8")
                                    padding (18, 14)
                                    vbox:
                                        text "SEARCH ENERGY" size 27 color "#fda4af" bold True xalign 0.5
                                        text "โอกาสค้นหาที่เหลือ" size 24 color "#ffffff" xalign 0.5

                            text "เลือกถูก" size 28 color "#86efac" bold True
                            text "วัตถุจะถูกบันทึกในรายการทันที" size 25 color "#e2e8f0"
                            text "เลือกพื้นที่ผิด" size 28 color "#fda4af" bold True
                            text "SEARCH ENERGY ลดลง 1 หน่วย แต่ HP จะยังไม่เปลี่ยน" size 25 color "#e2e8f0" line_spacing 3
                            text "จบภารกิจเมื่อค้นพบครบ 5 ชิ้น หรือเมื่อเวลา / พลังค้นหาหมด" size 24 color "#bfdbfe" text_align 0.5 xalign 0.5 line_spacing 3

        else:
            vbox:
                xfill True
                spacing 22

                text "3  ตัวช่วยและเงื่อนไขสำเร็จ":
                    xalign 0.5
                    size 42
                    color "#c4b5fd"
                    bold True

                hbox:
                    xalign 0.5
                    spacing 24

                    frame:
                        xsize 828
                        ysize 585
                        background Solid("#18304bea")
                        padding (32, 26)
                        vbox:
                            spacing 18
                            text "HINT" size 36 color "#67e8f9" bold True
                            text "กดคำใบ้เพื่อเน้นเป้าหมายหนึ่งชิ้นเป็นเวลา 2 วินาที" size 27 color "#ffffff" line_spacing 3
                            text "ค่าตอบแทน: เวลาลดลง 8 วินาที" size 27 color "#fcd34d" bold True
                            null height 8
                            text "เมื่อเวลา หรือ SEARCH ENERGY หมด" size 30 color "#fda4af" bold True
                            text "เลือกลองใหม่ได้ หรือใช้โหมดช่วยเหลือเพื่อดำเนินเรื่องต่อ โดยเกมจะบันทึกการใช้ตัวช่วยไว้อย่างชัดเจน" size 26 color "#e2e8f0" line_spacing 3

                    frame:
                        xsize 828
                        ysize 585
                        background Solid("#163526ea")
                        padding (32, 26)
                        vbox:
                            spacing 18
                            text "ก่อนเริ่มค้นหา" size 36 color "#86efac" bold True
                            text "1  ตรวจชื่อภารกิจและรายการเป้าหมาย" size 27 color "#ffffff"
                            text "2  สำรวจฉากจากภาพรวมก่อนคลิก" size 27 color "#ffffff"
                            text "3  ใช้คำใบ้เฉพาะเมื่อจำเป็น" size 27 color "#ffffff"
                            text "4  ผ่านให้ครบทั้ง 5 ภารกิจ" size 27 color "#ffffff"
                            frame:
                                xfill True
                                background Solid("#052e16e8")
                                padding (20, 16)
                                text "เป้าหมายสุดท้าย: Carbon Monster HP = 0" size 28 color "#bbf7d0" bold True text_align 0.5 xalign 0.5

    hbox:
        xpos 70
        ypos 934
        xsize 1780
        spacing 22

        if page > 0:
            textbutton "<  BACK  ย้อนกลับ":
                xminimum 330
                yminimum 80
                background Solid("#1e293be8")
                hover_background Solid("#334155")
                padding (24, 16)
                text_color "#e2e8f0"
                text_hover_color "#ffffff"
                text_size 28
                text_bold True
                action Return("back")
        else:
            null width 330

        text "คีย์บอร์ด: ลูกศรซ้าย / ขวา และ Enter    |    คอนโทรลเลอร์: D-pad / Stick และ A":
            xsize 1050
            yalign 0.5
            size 23
            color "#cbd5e1"
            text_align 0.5
            xalign 0.5

        if page < 2:
            textbutton "NEXT  ถัดไป  >":
                default_focus True
                xminimum 360
                yminimum 80
                background Solid("#075985ed")
                hover_background Solid("#0891b2")
                padding (24, 16)
                text_color "#cffafe"
                text_hover_color "#ffffff"
                text_size 29
                text_bold True
                action Return("next")
        else:
            textbutton "START  เริ่มค้นหา  >":
                default_focus True
                xminimum 360
                yminimum 80
                background Solid("#047857ed")
                hover_background Solid("#059669")
                padding (24, 16)
                text_color "#d1fae5"
                text_hover_color "#ffffff"
                text_size 29
                text_bold True
                action Return("start")

    key "K_LEFT" action If(page > 0, true=Return("back"), false=NullAction())
    key "K_RIGHT" action If(page < 2, true=Return("next"), false=Return("start"))
    key "K_RETURN" action If(page < 2, true=Return("next"), false=Return("start"))
    key "K_SPACE" action If(page < 2, true=Return("next"), false=Return("start"))
    key "game_menu" action If(page > 0, true=Return("back"), false=NullAction())


screen nextopia_hidden_object_screen(game_id):
    tag nextopia_hidden_object
    modal True

    $ game = NEXTOPIA_HIDDEN_GAMES[game_id]
    $ target_total = len(game["targets"])
    $ found_total = len(nextopia_hidden_found)
    $ accent = game["accent"]
    $ current_hp = nextopia_stage_current_hp
    $ start_hp = max(1, nextopia_stage_start_hp)

    add game["scene"] xysize (1920, 1080)
    add Solid("#02061712")

    if found_total >= target_total:
        timer 0.30 action Return("success")
    elif nextopia_hidden_lives <= 0:
        timer 0.25 action Return("failed")
    elif nextopia_hidden_time <= 0:
        timer 0.25 action Return("timeout")
    else:
        timer 1.0 repeat True action Function(nextopia_hidden_tick)

    # Only the scene area consumes a miss; clicking the information panel is
    # never punished.  Target buttons are declared later and sit above it.
    button:
        xpos 520
        ypos 145
        xsize 1400
        ysize 935
        background Solid("#00000001")
        hover_background Solid("#00000001")
        focus_mask True
        action Function(nextopia_hidden_miss)

    for target in game["targets"]:
        $ target_id = target["id"]

        if target_id == nextopia_hidden_hint_target and target_id not in nextopia_hidden_found:
            add Solid(accent + "66"):
                xpos target["x"] - 12
                ypos target["y"] - 12
                xsize target["w"] + 24
                ysize target["h"] + 24
                at nextopia_hint_pulse

        if target_id in nextopia_hidden_found:
            fixed:
                xpos target["x"]
                ypos target["y"]
                xsize target["w"]
                ysize target["h"]

                add Solid(accent + "dd") xpos 0 ypos 0 xsize target["w"] ysize 5
                add Solid(accent + "dd") xpos 0 ypos target["h"] - 5 xsize target["w"] ysize 5
                add Solid(accent + "dd") xpos 0 ypos 0 xsize 5 ysize target["h"]
                add Solid(accent + "dd") xpos target["w"] - 5 ypos 0 xsize 5 ysize target["h"]

                frame:
                    xpos 8
                    ypos 8
                    background Solid("#052e16e8")
                    padding (10, 6)
                    text "FOUND" size 18 color "#dcfce7" bold True
        else:
            button:
                xpos target["x"]
                ypos target["y"]
                xsize target["w"]
                ysize target["h"]
                background Solid("#00000001")
                hover_background Solid(accent + "38")
                focus_mask True
                action Function(nextopia_hidden_find, target_id, target["name"])
                hovered Function(nextopia_hidden_hover, target["name"])
                unhovered Function(nextopia_hidden_unhover)

    if nextopia_hidden_hint_target is not None:
        timer 2.0 action Function(nextopia_hidden_hide_hint)

    # Carbon Monster HP is authoritative shared state after the decision.
    frame:
        xpos 548
        ypos 24
        xsize 1340
        ysize 112
        background Solid("#020817eb")
        padding (24, 16)

        hbox:
            xfill True
            yalign 0.5
            spacing 24

            vbox:
                xsize 310
                spacing 2
                text "CARBON MONSTER" size 25 color "#fda4af" bold True
                text ("HP  {:,} / {:,}".format(current_hp, start_hp)) size 24 color "#ffffff" bold True

            vbox:
                xsize 960
                yalign 0.5
                spacing 8
                bar:
                    value StaticValue(current_hp, start_hp)
                    xsize 940
                    ysize 26
                    left_bar Solid("#ef4444")
                    right_bar Solid("#1e293b")
                text "ชัยชนะแต่ละภารกิจลด HP เท่ากับ 20% ของค่าเริ่มต้นหลังการตัดสินใจ" size 18 color "#cbd5e1"

    # Left information rail stays clear of every generated target.
    frame:
        xpos 22
        ypos 22
        xsize 492
        ysize 1035
        background Solid("#020817ee")
        padding (24, 20)

        vbox:
            xfill True
            spacing 13

            text ("MISSION %d / 5" % game["number"]):
                size 23
                color accent
                bold True

            text game["title"]:
                size 31
                color "#ffffff"
                bold True

            text game["subtitle"]:
                size 20
                color "#cbd5e1"
                layout "subtitle"

            frame:
                xfill True
                background Solid("#0f172ad9")
                padding (16, 12)

                hbox:
                    xfill True
                    text ("FOUND  %d / %d" % (found_total, target_total)) size 22 color "#ffffff" bold True
                    text ("TIME  %02d" % nextopia_hidden_time) xalign 1.0 size 22 color ("#fb7185" if nextopia_hidden_time <= 12 else "#fcd34d") bold True

            text ("SEARCH ENERGY  %d / 4" % nextopia_hidden_lives):
                size 20
                color "#fda4af"
                bold True

            bar:
                value StaticValue(found_total, target_total)
                xsize 440
                ysize 14
                left_bar Solid(accent)
                right_bar Solid("#1e293b")

            text "TARGET CHECKLIST" size 20 color accent bold True

            for index, target in enumerate(game["targets"]):
                $ target_found = target["id"] in nextopia_hidden_found
                frame:
                    xfill True
                    background Solid("#064e3b99" if target_found else "#111827d9")
                    padding (12, 9)

                    hbox:
                        spacing 11
                        text ("%02d" % (index + 1)) size 18 color (accent if target_found else "#64748b") bold True
                        text target["name"] size 18 color ("#dcfce7" if target_found else "#e2e8f0") bold target_found

            frame:
                xfill True
                yminimum 74
                background Solid("#0f172add")
                padding (14, 11)
                text nextopia_hidden_feedback size 18 color "#dbeafe" layout "subtitle"

            textbutton "HINT  เน้นเป้าหมาย 2 วินาที  (-8s)":
                xfill True
                yminimum 58
                background Solid("#164e63e8")
                hover_background Solid("#0e7490")
                insensitive_background Solid("#334155bb")
                padding (16, 12)
                text_color "#cffafe"
                text_hover_color "#ffffff"
                text_insensitive_color "#94a3b8"
                text_size 20
                text_bold True
                sensitive (nextopia_hidden_hint_target is None and found_total < target_total and nextopia_hidden_time > 8)
                action Function(nextopia_hidden_show_hint)


screen nextopia_hidden_result_screen(game_id, outcome, hp_before=None, hp_after=None, hp_damage=0):
    tag nextopia_hidden_result
    modal True

    $ game = NEXTOPIA_HIDDEN_GAMES[game_id]
    $ cleared = outcome in ("success", "assist")
    $ assisted = outcome == "assist"

    add game["scene"] xysize (1920, 1080)
    add Solid("#020617c7")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1040
        background Solid("#020817f5")
        padding (50, 42)

        vbox:
            xalign 0.5
            spacing 22

            if cleared:
                text ("ACCESSIBILITY COMPLETE" if assisted else "MISSION COMPLETE"):
                    size 48
                    color ("#fcd34d" if assisted else "#86efac")
                    xalign 0.5
                    bold True

                text ("ผ่านด้วยโหมดช่วยเหลือ — บันทึกผลอย่างชัดเจน" if assisted else "ค้นพบวัตถุเป้าหมายครบทุกชิ้น"):
                    size 24
                    color "#e2e8f0"
                    xalign 0.5

                frame:
                    xfill True
                    background Solid("#0f172ae8")
                    padding (28, 22)

                    vbox:
                        xalign 0.5
                        spacing 12
                        text "CARBON MONSTER HP" size 23 color "#fda4af" xalign 0.5 bold True
                        text ("{:,}  >  {:,}".format(int(hp_before), int(hp_after))) size 39 color "#ffffff" xalign 0.5 bold True
                        text ("พลังโจมตี {:,} HP  (20% ของ HP เริ่มต้น)".format(int(hp_damage))) size 23 color game["accent"] xalign 0.5
                        bar:
                            value StaticValue(int(hp_after), max(1, nextopia_stage_start_hp))
                            xalign 0.5
                            xsize 770
                            ysize 24
                            left_bar Solid("#ef4444")
                            right_bar Solid("#1e293b")

                textbutton "ดำเนินเรื่องต่อ  >":
                    xalign 0.5
                    xminimum 390
                    yminimum 72
                    background Solid("#065f46e8")
                    hover_background Solid("#047857")
                    padding (24, 14)
                    text_color "#d1fae5"
                    text_hover_color "#ffffff"
                    text_size 27
                    text_bold True
                    action Return("continue")
            else:
                text ("TIME LIMIT REACHED" if outcome == "timeout" else "SEARCH ENERGY DEPLETED"):
                    size 44
                    color "#fb7185"
                    xalign 0.5
                    bold True

                text "ยังค้นพบเป้าหมายไม่ครบ เลือกลองใหม่หรือใช้โหมดช่วยเหลือ":
                    size 24
                    color "#e2e8f0"
                    xalign 0.5
                    text_align 0.5

                text "โหมดช่วยเหลือจะผ่านภารกิจนี้และลด HP ตามกติกา พร้อมบันทึกว่าใช้การช่วยเหลือ":
                    size 20
                    color "#fcd34d"
                    xalign 0.5
                    text_align 0.5

                hbox:
                    xalign 0.5
                    spacing 28

                    textbutton "ลองใหม่":
                        xminimum 280
                        yminimum 72
                        background Solid("#164e63e8")
                        hover_background Solid("#0e7490")
                        padding (22, 14)
                        text_color "#cffafe"
                        text_hover_color "#ffffff"
                        text_size 26
                        text_bold True
                        action Return("retry")

                    textbutton "ผ่านด้วยโหมดช่วยเหลือ":
                        xminimum 350
                        yminimum 72
                        background Solid("#854d0ee8")
                        hover_background Solid("#a16207")
                        padding (22, 14)
                        text_color "#fef3c7"
                        text_hover_color "#ffffff"
                        text_size 24
                        text_bold True
                        action Return("assist")


screen nextopia_final_screen():
    tag nextopia_final
    modal True

    $ wins = len(nextopia_completed_games)
    $ reward = nextopia_reward_record if isinstance(nextopia_reward_record, dict) else {}
    $ awarded = int(reward.get("coins_awarded", 0))
    $ eco_awarded = int(reward.get("eco_score_awarded", 0))
    $ coin_balance = int(reward.get("coin_balance", 0))
    $ eco_balance = int(reward.get("eco_score_balance", 0))
    $ new_reward = bool(reward.get("new_reward", False))

    add "minigames/2-NEXTOPIA/images/scenes/future_knowledge_scene.png" xysize (1920, 1080)
    add Solid("#020617c2")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1260
        background Solid("#020817f5")
        padding (58, 44)

        vbox:
            xalign 0.5
            spacing 20

            text "NEXTOPIA MISSION COMPLETE":
                size 58
                color "#86efac"
                xalign 0.5
                bold True

            text ("HIDDEN-OBJECT MISSIONS  %d / 5" % wins):
                size 34
                color "#ffffff"
                xalign 0.5
                bold True

            frame:
                xfill True
                background Solid("#0f172ae8")
                padding (32, 24)

                vbox:
                    spacing 12
                    text "CARBON MONSTER HP" size 28 color "#fda4af" xalign 0.5 bold True
                    text ("0 / {:,}".format(nextopia_stage_start_hp)) size 48 color "#ffffff" xalign 0.5 bold True
                    bar:
                        value StaticValue(0, max(1, nextopia_stage_start_hp))
                        xalign 0.5
                        xsize 1000
                        ysize 28
                        left_bar Solid("#ef4444")
                        right_bar Solid("#1e293b")

            hbox:
                xalign 0.5
                spacing 26

                frame:
                    xsize 500
                    background Solid("#312e81df")
                    padding (24, 18)
                    vbox:
                        spacing 6
                        text "SDG 4 BADGE" size 32 color "#c4b5fd" xalign 0.5 bold True
                        text "การศึกษาที่มีคุณภาพ" size 27 color "#ffffff" xalign 0.5

                frame:
                    xsize 500
                    background Solid("#713f12df")
                    padding (24, 18)
                    vbox:
                        spacing 6
                        if new_reward:
                            text ("+{:,} MEOW COIN".format(awarded)) size 30 color "#fde68a" xalign 0.5 bold True
                            text ("+{:,} ECO SCORE".format(eco_awarded)) size 30 color "#86efac" xalign 0.5 bold True
                        else:
                            text "REWARD ALREADY SAVED" size 28 color "#cbd5e1" xalign 0.5 bold True
                        text ("คงเหลือ Coin {:,} • Eco {:,}".format(coin_balance, eco_balance)) size 24 color "#ffffff" xalign 0.5

            if nextopia_accessibility_completions:
                text ("Accessibility assistance used: %d mission(s)" % len(nextopia_accessibility_completions)) size 23 color "#fcd34d" xalign 0.5

            textbutton "LEARNING CONNECTION  ดูสถานที่จริงและนโยบาย  >":
                xalign 0.5
                xminimum 900
                yminimum 92
                background Solid("#0e7490e8")
                hover_background Solid("#0891b2")
                padding (32, 18)
                text_color "#cffafe"
                text_hover_color "#ffffff"
                text_size 32
                text_bold True
                action Return("learning")

    key "K_RETURN" action Return("learning")


# -----------------------------------------------------------------------------
# Reusable flow helpers and public minigame labels
# -----------------------------------------------------------------------------

label nextopia_story_16_to_24:
    scene nextopia_story_16
    PROF_NEXT "สวัสดี...แมวอาสาสมัคร ฉันคือ PROF. NEXT ศาสตราจารย์ประธานกลุ่มงานสร้างสรรค์และนวัตกรรมแห่ง NEXTOPIA ผลงานจากภารกิจที่เเล้ว... พิสูจน์แล้วว่าเธอพร้อมสำหรับภารกิจใหม่ ฉันกำลังรอเธออยู่ที่ NEXTOPIA"

    scene nextopia_story_17
    PROF_NEXT "ทุกวันนี้... ผู้คนหลายล้านคนกำลังเผชิญผลกระทบจากมลพิษ แต่ศัตรูที่แท้จริง... ไม่ใช่ Carbon Monster เพียงอย่างเดียว"

    scene nextopia_story_18
    PROF_NEXT "ความไม่รู้... ทำให้ Carbon Monster แข็งแกร่งขึ้นทุกวัน หากเราอยากช่วยโลก... เราต้องเริ่มจากการเรียนรู้"

    scene nextopia_story_19
    PROF_NEXT "ยินดีต้อนรับ... สู่ Future Learning Mission"

    scene nextopia_story_20
    PROF_NEXT "หัวใจแต่ละดวง... คือความรู้ที่จะช่วยโลก"

    scene nextopia_story_21
    PROF_NEXT "ทุกครั้งที่เธอค้นพบความรู้ หัวใจจะปลดปล่อยพลัง"

    scene nextopia_story_22
    PROF_NEXT "หัวใจที่ 1 ถูกปลดล็อกแล้ว! ภารกิจใหม่เริ่มต้นขึ้น!"

    scene nextopia_story_23
    PROF_NEXT "หลายคนมองว่าขยะเป็นจุดจบ แต่ที่ ECOTOPIA เรามองว่ามันคือจุดเริ่มต้น"

    scene nextopia_story_24
    PROF_NEXT """คุณค่าของคน... ไม่ได้ถูกกำหนดจากข้อจำกัด เช่นเดียวกันกับวัสดุเหลือใช้"""

    return


label nextopia_story_25_to_27:
    scene nextopia_story_25
    PROF_NEXT "เมื่อเราเปลี่ยนมุมมอง ของที่เคยมองว่าไร้ค่า... ก็สามารถสร้างคุณค่าใหม่ได้"

    scene nextopia_story_26
    PROF_NEXT "ยอดเยี่ยม หัวใจแห่งการสร้างสรรค์กลับมาเต้นอีกครั้ง"

    scene nextopia_story_27_1
    PROF_NEXT "อาหาร... ไม่ควรจบลงที่ถังขยะ เพราะทุกเมล็ดพันธุ์ล้วนใช้ทรัพยากรของโลกในการเติบโต"
    scene nextopia_story_27_2
    PROF_NEXT "นี่คือ The Vertical Farm เมืองเล็กก็ปลูกอาหารเองได้"

    return


label nextopia_story_28_to_31:
    scene nextopia_story_28
    PROF_NEXT "การสร้างแหล่งอาหารเองได้ ทำให้เราสามารถนำทรัพยากรมาใช้ได้ตามปริมาณที่ต้องการในแต่ละมื้อ จึงหมดปัญหาอาหารเหลือทิ้ง"

    scene nextopia_story_29
    PROF_NEXT "เยี่ยมมาก! ความรู้ไม่ได้หยุดอยู่แค่ในห้องเรียน เมื่อเรานำมันไปใช้... โลกก็เริ่มเปลี่ยนแปลงได้จริง"

    scene nextopia_story_30
    PROF_NEXT "ที่ The Ocean Canopy ธรรมชาติ... ไม่เคยสร้างขยะ มีเพียงมนุษย์... ที่ลืมวิธีอยู่ร่วมกับธรรมชาติ"

    scene nextopia_story_31
    PROF_NEXT "ผลงานชิ้นนี้... เคยเป็นอวนจับปลา ที่ถูกทิ้งไว้ในทะเล วันนี้... มันกำลังบอกเล่าเรื่องราว ของการเริ่มต้นใหม่"
    return


label nextopia_story_32_to_35:
    scene nextopia_story_32
    PROF_NEXT "ยอดเยี่ยมมาก! วันนี้เธอไม่ได้ช่วยมหาสมุทร แต่กำลังสร้างแรงบันดาลใจ ให้ผู้คนดูแลโลกในทุก ๆ วัน"

    scene nextopia_story_33
    PROF_NEXT "ที่ Ride · Glow · Repeat พลังของคนหนึ่งคน อาจดูเล็กน้อย แต่เมื่อทุกคนร่วมมือกัน... มันสามารถเปลี่ยนทั้งเมืองได้"

    scene nextopia_story_34
    PROF_NEXT "ทุกการปั่นของเราคือพลังงานที่มอบให้กับโลก"

    scene nextopia_story_35
    PROF_NEXT "นี่ไม่ใช่คะแนนของใครคนหนึ่ง แต่เป็น... ผลงานของพวกเราทุกคน"

    return


label nextopia_story_36_to_37:
    scene nextopia_story_36
    PROF_NEXT "ยอดเยี่ยมมาก! ตอนนี้เธอเข้าใจแล้วว่า การเปลี่ยนโลก ไม่ใช่หน้าที่ของฮีโร่เพียงคนเดียว แต่มาจากความร่วมมือของทุกคน"

    scene nextopia_story_37
    PROF_NEXT "ต้นไม้นี้... ไม่ได้เติบโตด้วยปาฏิหาริย์ แต่มันเติบโต... จากความรู้ของมนุษย์"

    return


label nextopia_story_38_only:
    scene nextopia_story_38
    PROF_NEXT "จำไว้ให้ดี... อาวุธที่ยิ่งใหญ่ที่สุด ไม่ใช่พลัง แต่คือ... ความรู้ที่ถูกนำไปลงมือทำ"

    return


label nextopia_conclusion_sequence:
    scene nextopia_conclusion_1
    PROF_NEXT "ภารกิจนี้สอดคล้องกับ SDG 4 การศึกษาที่มีคุณภาพ"

    scene nextopia_conclusion_2
    pause

    scene nextopia_conclusion_3
    PROF_NEXT "คุณคือแสงแห่งการเรียนรู้ที่ช่วยสร้าง NEXTOPIA ให้สว่างไสว เดินหน้าต่อไป เพราะการเรียนรู้ไม่มีที่สิ้นสุด!"

    return


screen nextopia_minigame_tutorial_1():
    tag nextopia_minigame_tutorial_1
    modal True
    add "nextopia_minigame_tutorial_asset_1"
    button:
        xfill True
        yfill True
        background None
        hover_background None
        action Return()
    key "K_RETURN" action Return()
    key "K_SPACE" action Return()
    key "K_RIGHT" action Return()

screen nextopia_minigame_tutorial_2():
    tag nextopia_minigame_tutorial_2
    modal True
    add "nextopia_minigame_tutorial_asset_2"
    button:
        xfill True
        yfill True
        background None
        hover_background None
        action Return()
    key "K_RETURN" action Return()
    key "K_SPACE" action Return()
    key "K_RIGHT" action Return()

screen nextopia_minigame_tutorial_3():
    tag nextopia_minigame_tutorial_3
    modal True
    add "nextopia_minigame_tutorial_asset_3"
    button:
        xfill True
        yfill True
        background None
        hover_background None
        action Return()
    key "K_RETURN" action Return()
    key "K_SPACE" action Return()
    key "K_RIGHT" action Return()

label nextopia_minigame_tutorial:
    call screen nextopia_minigame_tutorial_1
    call screen nextopia_minigame_tutorial_2
    call screen nextopia_minigame_tutorial_3
    return


label nextopia_hidden_game(game_id):
    $ nextopia_hidden_keep_playing = True

    while nextopia_hidden_keep_playing:
        $ nextopia_hidden_reset(game_id)
        call screen nextopia_hidden_object_screen(game_id)
        $ nextopia_hidden_outcome = _return

        if nextopia_hidden_outcome == "success":
            $ nextopia_hp_record = nextopia_register_win(game_id, assisted=False)
            call screen nextopia_hidden_result_screen(
                game_id,
                "success",
                nextopia_hp_record["previous_hp"],
                nextopia_hp_record["current_hp"],
                nextopia_hp_record["damage"],
            )
            $ nextopia_hidden_keep_playing = False
        else:
            call screen nextopia_hidden_result_screen(game_id, nextopia_hidden_outcome)
            if _return == "assist":
                $ nextopia_hp_record = nextopia_register_win(game_id, assisted=True)
                call screen nextopia_hidden_result_screen(
                    game_id,
                    "assist",
                    nextopia_hp_record["previous_hp"],
                    nextopia_hp_record["current_hp"],
                    nextopia_hp_record["damage"],
                )
                $ nextopia_hidden_keep_playing = False

    return


label Waste_to_Wonder:
    call nextopia_hidden_game("waste")
    return


label Food_Rescue:
    call nextopia_hidden_game("food")
    return


label Harmonious_Nature:
    call nextopia_hidden_game("nature")
    return


label Collective_Clean_Energy:
    call nextopia_hidden_game("energy")
    return


label Future_Knowledge:
    call nextopia_hidden_game("knowledge")
    return


# -----------------------------------------------------------------------------
# NEXTOPIA chapter order
# -----------------------------------------------------------------------------

label nextopia_start:
    $ save_name = "NEXTOPIA"
    window hide
    $ nextopia_play_stage_bgm()
    scene nextopia black with fade

    # Scenes 16-24 -> Sustainability Decision -> Waste to Wonder.
    call nextopia_story_16_to_24
    call sustainability_decision("nextopia")
    call nextopia_minigame_tutorial
    $ nextopia_prepare_stage_run()
    call Waste_to_Wonder

    # Scenes 25-27 -> Food Rescue.
    call nextopia_story_25_to_27
    call Food_Rescue

    # Scenes 28-31 -> Harmonious Nature.
    call nextopia_story_28_to_31
    call Harmonious_Nature

    # Scenes 32-35 -> Collective Clean Energy.
    call nextopia_story_32_to_35
    call Collective_Clean_Energy

    # Scenes 36-37 -> Future Knowledge.
    call nextopia_story_36_to_37
    call Future_Knowledge

    # Scene 38 -> three conclusion scenes -> result UI -> learning flow.
    call nextopia_story_38_only
    call nextopia_conclusion_sequence
    $ nextopia_sync_stage_hp()
    $ nextopia_stage_current_hp = 0
    $ nextopia_reward_record = nextopia_grant_rewards()
    call screen nextopia_final_screen

    $ nextopia_stop_stage_bgm()
    call stage_learning_flow("nextopia", "lumpini_start")
    $ nextopia_next_label = _return

    if nextopia_next_label == "lumpini_start":
        jump lumpini_start

    return
