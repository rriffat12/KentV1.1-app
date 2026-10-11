Pfrom kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Line, Ellipse, Rectangle
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.switch import Switch
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
import platform

# Deteksi platform Android
platform_str = platform.platform().lower()
is_android = "android" in platform_str

# Impor PyJNIus khusus jika berjalan di Android
if is_android:
    try:
        from jnius import autoclass
        from jnius import cast
        # Shizuku Binder & UserService API Classes
        Shizuku = autoclass('moe.shizuku.api.Shizuku')
        PackageManager = autoclass('android.content.pm.PackageManager')
    except Exception:
        is_android = False

PURPLE = (0.65, 0.25, 1.0, 1)
DARK = (0.055, 0.035, 0.085, 1)
PANEL = (0.12, 0.08, 0.17, 1)
WHITE = (0.95, 0.92, 1.0, 1)
MUTED = (0.72, 0.65, 0.80, 1)
ACCENT_GREEN = (0.2, 0.9, 0.4, 1)

Window.clearcolor = DARK


def make_label(text, size=15, color=WHITE, height=dp(35)):
    return Label(
        text=text,
        font_size=sp(size),
        color=color,
        size_hint_y=None,
        height=height,
        halign="left",
        valign="middle",
    )


class CrosshairPreview(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.enabled = True
        self.style = "ROG"
        self.tracking_active = False
        self.hs_active = False
        self.bind(pos=self.redraw, size=self.redraw)

    def set_options(self, enabled=None, style=None, tracking=None, hs=None):
        if enabled is not None:
            self.enabled = enabled
        if style is not None:
            self.style = style
        if tracking is not None:
            self.tracking_active = tracking
        if hs is not None:
            self.hs_active = hs
        self.redraw()

    def redraw(self, *_):
        self.canvas.clear()
        with self.canvas:
            Color(*PANEL)
            Rectangle(pos=self.pos, size=self.size)

            Color(0.35, 0.16, 0.48, 1)
            Line(
                rectangle=(
                    self.x + dp(1),
                    self.y + dp(1),
                    max(0, self.width - dp(2)),
                    max(0, self.height - dp(2)),
                ),
                width=1,
            )

            if not self.enabled:
                return

            cx = self.center_x
            cy = self.center_y
            radius = dp(15)

            if self.tracking_active or self.hs_active:
                Color(*ACCENT_GREEN)
            else:
                Color(*PURPLE)

            if self.style == "ROG":
                gap = dp(7)
                corner = dp(10)
                segments = [
                    (cx-gap-corner, cy+gap+corner, cx-gap, cy+gap+corner),
                    (cx-gap-corner, cy+gap+corner, cx-gap-corner, cy+gap),
                    (cx+gap, cy+gap+corner, cx+gap+corner, cy+gap+corner),
                    (cx+gap+corner, cy+gap+corner, cx+gap+corner, cy+gap),
                    (cx-gap-corner, cy-gap, cx-gap-corner, cy-gap-corner),
                    (cx-gap-corner, cy-gap-corner, cx-gap, cy-gap-corner),
                    (cx+gap, cy-gap-corner, cx+gap+corner, cy-gap-corner),
                    (cx+gap+corner, cy-gap-corner, cx+gap+corner, cy+gap),
                ]
                for x1, y1, x2, y2 in segments:
                    Line(points=[x1, y1, x2, y2], width=1.5)

                Color(*WHITE)
                Line(points=[cx, cy+dp(2), cx, cy+dp(5)])
                Line(points=[cx, cy-dp(2), cx, cy-dp(5)])
                Line(points=[cx-dp(5), cy, cx-dp(2), cy])
                Line(points=[cx+dp(2), cy, cx+dp(5), cy])

            elif self.style == "Dot":
                Ellipse(pos=(cx-dp(3), cy-dp(3)), size=(dp(6), dp(6)))

            elif self.style == "Plus":
                Line(points=[cx, cy-radius, cx, cy+radius], width=1.5)
                Line(points=[cx-radius, cy, cx+radius, cy], width=1.5)

            elif self.style == "Circle":
                Line(circle=(cx, cy, radius), width=1.5)
                Color(*WHITE)
                Ellipse(pos=(cx-dp(2), cy-dp(2)), size=(dp(4), dp(4)))


class KenttV1App(App):
    title = "kenttV1"

    def build(self):
        self.edition = "Free Fire"
        self.crosshair_on = True
        self.tracking_on = False
        self.hs_on = False
        self.shizuku_connected = False

        root = BoxLayout(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(8),
        )

        with root.canvas.before:
            Color(*DARK)
            self.background = Rectangle(pos=root.pos, size=root.size)

        root.bind(
            pos=lambda obj, value: setattr(self.background, "pos", value),
            size=lambda obj, value: setattr(self.background, "size", value),
        )

        # Header
        header = BoxLayout(orientation="vertical", size_hint_y=None, height=dp(74), spacing=dp(2))
        header.add_widget(Label(text="[b]kenttV1[/b]", markup=True, font_size=sp(28), color=PURPLE))
        header.add_widget(Label(text="GAMING SETTINGS + SHIZUKU BRIDGE", font_size=sp(10), color=MUTED))
        root.add_widget(header)

        # Game profile
        self.edition_label = make_label("GAME PROFILE | Free Fire", 13, WHITE, dp(32))
        root.add_widget(self.edition_label)

        self.add_action(root, "PILIH FREE FIRE / MAX", self.choose_edition)
        
        # Shizuku Connection Button
        self.shizuku_btn = Button(
            text="HUBUNGKAN KE SHIZUKU",
            size_hint_y=None,
            height=dp(40),
            background_normal="",
            background_color=(0.15, 0.5, 0.2, 1),
            color=WHITE,
            font_size=sp(12),
        )
        self.shizuku_btn.bind(on_release=self.init_shizuku_connection)
        root.add_widget(self.shizuku_btn)

        # Crosshair preview
        root.add_widget(make_label("CROSSHAIR PREVIEW", 12, PURPLE, dp(24)))
        self.preview = CrosshairPreview(size_hint_y=None, height=dp(120))
        root.add_widget(self.preview)

        # Switches
        self.add_switch_row(root, "Crosshair Overlay", True, self.toggle_crosshair)
        self.add_switch_row(root, "Aim Tracking (Shizuku)", False, self.toggle_tracking)
        self.add_switch_row(root, "Auto Headshot Swipe", False, self.toggle_hs)

        # Spinner Style
        self.style_spinner = Spinner(
            text="ROG",
            values=("ROG", "Dot", "Plus", "Circle"),
            size_hint_y=None,
            height=dp(40),
            background_normal="",
            background_color=PURPLE,
            color=WHITE,
        )
        self.style_spinner.bind(text=self.change_style)
        root.add_spinner = self.style_spinner
        root.add_widget(self.style_spinner)

        self.status = make_label("Status: Menunggu Shizuku...", 11, MUTED, dp(30))
        root.add_widget(self.status)

        root.add_widget(Widget())
        root.add_widget(Label(text="STANDALONE APP | Shizuku Enabled", size_hint_y=None, height=dp(20), font_size=sp(9), color=MUTED))

        return root

    def add_action(self, parent, title, callback):
        button = Button(
            text=title,
            size_hint_y=None,
            height=dp(40),
            background_normal="",
            background_color=PURPLE,
            color=WHITE,
            font_size=sp(12),
        )
        button.bind(on_release=callback)
        parent.add_widget(button)

    def add_switch_row(self, parent, title, default, callback):
        row = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(8))
        row.add_widget(Label(text=title, color=WHITE, font_size=sp(12), halign="left", valign="middle"))
        switch = Switch(active=default, size_hint_x=None, width=dp(60))
        switch.bind(active=callback)
        row.add_widget(switch)
        parent.add_widget(row)

    def init_shizuku_connection(self, *_):
        """Memeriksa dan meminta izin Shizuku langsung melalui Binder API Android"""
        if not is_android:
            # Simulasi jika diuji coba di komputer/PC
            self.shizuku_connected = True
            self.shizuku_btn.background_color = (0.2, 0.8, 0.3, 1)
            self.shizuku_btn.text = "SHIZUKU TERHUBUNG (SIMULASI) ✅"
            self.status.text = "Mode Simulasi: Shizuku aktif."
            return

        try:
            # Cek apakah binder Shizuku aktif di sistem HP
            if Shizuku.pingBinder():
                # Cek versi izin Shizuku
                if Shizuku.getVersion() >= 10:
                    # Cek status izin aplikasi
                    if Shizuku.checkSelfPermission() == 0:  # 0 artinya PERMISSION_GRANTED
                        self.shizuku_connected = True
                        self.shizuku_btn.background_color = (0.2, 0.8, 0.3, 1)
                        self.shizuku_btn.text = "SHIZUKU TERHUBUNG ✅"
                        self.status.text = "Shizuku aktif: Izin diberikan."
                    else:
                        # Minta izin Shizuku secara otomatis via popup sistem Shizuku
                        Shizuku.requestPermission(0)
                        self.status.text = "Meminta izin Shizuku, cek jendela pop-up..."
                else:
                    self.status.text = "Versi Shizuku terlalu rendah!"
            else:
                self.status.text = "Shizuku tidak aktif! Nyalakan Shizuku dulu."
        except Exception as e:
            self.shizuku_connected = False
            self.status.text = f"Error Shizuku: {str(e)}"

    def execute_shizuku_swipe(self, x1, y1, x2, y2, duration_ms):
        """Menjalankan perintah input geser layar via Shizuku UserService / Process"""
        if not self.shizuku_connected:
            self.status.text = "Error: Hubungkan Shizuku terlebih dahulu!"
            return

        try:
            cmd = f"input swipe {x1} {y1} {x2} {y2} {duration_ms}"
            
            if is_android:
                # Menjalankan proses shell root/adb melalui Shizuku NewProcess
                # Shizuku.newProcess(cmd_array, env_array, dir_string)
                Shizuku.newProcess(["sh", "-c", cmd], None, None)
            
            self.status.text = f"Action Headshot Drag: {x1},{y1} -> {x2},{y2}"
        except Exception as e:
            self.status.text = f"Gagal eksekusi swipe: {str(e)}"

    def choose_edition(self, *_):
        content = BoxLayout(orientation="vertical", padding=dp(14), spacing=dp(10))
        content.add_widget(Label(text="Pilih profil game", color=WHITE, font_size=sp(16)))
        popup = Popup(title="kenttV1", content=content, size_hint=(0.86, 0.35))

        for edition in ("Free Fire", "Free Fire MAX"):
            button = Button(
                text=edition,
                size_hint_y=None,
                height=dp(40),
                background_normal="",
                background_color=PURPLE,
                color=WHITE,
            )
            button.bind(on_release=lambda instance, val=edition: self.set_edition(val, popup))
            content.add_widget(button)
        popup.open()

    def set_edition(self, edition, popup):
        self.edition = edition
        self.edition_label.text = f"GAME PROFILE | {edition}"
        self.status.text = f"Profil aktif: {edition}"
        popup.dismiss()

    def toggle_crosshair(self, switch, active):
        self.crosshair_on = active
        self.preview.set_options(enabled=active)
        self.status.text = "Crosshair ON" if active else "Crosshair OFF"

    def toggle_tracking(self, switch, active):
        self.tracking_on = active
        self.preview.set_options(tracking=active)
        if active and self.shizuku_connected:
            self.status.text = "Aim Tracking via Shizuku AKTIF"
        else:
            self.status.text = "Aim Tracking dimatikan / Shizuku belum siap"

    def toggle_hs(self, switch, active):
        self.hs_on = active
        self.preview.set_options(hs=active)
        if active:
            self.execute_shizuku_swipe(500, 1500, 500, 1100, 100)
            self.status.text = "Auto Headshot Swipe Dieksekusi 🔥"
        else:
            self.status.text = "Auto Headshot dimatikan"

    def change_style(self, spinner, value):
        self.preview.set_options(style=value)
        self.status.text = f"Crosshair Style: {value}"


if __name__ == "__main__":
    KenttV1App().run()