# =============================================================================
# rama4.rpy — ด่านที่ 1: RAMA 4 ROAD (SDG 11) — Net Zero Mission
# เนื้อเรื่องช่วงก่อน/หลังมินิเกม + มินิเกมแยกขยะ 25 ชิ้น 5 บ้าน
# พอร์ตระบบเกมทั้งหมดจาก "Meow Khiao Draft 3" (React/TypeScript) มาเป็น Ren'Py
#
# ตำแหน่ง asset ที่ใช้:
#   - ภาพเนื้อเรื่อง : images/story/1-RAMA_4_ROAD/   (ประกาศนามแฝงใน screens.rpy)
#   - ภาพมินิเกม    : minigames/1-RAMA_4_ROAD/images/ (garbage / bins / backgrounds / tutorial)
#   - เพลงประกอบ    : audio/1-RAMA_4_ROAD/           (เล่นจาก script.rpy)
#   - วิดีโอสรุป     : videos/1-RAMA_4_ROAD/RAMA_4_ROAD.ogv (ผ่าน learning_connections.rpy)
#
# สรุปการแปลง syntax (Draft 3  ->  Ren'Py):
#   - React useState<GameState>   ->  default nz_* (ตัวแปร persistent)
#   - Sustainability Decision      ->  shared sustainability_core.rpy
#   - Component WasteSortTutorial  ->  screen nz_tutorial_screen
#   - Component Rama4RoadGame       ->  screen nz_sorting_screen + nz_validate/nz_tick/nz_advance
#   - Component SdgResultScreen     ->  screen nz_result_screen
#   - CarbonMonster                ->  shared HP + screen nz_hud
#   - AudioEngine (Web Audio)       ->  nz_sfx() (เล่นไฟล์เสียงถ้ามี ไม่งั้นเงียบ)
#
# จุดเข้าเกม: jump nz_mission  (ถูกเรียกจาก script.rpy)
# ใช้ prefix nz_ กับทุกตัวแปร เพื่อไม่ชนของเดิมในโปรเจกต์
# =============================================================================


# ---------------------------------------------------------------------------
# 1) STATE  (เทียบเท่า interface GameState ของ Draft 3)
# ---------------------------------------------------------------------------
default nz_eco_score = 0            # ecoScore
default nz_carbon_footprint = 50    # carbonFootprint (0..100, เริ่ม 50%)
default nz_monster_hp = 30000       # Carbon Monster HP แบบตัวเลขจริง
default nz_carbon_tax = 0           # carbonTax (บาท)
default nz_budget = 1000            # budget (กระเป๋าเงิน, บาท)
default nz_selected_cat = "bastian-orange"   # selectedCat
default nz_level = 1                # level
default nz_lives = 3               # lives (หัวใจ)
default nz_sorted_count = 0         # sortedCount
default nz_user_choice = None       # userChoice: "bicycle" | "sports_car"
default nz_badges = []              # ตราสัญลักษณ์ SDG ที่ปลดล็อก

# ตัวแปรควบคุมรอบเล่นมินิเกม (ภายในด่าน Rama 4)
default nz_house_index = 0          # currentHouseIndex
default nz_item_index = 0           # currentItemIndex
default nz_time_left = 45.0         # timeLeft (วินาที, นับถอยหลัง)
default nz_feedback = ""            # ข้อความผลลัพธ์ล่าสุด
default nz_feedback_title = ""
default nz_feedback_detail = ""
default nz_feedback_correct = False
default nz_feedback_visible = False
default nz_pending_advance = False
default nz_round_items = []         # ขยะจริงจาก minigames/1-RAMA_4_ROAD/images/garbage (shuffle ใหม่ทุกรอบ)
default nz_route_houses = []        # แบ่งขยะทั้งหมดออกเป็น 5 บ้าน
default nz_total_items = 0
default nz_correct_count = 0
default nz_wrong_count = 0
default nz_elapsed_time = 0.0
default nz_reward_eco = 0
default nz_reward_coins = 0
default nz_rewards_applied = False
default nz_monster_start_hp = 30000
# ตัวแปรควบคุมแท็บของหน้าจอข้อมูล
default nz_tut_tab = "howto"
default nz_res_tab = "sdg11"


