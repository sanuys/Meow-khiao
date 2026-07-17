# =============================================================================
# sustainability_core.rpy — ระบบกลางของเกม (ใช้ร่วมทุกด่าน)
# =============================================================================
# รวมระบบ: Sustainability Decision, Carbon Monster HP, Meow Coin, Eco Score,
# SDG Badge, Inventory และ claim ledger กันการรับรางวัลซ้ำต่อด่าน
#
# จุดเรียกใช้จากด่านต่างๆ:
#     call sustainability_decision("rama4")
# รองรับ stage id: "rama4", "nextopia", "lumpini" (ชื่อเรียกอื่นแปลงผ่าน mk_stage_key())
# การตัดสินใจถูกบันทึกครั้งเดียวต่อด่าน เรียกซ้ำจะแสดงเฉพาะสรุปผลเดิม ไม่หักภาษีซ้ำ
#
# ภาพพื้นหลังหน้าตัดสินใจ: images/sustainability/decision_<stage>_bg.png

define MK_CARBON_BASE_HP = 30000
define MK_SUSTAINABILITY_HP_DELTA = 5000
define MK_CARBON_TAX = 250
define MK_STAGE_REWARD_COINS = 200
define MK_STAGE_REWARD_ECO_SCORE = 150
define MK_REWARD_SCHEMA_VERSION = 1

image mk sustainability rama4 = "images/sustainability/decision_rama4_bg.png"
image mk sustainability nextopia = "images/sustainability/decision_nextopia_bg.png"
image mk sustainability lumpini = "images/sustainability/decision_lumpini_bg.png"


# Save-migration friendly shared state.  Ren'Py adds missing defaults when an
# older save is loaded, while _mk_ensure_state() also repairs unexpected types.
default mk_meow_coins = 1250
default mk_eco_score = 0
default mk_reward_schema_version = 0
default mk_stage_decisions = {}
default mk_decision_history = []
default mk_stage_start_hp = {}
default mk_stage_current_hp = {}
default mk_stage_steps = {}
default mk_stage_completion = {}
default mk_stage_rewards_claimed = []
default mk_inventory = []
default mk_sdg_badges = []


