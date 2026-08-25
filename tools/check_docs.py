#!/usr/bin/env python3
"""
原稿・配布物の整合を機械的に検査する。

使い方:
    python3 tools/check_docs.py                    # 既定のチェックをすべて実行
    python3 tools/check_docs.py --only nav,style   # 一部だけ実行（カンマ区切り）
    python3 tools/check_docs.py --list-checks      # チェックの一覧を表示
    python3 tools/check_docs.py --list-allowed     # 除外リストの内容を一覧表示
    python3 tools/check_docs.py --list-kinds       # 除外リストに書ける検出種別を表示

チェック一覧:
    frontmatter 各回の原稿に session / track / description / introduces / requires が
                あり、型が正しく、session が 1〜15 の範囲で重複していないか
    nav         site/nav.yaml に載っていない materials/**/*.md がないか。
                逆に nav.yaml の登録先に実体があるか
    structure   基礎回（01〜10）に「この回の目標」「必須演習」「完了チェック」の
                H2 があるか。自由課題回（11〜15）は簡略形なので「この回の目標」
                「今回やること」「支援物」「チェックポイント」を見る。
                どちらもその種類の標準の並び順に沿っているか
    codeblock   すべてのコードブロックに言語名が付いているか。console ブロックに
                実行結果が混ざっていないか
    figure      すべての画像に代替テキストがあり、参照先の SVG が実在するか
    style       表記の統一（回は「第NN回」の2桁ゼロ埋め、学ぶ人の呼称は「学習者」）
    publish     公開物への教員用資産の混入防止（teacher を含むパス、
                answer / solution / rubric を含むファイル名、非公開側への相対リンク）
    privacy     個人情報・環境固有識別子の検出（/home/ で始まる絶対パス、
                IP アドレス、学籍番号らしき連続数字）
    numbers     派生する数値（演習ファイルの本数、コード行数）を本文に書いていないか
    concepts    用語初出台帳 design/glossary-ledger.md と各回の introduces / requires が
                一致しているか。同じ概念を二度「初出」していないか。未導入の概念を
                先取りしていないか
    glossary    台帳の用語が materials/references/glossary.md に項目を持ち、
                初出回への案内があるか。用語集に台帳外の項目がないか

内部リンクの検査は tools/build_site.py --check-links（make check-links）が行う。

除外リストは tools/doc_check_allowlist.yaml。理由は各エントリの reason に書く。
除外は「ファイル + 行の内容（match） + 検出種別（check）」の3点で指定する。
依存: PyYAML（tools/build_site.py と共通）。
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_site import ROOT, load_nav, strip_frontmatter  # noqa: E402

ALLOWLIST_PATH = Path(__file__).resolve().parent / "doc_check_allowlist.yaml"

MATERIALS = ROOT / "materials"
MATERIALS_SESSIONS = MATERIALS / "sessions"
FIGURES = MATERIALS / "figures"
WORKBOOK = ROOT / "workbook"
DESIGN = ROOT / "design"

# 生成物・依存物は検査しない。vendor/ は同梱した第三者ソフトウェア
# （web/prolog/vendor/tau-prolog/）の置き場で、こちらが書いた文章ではない。
# 中身の素性は THIRD_PARTY_NOTICES.md で管理し、公開物への混入は
# tools/build_pages.py の verify_output() が公開ツリー全体で検査する。
SKIP_DIRNAMES = {".git", ".site", ".pages", "_build", "__pycache__",
                 "node_modules", "vendor"}

# 検査対象にする素のテキストの拡張子
TEXT_SUFFIXES = {".md", ".py", ".mzn", ".dzn", ".pl", ".txt", ".yaml", ".yml",
                 ".tex", ".lua", ".css", ".js", ".html"}

# チェックの途中で出す補足（違反ではない）。各チェックの先頭で clear される。
NOTES: list[str] = []


class Violation:
    def __init__(self, path: Path, line: int, message: str):
        self.path = path
        self.line = line
        self.message = message

    @property
    def relpath(self) -> str:
        try:
            return self.path.relative_to(ROOT).as_posix()
        except ValueError:
            return self.path.as_posix()

    def __str__(self) -> str:
        return f"{self.relpath}:{self.line}: {self.message}"


# ── 除外リスト ──────────────────────────────────────────────
#
# 除外リストに書ける検出種別。セクションごとに閉じた集合として持ち、綴り違いを
# その場で違反にする。ここに無い種別を書いた除外は「効かない除外」になるが、
# それは死んだ除外としてしか現れず原因が分かりにくいので明示的に弾く。

ALLOWLIST_KINDS: dict[str, set[str]] = {
    "style_terms": {"dai-kai-zero-pad", "gakusei", "jukousha"},
    "privacy": {"home-path", "ip-address", "long-digits"},
    "numbers": {"derived-count"},
    "codeblock": {"no-language", "console-mixed"},
}


def _load_allowlist_section(section: str) -> list[dict]:
    if not ALLOWLIST_PATH.is_file():
        return []
    with ALLOWLIST_PATH.open(encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data.get(section) or []


class Allowlist:
    """除外リスト。行番号ではなく「行の内容 + 検出種別」で照合する。

    行番号で留めると、上の行を1行足し引きしただけで除外が外れて誤検出になり、
    逆にずれた先に別の違反があれば黙って握り潰す。そこで `match`（その行に
    必ず含まれる文字列）で照合する。

    さらに、1行が複数の検出種別に引っかかることがあるので、`check`（検出種別。
    文字列またはその配列）を必須にし、名指しした種別だけを除外する。

    一度も一致しなかったエントリは「死んだ除外」として違反にする。本文を直して
    対象語が消えたのにエントリだけ残る状態を、このチェック自身が見つけるため。
    """

    def __init__(self, section: str):
        self.section = section
        self.entries = _load_allowlist_section(section)
        self._used: set[int] = set()
        self.malformed: list[tuple[dict, str]] = []
        known = ALLOWLIST_KINDS.get(section, set())
        self._kinds: list[set[str]] = []
        for entry in self.entries:
            raw = entry.get("check")
            if raw is None:
                self._kinds.append(set())
                self.malformed.append((entry, "check（検出種別）が無い"))
                continue
            kinds = {raw} if isinstance(raw, str) else set(raw)
            unknown = sorted(kinds - known)
            if unknown:
                self.malformed.append(
                    (entry, f"未知の検出種別: {', '.join(unknown)}"
                            f"（使えるのは {', '.join(sorted(known))}）"))
            self._kinds.append(kinds)

    def matches(self, rel: str, line: str, kind: str) -> bool:
        hit = False
        for idx, entry in enumerate(self.entries):
            if entry.get("file") != rel:
                continue
            if kind not in self._kinds[idx]:
                continue
            needle = entry.get("match")
            if not needle or needle not in line:
                continue
            self._used.add(idx)
            hit = True
        return hit

    def unused(self) -> list[dict]:
        return [e for i, e in enumerate(self.entries) if i not in self._used]

    def dead_violations(self) -> list[Violation]:
        """書式不備の除外と、一度も一致しなかった除外エントリを違反として返す。"""
        out: list[Violation] = []
        for entry, why in self.malformed:
            out.append(Violation(
                ALLOWLIST_PATH, 0,
                f"除外エントリの書式不備（{self.section}）: "
                f"{entry.get('file', '?')} / 「{entry.get('match', '')}」: {why}"))
        for entry in self.unused():
            out.append(Violation(
                ALLOWLIST_PATH, 0,
                f"死んだ除外（{self.section}）: {entry.get('file', '?')} の検出種別 "
                f"{entry.get('check', '?')} に「{entry.get('match', '')}」が"
                "見つからない。本文を直したならこのエントリを消す"))
        return out


# ── 共通の走査 ──────────────────────────────────────────────

def iter_files(bases, suffixes=None):
    """SKIP_DIRNAMES を避けて、指定したディレクトリ／ファイルの下を歩く。"""
    for base in bases:
        if base.is_file():
            yield base
            continue
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            if not path.is_file():
                continue
            if any(part in SKIP_DIRNAMES for part in path.relative_to(ROOT).parts):
                continue
            if suffixes and path.suffix not in suffixes:
                continue
            yield path


def read_lines(path: Path) -> list[str] | None:
    try:
        return path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return None


def session_manuscripts() -> list[Path]:
    return sorted(MATERIALS_SESSIONS.glob("*.md"))


# 地の文を照合するとき、コードや URL を巻き込まないための遮蔽。
_MASK_SPAN_RE = re.compile(r"`[^`]*`")
_MASK_LINKTARGET_RE = re.compile(r"\]\([^)]*\)")
_MASK_URL_RE = re.compile(r"\bhttps?://\S+")


def mask_protected(line: str) -> str:
    """インラインコード・リンク先・URL を伏せ字にする（長さは保つ）。"""
    for pattern in (_MASK_SPAN_RE, _MASK_LINKTARGET_RE, _MASK_URL_RE):
        line = pattern.sub(lambda m: "　" * len(m.group(0)), line)
    return line


def parse_frontmatter(path: Path) -> tuple[dict | None, str | None]:
    """先頭の YAML frontmatter を返す。無ければ (None, None)、壊れていれば (None, 理由)。"""
    lines = read_lines(path)
    if not lines or lines[0].strip() != "---":
        return None, None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            try:
                data = yaml.safe_load("\n".join(lines[1:i])) or {}
            except yaml.YAMLError as error:
                return None, f"frontmatter の YAML が壊れている: {error}"
            if not isinstance(data, dict):
                return None, "frontmatter が辞書になっていない"
            return data, None
    return None, "frontmatter の終わりの --- が無い"


# ── frontmatter ─────────────────────────────────────────────

FRONTMATTER_REQUIRED = {
    "session": int,
    "track": str,
    "description": str,
    "introduces": list,
    "requires": list,
}
TRACKS = {"prolog", "minizinc", "z3", "project", "presentation"}
SESSION_COUNT = 15


def check_frontmatter() -> list[Violation]:
    violations: list[Violation] = []
    seen: dict[int, str] = {}

    for path in session_manuscripts():
        data, error = parse_frontmatter(path)
        if error:
            violations.append(Violation(path, 1, error))
            continue
        if data is None:
            violations.append(Violation(path, 1, "frontmatter が無い"))
            continue
        for key, kind in FRONTMATTER_REQUIRED.items():
            if key not in data:
                violations.append(Violation(path, 1, f"frontmatter に {key} が無い"))
            elif not isinstance(data[key], kind):
                violations.append(Violation(
                    path, 1,
                    f"frontmatter の {key} の型が違う"
                    f"（{kind.__name__} を期待、実際は {type(data[key]).__name__}）"))
        track = data.get("track")
        if isinstance(track, str) and track not in TRACKS:
            violations.append(Violation(
                path, 1,
                f"frontmatter の track が未知の値: {track}"
                f"（使えるのは {', '.join(sorted(TRACKS))}）"))
        number = data.get("session")
        if isinstance(number, int):
            if not 1 <= number <= SESSION_COUNT:
                violations.append(Violation(
                    path, 1, f"session が 1〜{SESSION_COUNT} の外にある: {number}"))
            elif number in seen:
                violations.append(Violation(
                    path, 1, f"session {number} が {seen[number]} と重複している"))
            else:
                seen[number] = path.name
            # ファイル名の先頭2桁と session が食い違うと、URL と回番号がずれる
            stem_number = path.stem[:2]
            if stem_number.isdigit() and int(stem_number) != number:
                violations.append(Violation(
                    path, 1,
                    f"ファイル名の回番号（{stem_number}）と session（{number}）が違う"))

    missing = [n for n in range(1, SESSION_COUNT + 1) if n not in seen]
    NOTES.append(f"原稿がある回: {len(seen)} / {SESSION_COUNT}")
    if missing:
        NOTES.append("未執筆の回（違反ではない）: "
                     + ", ".join(f"第{n:02d}回" for n in missing))
    return violations


# ── nav ─────────────────────────────────────────────────────

def check_nav_listing() -> list[Violation]:
    """nav.yaml と materials/ の突合。

    nav.yaml に載せ忘れた原稿はサイトに出ないので、書いたのに読めない状態になる。
    逆に nav.yaml が実体の無いパスを指していると build_site.py が落ちる。
    """
    nav = load_nav()
    nav_path = ROOT / "site" / "nav.yaml"
    violations: list[Violation] = []

    listed: list[str] = []
    for section in nav.get("sections") or []:
        for entry in section.get("pages") or []:
            listed.append(entry)
            if not (ROOT / entry).is_file():
                violations.append(Violation(
                    nav_path, 1, f"nav.yaml の登録先に実体がない: {entry}"))
    listed_set = set(listed)

    found = {p.relative_to(ROOT).as_posix() for p in MATERIALS.glob("*/*.md")}
    for item in sorted(found - listed_set):
        violations.append(Violation(
            nav_path, 1,
            f"nav.yaml に未掲載: {item}"
            "（書いた原稿はサイトに出ない。該当セクションに1行足す）"))

    duplicated = sorted({p for p in listed if listed.count(p) > 1})
    for item in duplicated:
        violations.append(Violation(nav_path, 1, f"nav.yaml に重複して載っている: {item}"))

    NOTES.append(f"nav.yaml 掲載 {len(listed_set)} ページ / materials の原稿 {len(found)} 本")
    return violations


# ── structure ───────────────────────────────────────────────

# site/boxes.lua の GOAL_HEADING と揃える。片方を変えたらもう片方も直す。
GOAL_HEADING = "この回の目標"

# 基礎回（第01〜10回）に必ずある H2。自由課題回（第11〜15回）は演習3段階を
# 持たないので、下の PROJECT_REQUIRED_H2 のほうを見る。
REQUIRED_H2 = (GOAL_HEADING, "必須演習", "完了チェック")

# 自由課題・発表会（第11〜15回）に必ずある H2。
# これらの回は各自の題材で進めるので、共通の演習も共通の完了チェックも置けない。
# 代わりに curriculum-2026.md §13.3 のチェックポイントが完了条件になる。
PROJECT_REQUIRED_H2 = (GOAL_HEADING, "今回やること", "支援物", "チェックポイント")

# 基礎回（第01〜10回）の H2 標準列。ここに無い H2（第05・06回の「理論概説」など）は
# 途中に入れてよい。並び順だけを見る。
STANDARD_H2 = (
    GOAL_HEADING,
    "前提と準備",
    "今回解く問題",
    "変数・定義域・制約・目的へ分解",
    "概念と構文",
    "小さな実行例",
    "予想してから試す",
    "必須演習",
    "標準演習",
    "発展演習",
    "よくある誤り",
    "完了チェック",
    "扱わないこと",
    "次回への接続",
)
BASIC_SESSIONS = range(1, 11)

# 自由課題回（第11〜15回）の H2 標準列。第15回だけは送り先が次の回ではないので、
# 末尾の「次回への接続」を持たない（代わりに「この科目のあと」を置く）。
# 並び順だけを見るので、末尾が欠けていても違反にはならない。
PROJECT_H2 = (
    GOAL_HEADING,
    "今回やること",
    "支援物",
    "チェックポイント",
    "扱わないこと",
    "次回への接続",
)
PROJECT_SESSIONS = range(11, 16)

H2_RE = re.compile(r"^##\s+(.+?)\s*$")
FENCE_RE = re.compile(r"^\s*(?:```|~~~)")


def headings(lines: list[str], level_prefix: str = "## ") -> list[tuple[int, str]]:
    """コードブロックの中を除いた見出しの一覧 [(行番号, 見出し文字列)]。"""
    out: list[tuple[int, str]] = []
    in_fence = False
    for i, line in enumerate(lines, 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if line.startswith(level_prefix) and not line.startswith(level_prefix + "#"):
            out.append((i, line[len(level_prefix):].strip()))
    return out


def check_structure() -> list[Violation]:
    violations: list[Violation] = []
    checked = 0

    for path in session_manuscripts():
        lines = read_lines(path)
        if lines is None:
            continue
        body = strip_frontmatter(lines)
        offset = len(lines) - len(body)
        found = [(i + offset, text) for i, text in headings(body)]
        names = [text for _, text in found]

        data, _ = parse_frontmatter(path)
        number = (data or {}).get("session")

        # 回の種類で必須の H2 と標準の並びが違う。自由課題回（第11〜15回）は
        # 演習3段階を持たない簡略形である（design/maintaining.md の標準構成）。
        if isinstance(number, int) and number in PROJECT_SESSIONS:
            required_h2, standard_h2 = PROJECT_REQUIRED_H2, PROJECT_H2
        else:
            required_h2, standard_h2 = REQUIRED_H2, STANDARD_H2

        for required in required_h2:
            if required not in names:
                violations.append(Violation(
                    path, 1, f"H2「{required}」が無い"))

        if isinstance(number, int) and (number in BASIC_SESSIONS
                                        or number in PROJECT_SESSIONS):
            # 標準列に含まれる H2 だけを取り出し、その並びが標準列の
            # 部分列になっているかを見る（余分な H2 の追加は許す）
            sequence = [n for n in names if n in standard_h2]
            expected = iter(standard_h2)
            for name in sequence:
                if not any(name == candidate for candidate in expected):
                    line = next(i for i, text in found if text == name)
                    violations.append(Violation(
                        path, line,
                        f"H2「{name}」の位置が標準の並びと違う"
                        "（design/maintaining.md の各回の標準構成を参照）"))
                    break
        checked += 1

    NOTES.append(f"{checked} 本の各回原稿の見出し構成を確認した")
    return violations


# ── codeblock ───────────────────────────────────────────────

FENCE_OPEN_RE = re.compile(r"^(?P<indent>\s*)```(?P<info>.*)$")
INFO_LANG_RE = re.compile(r"^\{?\.?([A-Za-z0-9_+-]+)")
# console ブロックに書いてよい行。プロンプト・継続行・コメント・空行だけ。
CONSOLE_OK_RE = re.compile(r"^\s*(?:[$#>]\s|#|$)")


def check_code_blocks() -> list[Violation]:
    violations: list[Violation] = []
    allowlist = Allowlist("codeblock")
    blocks = 0

    for path in iter_files([MATERIALS, WORKBOOK], {".md"}):
        lines = read_lines(path)
        if lines is None:
            continue
        rel = path.relative_to(ROOT).as_posix()
        i = 0
        while i < len(lines):
            opened = FENCE_OPEN_RE.match(lines[i])
            if not opened:
                i += 1
                continue
            info = opened.group("info").strip()
            start = i + 1
            # 閉じフェンスを探す
            j = start
            while j < len(lines) and not re.match(r"^\s*```\s*$", lines[j]):
                j += 1
            body = lines[start:j]
            blocks += 1

            match = INFO_LANG_RE.match(info)
            lang = match.group(1) if match else None
            if not lang:
                if not allowlist.matches(rel, lines[i], "no-language"):
                    violations.append(Violation(
                        path, i + 1,
                        "コードブロックに言語名が無い"
                        "（text / console / solver など、区分が分かる綴りを付ける）"))
            elif lang == "console":
                bad = [(start + k + 1, line) for k, line in enumerate(body)
                       if not CONSOLE_OK_RE.match(line)]
                if bad and not allowlist.matches(rel, lines[i], "console-mixed"):
                    line_no, sample = bad[0]
                    violations.append(Violation(
                        path, line_no,
                        "console ブロックに実行結果らしい行が混ざっている"
                        f"（出力は別のブロックに分ける）: {sample.strip()[:40]}"))
            i = j + 1

    violations.extend(allowlist.dead_violations())
    NOTES.append(f"{blocks} 個のコードブロックを確認した")
    return violations


# ── figure ──────────────────────────────────────────────────

IMAGE_RE = re.compile(r"!\[(?P<alt>[^\]]*)\]\((?P<src>[^)\s]+)(?:\s+\"[^\"]*\")?\)")


def check_figures() -> list[Violation]:
    violations: list[Violation] = []
    images = 0

    for path in iter_files([MATERIALS, WORKBOOK], {".md"}):
        lines = read_lines(path)
        if lines is None:
            continue
        for i, line in enumerate(lines, 1):
            for match in IMAGE_RE.finditer(line):
                images += 1
                alt = match.group("alt").strip()
                src = match.group("src")
                if not alt:
                    violations.append(Violation(
                        path, i,
                        f"画像に代替テキストが無い: {src}"
                        "（図が見えない読者にも内容が伝わる文を書く）"))
                elif len(alt) < 10:
                    violations.append(Violation(
                        path, i,
                        f"画像の代替テキストが短すぎる（{alt}）: {src}"
                        "（何を表す図かが分かる文にする）"))
                if src.startswith(("http://", "https://", "data:")):
                    continue
                # 原稿は figures/<name>.svg の相対参照で書く（boxes.lua が書き換える）
                name = src.split("figures/", 1)[-1] if "figures/" in src else src
                target = FIGURES / name
                if not target.is_file():
                    violations.append(Violation(
                        path, i,
                        f"参照先の図が無い: materials/figures/{name}"
                        "（make figures で生成してコミットする）"))

    orphans = [p.name for p in sorted(FIGURES.glob("*.svg"))
               if not (FIGURES / p.name).with_suffix(".tex").is_file()]
    for name in orphans:
        NOTES.append(f"TikZ ソースの無い SVG（手描きの図か、消し忘れ）: {name}")

    NOTES.append(f"{images} 個の画像参照を確認した")
    return violations


# ── style ───────────────────────────────────────────────────

# 回の呼称は「第NN回」の2桁ゼロ埋め（site-plan-2026.md §9.0-20）
STYLE_DAI_KAI_RE = re.compile(r"第[0-9]回")
# 学ぶ人の呼称は「学習者」に統一する
STYLE_GAKUSEI_RE = re.compile(r"学生")
STYLE_JUKOUSHA_RE = re.compile(r"受講者")

STYLE_TARGETS = (MATERIALS, WORKBOOK, DESIGN, ROOT / "README.md")


def check_style_terms() -> list[Violation]:
    violations: list[Violation] = []
    allowlist = Allowlist("style_terms")
    checked = 0

    for path in iter_files(STYLE_TARGETS, {".md"}):
        lines = read_lines(path)
        if lines is None:
            continue
        rel = path.relative_to(ROOT).as_posix()
        checked += 1
        for i, line in enumerate(lines, 1):
            masked = mask_protected(line)
            if (STYLE_DAI_KAI_RE.search(masked)
                    and not allowlist.matches(rel, line, "dai-kai-zero-pad")):
                violations.append(Violation(
                    path, i,
                    f"回の呼称が2桁ゼロ埋めでない（第NN回にする）: {line.strip()[:60]}"))
            if (STYLE_GAKUSEI_RE.search(masked)
                    and not allowlist.matches(rel, line, "gakusei")):
                violations.append(Violation(
                    path, i,
                    f"「学生」表記の残存（「学習者」を使う）: {line.strip()[:60]}"))
            if (STYLE_JUKOUSHA_RE.search(masked)
                    and not allowlist.matches(rel, line, "jukousha")):
                violations.append(Violation(
                    path, i,
                    f"「受講者」表記の残存（「学習者」を使う）: {line.strip()[:60]}"))

    violations.extend(allowlist.dead_violations())
    NOTES.append(f"{checked} 本の Markdown の表記を確認した")
    return violations


# ── publish ─────────────────────────────────────────────────
#
# 公開リポジトリに教員用資産が入り込んでいないかを見る。非公開リポジトリ
# `../cp-practice-design/teacher/` との分離（site-plan-2026.md §3.2）に加えた
# 二重化であり、tools/build_pages.py の verify_output() と同じ考え方をリポジトリ
# 側に当てる。build_pages.py は公開物を、こちらはリポジトリそのものを見る。

FORBIDDEN_PATH_PARTS = {"teacher"}
FORBIDDEN_NAME_WORDS = ("answer", "solution", "rubric")
PUBLISH_TARGETS = (MATERIALS, WORKBOOK, ROOT / "web", ROOT / "site", ROOT / "tools")

# 原稿から非公開側を指してしまうリンク。
# 地の文で「非公開側の teacher/answers/ に置く」と説明するのは正当なので、
# Markdown のリンク先だけを見る。
LINK_TARGET_RE = re.compile(r"\]\(([^)\s]+)")
PRIVATE_TARGET_RE = re.compile(r"cp-practice-design|(?:^|/)teacher/")


def check_publish() -> list[Violation]:
    violations: list[Violation] = []
    files = 0

    for path in iter_files(PUBLISH_TARGETS):
        relative = path.relative_to(ROOT)
        files += 1
        if any(part in FORBIDDEN_PATH_PARTS for part in relative.parts):
            violations.append(Violation(
                path, 0,
                "非公開側の置き場（teacher/）が公開リポジトリにある"
                "（../cp-practice-design/teacher/ へ移す）"))
            continue
        stem = relative.stem.lower()
        for word in FORBIDDEN_NAME_WORDS:
            if word in stem:
                violations.append(Violation(
                    path, 0,
                    f"解答らしいファイル名（{word}）が公開リポジトリにある"
                    "（標準演習の中心部分と発展演習の完成コードは非公開側にだけ置く）"))
                break

    for path in iter_files([MATERIALS, WORKBOOK], {".md"}):
        lines = read_lines(path)
        if lines is None:
            continue
        for i, line in enumerate(lines, 1):
            for target in LINK_TARGET_RE.findall(line):
                if PRIVATE_TARGET_RE.search(target):
                    violations.append(Violation(
                        path, i,
                        f"非公開リポジトリへのリンクがある: {target}"
                        "（公開側の原稿から非公開側を指さない）"))

    NOTES.append(f"{files} ファイルの名前と、原稿中の参照を確認した")
    return violations


# ── privacy ─────────────────────────────────────────────────
#
# `2026nendo`（他科目の採点データを含むリポジトリ）から切り出した経緯があるので、
# 移設事故を機械で止める価値が高い（site-plan-2026.md §7.1）。

HOME_PATH_RE = re.compile(r"/home/[A-Za-z0-9_][A-Za-z0-9_.-]*")
IPV4_RE = re.compile(r"(?<![0-9.])((?:[0-9]{1,3}\.){3}[0-9]{1,3})(?![0-9.])")
# 学籍番号らしき連続数字。年号（2026）や版番号に当たらないよう7桁以上にする。
LONG_DIGITS_RE = re.compile(r"(?<![0-9.])[0-9]{7,}(?![0-9.])")

# 文書に書いてよいアドレス。待ち受け先の説明に必要なもの（環境固有ではない）。
ALLOWED_ADDRESSES = {"127.0.0.1", "0.0.0.0", "255.255.255.255", "0.0.0.1"}

PRIVACY_TARGETS = (MATERIALS, WORKBOOK, DESIGN, ROOT / "site", ROOT / "tools",
                   ROOT / "web", ROOT / "Makefile", ROOT / "README.md",
                   ROOT / "AGENTS.md", ROOT / "CLAUDE.md")


def _is_version_like(text: str, line: str) -> bool:
    """3.10.2 のような版番号を IP アドレスと誤認しないための判定。"""
    parts = text.split(".")
    if any(len(part) > 1 and part.startswith("0") for part in parts):
        return False
    if all(int(part) < 256 for part in parts) and "." in text:
        # 版番号は前後に v / version / pandoc などの手がかりがあることが多い
        return bool(re.search(r"(?i)version|v[0-9]|pandoc|python|z3|minizinc", line))
    return True


def check_privacy() -> list[Violation]:
    violations: list[Violation] = []
    allowlist = Allowlist("privacy")
    files = 0

    for path in iter_files(PRIVACY_TARGETS, TEXT_SUFFIXES | {""}):
        lines = read_lines(path)
        if lines is None:
            continue
        rel = path.relative_to(ROOT).as_posix()
        files += 1
        for i, line in enumerate(lines, 1):
            if (HOME_PATH_RE.search(line)
                    and not allowlist.matches(rel, line, "home-path")):
                violations.append(Violation(
                    path, i,
                    f"/home/ で始まる絶対パスがある: {line.strip()[:60]}"
                    "（リポジトリ相対パスで書く）"))
            for match in IPV4_RE.finditer(line):
                address = match.group(1)
                if address in ALLOWED_ADDRESSES:
                    continue
                if _is_version_like(address, line):
                    continue
                if allowlist.matches(rel, line, "ip-address"):
                    continue
                violations.append(Violation(
                    path, i, f"IP アドレスらしい記述がある: {address}"))
            if (LONG_DIGITS_RE.search(line)
                    and not allowlist.matches(rel, line, "long-digits")):
                violations.append(Violation(
                    path, i,
                    f"学籍番号らしき連続数字がある: {line.strip()[:60]}"))

    violations.extend(allowlist.dead_violations())
    NOTES.append(f"{files} ファイルを個人情報・環境固有識別子の観点で確認した")
    return violations


# ── numbers ─────────────────────────────────────────────────
#
# テストファイルの本数・コード行数など、修正のたびに増減しうる派生的な数値は
# 本文に書かない。数量に触れたいときは「対応する演習ファイルで確認できる」の
# ように、実測し直さなくても正しさが保たれる表現へ言い換える。
# 対象外: 回番号・全15回のような教材の骨格を表す数値。

DERIVED_COUNT_RE = re.compile(
    r"全[0-9]+(?:本|ファイル)"
    r"|[0-9]+本の(?:ファイル|演習|モデル|プログラム|テスト)"
    r"|[0-9]+行の(?:コード|プログラム|モデル)"
    r"|[0-9]+個の(?:テスト|演習ファイル)"
)


def check_numbers() -> list[Violation]:
    violations: list[Violation] = []
    allowlist = Allowlist("numbers")
    checked = 0

    for path in iter_files([MATERIALS, WORKBOOK], {".md"}):
        lines = read_lines(path)
        if lines is None:
            continue
        rel = path.relative_to(ROOT).as_posix()
        checked += 1
        for i, line in enumerate(lines, 1):
            masked = mask_protected(line)
            match = DERIVED_COUNT_RE.search(masked)
            if match and not allowlist.matches(rel, line, "derived-count"):
                violations.append(Violation(
                    path, i,
                    f"派生する数値を本文に書いている（{match.group(0)}）: "
                    f"{line.strip()[:60]}"))

    violations.extend(allowlist.dead_violations())
    NOTES.append(f"{checked} 本の Markdown を派生数値の観点で確認した")
    return violations


# ── 用語初出台帳の読み取り ──────────────────────────────────
#
# design/glossary-ledger.md が「どの概念をどの回で初めて導入するか」の
# 単一の出典である（site-plan-2026.md §7.2）。concepts 検査と glossary 検査は
# どちらもこの台帳を読み、原稿の frontmatter と用語集をそれに突き合わせる。
#
# 台帳の様式（読み取れる形はこれだけ。台帳の「様式」節と揃える）:
#
#   ## 第03回 <回のタイトル>
#
#   **前提**: `slug_a` / `slug_b`        ← 前提が無い回は「なし」
#
#   | 識別子 | 用語 | 意味の要点 |
#   |---|---|---|
#   | `csp_vocabulary` | 制約充足問題（CSP）の基本語彙 | … |
#
# 第NN回の H2 以外の見出しに入ったら、その節の外と見なして表を拾わない
# （台帳末尾の「用語の粒度について」の表を概念として数えないため）。

LEDGER = DESIGN / "glossary-ledger.md"
GLOSSARY = MATERIALS / "references" / "glossary.md"

LEDGER_SESSION_RE = re.compile(r"^##\s+第(\d{2})回")
LEDGER_H2_RE = re.compile(r"^##\s+")
LEDGER_REQUIRES_RE = re.compile(r"^\*\*前提\*\*\s*[:：]\s*(?P<body>.*)$")
LEDGER_ROW_RE = re.compile(r"^\|\s*`(?P<slug>[a-z0-9_]+)`\s*\|\s*(?P<term>[^|]+?)\s*\|")
SLUG_RE = re.compile(r"`([a-z0-9_]+)`")


class Ledger:
    """用語初出台帳の中身。読み取りに失敗した箇所は errors に残す。"""

    def __init__(self) -> None:
        self.sessions: list[int] = []              # 台帳に節を持つ回（昇順）
        self.introduces: dict[int, list[str]] = {}  # 回 -> その回が初出の識別子
        self.requires: dict[int, list[str]] = {}    # 回 -> その回が前提にする識別子
        self.term: dict[str, str] = {}              # 識別子 -> 用語（用語集の見出し）
        self.first: dict[str, int] = {}             # 識別子 -> 初出の回
        self.line: dict[str, int] = {}              # 識別子 -> 台帳での行番号
        self.errors: list[Violation] = []

    @property
    def slugs(self) -> set[str]:
        return set(self.first)


def load_ledger() -> Ledger:
    ledger = Ledger()
    lines = read_lines(LEDGER)
    if lines is None:
        ledger.errors.append(Violation(
            LEDGER, 0,
            "用語初出台帳が無い（design/glossary-ledger.md を作る）"))
        return ledger

    current: int | None = None
    for i, line in enumerate(lines, 1):
        heading = LEDGER_SESSION_RE.match(line)
        if heading:
            current = int(heading.group(1))
            if current in ledger.introduces:
                ledger.errors.append(Violation(
                    LEDGER, i, f"第{current:02d}回の節が2つある"))
            ledger.sessions.append(current)
            ledger.introduces[current] = []
            ledger.requires[current] = []
            continue
        if LEDGER_H2_RE.match(line):
            current = None
            continue
        if current is None:
            continue

        needs = LEDGER_REQUIRES_RE.match(line)
        if needs:
            ledger.requires[current] = SLUG_RE.findall(needs.group("body"))
            continue

        row = LEDGER_ROW_RE.match(line)
        if row:
            slug = row.group("slug")
            if slug in ledger.first:
                ledger.errors.append(Violation(
                    LEDGER, i,
                    f"同じ識別子が二度「初出」している: {slug}"
                    f"（第{ledger.first[slug]:02d}回で導入済み）"))
                continue
            ledger.first[slug] = current
            ledger.term[slug] = row.group("term").strip()
            ledger.line[slug] = i
            ledger.introduces[current].append(slug)

    ledger.sessions = sorted(set(ledger.sessions))

    # 前提は「より前の回で導入した識別子」だけを書ける
    for number in ledger.sessions:
        for slug in ledger.requires[number]:
            if slug not in ledger.first:
                ledger.errors.append(Violation(
                    LEDGER, 0,
                    f"第{number:02d}回の前提に、台帳に無い識別子がある: {slug}"))
            elif ledger.first[slug] >= number:
                ledger.errors.append(Violation(
                    LEDGER, 0,
                    f"第{number:02d}回が未導入の概念を先取りしている: {slug}"
                    f"（初出は第{ledger.first[slug]:02d}回）"))
    return ledger


def session_manuscript(number: int) -> Path | None:
    """第NN回の原稿。まだ書かれていなければ None。"""
    for path in session_manuscripts():
        data, _ = parse_frontmatter(path)
        if (data or {}).get("session") == number:
            return path
    return None


def _as_slug_list(value) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


# ── concepts ────────────────────────────────────────────────

def check_concepts() -> list[Violation]:
    ledger = load_ledger()
    violations: list[Violation] = list(ledger.errors)

    written: set[int] = set()
    for path in session_manuscripts():
        data, error = parse_frontmatter(path)
        if error or data is None:
            continue  # frontmatter 検査が別に報告する
        number = data.get("session")
        if not isinstance(number, int):
            continue
        written.add(number)
        introduces = _as_slug_list(data.get("introduces"))
        requires = _as_slug_list(data.get("requires"))

        if number in ledger.introduces:
            expected_in = ledger.introduces[number]
            if set(introduces) != set(expected_in):
                missing = sorted(set(expected_in) - set(introduces))
                extra = sorted(set(introduces) - set(expected_in))
                detail = []
                if missing:
                    detail.append(f"台帳にあって原稿に無い: {', '.join(missing)}")
                if extra:
                    detail.append(f"原稿にあって台帳に無い: {', '.join(extra)}")
                violations.append(Violation(
                    path, 1,
                    "introduces: が台帳と一致しない（"
                    + " / ".join(detail)
                    + "）。台帳 design/glossary-ledger.md を先に直す"))
            expected_req = ledger.requires[number]
            if set(requires) != set(expected_req):
                missing = sorted(set(expected_req) - set(requires))
                extra = sorted(set(requires) - set(expected_req))
                detail = []
                if missing:
                    detail.append(f"台帳にあって原稿に無い: {', '.join(missing)}")
                if extra:
                    detail.append(f"原稿にあって台帳に無い: {', '.join(extra)}")
                violations.append(Violation(
                    path, 1,
                    "requires: が台帳の「前提」と一致しない（"
                    + " / ".join(detail)
                    + "）。requires は台帳からの導出値なので手で足し引きしない"))
        else:
            # 台帳に節を持たない回（自由課題・発表会）は新しい概念を導入しない
            if introduces:
                violations.append(Violation(
                    path, 1,
                    f"第{number:02d}回は台帳に節を持たないので introduces: は空にする"
                    f"（余分: {', '.join(sorted(introduces))}）。"
                    "概念を導入するなら台帳に節を足す"))
            for slug in requires:
                if slug not in ledger.first:
                    violations.append(Violation(
                        path, 1, f"requires: に台帳に無い識別子がある: {slug}"))
                elif ledger.first[slug] >= number:
                    violations.append(Violation(
                        path, 1,
                        f"requires: が未導入の概念を先取りしている: {slug}"
                        f"（初出は第{ledger.first[slug]:02d}回）"))

    pending = [n for n in ledger.sessions if n not in written]
    NOTES.append(f"台帳の概念 {len(ledger.first)} 件 / 節を持つ回 {len(ledger.sessions)}")
    if pending:
        NOTES.append("原稿が未執筆で突合できない回（違反ではない）: "
                     + ", ".join(f"第{n:02d}回" for n in pending))
    return violations


# ── glossary ────────────────────────────────────────────────

GLOSSARY_ENTRY_RE = re.compile(r"^###\s+(?P<term>.+?)\s*\{#(?P<slug>[a-z0-9_]+)\}\s*$")
GLOSSARY_BREAK_RE = re.compile(r"^(?:#{1,3}\s|---\s*$)")


def _glossary_entries(lines: list[str]) -> dict[str, tuple[int, str, list[str]]]:
    """識別子 -> (行番号, 見出しの用語, 本文の行)"""
    entries: dict[str, tuple[int, str, list[str]]] = {}
    open_slug: str | None = None
    for i, line in enumerate(lines, 1):
        found = GLOSSARY_ENTRY_RE.match(line)
        if found:
            open_slug = found.group("slug")
            entries[open_slug] = (i, found.group("term").strip(), [])
            continue
        if open_slug and GLOSSARY_BREAK_RE.match(line):
            open_slug = None
            continue
        if open_slug:
            entries[open_slug][2].append(line)
    return entries


def check_glossary() -> list[Violation]:
    ledger = load_ledger()
    violations: list[Violation] = list(ledger.errors)

    lines = read_lines(GLOSSARY)
    if lines is None:
        violations.append(Violation(
            GLOSSARY, 0,
            "用語集が無い（materials/references/glossary.md を作る）"))
        return violations

    entries = _glossary_entries(lines)
    pending_links: list[str] = []

    for slug, number in sorted(ledger.first.items(), key=lambda kv: (kv[1], kv[0])):
        if slug not in entries:
            violations.append(Violation(
                GLOSSARY, 0,
                f"台帳の用語に項目が無い: {slug}"
                f"（`### {ledger.term[slug]} {{#{slug}}}` を足す）"))
            continue
        line_no, term, body = entries[slug]
        if term != ledger.term[slug]:
            violations.append(Violation(
                GLOSSARY, line_no,
                f"項目の見出しが台帳の用語と違う: 「{term}」"
                f"（台帳は「{ledger.term[slug]}」）"))
        text = "\n".join(body)
        label = f"第{number:02d}回"
        if label not in text:
            violations.append(Violation(
                GLOSSARY, line_no,
                f"項目「{term}」に初出回（{label}）の案内が無い"))
            continue
        manuscript = session_manuscript(number)
        if manuscript is None:
            pending_links.append(label)
            continue
        target = f"../sessions/{manuscript.name}"
        if target not in text:
            violations.append(Violation(
                GLOSSARY, line_no,
                f"項目「{term}」から初出回へのリンクが無い"
                f"（{label} の原稿があるので `[{label}]({target})` を張る）"))

    for slug, (line_no, term, _) in entries.items():
        if slug not in ledger.first:
            violations.append(Violation(
                GLOSSARY, line_no,
                f"台帳に無い項目がある: {slug}「{term}」"
                "（台帳 design/glossary-ledger.md に1行足すか、項目を消す）"))

    NOTES.append(f"用語集の項目 {len(entries)} 件 / 台帳の概念 {len(ledger.first)} 件")
    if pending_links:
        counts = {label: pending_links.count(label) for label in sorted(set(pending_links))}
        NOTES.append(
            "初出回の原稿が未執筆のため、まだリンクにできない用語（違反ではない。"
            "原稿を書いたらリンクに変える）: "
            + ", ".join(f"{label} {n} 件" for label, n in counts.items()))
    return violations


CHECKS = {
    "frontmatter": ("各回 frontmatter の整合", check_frontmatter),
    "nav": ("nav.yaml と原稿の突合", check_nav_listing),
    "structure": ("各回の見出し構成", check_structure),
    "codeblock": ("コードブロックの言語名と区分", check_code_blocks),
    "figure": ("図の代替テキストと実体", check_figures),
    "style": ("用語・表記の統一", check_style_terms),
    "publish": ("公開範囲（教員用資産の混入）", check_publish),
    "privacy": ("個人情報・環境固有識別子", check_privacy),
    "numbers": ("派生する数値", check_numbers),
    "concepts": ("用語初出台帳と各回の introduces / requires", check_concepts),
    "glossary": ("用語初出台帳と用語集の突合", check_glossary),
}

# 既定で走らせるもの。いまはすべて実装済みなので全部走る。
DEFAULT_CHECKS = list(CHECKS)


def print_checks() -> None:
    print("チェック一覧（既定で走るものに *）:")
    for name, (title, _) in CHECKS.items():
        mark = "*" if name in DEFAULT_CHECKS else " "
        print(f"  {mark} {name:<12} {title}")


def print_allowlist() -> None:
    empty = True
    for section in ALLOWLIST_KINDS:
        entries = _load_allowlist_section(section)
        if not entries:
            continue
        empty = False
        print(f"{section} 除外リスト {len(entries)} 件:")
        for entry in entries:
            status = entry.get("status", "?")
            check = entry.get("check", "?")
            if not isinstance(check, str):
                check = ",".join(check)
            reason = " ".join(entry.get("reason", "").split())
            print(f"  [{status}] <{check}> {entry.get('file', '?')}  "
                  f"{entry.get('match', '')}  {reason}")
    if empty:
        print("除外リストは空。")


def print_allowlist_kinds() -> None:
    print("除外リストの check: に書ける検出種別:")
    for section, kinds in ALLOWLIST_KINDS.items():
        print(f"  {section}: {', '.join(sorted(kinds))}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--only",
                        help=f"実行するチェック（カンマ区切り: {','.join(CHECKS)}）")
    parser.add_argument("--list-checks", action="store_true",
                        help="チェックの一覧を表示して終了する")
    parser.add_argument("--list-allowed", action="store_true",
                        help="除外リストの内容を表示して終了する")
    parser.add_argument("--list-kinds", action="store_true",
                        help="除外リストに書ける検出種別を表示して終了する")
    args = parser.parse_args()

    if args.list_checks:
        print_checks()
        return 0
    if args.list_allowed:
        print_allowlist()
        return 0
    if args.list_kinds:
        print_allowlist_kinds()
        return 0

    names = list(DEFAULT_CHECKS)
    if args.only:
        names = [n.strip() for n in args.only.split(",") if n.strip()]
        unknown = [n for n in names if n not in CHECKS]
        if unknown:
            print(f"未知のチェック: {', '.join(unknown)}", file=sys.stderr)
            return 2

    total = 0
    for name in names:
        title, func = CHECKS[name]
        NOTES.clear()
        violations = func()
        if violations:
            print(f"\n[{name}] {title}: {len(violations)} 件の違反")
            for v in violations:
                print(f"  {v}")
            total += len(violations)
        else:
            print(f"[{name}] {title}: 違反なし")
        for note in NOTES:
            print(f"       … {note}")

    if total:
        print(f"\n合計 {total} 件の違反")
        return 1
    print("\nすべてのチェックを通過")
    return 0


if __name__ == "__main__":
    sys.exit(main())