# ---------------------------------------------------------------------------
# 2) DATA + LOGIC  (เทียบเท่า const data + ฟังก์ชันใน Draft 3)
# ---------------------------------------------------------------------------
init python:

    # --- เสียงเอฟเฟกต์ (พอร์ตจาก AudioEngine) -------------------------------
    # Draft 3 สังเคราะห์เสียงด้วย Web Audio; ใน Ren'Py ให้วางไฟล์เสียงไว้ที่
    # game/audio/1-RAMA_4_ROAD/sfx/<name>.ogg แล้วระบบจะเล่นให้อัตโนมัติ
    # (ปัจจุบันยังไม่มีไฟล์เสียงเอฟเฟกต์ -> เงียบ ไม่ error)
    #   success / error / levelup / choice_eco / choice_polluter
    def nz_sfx(name):
        path = "audio/1-RAMA_4_ROAD/sfx/" + name + ".ogg"
        if renpy.loadable(path):
            renpy.sound.play(path)

    # --- ถังขยะ 4 สี (เทียบ binGuideData / binsList) -----------------------
    NZ_CAT_NAMES = {
        "organic":   "อินทรีย์ (เขียว)",
        "recycle":   "รีไซเคิล (เหลือง)",
        "general":   "ทั่วไป (น้ำเงิน)",
        "hazardous": "อันตราย (แดง)",
    }

    NZ_BINS = [
        {"cat": "organic",   "label": "ขยะอินทรีย์", "sub": "ORGANIC / ถังเขียว",
         "accepts": "เศษอาหาร เปลือกผลไม้ ใบไม้แห้ง",     "avoid": "พลาสติก/โฟมเปื้อนอาหาร"},
        {"cat": "recycle",   "label": "ขยะรีไซเคิล", "sub": "RECYCLE / ถังเหลือง",
         "accepts": "ขวด PET แก้ว กล่องนม UHT กระป๋อง",   "avoid": "แก้วแตก ถุงเปื้อนแกง"},
        {"cat": "general",   "label": "ขยะทั่วไป",   "sub": "GENERAL / ถังน้ำเงิน",
         "accepts": "โฟมเปื้อน ซองขนม ช้อนพลาสติกใช้เดียว", "avoid": "ถ่านไฟฉาย สารเคมี"},
        {"cat": "hazardous", "label": "ขยะอันตราย",  "sub": "HAZARDOUS / ถังแดง",
         "accepts": "ถ่านไฟฉาย หลอดไฟ กระป๋องสเปรย์",      "avoid": "ฝากระป๋องน้ำธรรมดา"},
    ]

    # ข้อมูลสำหรับ legend แบบ code-native ใน Tutorial เท่านั้น
    # ส่วนหน้าจอเล่นจริงใช้ภาพระบบถัง 4 ช่องที่ติดตั้งรวมกับรถเป็นภาพเดียว
    # และใช้ hitbox โปร่งใสซ้อนตามตำแหน่งช่องรับ โดยไม่วาดภาพถังเพิ่มอีกชั้น
    NZ_BIN_VISUALS = {
        "organic":   {"color": "#166534", "symbol": "ใบไม้"},
        "recycle":   {"color": "#a16207", "symbol": "ลูกศรรีไซเคิล"},
        "general":   {"color": "#1d4ed8", "symbol": "คนทิ้งขยะ"},
        "hazardous": {"color": "#b91c1c", "symbol": "เครื่องหมายอันตราย"},
    }

    # --- Metadata ของภาพทุกไฟล์ใน minigames/1-RAMA_4_ROAD/images/garbage ---------------
    # ระบบค้นหาไฟล์จริงด้วย renpy.list_files() ทุกครั้งก่อนเริ่มรอบ จึงไม่ตกหล่น
    # แม้ลำดับไฟล์บนดิสก์เปลี่ยน และจะสุ่มลำดับใหม่ด้วย renpy.random.shuffle().
    NZ_GARBAGE_META = {
        "aluminum_can.png": {"name": "กระป๋องอะลูมิเนียม", "category": "recycle", "desc": "ล้างให้สะอาดและบีบให้แบน โลหะนำกลับมารีไซเคิลได้"},
        "apple.png": {"name": "เศษแอปเปิล", "category": "organic", "desc": "เศษผลไม้ย่อยสลายได้ เหมาะสำหรับทำปุ๋ยหมัก"},
        "banana.png": {"name": "เปลือกกล้วย", "category": "organic", "desc": "เปลือกผลไม้เป็นขยะเปียก ย่อยสลายและทำปุ๋ยได้"},
        "battery_old.png": {"name": "ถ่านไฟฉายเก่า", "category": "hazardous", "desc": "มีสารเคมีและโลหะหนัก ต้องแยกส่งกำจัดอย่างปลอดภัย"},
        "bottle1.png": {"name": "ขวดพลาสติกใส", "category": "recycle", "desc": "เทของเหลวออก ล้าง และบีบขวดก่อนส่งรีไซเคิล"},
        "bread.png": {"name": "เศษขนมปัง", "category": "organic", "desc": "เศษอาหารย่อยสลายได้ ไม่ควรปนกับวัสดุรีไซเคิล"},
        "cardbord.png": {"name": "กระดาษลัง", "category": "recycle", "desc": "พับให้แบนและเก็บให้แห้งเพื่อรักษามูลค่ารีไซเคิล"},
        "carrot.png": {"name": "เศษแครอต", "category": "organic", "desc": "เศษผักเป็นขยะอินทรีย์ ใช้ทำปุ๋ยหมักได้"},
        "cloth.png": {"name": "เศษผ้าชำรุด", "category": "general", "desc": "ถ้ายังใช้ได้ควรบริจาค; หากชำรุดและไม่มีจุดรับผ้าให้ทิ้งทั่วไป"},
        "crange.png": {"name": "เปลือกส้ม", "category": "organic", "desc": "เปลือกผลไม้ย่อยสลายได้ ควรแยกจากขยะแห้ง"},
        "eggshell.png": {"name": "เปลือกไข่", "category": "organic", "desc": "บดผสมปุ๋ยหมักได้และช่วยเพิ่มแคลเซียมให้ดิน"},
        "foam.png": {"name": "กล่องโฟมใช้แล้ว", "category": "general", "desc": "โฟมเปื้อนอาหารรีไซเคิลยาก ให้ทิ้งเป็นขยะทั่วไป"},
        "glass_jar.png": {"name": "ขวดแก้ว", "category": "recycle", "desc": "ล้างให้สะอาด แยกฝา และระวังไม่ให้แตกก่อนส่งรีไซเคิล"},
        "lightbulb2.png": {"name": "หลอดไฟใช้แล้ว", "category": "hazardous", "desc": "อาจมีสารปรอทและเศษแก้ว ต้องใส่กล่องป้องกันแตกแล้วแยกทิ้ง"},
        "medicine.png": {"name": "ยาเหลือใช้", "category": "hazardous", "desc": "ห้ามทิ้งลงชักโครก ควรส่งคืนโรงพยาบาลหรือจุดรับยา"},
        "newspaper.png": {"name": "หนังสือพิมพ์", "category": "recycle", "desc": "กระดาษสะอาดและแห้งสามารถนำกลับมารีไซเคิลได้"},
        "paint_can2.png": {"name": "กระป๋องสี", "category": "hazardous", "desc": "สีและตัวทำละลายตกค้างเป็นสารอันตราย ต้องแยกกำจัด"},
        "paper.png": {"name": "กระดาษใช้แล้ว", "category": "recycle", "desc": "กระดาษแห้งไม่เปื้อนอาหารรีไซเคิลได้ ควรพับให้เรียบร้อย"},
        "paper_cup.png": {"name": "แก้วกระดาษเคลือบ", "category": "general", "desc": "มีชั้นเคลือบและมักเปื้อนเครื่องดื่ม จึงแยกรีไซเคิลได้ยาก"},
        "pesticade.png": {"name": "ภาชนะสารกำจัดศัตรูพืช", "category": "hazardous", "desc": "มีสารพิษตกค้าง ห้ามล้างลงท่อและต้องส่งจุดรับขยะอันตราย"},
        "plastic_bag.png": {"name": "ถุงพลาสติกใช้แล้ว", "category": "general", "desc": "ฟิล์มพลาสติกปนเปื้อนและพันเครื่องจักรง่าย ให้ทิ้งทั่วไปเมื่อไม่มีจุดรับเฉพาะ"},
        "plastic_bottle.png": {"name": "ขวดน้ำพลาสติก PET", "category": "recycle", "desc": "เทน้ำออก ล้าง บีบ และปิดฝาเพื่อประหยัดพื้นที่ขนส่ง"},
        "plastic_wrapper.png": {"name": "ซองพลาสติกหลายชั้น", "category": "general", "desc": "วัสดุหลายชั้นแยกออกจากกันยาก จึงเป็นขยะทั่วไป"},
        "rubber_band.png": {"name": "หนังยาง", "category": "general", "desc": "ชิ้นเล็กและไม่มีระบบรับรีไซเคิลทั่วไป ควรรวบรวมก่อนทิ้ง"},
        "snack_bag.png": {"name": "ถุงขนม", "category": "general", "desc": "ซองฟิล์มผสมอะลูมิเนียมรีไซเคิลในระบบทั่วไปได้ยาก"},
    }

    NZ_HOUSE_NAMES = [
        "ทาวน์เฮาส์ท้ายซอยพระราม 4",
        "บ้านเดี่ยวหัวมุมรักษ์โลก",
        "ร้านอาหารชุมชนพระราม 4",
        "สมาร์ทแมนชั่นพระราม 4",
        "บ้านริมคลองพระราม 4",
    ]

    # --- helpers --------------------------------------------------------------
    def nz_discover_garbage():
        """คืนรายการ PNG จริงทุกไฟล์ใน minigames/1-RAMA_4_ROAD/images/garbage พร้อม metadata สำหรับสอน."""
        prefix = "minigames/1-RAMA_4_ROAD/images/garbage/"
        files = sorted(
            path for path in renpy.list_files()
            if path.lower().startswith(prefix.lower()) and path.lower().endswith(".png")
        )
        items = []
        for path in files:
            filename = path.rsplit("/", 1)[-1]
            meta = dict(NZ_GARBAGE_META.get(filename, {}))
            if not meta:
                pretty_name = filename.rsplit(".", 1)[0].replace("_", " ").title()
                meta = {
                    "name": pretty_name,
                    "category": "general",
                    "desc": "ยังไม่มีข้อมูลเฉพาะ ระบบจัดเป็นขยะทั่วไปชั่วคราว",
                }
            meta["filename"] = filename
            meta["image"] = path
            items.append(meta)
        return items

    def nz_build_houses(items):
        """กระจายขยะที่ shuffle แล้วให้ครบ 5 บ้าน โดยใช้ทุกชิ้นหนึ่งครั้ง."""
        if not items:
            return []
        house_count = min(len(NZ_HOUSE_NAMES), len(items))
        base_size = len(items) // house_count
        remainder = len(items) % house_count
        houses = []
        cursor = 0
        for index in range(house_count):
            size = base_size + (1 if index < remainder else 0)
            houses.append({
                "name": "House %d" % (index + 1),
                "thai": NZ_HOUSE_NAMES[index],
                "items": items[cursor:cursor + size],
            })
            cursor += size
        return houses

    def nz_reset():
        # เทียบ handleRestart / initial state ของ Draft 3
        store.nz_eco_score = 0
        store.nz_carbon_footprint = 50
        store.nz_monster_hp = 30000
        store.nz_monster_start_hp = 30000
        store.nz_carbon_tax = 0
        # Mirror the shared Meow Coin wallet, including on a replay where the
        # Sustainability Decision is only recapped and therefore is not
        # applied a second time.
        store.nz_budget = int(getattr(store, "mk_meow_coins", 1000))
        store.nz_selected_cat = "bastian-orange"
        store.nz_level = 1
        store.nz_lives = 3
        store.nz_sorted_count = 0
        store.nz_user_choice = None
        store.nz_badges = []
        store.nz_house_index = 0
        store.nz_item_index = 0
        store.nz_time_left = 45.0
        store.nz_feedback = ""
        store.nz_feedback_title = ""
        store.nz_feedback_detail = ""
        store.nz_feedback_correct = False
        store.nz_feedback_visible = False
        store.nz_pending_advance = False
        store.nz_round_items = []
        store.nz_route_houses = []
        store.nz_total_items = 0
        store.nz_correct_count = 0
        store.nz_wrong_count = 0
        store.nz_elapsed_time = 0.0
        store.nz_reward_eco = 0
        store.nz_reward_coins = 0
        store.nz_rewards_applied = False

    def nz_get_stage_start_hp():
        """อ่าน HP หลัง Sustainability Decision และมี fallback ที่ lint/runtime ปลอดภัย."""
        getter = getattr(store, "mk_get_stage_start_hp", None)
        if getter is not None:
            try:
                return max(1, int(getter("rama4")))
            except Exception:
                pass
        return 30000

    def nz_sync_shared_hp(value):
        """ทำให้ HUD, Lobby และฐานข้อมูลกลางเห็น HP ค่าเดียวกับมินิเกม."""
        setter = getattr(store, "mk_set_stage_current_hp", None)
        if setter is not None:
            try:
                setter("rama4", max(0, int(value)))
            except Exception:
                pass

    def nz_start_route():
        # อ่านทุก PNG จากโฟลเดอร์จริงและ shuffle ใหม่ทุกครั้งที่เริ่มรอบ
        items = nz_discover_garbage()
        renpy.random.shuffle(items)
        store.nz_round_items = items
        store.nz_route_houses = nz_build_houses(items)
        store.nz_total_items = len(items)
        store.nz_house_index = 0
        store.nz_item_index = 0
        store.nz_time_left = 45.0
        store.nz_feedback = ""
        store.nz_feedback_title = ""
        store.nz_feedback_detail = ""
        store.nz_feedback_visible = False
        store.nz_pending_advance = False
        store.nz_correct_count = 0
        store.nz_wrong_count = 0
        store.nz_sorted_count = 0
        store.nz_elapsed_time = 0.0
        store.nz_reward_eco = 0
        store.nz_reward_coins = 0
        store.nz_rewards_applied = False
        store.nz_monster_start_hp = nz_get_stage_start_hp()
        store.nz_monster_hp = store.nz_monster_start_hp
        nz_sync_shared_hp(store.nz_monster_hp)

    def nz_route_complete():
        return bool(store.nz_route_houses) and store.nz_house_index >= len(store.nz_route_houses)

    def nz_current_house_complete():
        if nz_route_complete() or not store.nz_route_houses:
            return True
        return store.nz_item_index >= len(store.nz_route_houses[store.nz_house_index]["items"])

    def nz_active_item():
        if nz_route_complete() or not store.nz_route_houses:
            return None
        house = store.nz_route_houses[store.nz_house_index]
        if store.nz_item_index < 0 or store.nz_item_index >= len(house["items"]):
            return None
        return house["items"][store.nz_item_index]

    def nz_advance():
        # เลื่อนไปขยะชิ้นถัดไปหรือบ้านถัดไป หลังผู้เล่นอ่าน tutorial รายชิ้นแล้ว
        if nz_route_complete() or not store.nz_route_houses:
            return
        house = store.nz_route_houses[store.nz_house_index]
        if store.nz_item_index < len(house["items"]) - 1:
            store.nz_item_index += 1
        else:
            store.nz_house_index += 1
            store.nz_item_index = 0
            store.nz_time_left = 45.0
            nz_sfx("levelup")
        if nz_route_complete():
            store.nz_monster_hp = 0
            nz_sync_shared_hp(0)

    def nz_validate(target):
        # แสดง tutorial หลังการทิ้งทุกครั้ง ก่อนเลื่อนไปชิ้นถัดไป
        if store.nz_lives <= 0 or nz_route_complete() or store.nz_feedback_visible:
            return
        item = nz_active_item()
        if item is None:
            return
        if item["category"] == target:
            nz_sfx("success")
            store.nz_eco_score += 50
            store.nz_carbon_footprint = max(0, store.nz_carbon_footprint - 2)
            store.nz_sorted_count += 1
            store.nz_correct_count += 1
            # คำนวณจาก progress สะสมเพื่อให้เศษจากการหารไม่ทำให้ HP ติดลบ
            # และขยะชิ้นสุดท้ายทำให้ HP เป็นศูนย์พอดีเสมอ
            damage_done = int(round(
                (store.nz_monster_start_hp * store.nz_sorted_count) /
                float(max(1, store.nz_total_items))
            ))
            store.nz_monster_hp = max(0, store.nz_monster_start_hp - damage_done)
            nz_sync_shared_hp(store.nz_monster_hp)
            store.nz_feedback_correct = True
            store.nz_feedback_title = "ถูกต้อง — %s" % NZ_CAT_NAMES[item["category"]]
            store.nz_feedback_detail = "%s\nผลลัพธ์: Eco +50 • Carbon Footprint -2%%" % item["desc"]
            store.nz_feedback = "%s ลงถัง%sถูกต้อง" % (item["name"], NZ_CAT_NAMES[item["category"]])
            store.nz_pending_advance = True
        else:
            nz_sfx("error")
            store.nz_lives = max(0, store.nz_lives - 1)
            store.nz_wrong_count += 1
            store.nz_carbon_footprint = min(100, store.nz_carbon_footprint + 4)
            store.nz_carbon_tax += 25
            if hasattr(store, "mk_meow_coins"):
                store.mk_meow_coins = max(0, int(store.mk_meow_coins) - 25)
                store.nz_budget = int(store.mk_meow_coins)
            else:
                store.nz_budget = max(0, store.nz_budget - 25)
            store.nz_feedback_correct = False
            store.nz_feedback_title = "ยังไม่ถูก — ต้องเป็น%s" % NZ_CAT_NAMES[item["category"]]
            store.nz_feedback_detail = "คุณเลือก%s\n%s\nเสียหัวใจ 1 ดวง • Carbon Tax ฿25" % (
                NZ_CAT_NAMES.get(target, target), item["desc"]
            )
            store.nz_feedback = "%s ต้องลงถัง%s" % (item["name"], NZ_CAT_NAMES[item["category"]])
            store.nz_pending_advance = False
        store.nz_feedback_visible = True

    def nz_continue_feedback():
        should_advance = store.nz_pending_advance
        store.nz_feedback_visible = False
        store.nz_pending_advance = False
        if should_advance:
            nz_advance()

    def nz_tick():
        # จับเวลาแยกต่อบ้าน และ pause ขณะเปิด tutorial feedback
        if store.nz_lives <= 0 or nz_route_complete() or store.nz_feedback_visible:
            return
        store.nz_time_left = round(store.nz_time_left - 0.1, 1)
        store.nz_elapsed_time = round(store.nz_elapsed_time + 0.1, 1)
        if store.nz_time_left <= 0:
            nz_sfx("error")
            store.nz_lives = max(0, store.nz_lives - 1)
            store.nz_wrong_count += 1
            store.nz_time_left = 45.0
            store.nz_feedback = "หมดเวลา เสียหัวใจ 1 ดวง และเริ่มจับเวลาบ้านนี้ใหม่"
            store.nz_feedback_correct = False
            store.nz_feedback_title = "หมดเวลาของบ้านนี้"
            store.nz_feedback_detail = "เวลารีเซ็ตเป็น 45 วินาที ลองสังเกตวัสดุและสีถังอีกครั้ง"
            store.nz_pending_advance = False
            store.nz_feedback_visible = True

    def nz_retry_current_house():
        """เริ่มต่อในบ้านเดิมโดยเก็บ progress ที่แยกถูกแล้วไว้."""
        store.nz_lives = 3
        store.nz_time_left = 45.0
        store.nz_feedback = ""
        store.nz_feedback_title = ""
        store.nz_feedback_detail = ""
        store.nz_feedback_visible = False
        store.nz_pending_advance = False

    def nz_apply_rewards():
        # รางวัลหลักแจกผ่านระบบกลางทันทีเมื่อแยกครบ ไม่ผูกกับการดูวิดีโอ
        # และใช้ claim ledger เดียวกับ Achievement/Lobby เพื่อป้องกันรับซ้ำ
        if store.nz_rewards_applied:
            return
        nz_sfx("levelup")
        grant_rewards = getattr(store, "mk_grant_stage_rewards", None)
        reward = grant_rewards("rama4") if callable(grant_rewards) else None
        reward = reward if isinstance(reward, dict) else {}
        store.nz_reward_coins = int(reward.get("coins_awarded", 0))
        store.nz_reward_eco = int(reward.get("eco_score_awarded", 0))
        store.nz_eco_score += store.nz_reward_eco
        store.nz_budget = int(reward.get(
            "coin_balance",
            getattr(store, "mk_meow_coins", store.nz_budget),
        ))
        store.nz_rewards_applied = True

    def nz_accuracy():
        attempts = store.nz_correct_count + store.nz_wrong_count
        if attempts <= 0:
            return 0
        return int(round((store.nz_correct_count * 100.0) / attempts))

    # --- ฟังก์ชันควบคุมระบบ Drag and Drop -----------------------------------
    def nz_drag_callback(drags, drop):
        if drop is not None:
            nz_validate(drop.drag_name)
        
        # ดีดกลับมาที่พิกัดพิกเซลกึ่งกลางจอที่แน่นอน (พิกัดการ์ดขยะชิ้นกลาง)
        drags[0].snap(800, 230, delay=0.0)
        renpy.restart_interaction()
        return None