init -20 python:
    MK_STAGE_ALIASES = {
        "rama": "rama4",
        "rama4": "rama4",
        "rama_4": "rama4",
        "rama_4_road": "rama4",
        "rama4road": "rama4",
        "next": "nextopia",
        "nextopia": "nextopia",
        "lumpini": "lumpini",
        "lumpini_wellness": "lumpini",
        "lumpini_wellness_quest": "lumpini",
        "wellness": "lumpini",
    }

    # Product language intentionally describes real product categories rather
    # than claiming a lifecycle result for any particular brand.  The fixed HP
    # changes are an educational game rule, not a product carbon audit.
    MK_SUSTAINABILITY_STAGES = {
        "rama4": {
            "title": "RAMA 4 ROAD",
            "sdg": "SDG 11 เมืองและชุมชนที่ยั่งยืน",
            "question": "ก่อนเริ่มภารกิจแยกขยะ คุณจะเลือกภาชนะดื่มแบบใด",
            "context": "พิจารณารูปแบบการใช้งานและปริมาณบรรจุภัณฑ์ที่เกิดขึ้น",
            "background": "images/sustainability/decision_rama4_bg.png",
            "accent": "#22d3ee",
            "soft_accent": "#a5f3fc",
            "badge": "SDG 11",
            "badge_name": "เมืองและชุมชนที่ยั่งยืน",
            "inventory_id": "sdg11_badge",
            "choices": (
                {
                    "id": "refillable_steel_bottle",
                    "short": "ทางเลือก ก",
                    "title": "ขวดน้ำสแตนเลสแบบเติมซ้ำ",
                    "feature": "ออกแบบให้พก เติมน้ำ และใช้ซ้ำได้หลายครั้ง",
                    "consider": "ต้องล้างและใช้ต่อเนื่องเพื่อให้คุ้มกับการผลิต",
                    "eco": True,
                    "result_title": "เลือกแนวทางใช้ซ้ำ",
                    "result_detail": "การใช้ภาชนะเดิมซ้ำช่วยหลีกเลี่ยงบรรจุภัณฑ์ใช้ครั้งเดียวในแต่ละวัน",
                },
                {
                    "id": "single_use_pet_bottle",
                    "short": "ทางเลือก ข",
                    "title": "ขวดน้ำ PET แบบใช้ครั้งเดียว",
                    "feature": "ซื้อพร้อมดื่มและมีบรรจุภัณฑ์ใหม่ทุกครั้ง",
                    "consider": "หลังใช้ควรแยกขวดสะอาดเข้าสู่ระบบรีไซเคิล",
                    "eco": False,
                    "result_title": "เลือกบรรจุภัณฑ์ใช้ครั้งเดียว",
                    "result_detail": "เกมจำลองภาระจากการผลิตและจัดการบรรจุภัณฑ์ใหม่ด้วย Carbon Tax",
                },
            ),
        },
        "nextopia": {
            "title": "NEXTOPIA",
            "sdg": "SDG 4 การศึกษาที่มีคุณภาพ",
            "question": "สำหรับการเรียนรู้และสร้างนวัตกรรม คุณจะเลือกอุปกรณ์แบบใด",
            "context": "พิจารณาอายุการใช้งาน การซ่อม และการใช้ทรัพยากรอิเล็กทรอนิกส์",
            "background": "images/sustainability/decision_nextopia_bg.png",
            "accent": "#f59e0b",
            "soft_accent": "#fde68a",
            "badge": "SDG 4",
            "badge_name": "การศึกษาที่มีคุณภาพ",
            "inventory_id": "sdg4_badge",
            "choices": (
                {
                    "id": "repairable_refurbished_laptop",
                    "short": "ทางเลือก ก",
                    "title": "โน้ตบุ๊ก Refurbished ที่ซ่อมและอัปเกรดได้",
                    "feature": "นำเครื่องที่ผ่านการตรวจสภาพกลับมาใช้งานและยืดอายุอุปกรณ์",
                    "consider": "ตรวจการรับประกัน แบตเตอรี่ และความเหมาะสมกับงานก่อนซื้อ",
                    "eco": True,
                    "result_title": "เลือกยืดอายุอุปกรณ์",
                    "result_detail": "การซ่อม อัปเกรด และใช้เครื่องเดิมให้นานขึ้นช่วยชะลอการเกิดขยะอิเล็กทรอนิกส์",
                },
                {
                    "id": "frequent_full_device_replacement",
                    "short": "ทางเลือก ข",
                    "title": "เปลี่ยนโน้ตบุ๊กใหม่ทั้งเครื่องบ่อยครั้ง",
                    "feature": "เปลี่ยนเครื่องแม้เครื่องเดิมยังซ่อมหรือใช้งานต่อได้",
                    "consider": "อุปกรณ์เดิมต้องเข้าสู่ระบบรับคืนหรือจัดการขยะอิเล็กทรอนิกส์",
                    "eco": False,
                    "result_title": "เลือกเปลี่ยนอุปกรณ์บ่อย",
                    "result_detail": "เกมจำลองภาระทรัพยากรจากการเปลี่ยนอุปกรณ์ก่อนหมดอายุด้วย Carbon Tax",
                },
            ),
        },
        "lumpini": {
            "title": "LUMPINI WELLNESS QUEST",
            "sdg": "SDG 3 สุขภาพและความเป็นอยู่ที่ดี",
            "question": "สำหรับการเดินทางระยะใกล้ไปสวนสาธารณะ คุณจะเลือกแบบใด",
            "context": "พิจารณาทั้งการเคลื่อนไหวร่างกายและพลังงานที่ใช้ในการเดินทาง",
            "background": "images/sustainability/decision_lumpini_bg.png",
            "accent": "#86efac",
            "soft_accent": "#d1fae5",
            "badge": "SDG 3",
            "badge_name": "สุขภาพและความเป็นอยู่ที่ดี",
            "inventory_id": "sdg3_badge",
            "choices": (
                {
                    "id": "bicycle_short_trip",
                    "short": "ทางเลือก ก",
                    "title": "จักรยานสำหรับการเดินทางระยะใกล้",
                    "feature": "ใช้แรงกายในการเดินทางและนำไปใช้ซ้ำได้ในชีวิตประจำวัน",
                    "consider": "เลือกเส้นทางปลอดภัย สวมอุปกรณ์ป้องกัน และดูแลจักรยาน",
                    "eco": True,
                    "result_title": "เลือกการเดินทางแบบ Active Mobility",
                    "result_detail": "การปั่นจักรยานในระยะที่เหมาะสมเชื่อมโยงการเคลื่อนไหวร่างกายกับเมืองคาร์บอนต่ำ",
                },
                {
                    "id": "fuel_car_short_trip",
                    "short": "ทางเลือก ข",
                    "title": "รถยนต์ใช้น้ำมันสำหรับการเดินทางระยะใกล้",
                    "feature": "ใช้เชื้อเพลิงเพื่อเดินทางคนเดียวในระยะที่สามารถเลือกวิธีอื่นได้",
                    "consider": "สภาพร่างกาย ความปลอดภัย และการเข้าถึงขนส่งสาธารณะอาจต่างกันในแต่ละคน",
                    "eco": False,
                    "result_title": "เลือกการเดินทางที่ใช้เชื้อเพลิง",
                    "result_detail": "เกมจำลองภาระการใช้เชื้อเพลิงในเที่ยวสั้นที่มีทางเลือกด้วย Carbon Tax",
                },
            ),
        },
    }


    def _mk_ensure_state():
        """Repair shared state after loading old or partially migrated saves."""
        s = renpy.store

        dict_defaults = (
            "mk_stage_decisions",
            "mk_stage_start_hp",
            "mk_stage_current_hp",
            "mk_stage_steps",
            "mk_stage_completion",
        )
        list_defaults = (
            "mk_decision_history",
            "mk_stage_rewards_claimed",
            "mk_inventory",
            "mk_sdg_badges",
        )

        for name in dict_defaults:
            if not isinstance(getattr(s, name, None), dict):
                setattr(s, name, {})
        for name in list_defaults:
            if not isinstance(getattr(s, name, None), list):
                setattr(s, name, [])

        # Older builds accepted stage aliases at API boundaries. Canonicalize
        # any legacy ledger entries before checking claims so an alias can
        # never reopen the same stage reward.
        normalized_claims = []
        for stage_id in s.mk_stage_rewards_claimed:
            key = mk_stage_key(stage_id)
            claim_id = key if key is not None else stage_id
            if claim_id not in normalized_claims:
                normalized_claims.append(claim_id)
        s.mk_stage_rewards_claimed = normalized_claims

        try:
            s.mk_meow_coins = int(getattr(s, "mk_meow_coins", 1250))
        except (TypeError, ValueError):
            s.mk_meow_coins = 1250

        try:
            s.mk_eco_score = max(0, int(getattr(s, "mk_eco_score", 0)))
        except (TypeError, ValueError):
            s.mk_eco_score = 0

        try:
            reward_schema_version = int(getattr(s, "mk_reward_schema_version", 0))
        except (TypeError, ValueError):
            reward_schema_version = 0

        # Saves created before Eco Score became a shared stage reward already
        # contain the canonical claimed-stage ledger. Backfill exactly one
        # 150-point Eco reward for each valid claimed stage, without changing
        # the historical Meow Coin balance or reopening any reward claim.
        if reward_schema_version < MK_REWARD_SCHEMA_VERSION:
            legacy_claimed = set()
            for stage_id in s.mk_stage_rewards_claimed:
                key = mk_stage_key(stage_id)
                if key is not None:
                    legacy_claimed.add(key)
            s.mk_eco_score += len(legacy_claimed) * int(MK_STAGE_REWARD_ECO_SCORE)
            s.mk_reward_schema_version = MK_REWARD_SCHEMA_VERSION

        # Keep Achievement, Inventory, and completion data coherent when an
        # older or partially migrated save has a claim ledger but is missing
        # one of the derived records.
        completion = dict(s.mk_stage_completion)
        badges = list(s.mk_sdg_badges)
        inventory = list(s.mk_inventory)
        for stage_id in s.mk_stage_rewards_claimed:
            key = mk_stage_key(stage_id)
            config = MK_SUSTAINABILITY_STAGES.get(key) if key else None
            if config is None:
                continue
            completion[key] = True
            if config["badge"] not in badges:
                badges.append(config["badge"])
            if not any(isinstance(item, dict) and item.get("id") == config["inventory_id"] for item in inventory):
                inventory.append({
                    "id": config["inventory_id"],
                    "type": "sdg_badge",
                    "stage_id": key,
                    "badge": config["badge"],
                    "name": config["badge_name"],
                })
        s.mk_stage_completion = completion
        s.mk_sdg_badges = badges
        s.mk_inventory = inventory


    def mk_stage_key(stage_id):
        if stage_id is None:
            return None
        key = str(stage_id).strip().lower().replace("-", "_").replace(" ", "_")
        return MK_STAGE_ALIASES.get(key)


    def mk_stage_config(stage_id):
        key = mk_stage_key(stage_id)
        if key is None:
            return None
        return MK_SUSTAINABILITY_STAGES.get(key)


    def mk_stage_choices(stage_id):
        config = mk_stage_config(stage_id)
        return config["choices"] if config else ()


    def mk_get_stage_decision(stage_id):
        _mk_ensure_state()
        key = mk_stage_key(stage_id)
        if key is None:
            return None
        return renpy.store.mk_stage_decisions.get(key)


    def mk_has_stage_decision(stage_id):
        return mk_get_stage_decision(stage_id) is not None


    def mk_get_stage_start_hp(stage_id):
        _mk_ensure_state()
        s = renpy.store
        key = mk_stage_key(stage_id)
        if key is None:
            return int(MK_CARBON_BASE_HP)
        record = s.mk_stage_decisions.get(key)
        if record:
            return int(record.get("start_hp", MK_CARBON_BASE_HP))
        return int(s.mk_stage_start_hp.get(key, MK_CARBON_BASE_HP))


    def mk_get_stage_current_hp(stage_id):
        _mk_ensure_state()
        s = renpy.store
        key = mk_stage_key(stage_id)
        if key is None:
            return int(MK_CARBON_BASE_HP)
        return int(s.mk_stage_current_hp.get(key, mk_get_stage_start_hp(key)))


    def mk_get_stage_hp_fraction(stage_id):
        start_hp = max(1, mk_get_stage_start_hp(stage_id))
        return max(0.0, min(1.0, mk_get_stage_current_hp(stage_id) / float(start_hp)))


    def mk_set_stage_current_hp(stage_id, hp):
        _mk_ensure_state()
        s = renpy.store
        key = mk_stage_key(stage_id)
        if key is None:
            return int(MK_CARBON_BASE_HP)
        start_hp = mk_get_stage_start_hp(key)
        value = max(0, min(start_hp, int(round(hp))))
        hp_map = dict(s.mk_stage_current_hp)
        hp_map[key] = value
        s.mk_stage_current_hp = hp_map
        return value


    def mk_damage_carbon_monster(stage_id, damage):
        current = mk_get_stage_current_hp(stage_id)
        return mk_set_stage_current_hp(stage_id, current - max(0, int(round(damage))))


    def mk_reset_stage_battle(stage_id, clear_steps=False):
        """Reset battle HP to the post-decision value without repeating tax."""
        _mk_ensure_state()
        s = renpy.store
        key = mk_stage_key(stage_id)
        if key is None:
            return int(MK_CARBON_BASE_HP)
        if clear_steps:
            step_map = dict(s.mk_stage_steps)
            step_map[key] = []
            s.mk_stage_steps = step_map
        return mk_set_stage_current_hp(key, mk_get_stage_start_hp(key))


    def mk_apply_sustainability_decision(stage_id, choice_id):
        """Apply one ethical-product decision exactly once for a stage."""
        _mk_ensure_state()
        s = renpy.store
        key = mk_stage_key(stage_id)
        config = mk_stage_config(key)
        if key is None or config is None:
            return None

        existing = s.mk_stage_decisions.get(key)
        if existing is not None:
            return existing

        choice = next((item for item in config["choices"] if item["id"] == choice_id), None)
        if choice is None:
            return None

        eco_choice = bool(choice["eco"])
        hp_delta = -int(MK_SUSTAINABILITY_HP_DELTA) if eco_choice else int(MK_SUSTAINABILITY_HP_DELTA)
        tax = 0 if eco_choice else int(MK_CARBON_TAX)
        start_hp = int(MK_CARBON_BASE_HP) + hp_delta
        coins_before = int(s.mk_meow_coins)
        s.mk_meow_coins = coins_before - tax

        record = {
            "stage_id": key,
            "choice_id": choice["id"],
            "choice_title": choice["title"],
            "eco": eco_choice,
            "hp_delta": hp_delta,
            "start_hp": start_hp,
            "tax": tax,
            "coins_before": coins_before,
            "coins_after": int(s.mk_meow_coins),
            "result_title": choice["result_title"],
            "result_detail": choice["result_detail"],
        }

        decisions = dict(s.mk_stage_decisions)
        decisions[key] = record
        s.mk_stage_decisions = decisions

        history = list(s.mk_decision_history)
        history.append(dict(record))
        s.mk_decision_history = history

        start_map = dict(s.mk_stage_start_hp)
        start_map[key] = start_hp
        s.mk_stage_start_hp = start_map

        current_map = dict(s.mk_stage_current_hp)
        current_map[key] = start_hp
        s.mk_stage_current_hp = current_map

        # Keep the pre-existing RAMA wallet HUD consistent when it is present.
        if hasattr(s, "nz_budget"):
            s.nz_budget = int(s.mk_meow_coins)

        return record


    def mk_complete_stage_step(stage_id, step_id, total_steps=5):
        """Record an idempotent minigame/house clear and recompute HP.

        NEXTOPIA can call this once after each of its five hidden-object games;
        RAMA can use the same helper for five houses.  Every unique clear removes
        exactly 1 / total_steps of the post-decision starting HP.
        """
        _mk_ensure_state()
        s = renpy.store
        key = mk_stage_key(stage_id)
        if key is None:
            return None

        total = max(1, int(total_steps))
        step_key = str(step_id)
        cleared = list(s.mk_stage_steps.get(key, []))
        is_new = step_key not in cleared
        previous_hp = mk_get_stage_current_hp(key)

        if is_new:
            cleared.append(step_key)
            step_map = dict(s.mk_stage_steps)
            step_map[key] = cleared
            s.mk_stage_steps = step_map

        completed = min(total, len(cleared))
        start_hp = mk_get_stage_start_hp(key)
        remaining = int(round(start_hp * ((total - completed) / float(total))))
        current_hp = mk_set_stage_current_hp(key, remaining)

        return {
            "stage_id": key,
            "step_id": step_key,
            "is_new": is_new,
            "completed_steps": completed,
            "total_steps": total,
            "damage": max(0, previous_hp - current_hp) if is_new else 0,
            "current_hp": current_hp,
            "start_hp": start_hp,
        }


    def mk_get_completed_steps(stage_id):
        _mk_ensure_state()
        key = mk_stage_key(stage_id)
        if key is None:
            return []
        return list(renpy.store.mk_stage_steps.get(key, []))


    def mk_award_stage_rewards(stage_id):
        """Award the stage badge, 200 coins, and 150 Eco Score exactly once."""
        _mk_ensure_state()
        s = renpy.store
        key = mk_stage_key(stage_id)
        config = mk_stage_config(key)
        if key is None or config is None:
            return None

        already_claimed = key in s.mk_stage_rewards_claimed
        if not already_claimed:
            s.mk_meow_coins = int(s.mk_meow_coins) + int(MK_STAGE_REWARD_COINS)
            s.mk_eco_score = int(s.mk_eco_score) + int(MK_STAGE_REWARD_ECO_SCORE)

            claimed = list(s.mk_stage_rewards_claimed)
            claimed.append(key)
            s.mk_stage_rewards_claimed = claimed

            badges = list(s.mk_sdg_badges)
            if config["badge"] not in badges:
                badges.append(config["badge"])
            s.mk_sdg_badges = badges

            inventory = list(s.mk_inventory)
            if not any(isinstance(item, dict) and item.get("id") == config["inventory_id"] for item in inventory):
                inventory.append({
                    "id": config["inventory_id"],
                    "type": "sdg_badge",
                    "stage_id": key,
                    "badge": config["badge"],
                    "name": config["badge_name"],
                })
            s.mk_inventory = inventory

        completion = dict(s.mk_stage_completion)
        completion[key] = True
        s.mk_stage_completion = completion

        if hasattr(s, "nz_budget"):
            s.nz_budget = int(s.mk_meow_coins)
        if hasattr(s, "nz_badges") and config["badge"] not in s.nz_badges:
            s.nz_badges.append(config["badge"])

        return {
            "stage_id": key,
            "new_reward": not already_claimed,
            "coins_awarded": int(MK_STAGE_REWARD_COINS) if not already_claimed else 0,
            "eco_score_awarded": int(MK_STAGE_REWARD_ECO_SCORE) if not already_claimed else 0,
            "badge": config["badge"],
            "badge_name": config["badge_name"],
            "coin_balance": int(s.mk_meow_coins),
            "eco_score_balance": int(s.mk_eco_score),
        }


    def mk_complete_stage(stage_id):
        return mk_award_stage_rewards(stage_id)


    def mk_grant_stage_rewards(stage_id):
        """Compatibility alias used by stage files; remains idempotent."""
        return mk_award_stage_rewards(stage_id)


    def mk_has_completed_stage(stage_id):
        _mk_ensure_state()
        key = mk_stage_key(stage_id)
        return bool(key and renpy.store.mk_stage_completion.get(key, False))


    def mk_has_stage_reward(stage_id):
        _mk_ensure_state()
        key = mk_stage_key(stage_id)
        return bool(key and key in renpy.store.mk_stage_rewards_claimed)


    def mk_progress_snapshot():
        """Small stable API for lobby/database screens."""
        _mk_ensure_state()
        s = renpy.store
        return {
            "coins": int(s.mk_meow_coins),
            "eco_score": int(s.mk_eco_score),
            "badges": list(s.mk_sdg_badges),
            "inventory": list(s.mk_inventory),
            "completed_stages": [key for key, complete in s.mk_stage_completion.items() if complete],
            "decisions": dict(s.mk_stage_decisions),
            "stage_hp": dict(s.mk_stage_current_hp),
        }


