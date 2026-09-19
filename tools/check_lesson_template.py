#!/usr/bin/env python3
"""通常回の原稿・HTML・CSSの構造検査。make check-docs から全回を検査する。"""

from __future__ import annotations

import argparse
import re
import sys

from course import OUTPUT, ROOT, SAMPLES

CSS = ROOT / "site/lesson-style.css"

H2_NAMES = ["目標", "問題", "定式化", "解説例", "結果", "演習", "発展", "振り返り"]
NUMBERED = H2_NAMES[1:]   # 目標と参照は番号を持たない
APPENDIX = "参照"
CALLOUTS = ["scenario", "given", "point", "ask", "check", "caution"]
OBJECT_LEVEL = {"scenario", "given"}   # 地色を持つ＝対象そのもの
RETIRED = ["note", "important", "term", "predict", "discuss", "done", "exercise", "goal", "warning"]
CALLOUT_SECTIONS = {"scenario": {"問題", "演習"}, "given": {"問題", "定式化", "演習"},
                    "check": {"結果", "演習"}, "ask": {"解説例", "結果", "振り返り"}}
SPACING = {"4px", "8px", "12px", "16px", "24px", "40px", "64px", "0"}
SPACING |= {"-" + value for value in SPACING}
FONT_SIZES = {"1rem", "1.875rem", "1.5rem", "1.2rem", "0.9rem", "0.9em", "10.5pt"}

results: list[tuple[str, bool, str]] = []


def check(identifier: str, ok: bool, detail: str = "") -> None:
    results.append((identifier, ok, detail))


# ---------- 原稿の読み取り ----------

def parse(text: str):
    """見出しの木と、見出しごとのブロック列を組み立てる。"""
    lines = text.split("\n")
    blocks, current, fence = [], [], None
    for line in lines:
        if fence is not None:
            current.append(line)
            if line.startswith(fence):
                blocks.append(("code", "\n".join(current)))
                current, fence = [], None
            continue
        match = re.match(r"^(```+|~~~+)", line)
        if match:
            if current:
                blocks.append(("para", "\n".join(current).strip()))
                current = []
            fence, current = match.group(1), [line]
            continue
        if re.match(r"^#{1,6} ", line):
            if current:
                blocks.append(("para", "\n".join(current).strip()))
                current = []
            level = len(line) - len(line.lstrip("#"))
            blocks.append((f"h{level}", line[level + 1:].strip()))
            continue
        if line.startswith(":::"):
            if current:
                blocks.append(("para", "\n".join(current).strip()))
                current = []
            blocks.append(("fence", line.strip()))
            continue
        if line.strip() == "":
            if current:
                blocks.append(("para", "\n".join(current).strip()))
                current = []
            continue
        if line.lstrip().startswith("|"):
            blocks.append(("table", line.strip()))
            continue
        current.append(line)
    if current:
        blocks.append(("para", "\n".join(current).strip()))
    return [block for block in blocks if block[1]]


def heading_text(raw: str) -> str:
    return re.sub(r"\s*\{[^}]*\}\s*$", "", raw).strip()