# ---------------------------------------------------------------------------
# 3) HUD  (Carbon Monster HP + mission stats)
# ---------------------------------------------------------------------------
# ภาพเดียวประกอบด้วยท้ายรถและระบบช่องรับขยะทั้ง 4 ประเภท
# จงอย่าวาดภาพถังแยกทับอีก เพื่อป้องกันถังซ้อนกันใน gameplay
image nz sorting truck v3 = Transform(
    "minigames/1-RAMA_4_ROAD/images/backgrounds/sorting_truck_4_compartment.png",
    xysize=(1920, 1080)
)

screen nz_hud():
    $ foot_color = "#f43f5e" if nz_carbon_footprint > 70 else "#34d399"

    frame:
        xfill True
        yalign 0.0
        ysize 108
        background "#020817f2"
        padding (34, 15)
        hbox:
            xfill True
            spacing 42

            vbox:
                xsize 370
                spacing 2
                text "RAMA 4 ROAD" size 28 color "#67e8f9" bold True
                text "SDG 11  |  ภารกิจไม่เทรวม" size 18 color "#cbd5e1"

            vbox:
                xsize 660
                spacing 4
                hbox:
                    spacing 36
                    text "คัดแยก [nz_sorted_count]/[nz_total_items]" size 19 color "#e2e8f0" bold True
                    text "ชีวิต [nz_lives]/3" size 19 color "#fca5a5" bold True
                hbox:
                    spacing 36
                    text "ECO SCORE [nz_eco_score]" size 17 color "#86efac"
                    text "CARBON FOOTPRINT [nz_carbon_footprint]%" size 17 color foot_color

            vbox:
                xsize 650
                xalign 1.0
                spacing 4
                text "CARBON MONSTER" size 20 color "#fca5a5" xalign 1.0 bold True
                bar value StaticValue(nz_monster_hp, max(1, nz_monster_start_hp)) xsize 560 ysize 18 xalign 1.0
                text "[nz_monster_hp] / [nz_monster_start_hp] HP" size 18 color "#ffffff" xalign 1.0 bold True


