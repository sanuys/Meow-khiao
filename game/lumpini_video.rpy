# =============================================================================
# lumpini_video.rpy — หน้าวิดีโอของด่าน Lumpini (โค้ดรองรับความเข้ากันได้)
# =============================================================================
# UI วิดีโอแบบเดิมสำหรับเซฟรุ่นเก่า + จุดเข้า (label lumpini_video_hub) ที่ปัจจุบัน
# ส่งต่อไปยัง learning flow กลางใน learning_connections.rpy โดยตรง

define LUMPINI_VIDEO_FILE = "videos/3-LUMPINI_WELLNESS_QUEST/LUMPINI.ogv"

image lumpini video black = Solid("#020b12")
image lumpini video background = Transform(
    "images/story/3-LUMPINI_WELLNESS_QUEST/lumpini_video_bg.png",
    xysize=(1920, 1080),
)


init -5 python:
    def lumpini_video_is_available():
        """Return True only when the packaged LUMPINI movie is loadable."""
        movie_path = getattr(renpy.store, "LUMPINI_VIDEO_FILE", "")
        return bool(movie_path and renpy.loadable(movie_path))


transform lumpini_video_button_pulse:
    alpha 0.88
    linear 0.8 alpha 1.0
    linear 0.8 alpha 0.88
    repeat


screen lumpini_video_start_screen(video_available):
    tag lumpini_video
    modal True

    add "lumpini video background"
    add Solid("#020b1266")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1100
        background Solid("#03111cf2")
        padding (58, 48)

        vbox:
            xalign 0.5
            spacing 24

            text "LUMPINI WELLNESS QUEST":
                size 52
                color "#86efac"
                xalign 0.5
                bold True
                outlines [(3, "#052e16", 0, 0)]

            text "MISSION VIDEO":
                size 30
                color "#67e8f9"
                xalign 0.5
                bold True

            if video_available:
                text "รับชมวิดีโอสรุปภารกิจภายในเกม":
                    size 26
                    color "#e2e8f0"
                    xalign 0.5

                text "คลิก แตะ หรือกด Space / Enter เพื่อข้าม":
                    size 20
                    color "#fcd34d"
                    xalign 0.5

                textbutton "PLAY LUMPINI VIDEO":
                    at lumpini_video_button_pulse
                    xalign 0.5
                    xminimum 480
                    yminimum 82
                    background Solid("#047857e8")
                    hover_background Solid("#059669")
                    padding (26, 16)
                    text_color "#d1fae5"
                    text_hover_color "#ffffff"
                    text_size 29
                    text_bold True
                    action Return("play")
            else:
                text "ไม่พบไฟล์ videos/3-LUMPINI_WELLNESS_QUEST/LUMPINI.ogv":
                    size 27
                    color "#fda4af"
                    xalign 0.5

                text "ตรวจสอบไฟล์วิดีโอ แล้วเปิดหน้านี้อีกครั้ง":
                    size 20
                    color "#fcd34d"
                    xalign 0.5

                textbutton "FINISH WITHOUT VIDEO":
                    xalign 0.5
                    xminimum 440
                    yminimum 76
                    background Solid("#475569e8")
                    hover_background Solid("#64748b")
                    padding (24, 15)
                    text_color "#f1f5f9"
                    text_hover_color "#ffffff"
                    text_size 26
                    text_bold True
                    action Return("finish")

            hbox:
                xalign 0.5
                spacing 28

                textbutton "<  BACK":
                    xminimum 250
                    yminimum 66
                    background Solid("#1e293be8")
                    hover_background Solid("#334155")
                    padding (22, 13)
                    text_color "#e2e8f0"
                    text_hover_color "#ffffff"
                    text_size 24
                    action Return("back")

                textbutton "MAIN MENU":
                    xminimum 250
                    yminimum 66
                    background Solid("#3f1d2de8")
                    hover_background Solid("#881337")
                    padding (22, 13)
                    text_color "#fecdd3"
                    text_hover_color "#ffffff"
                    text_size 24
                    action MainMenu(confirm=True)

    key "K_ESCAPE" action Return("back")


screen lumpini_video_complete_screen():
    tag lumpini_video
    modal True

    add "lumpini video background"
    add Solid("#020b1275")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1040
        background Solid("#03111cf2")
        padding (58, 48)

        vbox:
            xalign 0.5
            spacing 25

            text "VIDEO COMPLETE":
                size 54
                color "#86efac"
                xalign 0.5
                bold True
                outlines [(3, "#052e16", 0, 0)]

            text "Lumpini Wellness Quest เสร็จสมบูรณ์":
                size 27
                color "#e2e8f0"
                xalign 0.5

            textbutton "FINISH QUEST":
                xalign 0.5
                xminimum 420
                yminimum 80
                background Solid("#047857e8")
                hover_background Solid("#059669")
                padding (25, 16)
                text_color "#d1fae5"
                text_hover_color "#ffffff"
                text_size 29
                text_bold True
                action Return("finish")

            hbox:
                xalign 0.5
                spacing 28

                textbutton "REPLAY VIDEO":
                    xminimum 280
                    yminimum 68
                    background Solid("#0e7490e8")
                    hover_background Solid("#0891b2")
                    padding (22, 14)
                    text_color "#cffafe"
                    text_hover_color "#ffffff"
                    text_size 24
                    action Return("replay")

                textbutton "MAIN MENU":
                    xminimum 260
                    yminimum 68
                    background Solid("#3f1d2de8")
                    hover_background Solid("#881337")
                    padding (22, 14)
                    text_color "#fecdd3"
                    text_hover_color "#ffffff"
                    text_size 24
                    action MainMenu(confirm=True)


label lumpini_video_hub:
    # Compatibility entry point for old saves and older stage code. The shared
    # learning flow now owns local video playback plus the public-policy section
    # so this label no longer duplicates that state machine.
    call stage_learning_flow("lumpini", "mk_lobby_start")
    return "finish"