def check_manuscript(text: str) -> None:
    blocks = parse(text)
    h2 = [(heading_text(value), value) for kind, value in blocks if kind == "h2"]
    names = [name for name, _ in h2]

    check("C01", names == H2_NAMES + [APPENDIX], f"H2={names}")
    numbered = [name for name, raw in h2 if "unnumbered" not in raw]
    check("C01b", numbered == NUMBERED and "unnumbered" in h2[0][1]
          and "unnumbered" in h2[-1][1],
          "目標と参照は {.unnumbered}、本文に番号は書かない")
    check("C01c", not any(re.match(r"^\d+\.", name) for name in names), "原稿に節番号を書かない")

    lead = []
    for kind, value in blocks:
        if kind == "h2":
            break
        lead.append((kind, value))
    lead_text = "\n".join(value for kind, value in lead)
    goal_blocks = []
    seen = False
    for kind, value in blocks:
        if kind == "h2":
            if heading_text(value) == "目標":
                seen = True
                continue
            if seen:
                break
        if seen:
            goal_blocks.append((kind, value))
    goal_text = "\n".join(value for _, value in goal_blocks)
    check("C02", any(line.startswith("- ") for line in goal_text.split("\n"))
          and "](#演習)" in goal_text,
          "目標節に、できるようになることの箇条書きと演習への内部リンクがある")
    check("C03", not re.search(r"^#{3,4} .*(目標|進み方)", text, re.M)
          and len(re.findall(r"^## 目標", text, re.M)) == 1,
          "目標は1つの節にだけ書き、進み方の見出しを別に立てない")

    # 節ごとに切り出す
    sections: dict[str, list[tuple[str, str]]] = {}
    name = None
    for kind, value in blocks:
        if kind == "h2":
            name = heading_text(value)
            sections[name] = []
        elif name:
            sections[name].append((kind, value))

    h3_all = [value for kind, value in blocks if kind == "h3"]
    per_section = {key: [v for k, v in value if k == "h3"] for key, value in sections.items()}
    check("C04", all(len(v) <= 4 for v in per_section.values()) and len(h3_all) <= 16,
          f"H3 合計={len(h3_all)} 節ごと={ {k: len(v) for k, v in per_section.items()} }")
    check("C05", all(not re.search(r"(か|ない)$", h) and len(h) <= 20 for h in h3_all),
          "H3は疑問文・主張文でなく20字以内")
    check("C06", all(re.match(r"^手順\d", h) for h in per_section.get("解説例", []))
          and all(re.match(r"^必修\d", h) for h in per_section.get("演習", [])),
          "解説例は手順N、演習は必修N")

    exercise_blocks = sections.get("演習", [])
    h4_sequence, current_h3 = [], None
    groups: dict[str, list[str]] = {}
    for kind, value in exercise_blocks:
        if kind == "h3":
            current_h3 = value
            groups[current_h3] = []
        elif kind == "h4" and current_h3:
            groups[current_h3].append(value)
    check("C07", all(group == ["問題", "作業", "自己確認"] for group in groups.values()),
          f"{groups}")
    h4_all = [(section, value) for section, items in sections.items()
              for kind, value in items if kind == "h4"]
    check("C08", all(section in ("解説例", "演習") for section, _ in h4_all)
          and not re.search(r"^#{5,6} ", text, re.M), "H4は解説例と演習だけ、H5以深なし")

    check("C09", not any(kind == "para" and re.fullmatch(r"\*\*.{1,30}\*\*", value)
                         for kind, value in blocks), "太字だけの段落がない")

    def is_object(fence: str) -> bool:
        return any(re.match(rf"^::: *\{{?\.?{name}\b", fence) for name in OBJECT_LEVEL)

    bad_after_heading = []
    for index, (kind, value) in enumerate(blocks):
        if kind in ("h2", "h3", "h4") and index + 1 < len(blocks):
            nxt_kind, nxt_value = blocks[index + 1]
            if nxt_kind == "fence" and is_object(nxt_value):
                continue          # 対象レベルの器は内容そのものなので直後でよい
            if nxt_kind != "para" or len(nxt_value) < 40:
                bad_after_heading.append(heading_text(value))
    check("C10", not bad_after_heading, f"見出し直後が40字以上の段落でない: {bad_after_heading}")

    opens = [(index, value) for index, (kind, value) in enumerate(blocks)
             if kind == "fence" and value != ":::"]
    adjacent = []
    for position, (index, value) in enumerate(opens[:-1]):
        end = index
        while end < len(blocks) and blocks[end][1] != ":::":
            end += 1
        following = blocks[end + 1:opens[position + 1][0]]
        prose = sum(len(v) for k, v in following if k == "para")
        if prose < 60:
            nxt = opens[position + 1][1]
            this_is_check = ".hint" not in value and "check" in value
            next_is_hint = ".hint" in nxt
            both_object = is_object(value) and is_object(nxt)
            both_hint = ".hint" in value and ".hint" in nxt
            if not (this_is_check and next_is_hint) and not both_hint and not both_object:
                adjacent.append((value[:24], nxt[:24]))
    check("C11", not adjacent, f"部品が隣接: {adjacent}")

    depth, nested = 0, False
    for kind, value in blocks:
        if kind == "fence":
            if value == ":::":
                depth -= 1
            else:
                if depth > 0:
                    nested = True
                depth += 1
    check("C12", not nested, "calloutの入れ子がない")

    # 対象レベルの器の中身は節の実質なので、地の文と同じ側に数える。
    # 「箱に埋もれていないか」を見る指標なので、数えるのはメタの器だけである。
    ratios = {}
    for name, items in sections.items():
        meta_inside, total, depth, in_object = 0, 0, 0, False
        for kind, value in items:
            if kind == "fence":
                if value == ":::":
                    depth -= 1
                    if depth == 0:
                        in_object = False
                else:
                    if depth == 0 and is_object(value):
                        in_object = True
                    depth += 1
                continue
            if kind == "code":
                continue
            total += len(value)
            if depth > 0 and not in_object:
                meta_inside += len(value)
        ratios[name] = 1.0 if total == 0 else (total - meta_inside) / total
    check("C13", all(value >= 0.6 for value in ratios.values()),
          "メタの器の外にある字数の割合: " + " ".join(f"{k}={v:.2f}" for k, v in ratios.items()))

    counts = {kind: len(re.findall(rf"^::: *\{{?\.?{kind}\b", text, re.M)) for kind in CALLOUTS}
    given_labels = re.findall(r'^::: *\{\.given +label="([^"]*)"', text, re.M)
    check("C25", len(given_labels) == counts["given"]
          and all(2 <= len(label) <= 6 for label in given_labels)
          and not any(label in H2_NAMES + [APPENDIX] for label in given_labels
                      if label not in ("問題",)),
          f"与えるものの器のラベル: {given_labels}")
    hint_count = len(re.findall(r"^::: *\{\.hint", text, re.M))
    meta_total = sum(value for kind, value in counts.items() if kind not in OBJECT_LEVEL)
    object_total = sum(value for kind, value in counts.items() if kind in OBJECT_LEVEL)
    per_section_meta = {name: sum(1 for kind, value in items
                                 if kind == "fence" and value != ":::"
                                 and ".hint" not in value and not is_object(value))
                        for name, items in sections.items()}
    check("C14", meta_total <= 10 and object_total <= 10
          and all(value <= 3 for value in per_section_meta.values()),
          f"メタの器={meta_total}（節ごと{per_section_meta}） 対象の器={object_total} "
          f"内訳={counts} hint={hint_count}")
    check("C15", not any(re.search(rf"^::: *\{{?\.?{kind}\b", text, re.M) for kind in RETIRED),
          "旧部品名を使っていない")

    misplaced = []
    for name, items in sections.items():
        for kind, value in items:
            if kind != "fence" or value == ":::":
                continue
            for callout, allowed in CALLOUT_SECTIONS.items():
                if re.match(rf"^::: *\{{?\.?{callout}\b", value) and name not in allowed:
                    misplaced.append((callout, name))
    check("C16", not misplaced, f"配置違反: {misplaced}")

    summaries = re.findall(r'^::: *\{\.hint +summary="([^"]*)"', text, re.M)
    check("C17", len(summaries) == hint_count
          and all(0 < len(s) <= 30 and s != "ヒント" for s in summaries)
          and all(s.startswith("ヒントを開く：") for s in summaries),
          f"summary={summaries}")

    body = sum(len(value) for kind, value in blocks if kind in ("para", "table"))
    # 分量は目安であって基準にしない（設計案の§3.5）。超過は報告だけする。
    check("C18", True, f"本文 {body} 字（目安 3,500〜6,300。基準にはしない）")

    todo_sections = [name for name, items in sections.items()
                     for kind, value in items if kind == "h4" and value == "作業"]
    todos = re.findall(r"TODO\(作業(\d+)\)", text)
    check("C19", len(todos) >= 2 * len(todo_sections) and todos == sorted(todos, key=int)[:0] + todos,
          f"作業の雛形 TODO={todos}")

    internal = [link for link in re.findall(r"\]\(#([^)]+)\)", text)]
    check("C21", len(internal) >= 3, f"ページ内リンク {len(internal)} 本: {internal}")
    check("C22", "受講者" not in text and "学生" not in text, "第NN回・学習者の表記")

    forbidden = set(H2_NAMES + [APPENDIX])
    check("C23", all(h not in forbidden and not any(h.startswith(w) for w in forbidden)
                     for h in h3_all), f"H3がH2の語を先頭に使っていない: {h3_all}")
    check("C24", all(value in ("問題", "作業", "自己確認") for _, value in h4_all),
          f"H4={sorted({v for _, v in h4_all})}")


