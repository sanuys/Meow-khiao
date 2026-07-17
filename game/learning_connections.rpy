# =============================================================================
# learning_connections.rpy — ระบบเชื่อมโยงการเรียนรู้หลังจบด่าน (ใช้ร่วมทุกด่าน)
# =============================================================================
# หลังจบแต่ละด่านจะมี 2 ส่วนแยกกันชัดเจน:
#   1) วิดีโอสถานที่จริงในกรุงเทพฯ ของด่านนั้น (เล่นด้วย renpy.movie_cutscene)
#   2) หน้าเชื่อมโยงหน่วยงาน/นโยบายภาครัฐตาม SDG ของด่าน (ลิงก์ภายนอกเปิดด้วย
#      OpenURL เฉพาะเมื่อผู้เล่นกดปุ่มเท่านั้น)
#
# ตำแหน่งวิดีโอ: videos/<ลำดับ-ชื่อด่าน>/ และวิดีโอนโยบาย สสส. ใน videos/0-COMMON/
# (ไฟล์ สสส. ใช้สำเนาชื่อ ASCII ของ "สืบสร้างสุข.ogv" เพื่อให้แพ็กลง ZIP ได้ทุกระบบไฟล์)

define LEARNING_RAMA4_MOVIE = "videos/1-RAMA_4_ROAD/RAMA_4_ROAD.ogv"
define LEARNING_NEXTOPIA_MOVIE = "videos/2-NEXTOPIA/NEXTOPIA.ogv"
define LEARNING_LUMPINI_MOVIE = "videos/3-LUMPINI_WELLNESS_QUEST/LUMPINI.ogv"
# No separate NEXTOPIA policy movie is currently packaged. The SDG 4 policy
# page uses its verified external CDTI/MHESI learning link instead.
define LEARNING_NEXTOPIA_POLICY_MOVIE = None
# Runtime uses an ASCII-safe copy of สืบสร้างสุข.ogv so packaged desktop ZIPs
# can include the movie reliably on every supported filesystem.
define LEARNING_THAIHEALTH_POLICY_MOVIE = "videos/0-COMMON/THAIHEALTH_SUEB_SANG_SOOK.ogv"

define LEARNING_BMA_URL = "https://greener.bangkok.go.th/waste-recycle/mai-te-ruam/"
define LEARNING_MHESI_CDTI_URL = "https://share.google/76Yy2UHG4awxoSPJd"
define LEARNING_THAIHEALTH_URL = "https://www.thaihealth.or.th/about-thaihealth"