# ---------------------------------------------------------------------------
# 6) คู่มือคัดแยกขยะ (เทียบ WasteSortTutorial — 4 แท็บ)
# ---------------------------------------------------------------------------
screen nz_route_screen():
    add "nz bg route"
    add Solid("#02061766")
    use nz_hud

    text "ภารกิจไม่เทรวม ตะลุยแยกขยะ 5 บ้านที่ถนนพระราม 4":
        xalign 0.5
        ypos 130
        size 36
        color "#67e8f9"
        bold True
        outlines [(2, "#000000", 0, 0)]

    text "เลือกบ้านที่ปลดล็อก ทำภารกิจให้ครบ แล้วกลับมาเลือกบ้านถัดไป":
        xalign 0.5
        ypos 184
        size 22
        color "#e2e8f0"
        outlines [(2, "#000000", 0, 0)]

    frame:
        xalign 0.5
        ypos 690
        xsize 1710
        ysize 330
        background "#04111fe8"
        padding (28, 26)

        vbox:
            xalign 0.5
            spacing 22
            hbox:
                xalign 0.5
                spacing 18
                for index, house in enumerate(nz_route_houses):
                    $ completed = index < nz_house_index
                    $ current = index == nz_house_index
                    $ card_bg = "#065f46ee" if completed else ("#0e7490ee" if current else "#172033ee")
                    $ status_text = "เสร็จแล้ว" if completed else ("พร้อมเริ่ม" if current else "ยังไม่ปลดล็อก")
                    button:
                        xsize 310
                        ysize 205
                        background card_bg
                        hover_background ("#0891b2ee" if current else card_bg)
                        insensitive_background card_bg
                        padding (16, 14)
                        sensitive current
                        action Return("start_house")
                        vbox:
                            xalign 0.5
                            spacing 8
                            text "บ้านหลังที่ [index + 1]" size 28 color "#ffffff" xalign 0.5 bold True
                            text "[house['thai']]" size 19 color "#e2e8f0" xalign 0.5 text_align 0.5
                            text "[len(house['items'])] ชิ้น" size 20 color "#fde68a" xalign 0.5 bold True
                            text status_text size 18 color ("#86efac" if completed else ("#cffafe" if current else "#94a3b8")) xalign 0.5 bold True

            if nz_route_complete():
                textbutton "ดูผลภารกิจ":
                    action Return("win")
                    xalign 0.5
                    text_color "#86efac"
                    text_size 26
            else:
                text "ความคืบหน้า [nz_house_index]/5 บ้าน  |  คัดแยกแล้ว [nz_sorted_count]/[nz_total_items] ชิ้น":
                    xalign 0.5
                    size 22
                    color "#cbd5e1"


