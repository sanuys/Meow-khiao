# =============================================================================
# lumpini.rpy — ด่านที่ 3: LUMPINI WELLNESS QUEST (SDG 3) — Rhythm Battle
# =============================================================================
# เนื้อเรื่องซีน 1-22 ใช้โครงสร้างมาตรฐาน scene + Character Say ของ Ren'Py
# มินิเกมจังหวะดนตรี 4 เลน (PERFECT/GREAT/GOOD + Combo) วาดเลนและโน้ตด้วยโค้ดล้วน
# เกณฑ์ผ่านด่านอิง HP ที่เหลือจาก Sustainability Decision และต้องเล่นจนจบเพลง
#
# ตำแหน่ง asset ที่ใช้:
#   - ภาพเนื้อเรื่อง        : images/story/3-LUMPINI_WELLNESS_QUEST/ (นามแฝงใน screens.rpy)
#   - พื้นหลังสนาม/แพ้/ชนะ  : minigames/3-LUMPINI_WELLNESS_QUEST/images/backgrounds/
#   - ภาพ tutorial          : minigames/3-LUMPINI_WELLNESS_QUEST/images/tutorial/
#   - เพลงมินิเกม (30.7 วิ)  : minigames/3-LUMPINI_WELLNESS_QUEST/audio/Lumpini_Song.mp3
#   - เพลงประกอบด่าน (BGM)  : audio/3-LUMPINI_WELLNESS_QUEST/Lumpini_Wellness_Quest_BGM.mp3

define LWQ_SONG_FILE = "minigames/3-LUMPINI_WELLNESS_QUEST/audio/Lumpini_Song.mp3"
define LWQ_STAGE_BGM_FILE = "audio/3-LUMPINI_WELLNESS_QUEST/Lumpini_Wellness_Quest_BGM.mp3"
define LWQ_SONG_DURATION = 30.746
define LWQ_ANALYZED_BPM = 192.0
define LWQ_BEAT_OFFSET = 0.137
# Fallback values for old saves or isolated testing. The live battle receives
# its post-decision HP from sustainability_core.rpy (25,000 or 35,000).
define LWQ_PASS_SCORE = 30000
define LWQ_MONSTER_MAX_HP = 30000

image lwq rhythm arena = Transform(
    "minigames/3-LUMPINI_WELLNESS_QUEST/images/backgrounds/lumpini_rhythm_arena_bg.png",
    xysize=(1920, 1080),
)
image lwq tutorial background = Transform(
    "minigames/3-LUMPINI_WELLNESS_QUEST/images/tutorial/lumpini_rhythm_tutorial_bg.png",
    xysize=(1920, 1080),
)
image lwq victory background = Transform(
    "minigames/3-LUMPINI_WELLNESS_QUEST/images/backgrounds/lumpini_victory_bg.png",
    xysize=(1920, 1080),
)
image lwq defeat background = Transform(
    "minigames/3-LUMPINI_WELLNESS_QUEST/images/backgrounds/lumpini_defeat_bg.png",
    xysize=(1920, 1080),
)


transform lwq_next_pulse:
    alpha 0.86
    linear 0.72 alpha 1.0
    linear 0.72 alpha 0.86
    repeat


