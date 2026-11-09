import os
import threading
import webbrowser
import urllib.parse
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
import tkinter as tk

CLIENT_ID = "1ba9b4bfa1ac7759e8420eed4ec863ba"
PORT = 7890

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

class ItchFixerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Itch Login Fixer")
        self.geometry("450x550")
        self.configure(bg="#242424")
        self.token = None
        self.pfp_image = None

        self.target_file = ""
        self.target_dir = ""

        self.kicker = tk.Label(self, text="SHADOWSLIME AUTH", font=("JetBrains Mono", 8), fg="#7b61ff", bg="#242424")
        self.kicker.pack(pady=(25, 7))

        self.version_label = tk.Label(self, text="v1.0 | 5.9.2026", font=("JetBrains Mono", 7), fg="#444", bg="#242424")
        self.version_label.pack()

        self.pfp_label = tk.Label(self, text="", bg="#242424")
        self.pfp_label.pack(pady=20)

        self.status_label = tk.Label(self, text="Not Logged In", font=("Sans Regular", 18, "bold"), fg="white", bg="#242424")
        self.status_label.pack(pady=5)

        self.action_text = tk.Label(self, text="Click login to fix the ownership error", font=("Sans Regular", 9), fg="#888", bg="#242424")
        self.action_text.pack(pady=5)

        self.prefix_label = tk.Label(self, text="Enter Proton/Wine prefix of your Among Us installation", 
                                     font=("Sans Regular", 10, "bold"), fg="white", bg="#242424")
        self.prefix_label.pack()
        
        self.prefix_entry = tk.Entry(self, font=("Sans Regular", 9), width="50")
        self.prefix_entry.pack(pady=5)

        self.prefix_button = tk.Button(self, text="Set", command=self.set_wine_prefix,
                                      bg="#6193ff", fg="white", activebackground="#7367b1",
                                      activeforeground="white", font=("Sans Regular", 10, "bold"),
                                      relief="flat", height=1)
        self.prefix_button.pack(padx=180, fill="x")

        self.login_button = tk.Button(self, state="disabled", text="Login with itch.io", command=self.start_login_thread,
                                      bg="#7b61ff", fg="white", activebackground="#5a44cc",
                                      activeforeground="white", font=("Arial", 10, "bold"),
                                      relief="flat", height=2)
        self.login_button.pack(pady=25, padx=60, fill="x")

        self.warning_label = tk.Label(self, text="This is a temporary fix, don't expect it to always work.",
                                      font=("Arial", 8, "italic"), fg="#555", bg="#242424")
        self.warning_label.pack(side="bottom", pady=(0, 15))

        

    def check_existing_login(self):
        if os.path.exists(self.target_file):
            with open(self.target_file, "r") as f:
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

                self.status_label.configure(text=f"Logged in as {username}", fg="#4ade80")
                self.action_text.configure(text="Login fixed! You can launch Among Us now. (you can also close this app)", fg="#4ade80")
                self.login_button.configure(text="Refresh Session")
            else:
                self.status_label.configure(text="Session Expired", fg="#ff4b4b")
        except:
            pass

    def set_wine_prefix(self):
        self.prefix_entry.configure(state="disabled")
        self.prefix_button.configure(state="disabled", text="Prefix set!")
        self.login_button.configure(state="active")

        wine_prefix = self.prefix_entry.get().split("/")
        target_file_list = ['drive_c', 'users', 'steamuser', 'AppData', 'LocalLow', 'Innersloth', 'Among Us', 'itch']

        target_dir_list = ["/"] + wine_prefix + target_file_list[0:6]
        target_file_list = ["/"] + wine_prefix + target_file_list
        print(f"{target_dir_list}")

        self.target_dir = os.path.join('', *target_dir_list)
        self.target_file = os.path.join('', *target_file_list)
        print(self.target_file)

        self.check_existing_login()

    def start_login_thread(self):
        self.login_button.configure(text="Check Browser...")
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
        os.makedirs(self.target_dir, exist_ok=True)
        with open(self.target_file, "w") as f:
            f.write(token)
        self.after(0, lambda: self.fetch_user_data(token))
        self.after(0, lambda: self.login_button.configure(state="normal", text="Success!"))

if __name__ == "__main__":
    app = ItchFixerApp()
    app.mainloop()