screen _legacy_rama4_minigame_tutorial():
    add "nz bg route"
    add Solid("#020617cc")
    use nz_hud

    text "WASTE SORTING TUTORIAL":
        xalign 0.5
        ypos 118
        size 44
        color "#67e8f9"
        bold True
        outlines [(2, "#000000", 0, 0)]

    text "คู่มือภารกิจไม่เทรวม ถนนพระราม 4":
        xalign 0.5
        ypos 174
        size 28
        color "#ffffff"
        outlines [(2, "#000000", 0, 0)]

    hbox:
        xalign 0.5
        ypos 220
        spacing 20

        frame:
            xsize 540
            ysize 680
            background "#061523f2"
            padding (30, 24)
            vbox:
                spacing 15
                text "1  วิธีเล่น" size 34 color "#67e8f9" bold True
                text "เลือกบ้านที่ปลดล็อกจากแผนที่" size 26 color "#ffffff" bold True
                text "ลากขยะทีละชิ้นไปยังถังที่ถูกประเภท" size 25 color "#dbeafe" line_spacing 3
                text "อ่านคำอธิบายหลังวางทุกชิ้น ก่อนดำเนินต่อ" size 25 color "#dbeafe" line_spacing 3
                text "เมื่อคัดครบหนึ่งบ้าน เกมจะพากลับสู่แผนที่" size 25 color "#dbeafe" line_spacing 3
                null height 5
                text "ระบบใช้ภาพขยะจริงครบทั้ง [nz_total_items] ชิ้น และสุ่มลำดับใหม่ทุกครั้งที่เริ่มภารกิจ" size 24 color "#a7f3d0" line_spacing 3

        frame:
            xsize 540
            ysize 680
            background "#061523f2"
            padding (24, 22)
            vbox:
                spacing 13
                text "2  ถังขยะ 4 ประเภท" size 34 color "#fcd34d" bold True xalign 0.5
                grid 2 2:
                    xalign 0.5
                    spacing 14
                    for b in NZ_BINS:
                        $ bin_visual = NZ_BIN_VISUALS[b["cat"]]
                        vbox:
                            xsize 226
                            ysize 270
                            spacing 7
                            frame:
                                xalign 0.5
                                xsize 190
                                ysize 145
                                background bin_visual["color"]
                                padding (10, 10)
                                vbox:
                                    xalign 0.5
                                    yalign 0.5
                                    spacing 5
                                    text "ช่องรับ" size 20 color "#ffffff" xalign 0.5 bold True
                                    text "[bin_visual['symbol']]" size 28 color "#ffffff" xalign 0.5 text_align 0.5 bold True line_spacing 2
                            text "[b['label']]" size 24 color "#ffffff" xalign 0.5 bold True
                            text "[b['sub']]" size 18 color "#cbd5e1" xalign 0.5

        frame:
            xsize 540
            ysize 680
            background "#061523f2"
            padding (30, 24)
            vbox:
                spacing 14
                text "3  กติกาภารกิจ" size 34 color "#fca5a5" bold True
                text "ถูกประเภท" size 27 color "#86efac" bold True
                text "ลด HP อสูรคาร์บอน และเพิ่ม ECO SCORE" size 24 color "#dbeafe" line_spacing 3
                text "ผิดประเภท" size 27 color "#fca5a5" bold True
                text "เสียชีวิต 1 หน่วย และเสีย Carbon Tax 25" size 24 color "#dbeafe" line_spacing 3
                text "เวลา" size 27 color "#fcd34d" bold True
                text "มีเวลา 45 วินาทีต่อบ้าน เวลาจะหยุดระหว่างอ่านคำอธิบาย" size 24 color "#dbeafe" line_spacing 3
                text "เป้าหมาย" size 27 color "#67e8f9" bold True
                text "คัดครบ 5 บ้าน เพื่อทำให้ Carbon Monster HP เหลือ 0" size 24 color "#dbeafe" line_spacing 3

    textbutton "เริ่มภารกิจไม่เทรวม":
        action Return()
        xalign 0.5
        ypos 930
        xminimum 480
        yminimum 70
        background "#065f46"
        hover_background "#059669"
        text_color "#ffffff"
        text_size 31
        text_bold True