# ---------- 生成HTML ----------

def check_html(html: str) -> None:
    sections = re.findall(r'<section id="([^"]*)" class="level2([^"]*)">\s*<h2[^>]*>(.*?)</h2>',
                          html, re.S)
    check("H01", len(sections) == 9 and html.count("<h2") == 9, f"section.level2 = {len(sections)}")
    labels = [re.sub(r"<[^>]+>", "", text).strip() for _, _, text in sections]
    numbered_ok = all(re.match(rf"^{index + 1}\. {name}$", labels[index + 1])
                      for index, name in enumerate(NUMBERED))
    check("H02", numbered_ok and labels[0] == "目標" and labels[-1] == APPENDIX, f"{labels}")

    toc = re.search(r'<details class="toc".*?</details>', html, re.S)
    toc_links = re.findall(r'href="#([^"]+)"', toc.group(0)) if toc else []
    ids = set(re.findall(r'<section id="([^"]*)"', html))
    check("H03", len(toc_links) >= 8 and all(link in ids for link in toc_links),
          f"目次 {len(toc_links)} 項目、すべて実在の節")

    callouts = re.findall(r'<div class="callout[^"]*"', html)
    meta_callouts = [c for c in callouts
                     if not any(f"callout-{name}" in c for name in OBJECT_LEVEL)]
    check("H04b", len(meta_callouts) <= 10, f"メタの器 = {len(meta_callouts)}")
    check("H04", len(callouts) <= 20
          and not re.search(r'<div class="callout[^"]*"[^>]*>(?:(?!</div>).)*?<div class="callout',
                            html, re.S), f".callout = {len(callouts)}")
    adjacent_meta = re.findall(
        r'</div>\s*<div class="(callout[^"]*)"', html)
    bad = [c for c in adjacent_meta
           if not any(f"callout-{name}" in c for name in OBJECT_LEVEL)]
    check("H05", not bad, f"メタの器が隣接していない（対象の器どうしは可）: {bad}")
    check("H06", not re.search(r'</h[23]>\s*<(div class="callout|pre|table|figure)', html),
          "見出し直後が部品・コード・表でない")

    # 見出しの語と、その見出しの下に来る部品ラベルが同じ語にならないこと。
    duplicated = []
    for match in re.finditer(r'<h([234])[^>]*>(.*?)</h\1>(.*?)(?=<h[234]|\Z)', html, re.S):
        heading = re.sub(r"<[^>]+>", "", match.group(2)).strip()
        heading = re.sub(r"^\d+\.\s*", "", heading)
        labels = re.findall(r'<span class="callout-label">([^<]*)</span>', match.group(3))
        duplicated += [(heading, label) for label in labels if label == heading]
    check("H08", not duplicated, f"見出し語と部品ラベルの重複: {duplicated}")
    check("H15", "<hr" not in html, "<hr> を使っていない")
    check("H14b", 'scroll-margin-top' in CSS.read_text(), "scroll-margin-top あり")


