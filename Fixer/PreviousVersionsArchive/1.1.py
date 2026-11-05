import os
import base64
import threading
import webbrowser
import urllib.parse
import requests
import io
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import customtkinter as ctk
from PIL import Image

FROG_PNG_B64 = "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"

DISCORD_PNG_B64 = "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"


def embedded_image(b64):
    return Image.open(io.BytesIO(base64.b64decode(b64)))

APP_VERSION = "v1.1"
APP_DATE = "8/22/2026"

CLIENT_ID = "1ba9b4bfa1ac7759e8420eed4ec863ba"
PORT = 7890
LOCAL_LOW = os.path.join(os.environ['USERPROFILE'], 'AppData', 'LocalLow')
TARGET_DIR = os.path.join(LOCAL_LOW, 'Innersloth', 'Among Us')
TARGET_FILE = os.path.join(TARGET_DIR, 'itch')
ASSET_DIR = os.path.dirname(os.path.abspath(__file__))

ACCOUNT_MANAGEMENT_URL = "https://accounts.innersloth.com/account-management"
EOS_AUTH_URL = "https://accounts.innersloth.com/eos-auth"
BACKEND_API = "https://backend.innersloth.com/api"

BACKEND_HEADERS = {
    "Accept": "application/vnd.api+json",
    "Origin": "https://accounts.innersloth.com",
    "Referer": "https://accounts.innersloth.com/",
}

STORES = ["steam", "epic", "microsoft", "itchio"]

PLATFORM_LABELS = {
    'itchio': 'itch.io', 'itch': 'itch.io',
    'steam': 'Steam',
    'epic': 'Epic Games', 'epicgames': 'Epic Games',
    'xbox': 'Xbox', 'xboxlive': 'Xbox', 'xbl': 'Xbox',
    'playstation': 'PlayStation', 'psn': 'PlayStation',
    'microsoft': 'Microsoft Store', 'winstore': 'Microsoft Store',
    'nintendo': 'Nintendo', 'switch': 'Nintendo Switch',
    'ios': 'iOS', 'android': 'Android',
    'google': 'Google Play', 'googleplay': 'Google Play',
}


def platform_label(p):
    return PLATFORM_LABELS.get(str(p).lower(), str(p)) if p else "?"


def eos_auth(store, token):
    r = requests.get(EOS_AUTH_URL, params={"store": store, "token": token},
                     headers={"Accept": "application/json"}, timeout=20)
    if r.status_code != 200:
        raise RuntimeError(f"auth failed ({r.status_code}): {r.text[:150]}")
    data = r.json()
    if not data.get("token") or not data.get("id_token"):
        raise RuntimeError("auth returned no tokens")
    return data


def query_primary(eos):
    r = requests.get(f"{BACKEND_API}/user/query-primary-before-merge",
                     params={"access_token": eos["token"]},
                     headers={"Authorization": "Bearer " + eos["id_token"], **BACKEND_HEADERS},
                     timeout=20)
    if r.status_code != 200:
        raise RuntimeError(f"account query failed ({r.status_code})")
    return r.json().get("data", {})


def query_secondary(eos, primary_puid):
    r = requests.get(f"{BACKEND_API}/user/query-secondary-before-merge",
                     params={"access_token": eos["token"], "primary_puid": primary_puid},
                     headers={"Authorization": "Bearer " + eos["id_token"], **BACKEND_HEADERS},
                     timeout=20)
    if r.status_code != 200:
        raise RuntimeError(f"secondary query failed ({r.status_code})")
    return r.json().get("data", {})


def fetch_username(eos):
    try:
        r = requests.get(f"{BACKEND_API}/user/username",
                         headers={"Authorization": "Bearer " + eos["id_token"], **BACKEND_HEADERS},
                         timeout=15)
        if r.status_code == 200:
            attrs = r.json().get("data", {}).get("attributes", {})
            name, disc = attrs.get("username"), attrs.get("discriminator")
            if name:
                return f"{name}#{disc}" if disc else name
    except Exception:
        pass
    return None


def do_merge(primary_eos, secondary_eos, secondary_store, secondary_platform_token):
    body = {"data": {"attributes": {
        "merge_to_id_token": primary_eos["id_token"],
        "merge_from_id_token": secondary_eos["id_token"],
        "merge_to_access_token": primary_eos["token"],
        "merge_from_access_token": secondary_eos["token"],
        "merge_from_platform_token": secondary_platform_token,
        "merge_from_platform": secondary_store,
    }}}
    headers = {"Accept": "application/vnd.api+json", "Content-Type": "application/json",
               "Origin": "https://accounts.innersloth.com", "Referer": "https://accounts.innersloth.com/"}
    r = requests.post(f"{BACKEND_API}/merge-account", json=body, headers=headers, timeout=30)
    if r.status_code != 200:
        raise RuntimeError(f"merge failed ({r.status_code}): {r.text[:200]}")
    return r.json()


