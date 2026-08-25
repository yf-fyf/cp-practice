#!/usr/bin/env python3
"""Build the allowlisted static site published from the main branch."""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = ROOT / "workbook"
BUILD_SITE = ROOT / "tools" / "build_site.py"
EXCLUDED_PARTS = {"__pycache__", "_build", "node_modules"}

# 配布アーカイブの名前。tools/build_site.py の WORKBOOK_ARCHIVE_PREFIX と揃える。
WORKBOOK_ARCHIVE_PREFIX = "cp-practice-workbook"

# main ブランチのルート直下に置いてよいものの許可リスト
# （design/maintaining.md の「公開時の除外」節と同期させる）。
ALLOWED_TOP_LEVEL = {
    "index.html", "assets", "figures",
    "sessions", "projects", "references", "guides",
    "tools", "downloads",
    "LICENSE", "LICENSE-MATERIALS", "THIRD_PARTY_NOTICES.md",
    ".nojekyll",
}

# 公開ツリー・ZIP に混ざってはいけないもの。
# ディレクトリ名 teacher/ は非公開リポジトリ側の置き場、answer / solution / rubric は
# 「うっかり公開側へ置いた解答」をファイル名で拾うための保険である
# （curriculum-2026.md §2「応用演習の解答は公開しない」の二重化）。
FORBIDDEN_PATH_PARTS = ("teacher",)
FORBIDDEN_NAME_WORDS = ("answer", "solution", "rubric")

# 公開ビルドに必ず存在すべきもの。原稿を1本増やすたびに足す必要はないが、
# セクションの入口が消えたことには気づけるようにしておく。
REQUIRED_OUTPUT = (
    Path("index.html"),
    Path("assets/style.css"),
    Path("assets/lightbox.js"),
    Path("sessions/index.html"),
    Path("guides/index.html"),
    Path(".nojekyll"),
)


def revision() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True
    )
    return result.stdout.strip() if result.returncode == 0 else "uncommitted"


def safe_version(value: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", value):
        raise ValueError("version must contain only letters, digits, dot, underscore, or hyphen")
    return value


def copy_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def build_site(output: Path, version: str, source_revision: str) -> None:
    """資料サイトを出力先へ直接生成する（tools/build_site.py が単一の出典）"""
    result = subprocess.run(
        [sys.executable, str(BUILD_SITE), "--output", str(output),
         "--release", version, "--revision", source_revision],
        cwd=ROOT, capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"build_site.py failed:\n{result.stdout}\n{result.stderr}")


def forbidden_reason(relative: Path) -> str | None:
    """公開してはいけないパスなら理由を返す。問題なければ None を返す。"""
    if any(part in FORBIDDEN_PATH_PARTS for part in relative.parts):
        return "非公開側の置き場（teacher/）のパスが混ざっている"
    stem = relative.stem.lower()
    for word in FORBIDDEN_NAME_WORDS:
        if word in stem:
            return f"解答らしいファイル名（{word}）が混ざっている"
    return None


def archive_workbook(destination: Path, version: str) -> None:
    """演習ファイルの配布アーカイブ。資料本文はサイトで配るので workbook だけ。"""
    prefix = f"{WORKBOOK_ARCHIVE_PREFIX}-{version}"
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for top_level in (ROOT / "README.md", ROOT / "LICENSE", ROOT / "LICENSE-MATERIALS"):
            if top_level.is_file():
                archive.write(top_level, f"{prefix}/{top_level.name}")
        for directory, subdirs, filenames in os.walk(WORKBOOK):
            path = Path(directory)
            subdirs[:] = [name for name in subdirs if name not in EXCLUDED_PARTS]
            for filename in filenames:
                source = path / filename
                if source.suffix in {".pyc", ".pyo"}:
                    continue
                relative = source.relative_to(ROOT)
                reason = forbidden_reason(relative)
                if reason:
                    raise RuntimeError(
                        f"forbidden path in workbook archive: {relative}（{reason}）")
                archive.write(source, f"{prefix}/{relative.as_posix()}")


def verify_output(output: Path) -> None:
    """公開ツリーに教員用資産・解答が混ざっていないかを実行時に確かめる。

    リポジトリ分離（site-plan-2026.md §3.2）に加えた二重化であり、
    許可リストを外れたトップレベルもここで落とす。
    """
    for path in output.rglob("*"):
        reason = forbidden_reason(path.relative_to(output))
        if reason:
            raise RuntimeError(
                f"forbidden path in release output: {path.relative_to(output)}（{reason}）")

    top_level = {path.name for path in output.iterdir()}
    disallowed = top_level - ALLOWED_TOP_LEVEL
    if disallowed:
        raise RuntimeError(f"許可リスト外のトップレベルパス: {', '.join(sorted(disallowed))}")

    missing = [rel for rel in REQUIRED_OUTPUT if not (output / rel).exists()]
    if missing:
        raise RuntimeError(
            f"missing release output: {', '.join(rel.as_posix() for rel in missing)}")
    if not any((output / "figures").glob("*.svg")):
        raise RuntimeError("no figures in release output")

    for release_zip in output.rglob("*.zip"):
        with zipfile.ZipFile(release_zip) as release:
            for name in release.namelist():
                reason = forbidden_reason(Path(name))
                if reason:
                    raise RuntimeError(
                        f"forbidden path in release archive: {release_zip.name}:{name}"
                        f"（{reason}）")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("version", help="release version used in the archive name")
    parser.add_argument("--output", type=Path, default=ROOT / ".pages", help="output directory")
    parser.add_argument("--revision", default=revision(),
                        help="source revision displayed in the page")
    args = parser.parse_args()
    try:
        version = safe_version(args.version)
        if args.output.resolve() == ROOT.resolve():
            raise RuntimeError("refusing to use the repository root as output")
        shutil.rmtree(args.output, ignore_errors=True)
        args.output.mkdir(parents=True)

        # ブラウザ補助ツール（web/）は build_site.py が .site/tools/ へコピーする。
        # c-comp と違いビルド工程を持たないので、ここでの前処理は要らない。
        build_site(args.output, version, args.revision)
        for name in ("LICENSE", "LICENSE-MATERIALS", "THIRD_PARTY_NOTICES.md"):
            source = ROOT / name
            if source.is_file():
                copy_file(source, args.output / name)
        archive = args.output / "downloads" / f"{WORKBOOK_ARCHIVE_PREFIX}-{version}.zip"
        archive.parent.mkdir(parents=True)
        archive_workbook(archive, version)
        (args.output / ".nojekyll").touch()
        verify_output(args.output)
    except (OSError, RuntimeError, ValueError) as error:
        print(f"build_pages: {error}", file=sys.stderr)
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
