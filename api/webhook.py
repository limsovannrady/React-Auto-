import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import asyncio
import logging
from http.server import BaseHTTPRequestHandler
from telegram import Update
from bot_handlers import build_application

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def process_update(update_data: dict) -> None:
    application = build_application()
    await application.initialize()
    try:
        update = Update.de_json(update_data, application.bot)
        await application.process_update(update)
    finally:
        await application.shutdown()


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            update_data = json.loads(body.decode('utf-8'))
            asyncio.run(process_update(update_data))
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK')
        except Exception as e:
            logger.error(f"Webhook error: {e}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b'Internal Server Error')

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Auto Reaction Bot webhook is active!')

    def log_message(self, format, *args):
        logger.info(f"Vercel request: {format % args}")