def parse_credentials(text):
    text = (text or "").strip().strip('"').strip("'")
    store, token = None, None
    if not text:
        raise ValueError("Paste your account link or token first.")
    if "access_token=" in text:
        token = text.split("access_token=")[1].split("&")[0].split("#")[0]
        if "store=" in text:
            store = text.split("store=")[1].split("&")[0].split("#")[0]
    elif "token=" in text:
        token = text.split("token=")[1].split("&")[0].split("#")[0]
        if "store=" in text:
            store = text.split("store=")[1].split("&")[0].split("#")[0]
    elif len(text.split()) == 1 and len(text) > 20:
        token = text
    else:
        raise ValueError("Couldn't find a token in what you pasted.")
    if not token:
        raise ValueError("Couldn't find a token in what you pasted.")
    if store not in STORES:
        store = None
    return store, token


def detect_store_for_token(token):
    last_err = None
    for store in ["steam", "epic", "microsoft"]:
        try:
            eos_auth(store, token)
            return store
        except Exception as e:
            last_err = e
    raise RuntimeError("That token didn't work with Steam, Epic or Microsoft.")


LOADING_PAGE = b"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ShadowSlime | Authenticating</title>
    <style>
        body { background: #060608; color: #7b61ff; display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh; font-family: 'Segoe UI', sans-serif; margin: 0; }
        .loader { border: 4px solid #1a1b1e; border-top: 4px solid #7b61ff; border-radius: 50%; width: 50px; height: 50px; animation: spin 1s linear infinite; margin-bottom: 20px; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .text { font-weight: bold; letter-spacing: 1px; }
    </style>
</head>
<body>
    <div class="loader"></div>
    <div class="text">CONNECTING TO ITCH.IO...</div>
    <script>
        const params = new URLSearchParams(window.location.hash.slice(1));
        const token = params.get('access_token');
        if (token) window.location = '/token?t=' + token;
    </script>
</body>
</html>"""

SUCCESS_PAGE = b"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ShadowSlime | Success</title>
    <style>
        body { background: #060608; color: #4ade80; display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh; font-family: 'Segoe UI', sans-serif; margin: 0; }
        .icon { font-size: 60px; margin-bottom: 10px; }
        .msg { font-size: 24px; font-weight: bold; }
        .sub { color: #888; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="icon">&#10004;</div>
    <div class="msg">AUTHORIZATION COMPLETE</div>
    <div class="sub">You can close this tab and return to the fixer.</div>
</body>
</html>"""


class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/token"):
            params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            self.server.token = params.get("t", [None])[0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(SUCCESS_PAGE)
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(LOADING_PAGE)

    def log_message(self, format, *args):
        pass


class ItchFixerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Itch Login Fixer")
        self.geometry("520x640")
        self.minsize(520, 560)
        ctk.set_appearance_mode("dark")

        self.purple = "#7b61ff"
        self.purple_dark = "#5a44cc"
        self.green = "#4ade80"
        self.red = "#ff4b4b"
        self.muted = "#888888"

        self.token = None
        self.eos = None
        self.busy = False
        self._pfp_img = None
        self._discord_img = None

        self.container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        self.build_header()
        self.build_profile()
        self.build_merge_section()
        self.build_footer()

        self.check_existing_login()

    def build_header(self):
        top = ctk.CTkFrame(self.container, fg_color="transparent")
        top.pack(fill="x", pady=(4, 0))
        ctk.CTkLabel(top, text="SHADOWSLIME AUTH", font=("JetBrains Mono", 10),
                     text_color=self.purple).pack(side="left", padx=15)
        ctk.CTkLabel(top, text=f"{APP_VERSION} | {APP_DATE}", font=("JetBrains Mono", 9),
                     text_color="#444444").pack(side="right", padx=15)

    def build_profile(self):
        self.pfp_label = ctk.CTkLabel(self.container, text="", width=120, height=120)
        self.pfp_label.pack(pady=(12, 6))

        self.status_label = ctk.CTkLabel(self.container, text="Not Logged In",
                                         font=("Arial", 22, "bold"))
        self.status_label.pack(pady=(2, 2))

        self.au_label = ctk.CTkLabel(self.container, text="", font=("Consolas", 13),
                                     text_color="#61a8ff")
        self.au_label.pack()

        self.action_text = ctk.CTkLabel(self.container, text="Click login to fix the ownership error",
                                        font=("Arial", 12), text_color=self.muted,
                                        wraplength=460, justify="center")
        self.action_text.pack(pady=(6, 2))

        self.merged_label = ctk.CTkLabel(self.container, text="", font=("Arial", 12),
                                         text_color="#59d499", wraplength=460, justify="center")
        self.merged_label.pack(pady=(2, 0))

        self.login_button = ctk.CTkButton(self.container, text="Login with itch.io",
                                          command=self.start_login_thread,
                                          fg_color=self.purple, hover_color=self.purple_dark,
                                          font=("Arial", 14, "bold"), height=40)
        self.login_button.pack(pady=(14, 4), padx=60, fill="x")

    def build_merge_section(self):
        self.merge_section = ctk.CTkFrame(self.container, fg_color="transparent")

        divider = ctk.CTkFrame(self.merge_section, height=2, fg_color="#333333")
        divider.pack(fill="x", padx=40, pady=(16, 8))

        title_row = ctk.CTkFrame(self.merge_section, fg_color="transparent")
        title_row.pack(fill="x")
        ctk.CTkLabel(title_row, text="MERGE YOUR ACCOUNT AS", font=("JetBrains Mono", 11, "bold"),
                     text_color="#bbbbbb").pack(side="left", padx=50)
        ctk.CTkButton(title_row, text="?", width=24, height=24, corner_radius=12,
                      command=self.show_help_popup, fg_color="#33334a",
                      hover_color=self.purple_dark, font=("Arial", 12, "bold")).pack(side="right", padx=50)

        btn_row = ctk.CTkFrame(self.merge_section, fg_color="transparent")
        btn_row.pack(fill="x", pady=(8, 2))
        self.primary_btn = ctk.CTkButton(btn_row, text="Primary", command=self.merge_as_primary,
                                         fg_color=self.purple, hover_color=self.purple_dark,
                                         font=("Arial", 13, "bold"), height=36)
        self.primary_btn.pack(side="left", padx=(60, 5), expand=True, fill="x")
        self.secondary_btn = ctk.CTkButton(btn_row, text="Secondary", command=self.merge_as_secondary,
                                           fg_color=self.green, hover_color="#2f9c66",
                                           font=("Arial", 13, "bold"), height=36)
        self.secondary_btn.pack(side="left", padx=(5, 60), expand=True, fill="x")

        self.merge_hint = ctk.CTkLabel(self.merge_section, text="", font=("Arial", 11),
                                       text_color="#666666", wraplength=440, justify="center")
        self.merge_hint.pack(pady=(2, 0))

        self.merge_section.pack_forget()

    def build_footer(self):
        self.warning_label = ctk.CTkLabel(self.container,
                                          text="This is a temporary fix, don't expect it to always work.",
                                          font=("Arial", 11, "italic"), text_color="#555555")
        self.warning_label.pack(pady=(14, 4))

        socials = ctk.CTkFrame(self.container, fg_color="transparent")
        socials.pack(pady=(2, 16))
        try:
            img = embedded_image(DISCORD_PNG_B64)
            self._discord_img = ctk.CTkImage(light_image=img, dark_image=img, size=(26, 26))
        except Exception:
            self._discord_img = None
        ctk.CTkButton(socials, text=" Discord", width=110, height=36, image=self._discord_img,
                      command=lambda: webbrowser.open("https://discord.gg/7Vvj2vpT6S"),
                      fg_color="#5865F2", hover_color="#4753c9").pack(side="left", padx=8)

    def set_merge_visible(self, visible):
        if visible:
            self.merge_section.pack(before=self.warning_label, fill="x")
        else:
            self.merge_section.pack_forget()

    def set_busy(self, busy):
        self.busy = busy
        state = "disabled" if busy else "normal"

        def apply():
            self.primary_btn.configure(state=state)
            self.secondary_btn.configure(state=state)
            self.login_button.configure(state=state)
        self.after(0, apply)

    # ---------- login ----------
    def check_existing_login(self):
        if os.path.exists(TARGET_FILE):
            try:
                with open(TARGET_FILE, "r") as f:
                    saved = f.read().strip()
                if saved:
                    self.token = saved
                    threading.Thread(target=self.load_account, args=(saved,), daemon=True).start()
            except Exception:
                pass

    def start_login_thread(self):
        if self.busy:
            return
        self.login_button.configure(state="disabled", text="Check Browser...")
        threading.Thread(target=self.run_server, daemon=True).start()
        webbrowser.open(f"https://itch.io/user/oauth?client_id={CLIENT_ID}&scope=profile:me"
                        f"&redirect_uri=http://127.0.0.1:{PORT}&response_type=token")

    def run_server(self):
        server = HTTPServer(("127.0.0.1", PORT), OAuthHandler)
        server.token = None
        server.timeout = 1
        deadline = time.time() + 300
        while server.token is None and time.time() < deadline:
            server.handle_request()
        if server.token:
            self.token = server.token
            os.makedirs(TARGET_DIR, exist_ok=True)
            with open(TARGET_FILE, "w") as f:
                f.write(server.token)
            self.after(0, lambda: self.load_account(server.token))
        else:
            self.after(0, lambda: self.login_button.configure(state="normal", text="Login with itch.io"))

    # ---------- account loading ----------
    def load_account(self, token):
        self.set_busy(True)
        self.after(0, lambda: self.status_label.configure(text="Loading...", text_color="#bbbbbb"))

        username, pfp_url = None, None
        try:
            r = requests.get("https://itch.io/api/1/key/me", headers={"Authorization": token}, timeout=15)
            if r.status_code == 200:
                u = r.json().get("user", {})
                username = u.get("username")
                pfp_url = u.get("cover_url")
        except Exception:
            pass

        def apply_profile():
            self.status_label.configure(
                text=f"Logged in as {username}" if username else "Logged in",
                text_color=self.green)
            self.action_text.configure(
                text="Login fixed! You can launch Among Us now. (you can also close this app)",
                text_color=self.green)
            self.login_button.configure(text="Refresh Session", state="normal")
            self.primary_btn.configure(state="normal")
            self.secondary_btn.configure(state="normal")
            self.set_merge_visible(True)
        self.after(0, apply_profile)
        self.set_avatar(pfp_url)

        try:
            self.eos = eos_auth("itchio", token)
            primary = query_primary(self.eos)
            au_name = fetch_username(self.eos)
            platforms = primary.get("platforms") or []

            def apply_info():
                if au_name:
                    self.au_label.configure(text=f"Among Us: {au_name}", text_color="#61a8ff")
                else:
                    self.au_label.configure(text="No Among Us Data yet", text_color=self.muted)
                if platforms:
                    labels = ", ".join(platform_label(p) for p in platforms)
                    self.merged_label.configure(text=f"Your account is merged with {labels}")
                else:
                    self.merged_label.configure(text="")
            self.after(0, apply_info)
        except Exception:
            def apply_err():
                self.au_label.configure(text="No Among Us Data yet", text_color=self.muted)
                self.merged_label.configure(text="")
            self.after(0, apply_err)

        self.set_busy(False)

    def set_avatar(self, pfp_url):
        img = None
        if pfp_url:
            try:
                img = Image.open(io.BytesIO(requests.get(pfp_url, timeout=10).content))
            except Exception:
                img = None
        if img is None:
            try:
                img = embedded_image(FROG_PNG_B64)
            except Exception:
                img = None
        if img is not None:
            self._pfp_img = ctk.CTkImage(light_image=img, dark_image=img, size=(120, 120))
            self.after(0, lambda: self.pfp_label.configure(image=self._pfp_img, text=""))

    # ---------- help ----------
    def show_help_popup(self):
        win = ctk.CTkToplevel(self)
        win.title("Which one do I pick?")
        win.geometry("560x500")
        win.minsize(520, 440)
        win.attributes("-topmost", True)
        win.grab_set()

        scroll = ctk.CTkScrollableFrame(win, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(scroll, text="Merge your account as...", font=("Arial", 18, "bold")).pack(pady=(4, 12))

        card1 = ctk.CTkFrame(scroll, fg_color="#1c1533")
        card1.pack(fill="x", padx=6, pady=6)
        ctk.CTkLabel(card1, text="PRIMARY", font=("Arial", 14, "bold"),
                     text_color=self.purple).pack(anchor="w", padx=14, pady=(12, 2))
        ctk.CTkLabel(card1, text="Makes this itch.io account your MAIN account.\n\nAny other account you link after this will take data "
                                 "FROM itch.io. Your itch progress, stars and cosmetics stay as the main ones.",
                     font=("Arial", 12), text_color="#cccccc", wraplength=480,
                     justify="left").pack(anchor="w", padx=14)
        ctk.CTkLabel(card1, text="\u26a0 Don't pick this one if you want to bring data from somewhere else onto itch.io!",
                     font=("Arial", 11, "italic"), text_color="#ffc857", wraplength=480,
                     justify="left").pack(anchor="w", padx=14, pady=(6, 12))

        card2 = ctk.CTkFrame(scroll, fg_color="#13251c")
        card2.pack(fill="x", padx=6, pady=6)
        ctk.CTkLabel(card2, text="SECONDARY", font=("Arial", 14, "bold"),
                     text_color=self.green).pack(anchor="w", padx=14, pady=(12, 2))
        ctk.CTkLabel(card2, text="Makes this itch.io account RECEIVE data from your main account.\n\nPick this if you want to play on "
                                 "itch.io using your existing progress, stars and cosmetics from another platform (Steam, Epic, "
                                 "Microsoft...). This is the right choice for most people.",
                     font=("Arial", 12), text_color="#cccccc", wraplength=480,
                     justify="left").pack(anchor="w", padx=14, pady=(0, 12))

        ctk.CTkButton(scroll, text="Got it!", command=win.destroy, fg_color=self.purple,
                      hover_color=self.purple_dark, width=120).pack(pady=10)

    # ---------- merge: PRIMARY ----------
    def merge_as_primary(self):
        """Opens Innersloth's official account page logged in as this itch.io account,
        where other platforms can be linked INTO it."""
        if self.busy or not self.token:
            return
        url = f"{ACCOUNT_MANAGEMENT_URL}?store=itchio&token={urllib.parse.quote(self.token)}"
        self.merge_hint.configure(text="Opened the official Innersloth account page in your browser. "
                                       "Link your other platform accounts there.",
                                  text_color="#61a8ff")
        webbrowser.open(url)

    # ---------- merge: SECONDARY ----------
    def merge_as_secondary(self):
        if self.busy or not self.token:
            return
        subtitle = ("Paste the link (or just the token) of your MAIN account, the one that already has "
                    "your progress, stars and cosmetics. The platform gets detected automatically.\n\n"
                    "How to get it: launch Among Us on that platform. When the browser opens "
                    "accounts.innersloth.com, copy the full URL from the address bar, something like:\n"
                    "https://accounts.innersloth.com/account-management?store=steam&token=YOUR_TOKEN")
        win = ctk.CTkToplevel(self)
        win.title("Merge as Secondary")
        win.geometry("620x470")
        win.minsize(580, 440)
        win.attributes("-topmost", True)
        win.grab_set()

        wrap = ctk.CTkFrame(win, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=18, pady=14)

        ctk.CTkLabel(wrap, text="Merge as Secondary", font=("Arial", 17, "bold")).pack(anchor="w")
        ctk.CTkLabel(wrap, text=subtitle, font=("Arial", 12), text_color=self.muted,
                     wraplength=560, justify="left").pack(anchor="w", pady=(6, 10))

        cred_box = ctk.CTkTextbox(wrap, height=90)
        cred_box.pack(fill="x")

        links_row = ctk.CTkFrame(wrap, fg_color="transparent")
        links_row.pack(fill="x", pady=(8, 0))
        ctk.CTkButton(links_row, text="Not sure where to find it?", width=180, height=28,
                      command=lambda: webbrowser.open(ACCOUNT_MANAGEMENT_URL),
                      fg_color="#22222c", hover_color="#33333f",
                      font=("Arial", 11)).pack(side="left")

        status = ctk.CTkLabel(wrap, text="", font=("Arial", 12), wraplength=560, justify="left")
        status.pack(anchor="w", pady=(8, 4))

        go = ctk.CTkButton(wrap, text="Start Merge", height=38, fg_color=self.green,
                           hover_color="#2f9c66", font=("Arial", 13, "bold"))

        def submit():
            raw = cred_box.get("1.0", "end")
            try:
                s, t = parse_credentials(raw)
                if s == "itchio":
                    status.configure(text="That's an itch.io link. Paste your main account here "
                                          "(Steam, Epic or Microsoft), not itch.io.", text_color=self.red)
                    return
            except ValueError as ve:
                status.configure(text=str(ve), text_color=self.red)
                return
            go.configure(state="disabled")
            self.run_secondary_merge(win, s, t, status, go)

        go.configure(command=submit)
        go.pack(pady=(6, 0))

    def run_secondary_merge(self, win, main_store, main_token, status, go_button):
        evt = threading.Event()
        confirmed = {"ok": False}

        def worker():
            nonlocal main_store
            try:
                self.after(0, lambda: status.configure(text="Authenticating itch.io...", text_color="#bbbbbb"))
                itch_eos = eos_auth("itchio", self.token)
                itch_primary = query_primary(itch_eos)

                if main_store is None:
                    self.after(0, lambda: status.configure(text="Detecting your main account's platform...",
                                                           text_color="#bbbbbb"))
                    try:
                        main_store = detect_store_for_token(main_token)
                    except Exception as e:
                        msg = str(e) or "That token didn't work."
                        self.after(0, lambda m=msg: status.configure(text=m, text_color=self.red))
                        return

                self.after(0, lambda s=main_store: status.configure(
                    text=f"Checking your {platform_label(s)} account...", text_color="#bbbbbb"))
                main_eos = eos_auth(main_store, main_token)
                main_data = query_primary(main_eos)

                if "itchio" in (main_data.get("platforms") or []):
                    self.after(0, lambda: status.configure(
                        text="\u2717 Your itch.io account is already merged into that account.", text_color=self.red))
                    return

                self.after(0, lambda: status.configure(text="Validating itch.io side...", text_color="#bbbbbb"))
                query_secondary(itch_eos, main_data.get("puid"))

                main_plat = platform_label(main_data.get("platform") or main_store)
                summary = f"{main_plat} (main, keeps everything)\n\u2193\nitch.io (receives the data)"

                def ask():
                    dlg = ctk.CTkToplevel(self)
                    dlg.title("Confirm merge")
                    dlg.geometry("460x250")
                    dlg.minsize(440, 240)
                    dlg.attributes("-topmost", True)
                    dlg.grab_set()
                    ctk.CTkLabel(dlg, text="Ready to merge!", font=("Arial", 16, "bold")).pack(pady=(16, 6))
                    ctk.CTkLabel(dlg, text=summary, font=("Consolas", 13), text_color="#cccccc",
                                 justify="center").pack()
                    ctk.CTkLabel(dlg, text="\u26a0 Your itch.io progress will be replaced by your main account's.",
                                 font=("Arial", 11, "italic"), text_color="#ffc857", wraplength=400,
                                 justify="center").pack(padx=16, pady=(8, 0))
                    rowf = ctk.CTkFrame(dlg, fg_color="transparent")
                    rowf.pack(pady=14)

                    def cancel():
                        confirmed["ok"] = False
                        dlg.destroy()

                    def yes():
                        confirmed["ok"] = True
                        dlg.destroy()

                    ctk.CTkButton(rowf, text="Cancel", width=110, command=cancel,
                                  fg_color="#33333d", hover_color="#44444f").pack(side="left", padx=8)
                    ctk.CTkButton(rowf, text="Yes, merge!", width=130, command=yes,
                                  fg_color=self.green, hover_color="#2f9c66").pack(side="left", padx=8)
                    dlg.wait_window()
                    evt.set()

                self.after(0, ask)
                evt.wait()

                if not confirmed["ok"]:
                    self.after(0, lambda: status.configure(text="Cancelled.", text_color=self.muted))
                    return

                self.after(0, lambda: status.configure(text="Merging... please wait...", text_color="#bbbbbb"))
                res = do_merge(main_eos, itch_eos, "itchio", self.token)

                if "Success" in str(res):
                    def done():
                        status.configure(text="\u2714 Merged! Restart Among Us and your main account's progress, "
                                              "stars and cosmetics will be on itch.io.", text_color=self.green)
                        if go_button.winfo_exists():
                            go_button.configure(state="normal")
                        if win.winfo_exists():
                            win.after(2000, win.destroy)
                        threading.Thread(target=self.load_account, args=(self.token,), daemon=True).start()
                    self.after(0, done)
                else:
                    self.after(0, lambda: status.configure(text=f"\u2717 Unexpected response: {str(res)[:140]}",
                                                           text_color=self.red))
            except Exception as e:
                msg = str(e)[:220]
                self.after(0, lambda: (status.configure(text=f"\u2717 {msg}", text_color=self.red),
                                       go_button.configure(state="normal") if go_button.winfo_exists() else None))

        threading.Thread(target=worker, daemon=True).start()


if __name__ == "__main__":
    app = ItchFixerApp()
    app.mainloop()