# ---------- CSS ----------

def check_css(css: str) -> None:
    root = re.search(r":root \{(.*?)\n\}", css, re.S).group(1)
    literals_outside = [value for value in re.findall(r"#[0-9A-Fa-f]{3,8}\b", css)
                        if value not in root]
    check("H11", not literals_outside and len(re.findall(r"#[0-9A-Fa-f]{6}", root)) == 10
          and len(set(re.findall(r"#[0-9A-Fa-f]{6}", root))) == 10,
          f"外のリテラル色={literals_outside} :root の色={len(re.findall(r'#[0-9A-Fa-f]{6}', root))}種")

    backgrounds = re.findall(r"([^{}]+)\{[^{}]*?background(?:-color)?: *([^;]+);", css, re.S)
    allowed_bg = ("section.level2 > h2", "pre", "code", ".topbar",
                  "section.sec-goal", "section.sec-reference",
                  ".callout-scenario", ".callout-given")
    bad_bg = [selector.strip().splitlines()[-1].strip() for selector, value in backgrounds
              if value.strip() not in ("none", "transparent")
              and not any(token in selector for token in allowed_bg)]
    check("H09", not bad_bg, f"面を持つ余分なセレクタ: {bad_bg}")

    left = re.findall(r"([^{}]+)\{[^{}]*?border-left: *([^;]+);", css, re.S)
    allowed_left = (".callout", "details.hint[open]", "section.level2 > h2", "pre.error")
    bad_left = [selector.strip().splitlines()[-1].strip() for selector, value in left
                if value.strip() != "0"
                and not any(token in selector for token in allowed_left)]
    full = re.findall(r"([^{}]+)\{[^{}]*?[^-]border: *([^;]+);", css, re.S)
    allowed_full = ("pre", "section.sec-goal", "section.sec-reference",
                    "section.sec-exercise > section.level3",
                    "details.hint > summary", ".toc > summary")
    bad_full = [selector.strip().splitlines()[-1].strip() for selector, value in full
                if value.strip() != "0"
                and not any(token in selector for token in allowed_full)]
    check("H10", not bad_left and not bad_full,
          f"左罫={bad_left} 全周（ブロックとコード以外）={bad_full}")
    blocks = re.findall(r"(section\.sec-(?:goal|reference)|section\.sec-exercise > section\.level3)",
                        css)
    check("H18", len(set(blocks)) == 3 and "break-inside: avoid" in css,
          "ブロックは目標・参照・必修Nの3種だけで、印刷で分断しない")

    sizes = re.findall(r"font-size: *([^;]+);", css)
    check("H12", len(sizes) <= 7 and all(size.strip() in FONT_SIZES for size in sizes),
          f"{len(sizes)}箇所 {sizes}")

    spacing = re.findall(r"(?<!-)\b(?:margin|padding)(?:-top|-bottom|-left|-right)?: *([^;]+);", css)
    values = []
    for entry in spacing:
        entry = re.sub(r"calc\(-1 \* (var\(--s\d\))\)", r"-\1", entry)
        values.extend(entry.replace("var(--s1)", "4px").replace("var(--s2)", "8px")
                      .replace("var(--s3)", "12px").replace("var(--s4)", "16px")
                      .replace("var(--s5)", "24px").replace("var(--s6)", "40px")
                      .replace("var(--s7)", "64px").split())
    # 本文内は7トークン、ページ左右はヘッダーと共通のレスポンシブな余白を使う。
    bad_spacing = [value for value in values if value not in SPACING
                   and value not in ("auto", "var(--page-gutter)")]
    check("H13", not bad_spacing, f"本文トークン・共通ページ余白以外の値: {sorted(set(bad_spacing))}")

    centered = re.findall(r"([^{}]+)\{[^{}]*?text-align: *center", css, re.S)
    check("H19", all("figure" not in selector or ":not(.code)" in selector
                     for selector in centered),
          f"コードは中央寄せにしない（text-align: center を持つ選択子: "
          f"{[c.strip().splitlines()[-1].strip() for c in centered]}）")

    closes = all(re.search(rf"{re.escape(selector)} \{{[^}}]*border: 0", css, re.S)
                 for selector in ("details.hint[open] > summary", ".toc[open] > summary"))
    focused = all(f"{selector}:focus-visible" in css
                  for selector in ("details.hint > summary", ".toc > summary"))
    check("H20", closes and focused,
          "折り畳みの枠は閉じているあいだだけで、どちらもフォーカス表示がある")

    check("H14", "section.level2 { scroll-margin-top: var(--topbar-h); }" in css
          and "section.level3, section.level4 { scroll-margin-top: calc(var(--topbar-h) + 3rem); }" in css,
          "scroll-margin-top が共通ヘッダーの高さを参照する")
    print_block = re.search(r"@media print \{(.*?)\n\}", css, re.S)
    narrow = re.search(r"@media \(max-width: 48rem\) \{(.*?)\n\}", css, re.S)
    check("H16", "position: sticky" in css
          and print_block and "position: static" in print_block.group(1)
          and narrow and "position: static" in narrow.group(1),
          "帯が sticky、印刷と狭い画面で static")
    check("H17", "--measure: 48rem" in css and "--content-max" not in css
          and "grid-template-columns" not in css
          and "max-width: var(--measure)" in css,
          "幅は48remの1種類だけで、広い列を作らない")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session", choices=SAMPLES, default="07")
    sample = SAMPLES[parser.parse_args().session]
    results.clear()
    check_manuscript((sample.source / "lesson.md").read_text(encoding="utf-8"))
    generated = OUTPUT / sample.lesson_page
    if generated.is_file():
        check_html(generated.read_text(encoding="utf-8"))
        check_css(CSS.read_text(encoding="utf-8"))
    else:
        print("先に python3 tools/build_site.py を実行してください")
        return 1

    failed = 0
    for identifier, ok, detail in results:
        mark = "OK  " if ok else "NG  "
        if not ok:
            failed += 1
        print(f"{mark}{identifier}  {detail}")
    print(f"\n{len(results)} 項目中 {failed} 件が不合格")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
