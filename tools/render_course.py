#!/usr/bin/env python3
"""通常回・発展・手引きのHTML生成。入口は build_site.py。"""

from __future__ import annotations

import html
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from course import LessonSample, OUTPUT, ROOT, SAMPLES
from site_header import site_header, session_navigation
from code_preview import ASSETS, build_previews, preview_path, text_handouts

TOOLS = ROOT / "site"

# 図の表示倍率。TikZ の図は preamble の font=\small（9pt）で描かれるので、
# 等倍だと図中の文字が 12px になり、本文の 16px より小さく見える。16/12 を掛けて
# 図の文字を本文と同じ大きさに揃える。列いっぱい（2.1〜3.1倍）まで伸ばすと図中の
# 文字が 25〜37px になり、節の帯（24px）や題名（30px）を超えてしまう。
FIGURE_SCALE = 16 / 12


def split_title(text: str) -> tuple[str, str]:
    """原稿の先頭の H1 を題名として取り出し、本文から外す。

    題名をテンプレートの pagetitle へ渡すことで、--section-divs が本文全体を
    section.level1 で包むのを避け、節が main の直下に並ぶようにする。
    """
    lines = text.split("\n")
    for index, line in enumerate(lines):
        if line.startswith("# "):
            title = line[2:].strip()
            return title, "\n".join(lines[:index] + lines[index + 1:]).lstrip("\n")
    raise SystemExit("原稿の先頭に H1 の題名が必要です")


def scale_svg(text: str, factor: float) -> str:
    """SVG の width と height だけを倍率で書き換える。

    viewBox はそのままにするので、中身の座標系は変えずに描画寸法だけが変わり、
    線も文字も一様に拡大される。LaTeX が出した元の SVG には手を入れない。
    """
    def replace(match: re.Match[str]) -> str:
        value = float(match.group(2))
        return f'{match.group(1)}="{value * factor:.3f}{match.group(3) or ""}"'

    head, rest = text[:1200], text[1200:]
    head = re.sub(r'\b(width|height)="([\d.]+)(pt|px)?"', replace, head, count=2)
    return head + rest


def rewrite_links(text: str, depth: int, sample: LessonSample, source_name: str) -> str:
    base = "../" * depth
    destinations = {
        (item.source / source).resolve(): page
        for item in SAMPLES.values() for page, (source, _, _) in item.pages.items()
    }
    for item in SAMPLES.values():
        for name in item.handouts:
            destinations[(item.handout_directory / name).resolve()] = f"downloads/session-{item.number}/{name}"
        for figure in (item.source / "figures").glob("*.svg"):
            destinations[figure.resolve()] = f"figures/session-{item.number}/{figure.name}"

    previews = {source.resolve(): preview_path(url)
                for url, (source, _) in text_handouts(SAMPLES.values()).items()}

    def replace(match: re.Match[str]) -> str:
        link = match.group(1)
        if link.startswith("#") or ":" in link:
            return match.group(0)
        path, separator, fragment = link.partition("#")
        source = (sample.source / source_name).parent / path
        target = destinations.get(source.resolve())
        if target is None:
            raise ValueError(f"未登録の原稿リンク: {sample.slug}/{source_name} -> {link}")
        attrs = match.group(2) or ""
        if source.resolve() in previews:
            extra = f'data-code-preview="{base}{previews[source.resolve()]}"'
            attrs = attrs[:-1] + " " + extra + "}" if attrs else "{" + extra + "}"
        return f"]({base}{target}{separator}{fragment}){attrs}"

    return re.sub(r"\]\(([^)]+)\)(\{[^}\n]*\})?", replace, text)


