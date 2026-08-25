#!/usr/bin/env python3
"""
講義資料の図を SVG で生成する。

使い方:
    python3 tools/build_figures.py                  # 全図
    python3 tools/build_figures.py graph- sudoku-   # ファイル名の前方一致で絞り込み

TikZ ソース: materials/figures/<name>.tex -> materials/figures/<name>.svg

TikZ は LuaLaTeX で一度 PDF にしてから SVG へ変換する。中間 PDF は残さない。
変換に poppler の pdftocairo を使うのは、dvisvgm --pdf が Ghostscript 10.01 以降で
動かないためである（mutool も要求されるが常用環境に無い）。
文字はグリフのパスとして埋まるので、閲覧側にフォントが無くても日本語が正しく出る。

依存: lualatex（TikZ 図）、poppler-utils の pdftocairo または pdf2svg。
図を書き換える人だけがこの依存を用意すればよい。生成 SVG はコミット対象なので、
サイト生成（make site）と CI では pandoc + PyYAML だけで足りる。
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIGURES = ROOT / "materials" / "figures"
LATEX_DIR = ROOT / "latex"
PREAMBLE = LATEX_DIR / "figure-preamble.tex"

LUALATEX = "lualatex"

def find_pdf_to_svg() -> list[str] | None:
    """PDF -> SVG の変換コマンドを決める。{src} {dst} を後ろに付けて使う。"""
    if shutil.which("pdftocairo"):
        return ["pdftocairo", "-svg"]
    if shutil.which("pdf2svg"):
        return ["pdf2svg"]
    return None


def needs_build(sources: list[Path], target: Path) -> bool:
    if not target.is_file():
        return True
    newest = max((p.stat().st_mtime for p in sources if p.is_file()), default=0)
    return target.stat().st_mtime < newest


def build_tikz_figure(tex: Path, converter: list[str]) -> bool:
    svg = tex.with_suffix(".svg")
    if not needs_build([tex, PREAMBLE], svg):
        print(f"[SKIP] {tex.name}: 最新")
        return True

    env = os.environ.copy()
    # 共通プリアンブルを latex/ から解決する(末尾の : でデフォルトパスを維持)
    env["TEXINPUTS"] = f".:{LATEX_DIR}:" + env.get("TEXINPUTS", "")

    print(f"[BUILD] {tex.name}  ->  {svg.name}")
    with tempfile.TemporaryDirectory() as tmp:
        # 中間 PDF と aux を materials/figures/ に散らかさないよう別ディレクトリへ出す
        result = subprocess.run(
            [LUALATEX, "-interaction=nonstopmode", "-halt-on-error",
             f"-output-directory={tmp}", tex.name],
            capture_output=True, text=True, cwd=str(FIGURES), env=env,
        )
        pdf = Path(tmp) / tex.with_suffix(".pdf").name
        if result.returncode != 0 or not pdf.is_file():
            print(f"[FAIL] {tex.name}: LuaLaTeX")
            print("\n".join(result.stdout.strip().splitlines()[-30:]))
            return False

        conv = subprocess.run(
            [*converter, str(pdf), str(svg)], capture_output=True, text=True
        )
        if conv.returncode != 0 or not svg.is_file():
            print(f"[FAIL] {tex.name}: SVG 変換 — {conv.stderr.strip()}")
            return False

    print(f"[ OK ] {tex.name}")
    return True


def main() -> int:
    if not FIGURES.is_dir():
        print(f"[WARN] 図ディレクトリがありません: {FIGURES}")
        return 0

    converter = find_pdf_to_svg()
    if converter is None:
        print("pdftocairo (poppler-utils) か pdf2svg が要る", file=sys.stderr)
        return 2
    if shutil.which(LUALATEX) is None:
        print(f"{LUALATEX} が見つからない", file=sys.stderr)
        return 2

    prefixes = tuple(sys.argv[1:]) if len(sys.argv) >= 2 else None

    tikz = sorted(FIGURES.glob("*.tex"))
    if prefixes:
        tikz = [t for t in tikz if t.name.startswith(prefixes)]

    if not tikz:
        print("[WARN] 対象の図がありません")
        return 0

    ok = fail = 0
    for tex in tikz:
        if build_tikz_figure(tex, converter):
            ok += 1
        else:
            fail += 1

    print(f"\n[DONE] 成功 {ok} / 失敗 {fail}")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