screen rama4_minigame_tutorial():
    """Image-only tutorial. The artwork contains the complete instructions."""
    tag rama4_minigame_tutorial
    modal True
    add "rama4_minigame_tutorial_asset"
    button:
        xfill True
        yfill True
        background None
        hover_background None
        action Return()
    key "K_RETURN" action Return()
    key "K_SPACE" action Return()
    key "K_RIGHT" action Return()
# ---------------------------------------------------------------------------
# 7) ด่านคัดแยกขยะหลัก  (เวอร์ชัน DRAG AND DROP - FIX ตำแหน่งถังขยะด้านล่าง)
# ---------------------------------------------------------------------------
screen nz_sorting_screen():
    # ภาพ composite นี้มีท้ายรถและช่องรับทั้ง 4 ช่องอยู่แล้ว จึงแสดงเพียงครั้งเดียว
    add "nz sorting truck v3"
    add Solid("#02061788")
    use nz_hud

    timer 0.1 repeat True action Function(nz_tick)

    if nz_route_complete() and not nz_feedback_visible:
        timer 0.35 action Return("win")
    elif nz_lives <= 0 and not nz_feedback_visible:
        timer 0.35 action Return("lose")

    $ item = nz_active_item()
    $ item_name = item["name"] if item else ""
    $ item_image = item["image"] if item else None
    $ item_desc = item["desc"] if item else ""
    $ house = nz_route_houses[nz_house_index] if item else None
    $ house_name = house["thai"] if house else ""
    $ house_total = len(house["items"]) if house else 0
    $ house_count = len(nz_route_houses)
    $ time_color = "#f43f5e" if nz_time_left <= 10 else "#fbbf24"

    # --- ส่วนข้อมูลสถานะด้านบน ---
    vbox:
        xalign 0.5
        ypos 118
        spacing 5
        if item:
            text "บ้านหลังที่ [nz_house_index + 1]/[house_count] — [house_name]" size 25 color "#fcd34d" xalign 0.5 bold True outlines [(2, "#000", 0, 0)]
            text "ชิ้นที่ [nz_item_index + 1]/[house_total]  |  รวม [nz_sorted_count]/[nz_total_items]  |  เวลา [nz_time_left] วินาที" size 21 color time_color xalign 0.5 outlines [(2, "#000", 0, 0)]

    # แสดง error เฉพาะเมื่อเริ่มรอบแล้วไม่มี asset จริงเท่านั้น ไม่แสดงระหว่างจบชิ้นสุดท้าย
    if not item and not nz_route_complete() and not nz_feedback_visible:
        frame:
            xalign 0.5
            yalign 0.5
            background "#3f0d19ee"
            padding (35, 28)
            vbox:
                spacing 12
                text "ไม่พบข้อมูลขยะสำหรับบ้านนี้" size 28 color "#fecaca" xalign 0.5
                text "กรุณาตรวจสอบไฟล์ใน game/minigames/1-RAMA_4_ROAD/images/garbage" size 20 color "#ffffff" xalign 0.5
                textbutton "กลับ" action Return("lose") xalign 0.5 text_color "#fda4af"

    if item:
        draggroup:
            # ขยะที่กำลังเล่นไม่มีพื้นหลังการ์ด เพื่อให้ silhouette อ่านง่าย
            drag:
                drag_name "garbage"
                droppable False
                draggable (not nz_feedback_visible)
                dragged nz_drag_callback
                xpos 800
                ypos 230
                xsize 320
                ysize 350

                vbox:
                    xalign 0.5
                    yalign 0.5
                    spacing 8
                    if item_image:
                        add item_image xysize (220, 220) fit "contain" xalign 0.5
                    text "[item_name]" size 27 color "#ffffff" xalign 0.5 text_align 0.5 bold True outlines [(3, "#020617", 0, 0)]
                    text "ลากไปยังถังที่ถูกประเภท" size 19 color "#a5f3fc" xalign 0.5 bold True outlines [(2, "#020617", 0, 0)]

            drag:
                drag_name "organic"
                draggable False
                droppable True
                # ช่องเขียวในภาพ composite: x≈300..630, y≈590..1030 ที่ 1920x1080
                xpos 300
                ypos 590
                xsize 330
                ysize 440
                fixed:
                    xfill True
                    yfill True
                    text "อินทรีย์  |  เขียว" size 23 xalign 0.5 ypos 0 color "#bbf7d0" bold True outlines [(3, "#000000", 0, 0)]

            drag:
                drag_name "recycle"
                draggable False
                droppable True
                # ช่องเหลืองในภาพ composite: x≈640..960
                xpos 640
                ypos 590
                xsize 320
                ysize 440
                fixed:
                    xfill True
                    yfill True
                    text "รีไซเคิล  |  เหลือง" size 23 xalign 0.5 ypos 0 color "#fef08a" bold True outlines [(3, "#000000", 0, 0)]

            drag:
                drag_name "general"
                draggable False
                droppable True
                # ช่องน้ำเงินในภาพ composite: x≈960..1280
                xpos 960
                ypos 590
                xsize 320
                ysize 440
                fixed:
                    xfill True
                    yfill True
                    text "ทั่วไป  |  น้ำเงิน" size 23 xalign 0.5 ypos 0 color "#bfdbfe" bold True outlines [(3, "#000000", 0, 0)]

            drag:
                drag_name "hazardous"
                draggable False
                droppable True
                # ช่องแดงในภาพ composite: x≈1280..1610
                xpos 1280
                ypos 590
                xsize 330
                ysize 440
                fixed:
                    xfill True
                    yfill True
                    text "อันตราย  |  แดง" size 23 xalign 0.5 ypos 0 color "#fecaca" bold True outlines [(3, "#000000", 0, 0)]

    # Tutorial หลังทิ้งขยะแต่ละชิ้น — บล็อกการลากและหยุดเวลาไว้จนกดต่อ
    if nz_feedback_visible:
        button:
            xfill True
            yfill True
            background "#020617cc"
            action NullAction()

        frame:
            xalign 0.5
            yalign 0.48
            xsize 1120
            yminimum 500
            background "#061523f5"
            padding (52, 38)

            vbox:
                xalign 0.5
                spacing 16
                text ("คัดแยกถูกต้อง" if nz_feedback_correct else "ยังไม่ถูกประเภท"):
                    size 36
                    color ("#86efac" if nz_feedback_correct else "#fca5a5")
                    xalign 0.5
                    text_align 0.5
                    bold True

                text "[nz_feedback_title]":
                    size 27
                    color "#ffffff"
                    xalign 0.5
                    text_align 0.5
                    bold True

                if item_image:
                    add item_image xysize (170, 170) fit "contain" xalign 0.5

                text "[item_name]":
                    size 28
                    color "#ffffff"
                    xalign 0.5
                    bold True

                text "[nz_feedback_detail]":
                    size 23
                    color "#dbeafe"
                    xalign 0.5
                    text_align 0.5

                if nz_lives <= 0:
                    textbutton "หัวใจหมด — ดูผลภารกิจ":
                        action Return("lose")
                        xalign 0.5
                        text_color "#fda4af"
                        text_size 25
                elif nz_pending_advance and house and nz_item_index == len(house["items"]) - 1 and nz_house_index == len(nz_route_houses) - 1:
                    textbutton "คัดแยกครบทั้ง 5 บ้าน — ดูผลภารกิจ":
                        action [Function(nz_continue_feedback), Return("win")]
                        xalign 0.5
                        text_color "#86efac"
                        text_size 25
                elif nz_pending_advance and house and nz_item_index == len(house["items"]) - 1:
                    textbutton "บ้านนี้เสร็จแล้ว — กลับสู่แผนที่":
                        action [Function(nz_continue_feedback), Return("house_complete")]
                        xalign 0.5
                        text_color "#67e8f9"
                        text_size 25
                elif nz_pending_advance:
                    textbutton "เข้าใจแล้ว — ชิ้นถัดไป":
                        action Function(nz_continue_feedback)
                        xalign 0.5
                        text_color "#67e8f9"
                        text_size 25
                else:
                    textbutton "เข้าใจแล้ว — ลองชิ้นเดิมอีกครั้ง":
                        action Function(nz_continue_feedback)
                        xalign 0.5
                        text_color "#fcd34d"
                        text_size 25