init -5 python:
    def stage_learning_info(stage_id):
        """Return presentation data for a supported post-stage learning flow."""
        flows = {
            "rama4": {
                "stage_title": "RAMA 4 ROAD",
                "sdg_title": "SDG 11 เมืองและชุมชนที่ยั่งยืน",
                "local_movie": LEARNING_RAMA4_MOVIE,
                "local_title": "ถนนพระราม 4 และภารกิจแยกขยะของเมือง",
                "local_description": "ชมสถานที่จริงที่เป็นแรงบันดาลใจให้ภารกิจจัดการขยะของด่านนี้",
                "agency": "กรุงเทพมหานคร",
                "policy_title": "โครงการไม่เทรวม",
                "policy_description": "การแยกเศษอาหารออกจากขยะทั่วไปช่วยลดการปนเปื้อน เพิ่มโอกาสรีไซเคิล และลดภาระการจัดการขยะของเมือง จึงเชื่อมตรงกับเป้าหมายเมืองและชุมชนที่ยั่งยืนของ SDG 11",
                "policy_link_label": "เปิดเว็บไซต์โครงการไม่เทรวม",
                "policy_url": LEARNING_BMA_URL,
                "policy_video": None,
                "policy_video_title": None,
                "source_note": "เว็บไซต์ Greener Bangkok ของกรุงเทพมหานคร",
                "accent": "#22d3ee",
                "accent_hover": "#67e8f9",
                "secondary": "#4ade80",
                "bg": "#020b18",
                "panel": "#071827f2",
            },
            "nextopia": {
                "stage_title": "NEXTOPIA",
                "sdg_title": "SDG 4 การศึกษาที่มีคุณภาพ",
                "local_movie": LEARNING_NEXTOPIA_MOVIE,
                "local_title": "NEXTOPIA พื้นที่เรียนรู้และนวัตกรรม",
                "local_description": "ชมสถานที่จริงที่เป็นแรงบันดาลใจให้การเรียนรู้ผ่านภารกิจทั้งห้าของด่านนี้",
                "agency": "กระทรวงการอุดมศึกษา วิทยาศาสตร์ วิจัยและนวัตกรรม",
                "policy_title": "การศึกษาเชื่อมโยงนวัตกรรม",
                "policy_description": "การเปิดโอกาสให้ผู้เรียนทดลองเทคโนโลยีและแก้ปัญหาจริง ช่วยต่อยอด SDG 4 จากการเข้าถึงความรู้ไปสู่ทักษะที่ใช้สร้างนวัตกรรมได้ โดยเชื่อมโยงกับประสบการณ์ของสถาบันเทคโนโลยีจิตรลดา",
                "policy_link_label": "เปิดข้อมูล อว. และสถาบันเทคโนโลยีจิตรลดา",
                "policy_url": LEARNING_MHESI_CDTI_URL,
                "policy_video": LEARNING_NEXTOPIA_POLICY_MOVIE,
                "policy_video_title": "รับชมวิดีโอการเชื่อมโยงนโยบาย",
                "source_note": "เปิดแหล่งข้อมูลภายนอกเพื่อศึกษาการเชื่อมโยงการศึกษา นวัตกรรม อว. และสถาบันเทคโนโลยีจิตรลดา",
                "accent": "#fbbf24",
                "accent_hover": "#fde68a",
                "secondary": "#4ade80",
                "bg": "#07120f",
                "panel": "#102019f2",
            },
            "lumpini": {
                "stage_title": "LUMPINI WELLNESS QUEST",
                "sdg_title": "SDG 3 สุขภาพและความเป็นอยู่ที่ดี",
                "local_movie": LEARNING_LUMPINI_MOVIE,
                "local_title": "สวนลุมพินีและสุขภาวะของคนเมือง",
                "local_description": "ชมสถานที่จริงที่เป็นแรงบันดาลใจให้ภารกิจจังหวะการเคลื่อนไหวเพื่อสุขภาพ",
                "agency": "สำนักงานกองทุนสนับสนุนการสร้างเสริมสุขภาพ (สสส.)",
                "policy_title": "นิทรรศการสืบสร้างสุข (Health Detective)",
                "policy_description": "นิทรรศการชวนผู้เรียนค้นหาปัจจัยเสี่ยงจากพฤติกรรมและฝึกตัดสินใจดูแลสุขภาวะ จึงสอดคล้องกับ SDG 3 ซึ่งมุ่งส่งเสริมสุขภาพและความเป็นอยู่ที่ดีสำหรับทุกคน",
                "policy_link_label": "เปิดหน้าข้อมูลองค์กรของ สสส.",
                "policy_url": LEARNING_THAIHEALTH_URL,
                "policy_video": LEARNING_THAIHEALTH_POLICY_MOVIE,
                "policy_video_title": "รับชมวิดีโอนิทรรศการสืบสร้างสุข",
                "source_note": "รับชมวิดีโอนิทรรศการสืบสร้างสุขภายในเกม และศึกษาบทบาทของ สสส. เพิ่มเติมจากแหล่งข้อมูลภายนอก",
                "policy_link_notice": "เนื่องจากข้อมูลส่วนนิทรรศการสืบสร้างสุขได้ถูกนำออกไปจากเว็บไซต์ สสส. จึงเชื่อมไปหน้าข้อมูลองค์กรของ สสส. แทน",
                "completion_button_label": "เข้าสู่หน้า Lobby",
                "accent": "#4ade80",
                "accent_hover": "#86efac",
                "secondary": "#67e8f9",
                "bg": "#03120b",
                "panel": "#071c14f2",
            },
        }
        return flows.get(stage_id)


