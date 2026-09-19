"""保存後にサイトを再生成してブラウザへ通知する開発サーバー。"""
import http.server
import shutil
import socket
import subprocess
import sys
import threading
import time
from pathlib import Path
from course import ROOT

RELOAD_SNIPPET = (b'<script>new EventSource("/__reload")'
                  b'.onmessage=function(){location.reload()}</script>')


class Reloader:
    """再ビルドの世代番号。SSE の待ち受けを起こすのに使う。"""

    def __init__(self) -> None:
        self.generation = 0
        self._condition = threading.Condition()

    def bump(self) -> None:
        with self._condition:
            self.generation += 1
            self._condition.notify_all()

    def wait(self, seen: int, timeout: float) -> int:
        with self._condition:
            if self.generation == seen:
                self._condition.wait(timeout)
            return self.generation


def make_handler(output: Path, reloader: Reloader, inject: bool):
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(output), **kwargs)

        def log_message(self, *args) -> None:
            pass  # 静かにする。再ビルドのログだけ見えていればよい

        def end_headers(self) -> None:
            # 付けないと再ビルドしてもブラウザが古い HTML を出す
            self.send_header("Cache-Control", "no-store")
            super().end_headers()

        def do_GET(self) -> None:
            if self.path.split("?")[0] == "/__reload":
                self._stream_reload()
                return
            target = Path(self.translate_path(self.path))
            if target.is_dir():
                if not self.path.split("?")[0].endswith("/"):
                    super().do_GET()  # 末尾スラッシュへリダイレクトさせる
                    return
                target = target / "index.html"
            if inject and target.suffix == ".html" and target.is_file():
                self._send_html(target)
                return
            super().do_GET()

        def _send_html(self, path: Path) -> None:
            body = path.read_bytes()
            marker = b"</body>"
            if marker in body:
                body = body.replace(marker, RELOAD_SNIPPET + marker, 1)
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _stream_reload(self) -> None:
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Connection", "keep-alive")
            self.end_headers()
            seen = reloader.generation
            try:
                while True:
                    current = reloader.wait(seen, 15.0)
                    if current != seen:
                        seen = current
                        self.wfile.write(b"data: reload\n\n")
                    else:
                        self.wfile.write(b": ping\n\n")  # 接続を保つ
                    self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError, ValueError):
                pass  # ブラウザが閉じただけ

    return Handler

def tailscale_address() -> str | None:
    """tailscale0 の IPv4 を実行時に引く。環境固有の値は持ち歩かない。"""
    if shutil.which("tailscale") is None:
        return None
    try:
        result = subprocess.run(["tailscale", "ip", "-4"],
                                capture_output=True, text=True, timeout=5)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if result.returncode != 0:
        return None
    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    return lines[0] if lines else None


def resolve_host(host: str) -> str:
    """`tailscale` という論理名だけ実アドレスへ置き換える"""
    if host != "tailscale":
        return host
    address = tailscale_address()
    if address is None:
        raise SystemExit(
            "tailscale のアドレスが引けない。"
            "tailscale が動いているか確かめるか、--host にアドレスを直接渡す"
        )
    return address


def announce(host: str, port: int) -> None:
    """到達できる URL を出す。端末に出すだけで、どこにも保存しない。"""
    if host in ("0.0.0.0", "::"):
        print(f"\n配信中: ポート {port}（全インターフェース）")
        print(f"  ローカル  : http://127.0.0.1:{port}/")
        address = tailscale_address()
        if address:
            print(f"  Tailscale : http://{address}:{port}/")
        print("  注意: LAN や docker のインターフェースからも見えます。"
              "Tailscale だけに絞るなら --host tailscale を使ってください。")
    else:
        shown = f"[{host}]" if ":" in host else host
        print(f"\n配信中: http://{shown}:{port}/")



def source_snapshot():
    paths = [path for folder in ("materials", "workbook", "site", "tools")
             for path in (ROOT / folder).rglob("*")
             if path.is_file() and not any(part in {"__pycache__", "_build"} for part in path.parts)]
    paths += [ROOT / name for name in ("LICENSE", "LICENSE-MATERIALS", "THIRD_PARTY_NOTICES.md")]
    return {path: (path.stat().st_mtime_ns, path.stat().st_size) for path in paths}


def serve(output: Path, host: str, port: int, watch: bool):
    reloader = Reloader()
    snapshot = source_snapshot()

    class DevServer(http.server.ThreadingHTTPServer):
        daemon_threads = True
        address_family = socket.AF_INET6 if ":" in host else socket.AF_INET

    with DevServer((host, port), make_handler(output, reloader, inject=watch)) as server:
        threading.Thread(target=server.serve_forever, daemon=True).start()
        announce(host, server.server_port)
        if watch:
            print("保存するとサイトを再生成します。Ctrl-C で終了。", flush=True)
        try:
            while True:
                time.sleep(0.5)
                if not watch:
                    continue
                current = source_snapshot()
                if current == snapshot:
                    continue
                # 新しいプロセスで nav と生成コードも読み直す。失敗しても監視を続ける。
                snapshot = current
                result = subprocess.run([sys.executable, str(ROOT / "tools/build_site.py"),
                                         "--output", str(output)])
                if result.returncode == 0:
                    reloader.bump()
                    print("再生成完了。ブラウザへ通知しました。", flush=True)
                else:
                    print("再生成に失敗しました。直前のサイトを引き続き表示します。", flush=True)
        except KeyboardInterrupt:
            pass
        finally:
            server.shutdown()
    return 0