init -10 python:
    import math

    LWQ_RHYTHM_CHANNEL = "lwq_rhythm_combat"
    LWQ_COUNTDOWN_SECONDS = 3.0
    LWQ_NOTE_TRAVEL_SECONDS = 1.75
    LWQ_PERFECT_WINDOW = 0.085
    LWQ_GREAT_WINDOW = 0.165
    LWQ_GOOD_WINDOW = 0.275

    # The source MP3 was decoded and analyzed at 22,050 Hz. Its dominant grid
    # is 192 BPM (96 BPM halftime), with a phase near 0.137 seconds. The intro
    # uses every third beat, the build uses every second beat, the chorus uses
    # each beat, and the outro returns to half-time. This produces 66 playable
    # notes spanning 1.0745-29.1995 seconds of the 30.746-second song.
    def lwq_build_beatmap():
        quarter = 60.0 / 192.0
        beat_indices = []
        beat_indices.extend(range(3, 29, 3))
        beat_indices.extend(range(29, 39, 2))
        beat_indices.extend(range(39, 87))
        beat_indices.extend(range(87, 95, 2))

        lane_pattern = (
            0, 1, 2, 3, 1, 0, 2, 3,
            0, 2, 1, 3, 2, 0, 3, 1,
        )

        chart = []
        for note_index, beat_index in enumerate(sorted(set(beat_indices))):
            note_time = round(0.137 + beat_index * quarter, 4)
            if note_time <= 29.55:
                chart.append((note_time, lane_pattern[note_index % len(lane_pattern)]))
        return tuple(chart)


    LWQ_BEATMAP = lwq_build_beatmap()
    LWQ_LANE_X = (555, 755, 955, 1155)
    LWQ_LANE_KEYS = ("A / LEFT", "W / UP", "S / DOWN", "D / RIGHT")
    LWQ_LANE_SYMBOLS = ("<", "^", "v", ">")
    LWQ_LANE_COLORS = ("#22d3ee", "#86efac", "#facc15", "#f472b6")

    renpy.music.register_channel(
        LWQ_RHYTHM_CHANNEL,
        mixer="music",
        loop=False,
        # Keep the timing channel advancing even when the player mutes Music;
        # otherwise get_pos() would never reach the beatmap/end state.
        stop_on_mute=False,
    )

    def lwq_stage_bgm_is_playing():
        """Return True when the Lumpini stage loop owns the music channel."""
        playing = renpy.music.get_playing(channel="music")
        if not playing:
            return False

        current_path = str(playing).replace("\\", "/").lower()
        target_path = str(renpy.store.LWQ_STAGE_BGM_FILE).replace("\\", "/").lower()
        return current_path == target_path or current_path.endswith("/" + target_path)

    def lwq_play_stage_bgm():
        """Start the one Lumpini BGM without restarting its active loop."""
        bgm_path = renpy.store.LWQ_STAGE_BGM_FILE
        if not renpy.loadable(bgm_path):
            return False
        if lwq_stage_bgm_is_playing():
            return True

        renpy.music.play(
            bgm_path,
            channel="music",
            loop=True,
            fadeout=0.35,
            fadein=0.35,
        )
        return True

    def lwq_stop_stage_bgm():
        """Release the stage BGM before rhythm combat or learning videos."""
        renpy.music.stop(channel="music", fadeout=0.25)

    def lwq_stop_background_audio():
        """Give the rhythm battle exclusive audio focus.

        The final two names belong to bundled rhythm/hidden-object examples and
        are stopped defensively when those channels have been registered.
        """
        for channel_name in (
                "music", "sound", "voice", LWQ_RHYTHM_CHANNEL,
                "CHANNEL_RHYTHM_GAME", "effect"):
            try:
                renpy.music.stop(channel=channel_name, fadeout=0.12)
            except Exception:
                pass


    class LWQRhythmCombat(renpy.Displayable):
        """Audio-synchronized, four-lane rhythm battle for Lumpini."""

        def __init__(self, monster_max_hp=None):
            super(LWQRhythmCombat, self).__init__()

            self.song_path = renpy.store.LWQ_SONG_FILE
            self.notes = [
                {"time": note_time, "lane": lane, "state": None}
                for note_time, lane in LWQ_BEATMAP
            ]
            self.total_notes = len(self.notes)

            self.score = 0
            self.combo = 0
            self.max_combo = 0
            self.perfect = 0
            self.great = 0
            self.good = 0
            self.miss = 0
            self.bad_taps = 0
            try:
                resolved_hp = int(monster_max_hp)
            except (TypeError, ValueError):
                resolved_hp = int(renpy.store.LWQ_MONSTER_MAX_HP)
            self.monster_max_hp = max(1, resolved_hp)
            self.pass_score = self.monster_max_hp
            self.monster_hp = self.monster_max_hp

            self.song_time = -LWQ_COUNTDOWN_SECONDS
            self.song_started = False
            self.has_ended = False
            self.is_paused = False
            self._first_st = None
            self._last_audio_time = 0.0

            self.last_judgment = "GET READY"
            self.last_judgment_color = "#d1fae5"
            self.last_judgment_until = 0.0
            self.hit_flash_until = 0.0
            self.lane_flash_until = [-99.0, -99.0, -99.0, -99.0]

            self.lane_panel = Solid("#03151dcc", xsize=154, ysize=610)
            self.hit_line = Solid("#d1fae5", xsize=770, ysize=5)
            self.progress_track = Solid("#0f172acc", xsize=1740, ysize=10)
            self.hp_track = Solid("#1e293b", xsize=620, ysize=28)
            self.note_drawables = [
                Solid(color, xsize=126, ysize=54)
                for color in LWQ_LANE_COLORS
            ]
            self.receptor_outer = [
                Solid(color, xsize=146, ysize=82)
                for color in LWQ_LANE_COLORS
            ]
            self.lane_flash_columns = [
                Solid(color + "62", xsize=174, ysize=620)
                for color in LWQ_LANE_COLORS
            ]
            self.lane_flash_receptors = [
                Solid(color + "d8", xsize=166, ysize=102)
                for color in LWQ_LANE_COLORS
            ]
            self.receptor_inner = Solid("#03111cf2", xsize=134, ysize=70)

            self._children = [
                self.lane_panel,
                self.hit_line,
                self.progress_track,
                self.hp_track,
                self.receptor_inner,
            ]
            self._children.extend(self.note_drawables)
            self._children.extend(self.receptor_outer)
            self._children.extend(self.lane_flash_columns)
            self._children.extend(self.lane_flash_receptors)

            # A silence prefix gives the player a countdown while preserving a
            # single deterministic playback flow. Once the MP3 begins, note
            # timing reads renpy.music.get_pos() for direct audio sync.
            renpy.music.play(
                ["<silence 3.0>", self.song_path],
                channel=LWQ_RHYTHM_CHANNEL,
                loop=False,
            )

        def visit(self):
            return self._children

        def _song_is_playing(self):
            playing = renpy.music.get_playing(channel=LWQ_RHYTHM_CHANNEL)
            if not playing:
                return False
            normalized = str(playing).replace("\\", "/").lower()
            return normalized.endswith("lumpini_song.mp3")

        def _current_audio_time(self, st=None):
            if self._song_is_playing():
                position = renpy.music.get_pos(channel=LWQ_RHYTHM_CHANNEL)
                if position is not None:
                    self.song_started = True
                    self._last_audio_time = max(0.0, float(position))
                    return self._last_audio_time

            if not self.song_started:
                if st is None or self._first_st is None:
                    return self.song_time
                return min(0.0, (st - self._first_st) - LWQ_COUNTDOWN_SECONDS)

            return self._last_audio_time

        def _mark_expired_notes(self, current_time):
            changed = False
            for note in self.notes:
                if note["state"] is None and current_time > note["time"] + LWQ_GOOD_WINDOW:
                    note["state"] = "miss"
                    self.miss += 1
                    self.combo = 0
                    self.last_judgment = "MISS"
                    self.last_judgment_color = "#fb7185"
                    self.last_judgment_until = current_time + 0.34
                    changed = True
            return changed

        def _judge(self, note, delta):
            absolute_delta = abs(delta)

            if absolute_delta <= LWQ_PERFECT_WINDOW:
                judgment = "perfect"
                base_points = 1000
                self.perfect += 1
                color = "#86efac"
            elif absolute_delta <= LWQ_GREAT_WINDOW:
                judgment = "great"
                base_points = 700
                self.great += 1
                color = "#67e8f9"
            else:
                judgment = "good"
                base_points = 400
                self.good += 1
                color = "#facc15"

            note["state"] = judgment
            self.combo += 1
            self.max_combo = max(self.max_combo, self.combo)
            combo_bonus = min(max(0, self.combo - 1), 20) * 10
            attack_points = base_points + combo_bonus
            self.score += attack_points
            self.monster_hp = max(0, self.monster_hp - attack_points)

            self.last_judgment = judgment.upper()
            self.last_judgment_color = color
            self.last_judgment_until = self.song_time + 0.42
            self.hit_flash_until = self.song_time + 0.15
            self.lane_flash_until[int(note["lane"])] = self.song_time + 0.24

        def lane_is_flashing(self, lane):
            try:
                return self.song_time <= self.lane_flash_until[int(lane)]
            except (IndexError, TypeError, ValueError):
                return False

        def press_lane(self, lane):
            if self.has_ended or self.is_paused or not self.song_started:
                return

            current_time = self._current_audio_time()
            self.song_time = current_time
            self._mark_expired_notes(current_time)

            candidates = [
                note for note in self.notes
                if note["lane"] == lane and note["state"] is None
            ]
            if candidates:
                closest = min(candidates, key=lambda note: abs(note["time"] - current_time))
                delta = current_time - closest["time"]
                if abs(delta) <= LWQ_GOOD_WINDOW:
                    self._judge(closest, delta)
                    renpy.redraw(self, 0)
                    return

            # Empty-key presses cannot cause damage and break the current combo.
            self.bad_taps += 1
            self.combo = 0
            self.last_judgment = "TOO EARLY / LATE"
            self.last_judgment_color = "#fb7185"
            self.last_judgment_until = current_time + 0.28
            renpy.redraw(self, 0)

        def pause(self):
            if self.song_started and not self.has_ended and not self.is_paused:
                self.is_paused = True
                renpy.music.set_pause(True, channel=LWQ_RHYTHM_CHANNEL)
                renpy.redraw(self, 0)

        def resume(self):
            if self.is_paused:
                renpy.music.set_pause(False, channel=LWQ_RHYTHM_CHANNEL)
                self.is_paused = False
                renpy.redraw(self, 0)

        def stop(self):
            renpy.music.stop(channel=LWQ_RHYTHM_CHANNEL)

        def _finish(self):
            if self.has_ended:
                return
            for note in self.notes:
                if note["state"] is None:
                    note["state"] = "miss"
                    self.miss += 1
            self.combo = 0
            self.has_ended = True
            renpy.timeout(0)

        def accuracy(self):
            judged_notes = self.perfect + self.great + self.good + self.miss
            if judged_notes <= 0:
                return 0.0
            weighted_hits = self.perfect + self.great * 0.75 + self.good * 0.45
            return 100.0 * weighted_hits / float(judged_notes)

        def result(self):
            passed_score = self.score >= self.pass_score
            monster_defeated = self.monster_hp <= 0
            return {
                "status": "victory" if passed_score and monster_defeated else "defeat",
                "score": self.score,
                "pass_score": self.pass_score,
                "monster_hp": self.monster_hp,
                "monster_max_hp": self.monster_max_hp,
                "accuracy": self.accuracy(),
                "perfect": self.perfect,
                "great": self.great,
                "good": self.good,
                "miss": self.miss,
                "bad_taps": self.bad_taps,
                "max_combo": self.max_combo,
                "total_notes": self.total_notes,
            }

        def _put_text(self, target, value, x, y, size, color="#ffffff", bold=False, outlines=None):
            if outlines is None:
                outlines = [(2, "#020617", 0, 0)]
            target.place(
                Text(str(value), size=size, color=color, bold=bold, outlines=outlines),
                x=x,
                y=y,
            )

        def render(self, width, height, st, at):
            if self._first_st is None:
                self._first_st = st

            target = renpy.Render(width, height)

            if not self.is_paused:
                current_time = self._current_audio_time(st)
                self.song_time = current_time

                if self.song_started:
                    self._mark_expired_notes(current_time)

                    playing = renpy.music.get_playing(channel=LWQ_RHYTHM_CHANNEL)
                    # HP reaching zero never ends the battle early. The result
                    # (and therefore the video button) unlocks only after the
                    # audio channel finishes or the full song duration elapses.
                    if (playing is None or
                            current_time >= float(renpy.store.LWQ_SONG_DURATION) + 0.15):
                        self._finish()

            current_time = self.song_time
            lane_top = 255
            lane_height = 610
            receptor_y = 812

            # Translucent lanes retain the newly generated arena art beneath.
            for lane, lane_x in enumerate(LWQ_LANE_X):
                flash_remaining = self.lane_flash_until[lane] - current_time
                target.place(self.lane_panel, x=lane_x, y=lane_top)
                if flash_remaining > 0.0:
                    flash_alpha = max(0.12, min(1.0, flash_remaining / 0.24))
                    # Draw the successful-hit flash over the dark lane panel so
                    # it remains clearly visible instead of being dimmed behind
                    # the panel's high-opacity fill.
                    target.place(
                        Transform(self.lane_flash_columns[lane], alpha=flash_alpha),
                        x=lane_x - 10,
                        y=lane_top,
                    )
                target.place(self.receptor_outer[lane], x=lane_x + 4, y=receptor_y)
                if flash_remaining > 0.0:
                    target.place(
                        Transform(self.lane_flash_receptors[lane], alpha=flash_alpha),
                        x=lane_x - 6,
                        y=receptor_y - 10,
                    )
                target.place(self.receptor_inner, x=lane_x + 10, y=receptor_y + 6)
                self._put_text(
                    target,
                    LWQ_LANE_SYMBOLS[lane],
                    lane_x + 60,
                    receptor_y + 12,
                    45,
                    LWQ_LANE_COLORS[lane],
                    True,
                )

            target.place(self.hit_line, x=548, y=receptor_y - 3)

            # Notes descend toward the receptor over a fixed travel time.
            for note in self.notes:
                if note["state"] is not None:
                    continue
                seconds_until_hit = note["time"] - current_time
                if seconds_until_hit < -LWQ_GOOD_WINDOW:
                    continue
                if seconds_until_hit > LWQ_NOTE_TRAVEL_SECONDS:
                    continue

                progress = 1.0 - max(0.0, seconds_until_hit) / LWQ_NOTE_TRAVEL_SECONDS
                note_y = lane_top + int(progress * (receptor_y - lane_top))
                lane = note["lane"]
                note_x = LWQ_LANE_X[lane] + 14
                target.place(self.note_drawables[lane], x=note_x, y=note_y)
                self._put_text(
                    target,
                    LWQ_LANE_SYMBOLS[lane],
                    note_x + 47,
                    note_y + 2,
                    37,
                    "#03111c",
                    True,
                    [],
                )

            # Mission HUD.
            target.place(Solid("#020b12dd", xsize=1920, ysize=185), x=0, y=0)
            self._put_text(target, "LUMPINI WELLNESS QUEST", 55, 25, 43, "#86efac", True)
            self._put_text(target, "RHYTHM POWER vs CARBON MONSTER", 58, 78, 24, "#67e8f9", True)
            self._put_text(target, "SCORE  {:,}".format(self.score), 58, 122, 32, "#ffffff", True)
            self._put_text(target, "COMBO  x{}".format(self.combo), 375, 122, 29, "#facc15", True)
            self._put_text(target, "ACCURACY  {:.1f}%".format(self.accuracy()), 620, 122, 27, "#d1fae5", True)

            self._put_text(target, "CARBON MONSTER HP", 1210, 28, 28, "#fda4af", True)
            hp_fraction = max(0.0, min(1.0, self.monster_hp / float(self.monster_max_hp)))
            target.place(self.hp_track, x=1210, y=76)
            if hp_fraction > 0.0:
                hp_color = "#ef4444" if hp_fraction > 0.35 else "#facc15"
                target.place(
                    Solid(hp_color, xsize=max(1, int(620 * hp_fraction)), ysize=28),
                    x=1210,
                    y=76,
                )
            self._put_text(
                target,
                "{:,} / {:,}".format(self.monster_hp, self.monster_max_hp),
                1390,
                70,
                23,
                "#ffffff",
                True,
            )
            self._put_text(
                target,
                "PASS SCORE  {:,}".format(self.pass_score),
                1210,
                121,
                27,
                "#fcd34d",
                True,
            )

            if current_time < 0.0:
                countdown = max(1, int(math.ceil(-current_time)))
                self._put_text(target, countdown, 930, 410, 112, "#86efac", True, [(5, "#052e16", 0, 0)])
            elif current_time <= self.last_judgment_until:
                self._put_text(
                    target,
                    self.last_judgment,
                    820,
                    200,
                    48,
                    self.last_judgment_color,
                    True,
                    [(4, "#020617", 0, 0)],
                )

            # A short wellness-energy flash makes each scored hit read as an
            # attack on the Carbon Monster while the HP bar drops 1:1.
            if current_time <= self.hit_flash_until:
                target.place(Solid("#86efac2b", xsize=720, ysize=300), x=600, y=185)

            progress_fraction = max(
                0.0,
                min(1.0, max(0.0, current_time) / float(renpy.store.LWQ_SONG_DURATION)),
            )
            target.place(self.progress_track, x=90, y=1045)
            if progress_fraction > 0.0:
                target.place(
                    Solid("#22c55e", xsize=max(1, int(1740 * progress_fraction)), ysize=10),
                    x=90,
                    y=1045,
                )

            if self.is_paused:
                target.place(Solid("#02061799", xsize=1920, ysize=1080), x=0, y=0)

            if not self.has_ended:
                renpy.redraw(self, 0)
            return target


