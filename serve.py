# -*- coding: utf-8 -*-
"""Локальный сервер мок-версии без кэширования.
Запуск: python serve.py  (порт 8088)"""
import http.server
import socketserver

PORT = 8088


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def log_message(self, *args):
        pass


if __name__ == '__main__':
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(('127.0.0.1', PORT), NoCacheHandler) as httpd:
        print(f'Serving on http://127.0.0.1:{PORT} (no cache)')
        httpd.serve_forever()
