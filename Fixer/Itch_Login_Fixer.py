import os
import threading
import webbrowser
import urllib.parse
import requests
import io
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import customtkinter as ctk
from PIL import Image

CLIENT_ID = "1ba9b4bfa1ac7759e8420eed4ec863ba"
PORT = 7890
LOCAL_LOW = os.path.join(os.environ['USERPROFILE'], 'AppData', 'LocalLow')
TARGET_DIR = os.path.join(LOCAL_LOW, 'Innersloth', 'Among Us')
TARGET_FILE = os.path.join(TARGET_DIR, 'itch')

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
    def log_message(self, format, *args): pass

class ItchFixerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Itch Login Fixer")
        self.geometry("450x550")
        ctk.set_appearance_mode("dark")
        self.token = None

        self.kicker = ctk.CTkLabel(self, text="SHADOWSLIME AUTH", font=("JetBrains Mono", 10), text_color="#7b61ff")
        self.kicker.pack(pady=(25, 5))

        self.version_label = ctk.CTkLabel(self, text="v1.0 | 5.9.2026", font=("JetBrains Mono", 9), text_color="#444")
        self.version_label.pack()

        self.pfp_label = ctk.CTkLabel(self, text="", width=120, height=120)
        self.pfp_label.pack(pady=20)
        
        self.status_label = ctk.CTkLabel(self, text="Not Logged In", font=("Arial", 22, "bold"))
        self.status_label.pack(pady=5)

        self.action_text = ctk.CTkLabel(self, text="Click login to fix the ownership error", font=("Arial", 13), text_color="#888")
        self.action_text.pack(pady=5)

        self.login_button = ctk.CTkButton(self, text="Login with itch.io", command=self.start_login_thread, 
                                          fg_color="#7b61ff", hover_color="#5a44cc", font=("Arial", 14, "bold"), height=40)
        self.login_button.pack(pady=25, padx=60, fill="x")

        self.warning_label = ctk.CTkLabel(self, text="This is a temporary fix, don't expect it to always work.", 
                                          font=("Arial", 11, "italic"), text_color="#555")
        self.warning_label.pack(side="bottom", pady=(0, 15))

        self.check_existing_login()

    def check_existing_login(self):
        if os.path.exists(TARGET_FILE):
            with open(TARGET_FILE, "r") as f:
                saved_token = f.read().strip()
                if saved_token:
                    self.fetch_user_data(saved_token)

    def fetch_user_data(self, token):
        try:
            headers = {"Authorization": token}
            response = requests.get("https://itch.io/api/1/key/me", headers=headers)
            if response.status_code == 200:
                data = response.json().get("user", {})
                username = data.get("username", "User")
                pfp_url = data.get("cover_url")

                self.status_label.configure(text=f"Logged in as {username}", text_color="#4ade80")
                self.action_text.configure(text="Login fixed! You can launch Among Us now. (you can also close this app)", text_color="#4ade80")
                self.login_button.configure(text="Refresh Session")
                
                if pfp_url:
                    img_data = requests.get(pfp_url).content
                    img = Image.open(io.BytesIO(img_data))
                    ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(120, 120))
                    self.pfp_label.configure(image=ctk_img)
            else:
                self.status_label.configure(text="Session Expired", text_color="#ff4b4b")
        except:
            pass

    def start_login_thread(self):
        self.login_button.configure(state="disabled", text="Check Browser...")
        threading.Thread(target=self.run_server, daemon=True).start()
        webbrowser.open(f"https://itch.io/user/oauth?client_id={CLIENT_ID}&scope=profile:me&redirect_uri=http://127.0.0.1:{PORT}&response_type=token")

    def run_server(self):
        server = HTTPServer(("127.0.0.1", PORT), OAuthHandler)
        server.token = None
        while server.token is None:
            server.handle_request()
        self.token = server.token
        self.save_and_update(server.token)

    def save_and_update(self, token):
        os.makedirs(TARGET_DIR, exist_ok=True)
        with open(TARGET_FILE, "w") as f:
            f.write(token)
        self.after(0, lambda: self.fetch_user_data(token))
        self.after(0, lambda: self.login_button.configure(state="normal", text="Success!"))

if __name__ == "__main__":
    app = ItchFixerApp()
    app.mainloop()