transform mk_decision_button_pulse:
    alpha 0.92
    linear 0.75 alpha 1.0
    linear 0.75 alpha 0.92
    repeat


screen mk_sustainability_header(stage):
    frame:
        xpos 54
        ypos 34
        xsize 1812
        ysize 142
        background Solid("#020817e8")
        padding (34, 20)

        hbox:
            xfill True
            yalign 0.5

            vbox:
                xsize 1320
                spacing 3
                text "SUSTAINABILITY DECISION":
                    size 48
                    color stage["soft_accent"]
                    bold True
                text stage["title"] + "  |  " + stage["sdg"]:
                    size 27
                    color "#e2e8f0"

            frame:
                xsize 370
                ysize 84
                yalign 0.5
                background Solid("#071827f2")
                padding (20, 10)

                vbox:
                    xalign 0.5
                    text "MEOW COIN":
                        xalign 0.5
                        size 20
                        color "#94a3b8"
                    text "{:,}".format(mk_meow_coins):
                        xalign 0.5
                        size 35
                        color "#fbbf24"
                        bold True


screen mk_sustainability_decision_screen(stage_id):
    modal True

    $ stage_key = mk_stage_key(stage_id)
    $ stage = mk_stage_config(stage_key)
    $ choices = stage["choices"]

    add stage["background"] xysize (1920, 1080)
    add Solid("#02061738")

    use mk_sustainability_header(stage)

    frame:
        xalign 0.5
        ypos 190
        xsize 1180
        ysize 132
        background Solid("#031522ed")
        padding (34, 16)

        vbox:
            xalign 0.5
            spacing 5
            text stage["question"]:
                xalign 0.5
                text_align 0.5
                size 36
                color "#ffffff"
                bold True
            text stage["context"]:
                xalign 0.5
                text_align 0.5
                size 24
                color "#cbd5e1"

    frame:
        xalign 0.5
        ypos 334
        xsize 520
        ysize 104
        background Solid("#020817ef")
        padding (20, 12)

        vbox:
            xalign 0.5
            spacing 7
            text "CARBON MONSTER HP ตั้งต้น 30,000":
                xalign 0.5
                size 23
                color "#f8fafc"
                bold True
            bar:
                value StaticValue(MK_CARBON_BASE_HP, MK_CARBON_BASE_HP + MK_SUSTAINABILITY_HP_DELTA)
                xsize 450
                ysize 22
                xalign 0.5
                left_bar Solid("#ef4444")
                right_bar Solid("#172033")

    for choice_index, choice in enumerate(choices):
        $ card_x = 70 if choice_index == 0 else 1030
        button:
            xpos card_x
            ypos 458
            xsize 820
            ysize 472
            background Solid("#031522ed")
            hover_background Solid("#0a2a36f5")
            insensitive_background Solid("#07111ce8")
            padding (46, 28)
            action Return(choice["id"])

            vbox:
                xalign 0.5
                yalign 0.5
                spacing 18

                text choice["short"]:
                    xalign 0.5
                    size 24
                    color stage["accent"]
                    bold True
                text choice["title"]:
                    xalign 0.5
                    text_align 0.5
                    xmaximum 710
                    size 38
                    color "#ffffff"
                    bold True
                null height 6
                text "รูปแบบการใช้งาน":
                    xalign 0.5
                    size 22
                    color stage["soft_accent"]
                    bold True
                text choice["feature"]:
                    xalign 0.5
                    text_align 0.5
                    xmaximum 690
                    size 25
                    color "#e2e8f0"
                text "สิ่งที่ควรพิจารณา":
                    xalign 0.5
                    size 22
                    color "#94a3b8"
                    bold True
                text choice["consider"]:
                    xalign 0.5
                    text_align 0.5
                    xmaximum 690
                    size 22
                    color "#cbd5e1"
                null height 5
                frame:
                    xalign 0.5
                    xsize 360
                    ysize 58
                    background Solid(stage["accent"])
                    text "เลือกสินค้านี้":
                        xalign 0.5
                        yalign 0.5
                        size 28
                        color "#020617"
                        bold True

    frame:
        xalign 0.5
        ypos 952
        xsize 1660
        ysize 86
        background Solid("#020817e8")
        padding (30, 12)

        text "ผลลัพธ์ในเกมเป็นแบบจำลองเพื่อการเรียนรู้ ไม่ใช่ผลการประเมินวัฏจักรชีวิตของแบรนด์ใดแบรนด์หนึ่ง":
            xalign 0.5
            yalign 0.5
            text_align 0.5
            size 22
            color "#cbd5e1"