screen lwq_rhythm_briefing_screen(song_available, required_hp):
    tag lwq_rhythm
    modal True
    zorder 100

    add "lwq rhythm arena"
    add Solid("#02061799")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1230
        background Solid("#03111cf2")
        padding (58, 46)

        vbox:
            xalign 0.5
            spacing 19

            text "LUMPINI WELLNESS QUEST":
                xalign 0.5
                size 54
                color "#86efac"
                bold True

            text "RHYTHM POWER BATTLE":
                xalign 0.5
                size 32
                color "#67e8f9"
                bold True

            text "กดให้ตรงจังหวะเพลงเพื่อเปลี่ยนคะแนนเป็นพลังโจมตี Carbon Monster":
                xalign 0.5
                size 27
                color "#e2e8f0"

            text "Keyboard: A W S D  หรือ  ลูกศร    |    Touch: ปุ่ม 4 เลนด้านล่าง":
                xalign 0.5
                size 24
                color "#cbd5e1"

            hbox:
                xalign 0.5
                spacing 28

                frame:
                    xsize 395
                    background Solid("#052e2be8")
                    padding (24, 18)
                    vbox:
                        text "PASS SCORE" xalign 0.5 size 24 color "#67e8f9" bold True
                        text "{:,}".format(required_hp) xalign 0.5 size 42 color "#facc15" bold True

                frame:
                    xsize 395
                    background Solid("#3f1019e8")
                    padding (24, 18)
                    vbox:
                        text "CARBON MONSTER HP" xalign 0.5 size 24 color "#fda4af" bold True
                        text "{:,}".format(required_hp) xalign 0.5 size 42 color "#fb7185" bold True

            if song_available:
                textbutton "START RHYTHM BATTLE":
                    xalign 0.5
                    xminimum 530
                    yminimum 82
                    background Solid("#047857ed")
                    hover_background Solid("#059669")
                    padding (28, 16)
                    text_color "#d1fae5"
                    text_hover_color "#ffffff"
                    text_size 31
                    text_bold True
                    action Return("start")
            else:
                text "ไม่พบไฟล์ minigames/3-LUMPINI_WELLNESS_QUEST/audio/Lumpini_Song.mp3":
                    xalign 0.5
                    size 27
                    color "#fda4af"

            textbutton "MAIN MENU":
                xalign 0.5
                xminimum 330
                yminimum 62
                background Solid("#1e293be8")
                hover_background Solid("#334155")
                padding (24, 12)
                text_color "#e2e8f0"
                text_hover_color "#ffffff"
                text_size 23
                action MainMenu(confirm=True)


