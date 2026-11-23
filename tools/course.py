"""通常回の原稿と、サイトへ出す学習者向けファイルの登録。"""

from dataclasses import dataclass
from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / ".site"


@dataclass(frozen=True)
class LessonSample:
    number: str
    slug: str
    advanced_slug: str
    handouts: tuple[str, ...]
    guides: tuple[str, ...] = ()

    @property
    def source(self) -> Path:
        return ROOT / "materials/sessions" / self.slug

    @property
    def handout_directory(self) -> Path:
        return ROOT / "workbook/sessions" / self.slug

    @property
    def lesson_page(self) -> str:
        return f"sessions/{self.slug}/index.html"

    @property
    def advanced_page(self) -> str:
        return f"advanced/{self.advanced_slug}/index.html"

    @property
    def pages(self) -> dict[str, tuple[str, str, str]]:
        pages = {
            self.lesson_page: ("lesson.md", "通常講義", "lesson"),
            self.advanced_page: ("advanced-exercises.md", "発展", "advanced"),
        }
        for guide in self.guides:
            pages[f"guides/{guide}/index.html"] = (f"guides/{guide}.md", "手引き", "guide")
        return pages



def load_sessions():
    entries = yaml.safe_load((ROOT / "site/nav.yaml").read_text(encoding="utf-8"))["sessions"]
    sessions, destinations = {}, set()
    for entry in entries:
        number = entry["number"]
        if not isinstance(number, str) or not re.fullmatch(r"0[1-9]|10", number):
            raise ValueError(f"invalid session number: {number}")
        if number in sessions:
            raise ValueError(f"duplicate session: {number}")
        for slug in [entry["slug"], entry["advanced_slug"], *entry["guides"]]:
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
                raise ValueError(f"invalid URL slug: {slug}")
        if not entry["slug"].startswith(number + "-"):
            raise ValueError(f"session number does not match slug: {entry['slug']}")
        handouts = entry["handouts"]
        if len(handouts) != len(set(handouts)):
            raise ValueError(f"duplicate handout: {number}")
        for name in handouts:
            path = Path(name)
            if path.is_absolute() or ".." in path.parts or path.as_posix() != name:
                raise ValueError(f"invalid handout path: {name}")
        sample = LessonSample(number, entry["slug"], entry["advanced_slug"],
                              tuple(handouts), tuple(entry["guides"]))
        for page in sample.pages:
            if page in destinations:
                raise ValueError(f"duplicate output: {page}")
            destinations.add(page)
        sessions[number] = sample
    if list(sessions) != [f"{i:02d}" for i in range(1, 11)]:
        raise ValueError("site/nav.yaml must list sessions 01 through 10 in order")
    return sessions


# 全回で共通の配布物（uv の環境定義など）。workbook/ 直下に置き、ここへ出す。
COURSE_DOWNLOADS = "downloads/course"


def load_course_handouts():
    names = yaml.safe_load((ROOT / "site/nav.yaml").read_text(encoding="utf-8")).get("course_handouts") or []
    if len(names) != len(set(names)):
        raise ValueError("duplicate course handout")
    for name in names:
        if (not isinstance(name, str) or name == "README.md"
                or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", name)):
            raise ValueError(f"invalid course handout: {name}")
    return tuple(names)


def course_handout(name: str) -> Path:
    """全回共通の配布物の置き場所。テストで ROOT を差し替えられるよう、呼出し時に解決する。"""
    return ROOT / "workbook" / name


SAMPLES = load_sessions()
COURSE_HANDOUTS = load_course_handouts()
