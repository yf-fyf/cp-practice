#!/usr/bin/env python3
"""教材サイトを生成・配信・検査する。make site / serve / check-links の入口。"""
import argparse
import html
from pathlib import Path
import shutil
import tempfile

from course import ROOT, OUTPUT, SAMPLES
from render_course import build
from course_home import homepage
from check_lesson_links import check_samples
from check_publish import check_sources


def output_directory(path):
    output = path.resolve()
    # 出力は毎回置き換えるため、ソースや親ディレクトリを指定させない。
    if output == ROOT or ROOT.is_relative_to(output):
        raise ValueError("ソースとその親を出力先にはできません")
    if output.is_relative_to(ROOT) and output.parts[len(ROOT.parts)] not in {".site", ".pages"}:
        raise ValueError("リポジトリ内の出力先は .site/ または .pages/ を使ってください")
    if path.is_symlink():
        raise ValueError("出力先にシンボリックリンクは使えません")
    return output


def generate(output, release=None, revision=None):
    output = output_directory(output)
    errors = check_sources()
    if errors:
        raise ValueError("\n".join(errors))
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".course-build-", dir=output.parent) as temporary:
        generated = Path(temporary) / "site"
        if build("all", generated, website=True):
            raise ValueError("生成時の警告を確認してください")
        homepage(generated)
        legal = generated / "legal"
        legal.mkdir()
        for name in ("LICENSE", "LICENSE-MATERIALS", "THIRD_PARTY_NOTICES.md"):
            shutil.copyfile(ROOT / name, legal / name)
        for page in generated.rglob("*.html"):
            base = "../" * (len(page.relative_to(generated).parts) - 1)
            footer = (f'<p><a href="{base}legal/LICENSE-MATERIALS">教材のライセンス</a> · '
                      f'<a href="{base}legal/THIRD_PARTY_NOTICES.md">第三者ソフトウェア</a></p>')
            if release:
                footer += f"<p>Release {html.escape(release)} · {html.escape(revision or 'working tree')}</p>"
                if page == generated / "index.html":
                    footer += (f'<p><a href="downloads/cp-practice-workbook-{html.escape(release, quote=True)}.zip">'
                               '演習ファイルをまとめてダウンロード</a></p>')
            page.write_text(page.read_text(encoding="utf-8").replace("</footer>", footer + "</footer>"), encoding="utf-8")
        if output.exists():
            shutil.rmtree(output)
        shutil.move(str(generated), str(output))


def check_links(output):
    errors, counts = check_samples(list(SAMPLES.values()), output)
    for error in errors:
        print("NG", error)
    print(f"HTML {counts[0]}ページ・参照 {counts[1]}件・原稿参照 {counts[2]}件・配布 {counts[3]}件")
    print(f"{'FAIL' if errors else 'PASS'}: {len(errors)}件の問題")
    return int(bool(errors))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--serve", action="store_true")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--no-watch", action="store_true")
    parser.add_argument("--check-links", action="store_true")
    parser.add_argument("--release")
    parser.add_argument("--revision")
    args = parser.parse_args()
    try:
        if args.check_links:
            return check_links(args.output)
        if args.release:
            from build_pages import safe_version
            safe_version(args.release)
        generate(args.output, args.release, args.revision)
        if args.serve:
            from serve_site import serve, resolve_host
            return serve(args.output.resolve(), resolve_host(args.host), args.port, not args.no_watch)
    except (OSError, ValueError, RuntimeError) as error:
        print(f"FAIL: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
