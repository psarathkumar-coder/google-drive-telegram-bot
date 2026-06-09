import os
import logging
from pyrogram import Client
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from bot import (
    APP_ID,
    API_HASH,
    BOT_TOKEN,
    DOWNLOAD_DIRECTORY
)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
LOGGER = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# Dummy web server to satisfy Render's port check
class DummyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Bot is active")

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), DummyServer)
    LOGGER.info(f"Dummy web server running on port {port}")
    server.serve_forever()

if __name__ == "__main__":
    if not os.path.isdir(DOWNLOAD_DIRECTORY):
        os.makedirs(DOWNLOAD_DIRECTORY)
        
    plugins = dict(root="bot/plugins")
    
    app = Client(
        "G-DriveBot",
        bot_token=BOT_TOKEN,
        api_id=APP_ID,
        api_hash=API_HASH,
        plugins=plugins,
        parse_mode="markdown",
        workdir=DOWNLOAD_DIRECTORY
    )
    
    # Start the dummy web server in the background
    threading.Thread(target=run_web_server, daemon=True).start()
    
    LOGGER.info('Starting Bot !')
    app.run()