screen stage_learning_local_screen(info, movie_available, local_handled):
    tag stage_learning
    modal True

    add Solid(info["bg"])
    add Solid("#00000038")

    frame:
        xalign 0.5
        yalign 0.07
        xsize 1740
        ysize 120
        background Solid(info["panel"])
        padding (42, 18)

        hbox:
            xfill True
            yalign 0.5

            vbox:
                spacing 2
                text info["stage_title"]:
                    size 48
                    color info["accent"]
                    bold True
                text info["sdg_title"]:
                    size 30
                    color "#e2e8f0"

            text "ส่วนที่ 1 จาก 2  |  REAL PLACE":
                xalign 1.0
                yalign 0.5
                size 30
                color "#f8fafc"
                bold True

    frame:
        xalign 0.5
        yalign 0.57
        xsize 1540
        ysize 720
        background Solid(info["panel"])
        padding (70, 54)

        vbox:
            xfill True
            spacing 24

            text "สถานที่จริงเบื้องหลังภารกิจ":
                xalign 0.5
                size 56
                color "#ffffff"
                bold True

            text info["local_title"]:
                xalign 0.5
                text_align 0.5
                size 42
                color info["accent"]
                bold True

            frame:
                xalign 0.5
                xsize 1280
                ysize 210
                background Solid("#020617bb")
                padding (42, 34)

                vbox:
                    xalign 0.5
                    spacing 14
                    text info["local_description"]:
                        xalign 0.5
                        text_align 0.5
                        size 34
                        color "#e2e8f0"
                    if movie_available:
                        text "ระหว่างรับชม คลิก แตะ หรือกด Space / Enter เพื่อข้ามวิดีโอ":
                            xalign 0.5
                            text_align 0.5
                            size 27
                            color "#fcd34d"
                    else:
                        text "ไม่พบไฟล์วิดีโอ [info[local_movie]] ในแพ็กเกจเกม":
                            xalign 0.5
                            text_align 0.5
                            size 28
                            color "#fda4af"

            null height 8

            if not local_handled:
                hbox:
                    xalign 0.5
                    spacing 34

                    if movie_available:
                        textbutton "WATCH VIDEO  รับชมวิดีโอ":
                            xminimum 510
                            yminimum 94
                            background Solid(info["accent"] + "dd")
                            hover_background Solid(info["accent_hover"])
                            padding (28, 20)
                            text_size 32
                            text_color "#03111c"
                            text_hover_color "#000000"
                            text_bold True
                            action Return("watch")

                    textbutton "SKIP VIDEO  ข้ามวิดีโอ":
                        xminimum 440
                        yminimum 94
                        background Solid("#334155ee")
                        hover_background Solid("#64748b")
                        padding (28, 20)
                        text_size 31
                        text_color "#f8fafc"
                        text_hover_color "#ffffff"
                        text_bold True
                        action Return("skip")
            else:
                hbox:
                    xalign 0.5
                    spacing 34

                    if movie_available:
                        textbutton "REPLAY VIDEO  รับชมอีกครั้ง":
                            xminimum 500
                            yminimum 94
                            background Solid("#0e7490ee")
                            hover_background Solid("#0891b2")
                            padding (28, 20)
                            text_size 31
                            text_color "#ecfeff"
                            text_hover_color "#ffffff"
                            text_bold True
                            action Return("watch")

                    textbutton "CONTINUE  ไปส่วนที่ 2":
                        xminimum 500
                        yminimum 94
                        background Solid("#15803dee")
                        hover_background Solid("#22c55e")
                        padding (28, 20)
                        text_size 32
                        text_color "#f0fdf4"
                        text_hover_color "#ffffff"
                        text_bold True
                        action Return("continue")

    key "K_ESCAPE" action Return("skip" if not local_handled else "continue")


