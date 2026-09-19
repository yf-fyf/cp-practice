"""登録済みの原稿・配布物を検査する。ZIPの中身も配布元と照合する。"""
from pathlib import Path
import re
import zipfile
from course import ROOT, SAMPLES

PRIVATE_PARTS = {"teacher", "answers", "rubric", "tests", "planning"}


def files(folder):
    return {p for p in folder.rglob("*") if (p.is_file() or p.is_symlink())
            and "__pycache__" not in p.parts and "_build" not in p.parts}


def check_sources():
    errors = []
    expected_materials, expected_workbook = set(), {ROOT / "workbook/README.md"}
    for sample in SAMPLES.values():
        expected_materials.update(sample.source / name for name, _, _ in sample.pages.values())
        expected_workbook.add(sample.handout_directory / "README.md")
        expected_workbook.update(sample.handout_directory / name for name in sample.handouts)
        expected_materials.update(p for p in (sample.source / "figures").glob("*")
                                  if p.suffix in {".svg", ".tex", ".py"})
        for name in sample.handouts:
            source = sample.handout_directory / name
            if source.suffix != ".zip" or not source.is_file():
                continue
            try:
                with zipfile.ZipFile(source) as archive:
                    entries = archive.namelist()
                    if len(entries) != len(set(entries)):
                        errors.append(f"ZIP内の名前重複: {source.relative_to(ROOT)}")
                    for entry in entries:
                        if entry.endswith("/"):
                            continue
                        # 個別配布と同じファイルだけを束ねる。
                        if entry not in sample.handouts or entry == name:
                            errors.append(f"ZIP内の未登録ファイル: {sample.slug}/{name}: {entry}")
                        else:
                            original = sample.handout_directory / entry
                            if not original.is_file() or archive.read(entry) != original.read_bytes():
                                errors.append(f"ZIPと配布元の内容不一致: {sample.slug}/{entry}")
            except zipfile.BadZipFile:
                errors.append(f"壊れたZIP: {source.relative_to(ROOT)}")
    for folder, expected in ((ROOT / "materials", expected_materials), (ROOT / "workbook", expected_workbook)):
        actual = files(folder)
        for path in sorted(expected - actual):
            errors.append(f"登録ファイルなし: {path.relative_to(ROOT)}")
        for path in sorted(actual - expected):
            errors.append(f"未登録のファイル: {path.relative_to(ROOT)}")
        for path in sorted(actual):
            relative = path.relative_to(ROOT)
            if path.is_symlink() or not path.resolve().is_relative_to(ROOT):
                errors.append(f"公開ソースのシンボリックリンク: {relative}")
                continue
            if PRIVATE_PARTS.intersection(relative.parts) or re.search(r"(?:^|[-_])(?:answers?|rubric|reference|verification|measurement)(?:$|[-_])", path.stem, re.I):
                errors.append(f"教員用ファイルの混入: {relative}")
            if path.suffix in {".md", ".py", ".pl", ".mzn", ".dzn", ".txt", ".tex"}:
                content = path.read_text(encoding="utf-8")
                if re.search(r"cp-practice-design|(?:\.\./)*(?:teacher|planning)/", content):
                    errors.append(f"公開資料から非公開資料への参照: {relative}")
    return errors