# -----------------------------------------------------------------------------
# Three-page rhythm tutorial shown directly after Sustainability Decision.
# The generated image supplies atmosphere only; all instructional copy and
# controls are code-native for readability, localization, and accessibility.
# -----------------------------------------------------------------------------

screen _legacy_lumpini_minigame_tutorial_page(page=0):
    tag lwq_tutorial
    modal True
    zorder 100

    $ decision_hp = max(1, int(mk_get_stage_start_hp("lumpini")))

    add "lwq tutorial background"
    add Solid("#020617b8")

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
                text "LUMPINI RHYTHM TUTORIAL" size 42 color "#86efac" bold True
                text "คู่มือสร้างพลังสุขภาวะด้วยจังหวะเพลง" size 26 color "#dbeafe"

            text "PAGE  [page + 1] / 3":
                xalign 1.0
                yalign 0.5
                size 28
                color "#67e8f9"
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

                text "1  กดปุ่มให้ตรงเลนและตรงจังหวะ":
                    xalign 0.5
                    size 42
                    color "#86efac"
                    bold True

                text "โน้ตจะเคลื่อนลงสู่เส้นรับจังหวะ กดปุ่มของเลนนั้นเมื่อตำแหน่งซ้อนกัน":
                    xalign 0.5
                    size 29
                    color "#ffffff"
                    text_align 0.5

                hbox:
                    xalign 0.5
                    spacing 20

                    for lane in range(4):
                        frame:
                            xsize 390
                            ysize 370
                            background Solid(LWQ_LANE_COLORS[lane] + "30")
                            padding (24, 20)

                            vbox:
                                xalign 0.5
                                spacing 13
                                text "LANE  [lane + 1]" size 27 color "#cbd5e1" bold True xalign 0.5
                                text LWQ_LANE_SYMBOLS[lane] size 112 color LWQ_LANE_COLORS[lane] bold True xalign 0.5
                                text LWQ_LANE_KEYS[lane] size 31 color "#ffffff" bold True xalign 0.5
                                text ("แตะปุ่มเลนนี้บนหน้าจอ") size 24 color "#dbeafe" text_align 0.5 xalign 0.5

                frame:
                    xalign 0.5
                    xsize 1580
                    background Solid("#052e2be8")
                    padding (24, 14)
                    text "เมื่อกดถูก เลนนั้นจะ Flash สีสว่าง พร้อมแสดง PERFECT / GREAT / GOOD":
                        xalign 0.5
                        size 27
                        color "#bbf7d0"
                        bold True
                        text_align 0.5

        elif page == 1:
            vbox:
                xfill True
                spacing 20

                text "2  คุณภาพจังหวะ คะแนน และ Combo":
                    xalign 0.5
                    size 42
                    color "#67e8f9"
                    bold True

                hbox:
                    xalign 0.5
                    spacing 20

                    frame:
                        xsize 525
                        ysize 310
                        background Solid("#123122e8")
                        padding (26, 22)
                        vbox:
                            xalign 0.5
                            spacing 13
                            text "PERFECT" size 38 color "#86efac" bold True xalign 0.5
                            text "+1,000" size 60 color "#ffffff" bold True xalign 0.5
                            text "กดใกล้จังหวะเป้าหมายที่สุด" size 25 color "#d1fae5" xalign 0.5 text_align 0.5

                    frame:
                        xsize 525
                        ysize 310
                        background Solid("#0b3143e8")
                        padding (26, 22)
                        vbox:
                            xalign 0.5
                            spacing 13
                            text "GREAT" size 38 color "#67e8f9" bold True xalign 0.5
                            text "+700" size 60 color "#ffffff" bold True xalign 0.5
                            text "กดคลาดจากจังหวะเล็กน้อย" size 25 color "#cffafe" xalign 0.5 text_align 0.5

                    frame:
                        xsize 525
                        ysize 310
                        background Solid("#3c2c12e8")
                        padding (26, 22)
                        vbox:
                            xalign 0.5
                            spacing 13
                            text "GOOD" size 38 color "#facc15" bold True xalign 0.5
                            text "+400" size 60 color "#ffffff" bold True xalign 0.5
                            text "กดทันในช่วงรับจังหวะ" size 25 color "#fef3c7" xalign 0.5 text_align 0.5

                hbox:
                    xalign 0.5
                    spacing 24

                    frame:
                        xsize 800
                        ysize 220
                        background Solid("#052e2be8")
                        padding (28, 20)
                        vbox:
                            spacing 10
                            text "COMBO" size 32 color "#86efac" bold True
                            text "กดถูกต่อเนื่องเพื่อรับคะแนนโบนัส Combo สูงสุด +200 ต่อโน้ต" size 26 color "#e2e8f0" line_spacing 3

                    frame:
                        xsize 800
                        ysize 220
                        background Solid("#3f1019e8")
                        padding (28, 20)
                        vbox:
                            spacing 10
                            text "MISS / กดเร็วหรือช้าเกินไป" size 32 color "#fda4af" bold True
                            text "ไม่เพิ่มคะแนน และทำให้ Combo กลับเป็น 0 รอจังหวะถัดไปแล้วเล่นต่อได้ทันที" size 26 color "#e2e8f0" line_spacing 3

        else:
            vbox:
                xfill True
                spacing 22

                text "3  ปราบ Carbon Monster และเล่นให้จบเพลง":
                    xalign 0.5
                    size 42
                    color "#fcd34d"
                    bold True

                hbox:
                    xalign 0.5
                    spacing 24

                    frame:
                        xsize 828
                        ysize 585
                        background Solid("#3f1019e8")
                        padding (32, 26)
                        vbox:
                            spacing 17
                            text "CARBON MONSTER HP" size 34 color "#fda4af" bold True xalign 0.5
                            text "{:,}".format(decision_hp) size 60 color "#ffffff" bold True xalign 0.5
                            bar:
                                value StaticValue(decision_hp, decision_hp)
                                xalign 0.5
                                xsize 690
                                ysize 32
                                left_bar Solid("#ef4444")
                                right_bar Solid("#1e293b")
                            text "คะแนน 1 หน่วย = พลังโจมตี 1 HP" size 28 color "#fef3c7" bold True xalign 0.5
                            text "ต้องทำคะแนนอย่างน้อยเท่ากับ HP หลัง Sustainability Decision และลด HP ให้เหลือ 0" size 26 color "#e2e8f0" text_align 0.5 xalign 0.5 line_spacing 3

                    frame:
                        xsize 828
                        ysize 585
                        background Solid("#123122e8")
                        padding (32, 26)
                        vbox:
                            spacing 16
                            text "กติกาสำคัญ" size 34 color "#86efac" bold True xalign 0.5
                            text "แม้ HP จะเหลือ 0 แล้ว ต้องเล่นต่อจน Lumpini_Song.mp3 จบเพลง" size 27 color "#ffffff" bold True text_align 0.5 xalign 0.5 line_spacing 3
                            text "หลังเพลงจบ ปุ่ม ดูสรุปผล จะปรากฏ" size 26 color "#cffafe" text_align 0.5 xalign 0.5
                            text "ชนะ: รับ SDG 3 Badge, Meow Coin +{:,} และ Eco Score +{:,}".format(MK_STAGE_REWARD_COINS, MK_STAGE_REWARD_ECO_SCORE) size 25 color "#bbf7d0"
                            text "แพ้: เลือก Retry หรือไปหน้าสรุปการเรียนรู้ได้" size 25 color "#fecdd3"
                            text "กด Esc หรือปุ่มพักเพื่อ Pause ระหว่างเพลง" size 25 color "#dbeafe"

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
            textbutton "START  ไปหน้าเตรียมพร้อม  >":
                default_focus True
                xminimum 360
                yminimum 80
                background Solid("#047857ed")
                hover_background Solid("#059669")
                padding (24, 16)
                text_color "#d1fae5"
                text_hover_color "#ffffff"
                text_size 27
                text_bold True
                action Return("start")

    key "K_LEFT" action If(page > 0, true=Return("back"), false=NullAction())
    key "K_RIGHT" action If(page < 2, true=Return("next"), false=Return("start"))
    key "K_RETURN" action If(page < 2, true=Return("next"), false=Return("start"))
    key "K_SPACE" action If(page < 2, true=Return("next"), false=Return("start"))
    key "game_menu" action If(page > 0, true=Return("back"), false=NullAction())


