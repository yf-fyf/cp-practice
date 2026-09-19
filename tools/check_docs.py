#!/usr/bin/env python3
"""新版の原稿・配布・表示構造を検査する。make site の後に実行する。"""
import argparse
import json
import subprocess
from course import ROOT, OUTPUT, SAMPLES
import check_lesson_template as template
from check_privacy import check_privacy, check_style_terms, NOTES
from check_publish import check_sources


def check_structure():
    errors, count = [], 0
    for sample in SAMPLES.values():
        template.results.clear()
        template.check_manuscript((sample.source / "lesson.md").read_text(encoding="utf-8"))
        page = OUTPUT / sample.lesson_page
        if not page.is_file():
            errors.append(f"HTML未生成: {sample.lesson_page}（先に make site）")
        else:
            template.check_html(page.read_text(encoding="utf-8"))
            template.check_css(template.CSS.read_text(encoding="utf-8"))
        count += len(template.results)
        errors += [f"第{sample.number}回 {key}: {detail}" for key, ok, detail in template.results if not ok]
    print(f"原稿・HTML・CSS {count}項目")
    return errors


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def check_markup():
    errors = []
    for sample in SAMPLES.values():
        for name, _, _ in sample.pages.values():
            path = sample.source / name
            ast = json.loads(subprocess.check_output(["pandoc", str(path), "--to=json"], text=True))
            for node in walk(ast):
                if node.get("t") == "CodeBlock" and not node["c"][0][1]:
                    errors.append(f"コードブロックの言語なし: {path.relative_to(ROOT)}")
                if node.get("t") == "Image" and not node["c"][1]:
                    errors.append(f"画像の代替テキストなし: {path.relative_to(ROOT)}")
    return errors


CHECKS = {"nav": check_sources, "structure": check_structure, "markup": check_markup,
          "style": check_style_terms, "publish": check_sources, "privacy": check_privacy}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", help="nav,structure,markup,style,publish,privacy のカンマ区切り")
    parser.add_argument("--list-checks", action="store_true")
    args = parser.parse_args()
    if args.list_checks:
        print("\n".join(CHECKS))
        return 0
    chosen = args.only.split(",") if args.only else ["structure", "markup", "style", "publish", "privacy"]
    if set(chosen) - CHECKS.keys():
        parser.error("未知の検査名: " + ", ".join(set(chosen) - CHECKS.keys()))
    failures = 0
    for name in chosen:
        NOTES.clear()
        errors = CHECKS[name]()
        for error in errors:
            print("NG", error)
        print(f"{name}: {'FAIL' if errors else 'PASS'} ({len(errors)}件)")
        failures += len(errors)
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
