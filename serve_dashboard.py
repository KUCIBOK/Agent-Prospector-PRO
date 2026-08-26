#!/usr/bin/env python
"""
Serveur HTTP simple pour le dashboard
Lancez ceci sur http://localhost:8001
"""
import http.server
import socketserver
import os
from urllib.parse import urlparse

PORT = 8001

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        path = urlparse(self.path).path

        # Routes
        if path == '/' or path == '/dashboard':
            self.serve_file('dashboard.html')
        elif path == '/summary' or path == '/dashboard-summary':
            self.serve_file('dashboard_summary.html')
        else:
            self.send_error(404, "File not found")

    def serve_file(self, filename):
        """Serve a file"""
        if os.path.exists(filename):
            self.send_response(200)
            if filename.endswith('.html'):
                self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open(filename, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404, f"File {filename} not found")

    def log_message(self, format, *args):
        """Log messages"""
        print(f"[{self.client_address[0]}] {format % args}")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
        print("=" * 70)
        print("🚀 DASHBOARD SERVER")
        print("=" * 70)
        print(f"\n📊 Main Dashboard:")
        print(f"   http://localhost:{PORT}/dashboard")
        print(f"\n📊 Summary Dashboard:")
        print(f"   http://localhost:{PORT}/summary")
        print(f"\n🏠 Home:")
        print(f"   http://localhost:{PORT}/")
        print(f"\n⏸️  Appuyez sur Ctrl+C pour arrêter")
        print("=" * 70 + "\n")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n✅ Serveur arrêté")
