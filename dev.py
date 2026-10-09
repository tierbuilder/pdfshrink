#!/usr/bin/env python3
"""Local dev server: serves dist/ on :8099 and rebuilds whenever a source file changes.

    python3 dev.py          # then open http://localhost:8099 and refresh after edits
"""
import functools
import http.server
import subprocess
import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).parent
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8099
WATCH = [ROOT / "build.py", ROOT / "content.py", ROOT / "tools_html.py", ROOT / "static"]


def snapshot():
    files = []
    for w in WATCH:
        files += [w] if w.is_file() else [p for p in w.rglob("*") if p.is_file()]
    return {p: p.stat().st_mtime for p in files}


def build():
    r = subprocess.run([sys.executable, "build.py"], cwd=ROOT, capture_output=True, text=True)
    out = (r.stdout + r.stderr).strip().splitlines()
    print(time.strftime("%H:%M:%S"), "rebuilt:" if r.returncode == 0 else "BUILD FAILED:", out[0] if r.returncode == 0 else "\n".join(out[-15:]), flush=True)


def watch():
    last = snapshot()
    while True:
        time.sleep(0.7)
        cur = snapshot()
        if cur != last:
            last = cur
            build()


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")  # always serve the latest build
        super().end_headers()

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    build()
    threading.Thread(target=watch, daemon=True).start()
    print(f"Serving http://localhost:{PORT}  (watching for changes, Ctrl+C to stop)", flush=True)
    http.server.ThreadingHTTPServer(("127.0.0.1", PORT), functools.partial(Handler, directory=str(ROOT / "dist"))).serve_forever()