screen nz_house_failed_screen():
    modal True
    add "nz bg route"
    add Solid("#020617cc")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 940
        background "#061523f5"
        padding (52, 42)

        vbox:
            xalign 0.5
            spacing 22
            text "ภารกิจบ้านนี้ยังไม่สำเร็จ" size 36 color "#fca5a5" xalign 0.5 bold True
            text "คุณสามารถเริ่มต่อจากขยะชิ้นปัจจุบัน หรือเริ่มภารกิจใหม่เพื่อสุ่มลำดับทั้งหมดอีกครั้ง" size 22 color "#e2e8f0" xalign 0.5 text_align 0.5
            text "คัดแยกแล้ว [nz_sorted_count]/[nz_total_items] ชิ้น" size 22 color "#a5f3fc" xalign 0.5

            hbox:
                xalign 0.5
                spacing 34
                textbutton "ลองบ้านนี้อีกครั้ง":
                    action Return("retry_house")
                    text_color "#86efac"
                    text_size 24
                textbutton "เริ่มภารกิจใหม่":
                    action Return("restart")
                    text_color "#fcd34d"
                    text_size 24
                textbutton "ออกจากภารกิจ":
                    action Return("exit")
                    text_color "#cbd5e1"
                    text_size 24

# ---------------------------------------------------------------------------
# 8) หน้าสรุปผล SDG  (เทียบ SdgResultScreen — 3 แท็บ)
# ---------------------------------------------------------------------------

screen nz_result_screen():
    add "nz bg complete"
    add Solid("#02061799")
    use nz_hud
    $ reward_snapshot = mk_progress_snapshot()
    $ badge_count = len(reward_snapshot.get("badges", []))
    $ accuracy = nz_accuracy()

    vbox:
        xalign 0.5
        yalign 0.54
        xsize 1260
        spacing 16

        text "MISSION CLEARED — เป้าหมายสำเร็จ" size 46 color "#fbbf24" xalign 0.5 bold True
        text "SDG 11 — SUSTAINABLE CITIES & COMMUNITIES" size 23 color "#fbbf24" xalign 0.5 bold True

        hbox:
            xalign 0.5
            spacing 24
            textbutton "SDG 11"          action SetVariable("nz_res_tab", "sdg11")      text_color ("#fbbf24" if nz_res_tab == "sdg11" else "#64748b") text_size 24 text_bold True
            textbutton "โครงการไม่เทรวม" action SetVariable("nz_res_tab", "maitayruam") text_color ("#34d399" if nz_res_tab == "maitayruam" else "#64748b") text_size 24 text_bold True
            textbutton "ผลลัพธ์เมือง"     action SetVariable("nz_res_tab", "before")     text_color ("#818cf8" if nz_res_tab == "before" else "#64748b") text_size 24 text_bold True

        frame:
            xsize 1260
            ysize 360
            background "#0b1220"
            padding (34, 26)

            if nz_res_tab == "sdg11":
                vbox:
                    spacing 10
                    text "SDG 11: เมืองและชุมชนที่ยั่งยืน" size 30 color "#fbbf24" bold True
                    text "ทำให้เมืองปลอดภัย ยืดหยุ่น และเป็นกลางทางคาร์บอน" size 24 color "#cbd5e1"
                    null height 6
                    if nz_reward_eco > 0 or nz_reward_coins > 0:
                        text "รางวัลด่าน: Eco Score +[nz_reward_eco] • Meow Coin +[nz_reward_coins] • SDG 11 Badge" size 26 color "#34d399" bold True
                    else:
                        text "รางวัลด่านนี้รับแล้ว: Eco Score +{:,} • Meow Coin +{:,} • SDG 11 Badge".format(MK_STAGE_REWARD_ECO_SCORE, MK_STAGE_REWARD_COINS) size 26 color "#94a3b8" bold True
                    text "คัดครบ [nz_sorted_count]/[nz_total_items] ชิ้น • แม่นยำ [accuracy]% • ผิด/หมดเวลา [nz_wrong_count] ครั้ง • เหลือชีวิต [nz_lives]" size 23 color "#e2e8f0"
                    text "คะแนนภารกิจ: Eco {:,} • รวมสะสม: Eco Score {:,} • Meow Coin {:,} • Badge {}/17".format(nz_eco_score, reward_snapshot.get("eco_score", 0), reward_snapshot.get("coins", 0), badge_count) size 22 color "#bae6fd"

            elif nz_res_tab == "maitayruam":

                vbox:
                    spacing 12
                    text "แคมเปญ 'ไม่เทรวม' (MAI TAY RUAM)" size 30 color "#34d399" bold True
                    text "แปลว่า 'อย่าทิ้งรวมกัน' — แม้ประชาชนแยกขยะ แต่ถ้ารถเก็บเทรวมถังเดียว ของเปียกจะทำให้รีไซเคิลเสียหาย" size 24 color "#cbd5e1"
                    text "BMA ปรับรถเก็บขยะให้มีช่องแยก เพื่อหมักปุ๋ยและรีไซเคิลแบบหมุนเวียนได้จริง" size 24 color "#cbd5e1"

            else:
                vbox:
                    spacing 12
                    text "กรุงเทพฯ ก่อนและหลังการเปลี่ยนแปลง" size 30 color "#818cf8" bold True
                    text "BEFORE: ถนนพระราม 4 มีขยะเปียกปนถังรวม วัสดุรีไซเคิลเสียคุณภาพ และเกิดภาระการกำจัด" size 24 color "#fca5a5"
                    text "AFTER: ชุมชนคัดแยกตั้งแต่ต้นทาง รถเก็บขนทำงานเป็นระบบ และวัสดุหมุนเวียนกลับมาใช้ประโยชน์" size 24 color "#86efac"

        hbox:
            xalign 0.5
            spacing 42
            textbutton "เล่นใหม่" action Return("replay") text_color "#34d399" text_size 25 text_bold True
            textbutton "สถานที่จริงและนโยบายภาครัฐ" action Return("vdo") text_color "#67e8f9" text_size 27 text_bold True
            textbutton "กลับ" action Return("done") text_color "#cbd5e1" text_size 25 text_bold True