screen lwq_rhythm_game_screen(game):
    tag lwq_rhythm
    modal True
    zorder 100

    key "K_LEFT" action Function(game.press_lane, 0)
    key "K_a" action Function(game.press_lane, 0)
    key "K_UP" action Function(game.press_lane, 1)
    key "K_w" action Function(game.press_lane, 1)
    key "K_DOWN" action Function(game.press_lane, 2)
    key "K_s" action Function(game.press_lane, 2)
    key "K_RIGHT" action Function(game.press_lane, 3)
    key "K_d" action Function(game.press_lane, 3)
    key "K_ESCAPE" action If(
        game.song_started,
        true=[Function(game.pause), Show("lwq_rhythm_pause_screen", game=game)],
        false=NullAction(),
    )

    add "lwq rhythm arena"
    add game

    for lane in range(4):
        textbutton LWQ_LANE_KEYS[lane]:
            xpos LWQ_LANE_X[lane]
            ypos 918
            xminimum 154
            yminimum 102
            background Solid("#03111ce8")
            hover_background Solid(LWQ_LANE_COLORS[lane] + "55")
            padding (12, 17)
            text_size 20
            text_color LWQ_LANE_COLORS[lane]
            text_hover_color "#ffffff"
            text_bold True
            action Function(game.press_lane, lane)

    textbutton "II":
        xpos 1780
        ypos 198
        xminimum 92
        yminimum 66
        background Solid("#0f172acc")
        hover_background Solid("#334155")
        text_size 27
        text_color "#e2e8f0"
        action If(
            game.song_started,
            true=[Function(game.pause), Show("lwq_rhythm_pause_screen", game=game)],
            false=NullAction(),
        )

    if game.has_ended:
        add Solid("#020617a8")

        frame:
            xalign 0.5
            yalign 0.5
            xsize 760
            background Solid("#03111cf5")
            padding (48, 38)

            vbox:
                xalign 0.5
                spacing 20

                text "เพลงจบแล้ว":
                    xalign 0.5
                    size 48
                    color "#86efac"
                    bold True

                text "คะแนนและผลการต่อสู้พร้อมสรุป":
                    xalign 0.5
                    size 27
                    color "#e2e8f0"

                textbutton "ดูสรุปผล":
                    xalign 0.5
                    xminimum 500
                    yminimum 88
                    background Solid("#047857")
                    hover_background Solid("#059669")
                    padding (30, 18)
                    text_size 34
                    text_color "#ffffff"
                    text_bold True
                    action Return(game.result())

        key "K_RETURN" action Return(game.result())
        key "K_SPACE" action Return(game.result())