screen stage_learning_policy_screen(info, policy_movie_available, policy_handled):
    tag stage_learning
    modal True

    add Solid(info["bg"])
    add Solid("#00000038")

    frame:
        xalign 0.5
        yalign 0.07
        xsize 1740
        ysize 120
        background Solid(info["panel"])
        padding (42, 18)

        hbox:
            xfill True
            yalign 0.5

            vbox:
                spacing 2
                text info["stage_title"]:
                    size 48
                    color info["accent"]
                    bold True
                text info["sdg_title"]:
                    size 30
                    color "#e2e8f0"

            text "ส่วนที่ 2 จาก 2  |  PUBLIC CONNECTION":
                xalign 1.0
                yalign 0.5
                size 30
                color "#f8fafc"
                bold True

    frame:
        xalign 0.5
        yalign 0.57
        xsize 1580
        ysize 780
        background Solid(info["panel"])
        padding (68, 34)

        vbox:
            xfill True
            spacing 14

            text "เชื่อมโยงภารกิจกับหน่วยงานและการลงมือทำจริง":
                xalign 0.5
                text_align 0.5
                size 47
                color "#ffffff"
                bold True

            text info["agency"]:
                xalign 0.5
                text_align 0.5
                size 36
                color info["secondary"]
                bold True

            text info["policy_title"]:
                xalign 0.5
                text_align 0.5
                size 42
                color info["accent"]
                bold True

            frame:
                xalign 0.5
                xsize 1340
                ysize 250
                background Solid("#020617bb")
                padding (46, 30)

                vbox:
                    xalign 0.5
                    spacing 13
                    text info["policy_description"]:
                        xalign 0.5
                        text_align 0.5
                        size 30
                        color "#f1f5f9"
                    text info["source_note"]:
                        xalign 0.5
                        text_align 0.5
                        size 24
                        color "#cbd5e1"

            hbox:
                xalign 0.5
                spacing 28

                if info["policy_video"] and not policy_handled:
                    if policy_movie_available:
                        textbutton "WATCH POLICY VIDEO":
                            xminimum 360
                            yminimum 80
                            background Solid("#0e7490ee")
                            hover_background Solid("#0891b2")
                            padding (24, 16)
                            text_size 27
                            text_color "#ecfeff"
                            text_hover_color "#ffffff"
                            text_bold True
                            action Return("watch_policy")

                        textbutton "SKIP POLICY VIDEO":
                            xminimum 340
                            yminimum 80
                            background Solid("#475569ee")
                            hover_background Solid("#64748b")
                            padding (24, 16)
                            text_size 25
                            text_color "#f8fafc"
                            text_hover_color "#ffffff"
                            text_bold True
                            action Return("skip_policy")
                    else:
                        textbutton "CONTINUE WITHOUT VIDEO":
                            xminimum 420
                            yminimum 80
                            background Solid("#475569ee")
                            hover_background Solid("#64748b")
                            padding (24, 16)
                            text_size 25
                            text_color "#f8fafc"
                            text_hover_color "#ffffff"
                            text_bold True
                            action Return("skip_policy")

                elif info["policy_video"] and policy_movie_available:
                    textbutton "REPLAY POLICY VIDEO":
                        xminimum 390
                        yminimum 80
                        background Solid("#0e7490ee")
                        hover_background Solid("#0891b2")
                        padding (24, 16)
                        text_size 27
                        text_color "#ecfeff"
                        text_hover_color "#ffffff"
                        text_bold True
                        action Return("watch_policy")

                textbutton info["policy_link_label"]:
                    xminimum 510
                    yminimum 80
                    background Solid(info["accent"] + "dd")
                    hover_background Solid(info["accent_hover"])
                    padding (24, 16)
                    text_size 27
                    text_color "#03111c"
                    text_hover_color "#000000"
                    text_bold True
                    action OpenURL(info["policy_url"])

            if info.get("policy_link_notice"):
                text info["policy_link_notice"]:
                    xalign 0.5
                    xmaximum 1340
                    text_align 0.5
                    size 23
                    color "#fcd34d"

            if policy_handled:
                textbutton info.get("completion_button_label", "CONTINUE  ไปยังด่านถัดไป"):
                    xalign 0.5
                    xminimum 560
                    yminimum 88
                    background Solid("#15803dee")
                    hover_background Solid("#22c55e")
                    padding (26, 18)
                    text_size 31
                    text_color "#f0fdf4"
                    text_hover_color "#ffffff"
                    text_bold True
                    action Return("continue")

    if info["policy_video"] and not policy_handled:
        key "K_ESCAPE" action Return("skip_policy")


label stage_learning_flow(stage_id, next_label=None):
    $ learning_info = stage_learning_info(stage_id)

    if learning_info is None:
        $ renpy.notify("ไม่พบข้อมูล Learning Connection สำหรับด่านนี้")
        return next_label

    $ learning_local_available = renpy.loadable(learning_info["local_movie"])
    $ learning_local_handled = False
    $ learning_local_complete = False

    while not learning_local_complete:
        call screen stage_learning_local_screen(learning_info, learning_local_available, learning_local_handled)

        if _return == "watch" and learning_local_available:
            $ renpy.movie_cutscene(learning_info["local_movie"], stop_music=True)
            $ learning_local_handled = True
        elif _return == "skip":
            $ learning_local_handled = True
        elif _return == "continue" and learning_local_handled:
            $ learning_local_complete = True

    $ learning_policy_movie = learning_info["policy_video"]
    $ learning_policy_available = bool(learning_policy_movie and renpy.loadable(learning_policy_movie))
    $ learning_policy_handled = not bool(learning_policy_movie)
    $ learning_policy_complete = False

    while not learning_policy_complete:
        call screen stage_learning_policy_screen(learning_info, learning_policy_available, learning_policy_handled)

        if _return == "watch_policy" and learning_policy_available:
            $ renpy.movie_cutscene(learning_policy_movie, stop_music=True)
            $ learning_policy_handled = True
        elif _return == "skip_policy":
            $ learning_policy_handled = True
        elif _return == "continue" and learning_policy_handled:
            $ learning_policy_complete = True

    return next_label


# Fixed wrappers keep stage files free from dynamic jumps.  Call one wrapper,
# inspect _return, and use a normal if/jump in the owning stage file.
label rama4_learning_connection:
    call stage_learning_flow("rama4", "nextopia_start")
    return "nextopia_start"


label nextopia_learning_connection:
    call stage_learning_flow("nextopia", "lumpini_start")
    return "lumpini_start"


label lumpini_learning_connection:
    call stage_learning_flow("lumpini", "mk_lobby_start")
    return "mk_lobby_start"