def build(session: str = "07", output: Path = OUTPUT, *, website: bool = False) -> int:
    if not shutil.which("pandoc"):
        raise SystemExit("pandoc が必要です")

    assets = output / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    for name in ("lesson-style.css", "lesson-syntax.css", "lesson-lightbox.css", "lesson-lightbox.js", "site-header.css", *ASSETS):
        shutil.copyfile(TOOLS / name, assets / name)
    shutil.copytree(TOOLS / "vendor/katex", assets / "katex", dirs_exist_ok=True)

    warnings = 0
    selected = list(SAMPLES.values()) if session == "all" else [SAMPLES[session]]
    for sample in selected:
        downloads = output / f"downloads/session-{sample.number}"
        downloads.mkdir(parents=True, exist_ok=True)
        for name in sample.handouts:
            target = downloads / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(sample.handout_directory / name, target)
        figures = output / f"figures/session-{sample.number}"
        figures.mkdir(parents=True, exist_ok=True)
        for source in sorted((sample.source / "figures").glob("*.svg")):
            (figures / source.name).write_text(
                scale_svg(source.read_text(encoding="utf-8"), FIGURE_SCALE), encoding="utf-8")
        warnings += build_pages(sample, output, website=website)

    build_previews(selected, output)
    for sample in selected:
        print(f"生成完了: {sample.lesson_page}")
    if warnings:
        print(f"フィルターの警告 {warnings} 件")
    return warnings


def build_pages(sample: LessonSample, output: Path = OUTPUT, *, website: bool = False) -> int:
    warnings = 0
    with tempfile.TemporaryDirectory(prefix="lesson-preview-") as temporary:
        folder = Path(temporary)
        for relative, (name, section_title, kind) in sample.pages.items():
            source = sample.source / name
            depth = len(Path(relative).parts) - 1
            base = "../" * depth
            title, body = split_title(source.read_text(encoding="utf-8"))
            body = rewrite_links(body, depth, sample, name)
            page = folder / "page.md"
            page.write_text(body, encoding="utf-8")

            destination = output / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            pager = ""
            if website:
                numbers = list(SAMPLES)
                index = numbers.index(sample.number)
                links = [f'<a href="{base}index.html">講義一覧</a>']
                if kind == "lesson":
                    if index > 0:
                        previous = SAMPLES[numbers[index - 1]]
                        links.insert(0, f'<a href="{base}{previous.lesson_page}">← 第{previous.number}回</a>')
                    if index + 1 < len(numbers):
                        following = SAMPLES[numbers[index + 1]]
                        links.append(f'<a href="{base}{following.lesson_page}">第{following.number}回 →</a>')
                else:
                    links.append(f'<a href="{base}{sample.lesson_page}">第{sample.number}回の本文へ</a>')
                pager = " · ".join(links)
            command = [
                "pandoc", str(page),
                "--from", "markdown+fenced_divs+bracketed_spans",
                "--to", "html5",
                "--standalone",
                "--section-divs",
                f"--template={TOOLS / 'lesson-template.html'}",
                f"--lua-filter={TOOLS / 'lesson-boxes.lua'}",
                "--wrap=preserve",
                # トークンを生成する。配色はテンプレートが読む lesson-syntax.css に集約。
                "--syntax-highlighting=tango",
                f"--syntax-definition={TOOLS / 'syntax/minizinc.xml'}",
                f"--katex={base}assets/katex/",
                "--metadata", f"pagetitle={title}",
                "--metadata", f"page-kind={kind}",
                "--variable", f"base={base}",
                "--variable", "site-title=実践・制約プログラミング",
                "--variable", "site-header=" + site_header(base + "index.html"),
                "--variable", "session-nav=" + (session_navigation(
                    sample.number, base + sample.lesson_page, base + sample.advanced_page, kind)
                    if name != "guides/course-start.md" else ""),
                "--variable", f"breadcrumb=<a href=\"{base}index.html\">ホーム</a> / {section_title}",
                "--variable", "release=" + ("2026年度" if website else "新テンプレートの試作"),
                "--variable", f"pager={pager}",
                "-o", str(destination),
            ]
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode != 0:
                sys.stderr.write(result.stderr)
                raise SystemExit(f"[FAIL] {source}")
            for line in result.stderr.splitlines():
                if line.strip():
                    print(f"  {line}")
                    warnings += 1

    return warnings