screen lwq_rhythm_pause_screen(game):
    tag lwq_rhythm_pause
    modal True
    zorder 250

    add Solid("#020617cc")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 720
        background Solid("#03111cf5")
        padding (54, 42)

        vbox:
            xalign 0.5
            spacing 24

            text "PAUSED":
                xalign 0.5
                size 55
                color "#86efac"
                bold True

            textbutton "RESUME":
                xalign 0.5
                xminimum 420
                yminimum 76
                background Solid("#047857e8")
                hover_background Solid("#059669")
                text_size 29
                text_color "#d1fae5"
                text_bold True
                action [Function(game.resume), Hide("lwq_rhythm_pause_screen")]

            textbutton "RESTART SONG":
                xalign 0.5
                xminimum 420
                yminimum 70
                background Solid("#0e7490e8")
                hover_background Solid("#0891b2")
                text_size 26
                text_color "#cffafe"
                action [Function(game.stop), Hide("lwq_rhythm_pause_screen"), Return("restart")]

            textbutton "MAIN MENU":
                xalign 0.5
                xminimum 420
                yminimum 70
                background Solid("#3f1d2de8")
                hover_background Solid("#881337")
                text_size 25
                text_color "#fecdd3"
                # No confirmation here: stopping first and then cancelling a
                # confirmation would leave the paused battle without audio.
                action [Function(game.stop), MainMenu(confirm=False)]

    key "K_ESCAPE" action [Function(game.resume), Hide("lwq_rhythm_pause_screen")]


