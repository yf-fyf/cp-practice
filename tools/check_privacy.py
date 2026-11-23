"""公開文書の表記・個人情報の検査。"""
from __future__ import annotations
import re
from pathlib import Path
import yaml
from course import ROOT
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
                 ".tex", ".lua", ".css", ".js", ".html", ".toml"}

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


_MASK_SPAN_RE = re.compile(r"`[^`]*`")
_MASK_LINKTARGET_RE = re.compile(r"\]\([^)]*\)")
_MASK_URL_RE = re.compile(r"\bhttps?://\S+")


def mask_protected(line: str) -> str:
    """インラインコード・リンク先・URL を伏せ字にする（長さは保つ）。"""
    for pattern in (_MASK_SPAN_RE, _MASK_LINKTARGET_RE, _MASK_URL_RE):
        line = pattern.sub(lambda m: "　" * len(m.group(0)), line)
    return line

STYLE_DAI_KAI_RE = re.compile(r"第[0-9]回")
# 学ぶ人の呼称は「学習者」に統一する
STYLE_GAKUSEI_RE = re.compile(r"学生")
STYLE_JUKOUSHA_RE = re.compile(r"受講者")

STYLE_TARGETS = (MATERIALS, WORKBOOK, DESIGN, ROOT / "README.md")

HOME_PATH_RE = re.compile(r"/home/[A-Za-z0-9_][A-Za-z0-9_.-]*")
IPV4_RE = re.compile(r"(?<![0-9.])((?:[0-9]{1,3}\.){3}[0-9]{1,3})(?![0-9.])")
# 学籍番号らしき連続数字。年号（2026）や版番号に当たらないよう7桁以上にする。
LONG_DIGITS_RE = re.compile(r"(?<![0-9.])[0-9]{7,}(?![0-9.])")

# 文書に書いてよいアドレス。待ち受け先の説明に必要なもの（環境固有ではない）。
ALLOWED_ADDRESSES = {"127.0.0.1", "0.0.0.0", "255.255.255.255", "0.0.0.1"}