screen mk_sustainability_result_screen(stage_id, record, recap=False):
    modal True

    $ stage_key = mk_stage_key(stage_id)
    $ stage = mk_stage_config(stage_key)
    $ result_color = "#86efac" if record["eco"] else "#fb7185"
    $ delta_text = "ลดลง 5,000" if record["eco"] else "เพิ่มขึ้น 5,000"

    add stage["background"] xysize (1920, 1080)
    add Solid("#0206178a")

    use mk_sustainability_header(stage)

    frame:
        xalign 0.5
        ypos 210
        xsize 1320
        ysize 680
        background Solid("#03111cf5")
        padding (68, 42)

        vbox:
            xalign 0.5
            spacing 20

            text ("ทบทวนการตัดสินใจ" if recap else "บันทึกการตัดสินใจแล้ว"):
                xalign 0.5
                size 35
                color stage["soft_accent"]
                bold True
            text record["choice_title"]:
                xalign 0.5
                text_align 0.5
                xmaximum 1120
                size 46
                color "#ffffff"
                bold True
            text record["result_title"]:
                xalign 0.5
                size 30
                color result_color
                bold True
            text record["result_detail"]:
                xalign 0.5
                text_align 0.5
                xmaximum 1100
                size 27
                color "#dbeafe"

            null height 4

            frame:
                xalign 0.5
                xsize 990
                ysize 182
                background Solid("#071827ef")
                padding (34, 20)

                vbox:
                    xalign 0.5
                    spacing 11
                    text "ผลต่อ Carbon Monster":
                        xalign 0.5
                        size 24
                        color "#94a3b8"
                    text "HP {}  |  HP เริ่มมินิเกม {:,}".format(delta_text, record["start_hp"]):
                        xalign 0.5
                        size 34
                        color result_color
                        bold True
                    bar:
                        value StaticValue(record["start_hp"], MK_CARBON_BASE_HP + MK_SUSTAINABILITY_HP_DELTA)
                        xsize 850
                        ysize 25
                        xalign 0.5
                        left_bar Solid(result_color)
                        right_bar Solid("#172033")

            if record["tax"] > 0:
                text "CARBON TAX 250 MEOW COIN  |  ยอดคงเหลือ {:,}".format(mk_meow_coins):
                    xalign 0.5
                    size 28
                    color "#fbbf24"
                    bold True
            else:
                text "ไม่มี Carbon Tax  |  Meow Coin {:,}".format(mk_meow_coins):
                    xalign 0.5
                    size 28
                    color "#fbbf24"
                    bold True

            if recap:
                text "การตัดสินใจนี้ถูกบันทึกไว้แล้ว ระบบจึงไม่ปรับ HP หรือหักเหรียญซ้ำ":
                    xalign 0.5
                    text_align 0.5
                    size 23
                    color "#cbd5e1"

    textbutton "เข้าสู่ภารกิจต่อ":
        xalign 0.5
        ypos 916
        xsize 430
        ysize 86
        background Solid(stage["accent"])
        hover_background Solid(stage["soft_accent"])
        text_color "#020617"
        text_hover_color "#020617"
        text_size 31
        text_bold True
        action Return(record)
        at mk_decision_button_pulse


label sustainability_decision(stage_id="rama4"):
    $ _mk_stage = mk_stage_key(stage_id)
    $ _mk_config = mk_stage_config(_mk_stage)

    if _mk_config is None:
        $ renpy.notify("ไม่พบข้อมูล Sustainability Decision สำหรับด่านนี้")
        return None

    $ _mk_existing = mk_get_stage_decision(_mk_stage)

    if _mk_existing is not None:
        call screen mk_sustainability_result_screen(_mk_stage, _mk_existing, True)
        return _mk_existing

    call screen mk_sustainability_decision_screen(_mk_stage)
    $ _mk_choice_id = _return
    $ _mk_result = mk_apply_sustainability_decision(_mk_stage, _mk_choice_id)

    if _mk_result is None:
        $ renpy.notify("ไม่สามารถบันทึกตัวเลือกได้ กรุณาลองใหม่")
        return None

    call screen mk_sustainability_result_screen(_mk_stage, _mk_result, False)
    return _mk_result