screen lwq_rhythm_result_screen(result):
    tag lwq_rhythm
    modal True
    zorder 100

    if result["status"] == "victory":
        add "lwq victory background"
        $ result_title = "CARBON MONSTER DEFEATED"
        $ result_color = "#86efac"
    else:
        add "lwq defeat background"
        $ result_title = "RHYTHM POWER INSUFFICIENT"
        $ result_color = "#fda4af"

    add Solid("#02061766")

    frame:
        xpos 850
        yalign 0.5
        xsize 1020
        background Solid("#03111cf2")
        padding (48, 36)

        vbox:
            xalign 0.5
            spacing 16

            text result_title:
                xalign 0.5
                size 52
                color result_color
                bold True
                text_align 0.5

            text "SCORE  {:,} / {:,}".format(result["score"], result["pass_score"]):
                xalign 0.5
                size 42
                color "#facc15"
                bold True

            text "Accuracy {:.1f}%    |    Max Combo x{}".format(result["accuracy"], result["max_combo"]):
                xalign 0.5
                size 31
                color "#e2e8f0"

            text "Perfect {}    Great {}    Good {}    Miss {}".format(
                result["perfect"], result["great"], result["good"], result["miss"]
            ):
                xalign 0.5
                size 29
                color "#cbd5e1"

            if result["status"] == "victory":
                text "พลังจังหวะฟื้นฟูสวนลุมพินีสำเร็จแล้ว":
                    xalign 0.5
                    size 31
                    color "#d1fae5"
                    text_align 0.5

                if result.get("reward") and result["reward"].get("new_reward"):
                    text "ได้รับ SDG 3 Badge\nMeow Coin +{:,} • Eco Score +{:,}".format(result["reward"].get("coins_awarded", 0), result["reward"].get("eco_score_awarded", 0)):
                        xalign 0.5
                        size 30
                        color "#fcd34d"
                        bold True
                        text_align 0.5
                else:
                    text "รางวัล SDG 3 ของด่านนี้ถูกรับไว้แล้ว":
                        xalign 0.5
                        size 28
                        color "#cbd5e1"
                        text_align 0.5

                textbutton "สรุปภารกิจการเรียนรู้":
                    xalign 0.5
                    xminimum 540
                    yminimum 82
                    background Solid("#047857ed")
                    hover_background Solid("#059669")
                    padding (28, 16)
                    text_size 32
                    text_color "#d1fae5"
                    text_hover_color "#ffffff"
                    text_bold True
                    action Return("continue")

                textbutton "PLAY RHYTHM AGAIN":
                    xalign 0.5
                    xminimum 420
                    yminimum 62
                    background Solid("#0e7490e8")
                    hover_background Solid("#0891b2")
                    text_size 26
                    text_color "#cffafe"
                    action Return("retry")
            else:
                text "ต้องทำคะแนนให้ถึงเกณฑ์และลด HP ของอสูรให้เหลือ 0":
                    xalign 0.5
                    size 30
                    color "#fecdd3"
                    text_align 0.5

                text "Carbon Monster HP คงเหลือ {:,}".format(result["monster_hp"]):
                    xalign 0.5
                    size 30
                    color "#fb7185"

                textbutton "RETRY BATTLE":
                    xalign 0.5
                    xminimum 500
                    yminimum 82
                    background Solid("#b91c1ce8")
                    hover_background Solid("#dc2626")
                    padding (28, 16)
                    text_size 33
                    text_color "#fee2e2"
                    text_hover_color "#ffffff"
                    text_bold True
                    action Return("retry")

                text "ยังไม่ได้รับ SDG 3 Badge, Meow Coin หรือ Eco Score รางวัลด่าน":
                    xalign 0.5
                    size 27
                    color "#cbd5e1"
                    text_align 0.5

                textbutton "สรุปภารกิจการเรียนรู้":
                    xalign 0.5
                    xminimum 500
                    yminimum 72
                    background Solid("#0e7490e8")
                    hover_background Solid("#0891b2")
                    padding (24, 14)
                    text_size 28
                    text_color "#cffafe"
                    text_hover_color "#ffffff"
                    text_bold True
                    action Return("continue")

            textbutton "MAIN MENU":
                xalign 0.5
                xminimum 330
                yminimum 60
                background Solid("#1e293be8")
                hover_background Solid("#334155")
                text_size 25
                text_color "#e2e8f0"
                action MainMenu(confirm=True)


screen lumpini_minigame_tutorial_1():
    tag lumpini_minigame_tutorial_1
    modal True
    add "lumpini_minigame_tutorial_asset_1"
    button:
        xfill True
        yfill True
        background None
        hover_background None
        action Return()
    key "K_RETURN" action Return()
    key "K_SPACE" action Return()
    key "K_RIGHT" action Return()

screen lumpini_minigame_tutorial_2():
    tag lumpini_minigame_tutorial_2
    modal True
    add "lumpini_minigame_tutorial_asset_2"
    button:
        xfill True
        yfill True
        background None
        hover_background None
        action Return()
    key "K_RETURN" action Return()
    key "K_SPACE" action Return()
    key "K_RIGHT" action Return()

screen lumpini_minigame_tutorial_3():
    tag lumpini_minigame_tutorial_3
    modal True
    add "lumpini_minigame_tutorial_asset_3"
    button:
        xfill True
        yfill True
        background None
        hover_background None
        action Return()
    key "K_RETURN" action Return()
    key "K_SPACE" action Return()
    key "K_RIGHT" action Return()

label lumpini_minigame_tutorial:
    call screen lumpini_minigame_tutorial_1
    call screen lumpini_minigame_tutorial_2
    call screen lumpini_minigame_tutorial_3
    return