# ---------------------------------------------------------------------------
# 9) Local Mission Video — เล่นไฟล์ OGV ภายใน Ren'Py
# ---------------------------------------------------------------------------
screen nz_video_ready_screen():
    modal True
    zorder 2000

    add "nz bg video"
    add Solid("#02061799")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 940
        background "#020817ee"
        padding (55, 45)

        vbox:
            xalign 0.5
            spacing 22

            text "วิดีโอภารกิจถนนพระราม 4":
                size 34
                color "#67e8f9"
                xalign 0.5
                bold True
                outlines [(2, "#000000", 0, 0)]

            text "วิดีโอจะเล่นแบบเต็มหน้าจอภายในเกม":
                size 22
                color "#ffffff"
                xalign 0.5

            text "ระหว่างรับชม สามารถคลิก/แตะ หรือกด Space หรือ Enter เพื่อข้ามวิดีโอได้":
                size 18
                color "#fcd34d"
                xalign 0.5
                text_align 0.5

            null height 8

            hbox:
                xalign 0.5
                spacing 45
                textbutton "เริ่มชมวิดีโอ":
                    action Return("play")
                    text_color "#67e8f9"
                    text_size 23
                textbutton "← กลับผลภารกิจ":
                    action Return("back")
                    text_color "#cbd5e1"
                    text_size 21

    key "game_menu" action Return("back")


screen nz_video_complete_screen():
    modal True
    zorder 2000

    add "nz bg video"
    add Solid("#020617aa")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 940
        background "#020817ee"
        padding (55, 45)

        vbox:
            xalign 0.5
            spacing 24

            text "พร้อมเดินทางสู่ NEXTOPIA":
                size 36
                color "#86efac"
                xalign 0.5
                bold True
                outlines [(2, "#000000", 0, 0)]

            text "วิดีโอสิ้นสุดหรือถูกข้ามแล้ว เลือกไปยังด่านถัดไปได้ทันที":
                size 20
                color "#e2e8f0"
                xalign 0.5
                text_align 0.5

            hbox:
                xalign 0.5
                spacing 45
                textbutton "ไปด่าน NEXTOPIA":
                    action Jump("nextopia_start")
                    text_color "#34d399"
                    text_size 25
                textbutton "← กลับผลภารกิจ":
                    action Return("back")
                    text_color "#cbd5e1"
                    text_size 21

    key "game_menu" action Return("back")


# ---------------------------------------------------------------------------
# 10) STORY + FLOW หลัก
#     command -> 1-6 -> Sustainability Decision -> tutorial -> houses
#     -> 7-10 -> result -> learning video
# ---------------------------------------------------------------------------

label rama4_pre_minigame_story:
    scene rama4_story_01
    CATLOARD "วันนี้...คุณคือคนขับรถเก็บขยะของเมืองนี้"

    scene rama4_story_02
    CATLOARD "คุณต้องจัดการขยะจาก 5 บ้าน"

    scene rama4_story_03
    CATLOARD "แยกขยะให้ถูกประเภท"

    scene rama4_story_04
    CATLOARD "ลองทำดู"

    scene rama4_story_05
    CATLOARD "ไม่แยกขยะ = ใช้แรงและเวลามาก"

    scene rama4_story_06
    CATLOARD "แยกขยะ = ทำงานง่ายขึ้น"

    return


label rama4_post_minigame_story:
    scene rama4_story_07
    CATLOARD "ภารกิจนี้สอดคล้องกับ SDG 11 Sustainable Cities and Communities"

    scene rama4_story_08
    pause

    scene rama4_story_09
    CATLOARD """เยี่ยมมาก! ตอนนี้นายรู้แล้วว่า... ขยะไม่ควรถูก “เทรวม”
แต่รู้ไหม... การแยกขยะเป็นเพียงจุดเริ่มต้นเท่านั้น
จากนี้... ผู้เชี่ยวชาญอีกคน จะพานายไปดู โลกหลังการรีไซเคิล"""

    scene rama4_story_10
    pause

    return


label nz_mission:
    $ nz_reset()

    # ระบบร่วมกำหนด HP เริ่มต้น: 25,000 / 30,000 / 35,000 ตามการตัดสินใจ
    call sustainability_decision("rama4")

    # โหลด PNG ทั้งหมด 25 ชิ้นและสุ่ม pattern เพียงครั้งเดียวสำหรับรอบนี้
    $ nz_start_route()

    # คู่มือคัดแยกขยะ
    call screen rama4_minigame_tutorial

label nz_route_hub_loop:
    call screen nz_route_screen

    if _return == "win":
        jump nz_mission_complete
    if _return != "start_house":
        return

label nz_house_play:
    call screen nz_sorting_screen

    if _return == "house_complete":
        # จบบ้านหนึ่งหลังแล้วกลับ hub เสมอ บ้านถัดไปจึงจะปลดล็อก
        jump nz_route_hub_loop
    if _return == "win":
        jump nz_mission_complete
    if _return == "lose":
        call screen nz_house_failed_screen
        if _return == "retry_house":
            $ nz_retry_current_house()
            jump nz_house_play
        if _return == "restart":
            jump nz_mission
        return

    jump nz_route_hub_loop

label nz_mission_complete:
    # ชนะ -> รับรางวัล -> ภาพบทสรุป 7-10 -> หน้าสรุปผล SDG เดิม
    $ nz_monster_hp = 0
    $ nz_sync_shared_hp(0)
    $ nz_apply_rewards()
    call rama4_post_minigame_story

label nz_result_loop:
    call screen nz_result_screen

    if _return == "replay":
        jump nz_mission
    if _return == "vdo":
        call stage_learning_flow("rama4", "nextopia_start")
        if _return == "nextopia_start":
            jump nextopia_start
        jump nz_result_loop

    return
