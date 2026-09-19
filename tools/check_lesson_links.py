#!/usr/bin/env python3
"""制作済みの回の参照先と、学習者向け配布範囲を検査する。

先に build_site.py で生成する。外部URLの到達性は対象外。
    python3 tools/check_lesson_links.py --session 02
    python3 tools/check_lesson_links.py --session all
"""

import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import subprocess
from urllib.parse import unquote, urlsplit

from course import OUTPUT, ROOT, SAMPLES
from code_preview import check_previews


class References(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = []
        self.links = []
        self.feed(text)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        for name in ("href", "src", "data-code-preview"):
            if attrs.get(name):
                self.links.append(attrs[name])


def markdown_links(value):
    if isinstance(value, dict):
        if value.get("t") in ("Link", "Image"):
            yield value["c"][-1][0]
        for item in value.values():
            yield from markdown_links(item)
    elif isinstance(value, list):
        for item in value:
            yield from markdown_links(item)


def check_samples(samples, output=OUTPUT):
    output = output.resolve()
    errors, cache = [], {}
    html_count = markdown_count = handout_count = 0

    def parse(path):
        if path not in cache:
            cache[path] = References(path.read_text(encoding="utf-8"))
        return cache[path]

    # 別の回の手引きが同じ出力先を上書きしないことも確認する。
    owners = {}
    for sample in SAMPLES.values():
        for page in sample.pages:
            if page in owners:
                errors.append(f"出力先重複: {page}: {owners[page]} / {sample.number}")
            owners[page] = sample.number

    pages = [output / page for sample in samples for page in sample.pages]
    pages.append(output / "index.html")
    for page in pages:
        if not page.is_file():
            errors.append(f"HTML未生成: {page.relative_to(output)}")
            continue
        document = parse(page)
        if len(document.ids) != len(set(document.ids)):
            errors.append(f"ID重複: {page.relative_to(output)}")
        for link in document.links:
            url = urlsplit(link)
            if url.scheme or url.netloc:
                continue
            target = (page.parent / unquote(url.path)).resolve() if url.path else page
            label = f"{page.relative_to(output)} -> {link}"
            if not target.is_relative_to(output) or not target.is_file():
                errors.append(f"参照先なし／出力外: {label}")
            elif url.fragment and target.suffix == ".html":
                if unquote(url.fragment) not in parse(target).ids:
                    errors.append(f"アンカーなし: {label}")
            html_count += 1

    for sample in samples:
        for source in sample.source.rglob("*.md"):
            ast = json.loads(subprocess.check_output(
                ["pandoc", str(source), "--to=json"], text=True))
            for link in markdown_links(ast):
                url = urlsplit(link)
                if url.scheme or url.netloc or not url.path:
                    continue
                target = (source.parent / unquote(url.path)).resolve()
                if not target.is_relative_to(ROOT) or not target.exists():
                    errors.append(f"原稿の参照先なし: {source.relative_to(sample.source)} -> {link}")
                markdown_count += 1
        folder = output / f"downloads/session-{sample.number}"
        actual = {p.relative_to(folder).as_posix() for p in folder.rglob("*") if p.is_file()}
        expected = set(sample.handouts)
        if actual != expected:
            errors.append(f"第{sample.number}回の配布一覧不一致: 不足={sorted(expected-actual)}, 余分={sorted(actual-expected)}")
        for name in expected:
            source, target = sample.handout_directory / name, folder / name
            if not source.is_file() or not target.is_file():
                errors.append(f"配布ファイルなし: 第{sample.number}回 {name}")
            elif source.read_bytes() != target.read_bytes():
                errors.append(f"配布内容不一致: 第{sample.number}回 {name}")
            handout_count += 1
    # 登録外の経路へコピーされた教員用ファイルも見つける。
    for path in output.rglob("*"):
        if path.is_file() and ("teacher" in path.relative_to(output).parts
                               or "reference" in path.stem
                               or path.name in {"verify.py", "verification.md", "measurement.md"}):
            errors.append(f"教員用ファイルの混入: {path.relative_to(output)}")
    errors.extend(check_previews(SAMPLES.values(), output))
    return errors, (len(pages), html_count, markdown_count, handout_count)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session", choices=[*SAMPLES, "all"], default="all")
    chosen = parser.parse_args().session
    samples = list(SAMPLES.values()) if chosen == "all" else [SAMPLES[chosen]]
    errors, (pages, html, markdown, handouts) = check_samples(samples)
    for error in errors:
        print(f"NG {error}")
    print(f"HTML {pages}ページ・ローカル参照 {html}件・原稿の参照 {markdown}件・配布 {handouts}件")
    print(f"{'FAIL' if errors else 'PASS'}: {len(errors)}件の問題")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