label lwq_intro_story:
    scene lumpini_story_01
    LUMI "ฉันรอเธออยู่ที่สวนลุมพินี ตอนนี้ถึงเวลา....เริ่มภารกิจใหม่"

    scene lumpini_story_02
    LUMI "ยินดีต้อนรับสู่ Lumpini Wellness Quest!"

    scene lumpini_story_03
    LUMI "สุขภาพที่ดี ไม่ได้เริ่มจากโรงพยาบาล... ...แต่เริ่มจากการขยับร่างกายทุกวัน"

    scene lumpini_story_04
    LUMI "เมื่อเราไม่ขยับร่างกาย... พลังของเมืองก็ลดลง"

    scene lumpini_story_05
    LUMI "เมื่อคนแข็งแรง เมืองก็แข็งแรง!"

    scene lumpini_story_06
    LUMI "ใส่ Smart Wristband นี้ไว้เลย! มาช่วยกันปลูกพลังสุขภาพของเมืองกันเถอะ!"

    scene lumpini_story_07
    LUMI "ตรวจพบพื้นที่ที่ต้องการการฟื้นฟูสุขภาพ! ภารกิจนี้เกี่ยวกับ “สุขภาพของเมือง”"

    scene lumpini_story_08
    LUMI "เกิดบางอย่างขึ้นที่สวนลุมพินี..."

    scene lumpini_story_09
    LUMI "ธรรมชาติยังแข็งแรง... แต่ผู้คนกำลังสูญเสียพลัง"

    scene lumpini_story_10
    LUMI "ไม่ใช่แค่คนเหนื่อย... มีบางอย่างกำลังดูดพลังของเมือง"

    scene lumpini_story_11
    LUMI "อสูรคาร์บอน..."

    scene lumpini_story_12
    LUMI "อสูรนี้ไม่ได้โจมตีด้วยกำลัง แต่ดูด “แรงจูงใจในการดูแลสุขภาพ”"

    scene lumpini_story_13
    LUMI "ภารกิจของเรา... คือคืนพลังให้สวนแห่งนี้กลับมามีชีวิตอีกครั้ง!"

    scene lumpini_story_14
    LUMI "เสียงเพลง... สามารถปลุกพลังของผู้คนได้!"

    scene lumpini_story_15
    LUMI "ทุกคน... เริ่มกลับมาแล้ว!"

    scene lumpini_story_16
    LUMI "ใช้จังหวะ! ใช้พลัง! เพื่อเอาชนะอสูรคาร์บอนแห่งความอ่อนล้า!"

    scene lumpini_story_17
    LUMI "ทุกจังหวะที่ถูกต้อง... จะกลายเป็นพลังของเมือง!"

    scene lumpini_story_18
    LUMI "สวนลุมพินีพร้อมแล้ว! มาสร้างพลังไปด้วยกัน!"

    return


label lwq_post_minigame_story:
    # This epilogue starts only after the player finishes the song and presses
    # the in-game summary button. Keeping it in its own call prevents a retry
    # selection on the result UI from entering scenes 20-22 by itself.
    scene lumpini_story_19
    LUMI "ภารกิจนี้สอดคล้องกับ SDG 3 สุขภาพและความเป็นอยู่ที่ดี"

    scene lumpini_story_20
    pause

    scene lumpini_story_21
    pause

    return


label lumpini_start:
    $ save_name = "Lumpini Wellness Quest"
    window hide
    $ lwq_play_stage_bgm()
    call lwq_intro_story

    # One idempotent ethical-product decision sets this stage's starting HP.
    call sustainability_decision("lumpini")
    call lumpini_minigame_tutorial

    $ lwq_battle_active = True

    while lwq_battle_active:
        # Story, tutorial and the briefing use the stage BGM. This is also the
        # retry path after the result screen, so the briefing regains its music.
        $ lwq_play_stage_bgm()
        $ lwq_stage_start_hp = max(1, int(mk_get_stage_start_hp("lumpini")))
        $ mk_reset_stage_battle("lumpini")
        $ lwq_song_available = renpy.loadable(LWQ_SONG_FILE)
        call screen lwq_rhythm_briefing_screen(lwq_song_available, lwq_stage_start_hp)

        if _return != "start":
            $ lwq_stop_stage_bgm()
            return

        # The rhythm battle has exclusive audio focus. This runs on every
        # start/retry and leaves only Lumpini_Song on its dedicated channel.
        $ lwq_stop_background_audio()
        $ lwq_game = LWQRhythmCombat(lwq_stage_start_hp)
        $ renpy.block_rollback()
        call screen lwq_rhythm_game_screen(lwq_game)
        $ lwq_battle_result = _return
        $ lwq_game.stop()
        $ del lwq_game

        if lwq_battle_result == "restart":
            $ renpy.pause(0.15, hard=True)
        else:
            $ mk_set_stage_current_hp("lumpini", lwq_battle_result["monster_hp"])
            if lwq_battle_result["status"] == "victory":
                $ lwq_battle_result["reward"] = mk_grant_stage_rewards("lumpini")
            else:
                $ lwq_battle_result["reward"] = None

            # Restore the stage loop after rhythm combat and show the existing
            # win/loss result first. Scenes 20-22 remain behind the explicit
            # learning-summary action, so a retry never enters the epilogue.
            $ lwq_play_stage_bgm()
            $ lwq_result_active = True

            while lwq_result_active:
                call screen lwq_rhythm_result_screen(lwq_battle_result)

                if _return == "retry":
                    $ lwq_result_active = False
                elif _return == "continue":
                    # Keep the Lumpini stage BGM across the result and authored
                    # epilogue, then release it before either learning video.
                    call lwq_post_minigame_story
                    $ lwq_stop_stage_bgm()
                    call stage_learning_flow("lumpini", "mk_lobby_start")
                    jump mk_lobby_start

    $ renpy.block_rollback()
    $ renpy.checkpoint()
    $ lwq_stop_stage_bgm()
    return
