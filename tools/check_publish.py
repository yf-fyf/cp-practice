"""登録済みの原稿・配布物を検査する。ZIPの中身も配布元と照合する。"""
from pathlib import Path
import re
import tomllib
import zipfile
from course import COURSE_HANDOUTS, ROOT, SAMPLES

PRIVATE_PARTS = {"teacher", "answers", "rubric", "tests", "planning"}


def files(folder):
    return {p for p in folder.rglob("*") if (p.is_file() or p.is_symlink())
            and "__pycache__" not in p.parts and "_build" not in p.parts}


def check_sources():
    errors = check_python_environment()
    expected_materials, expected_workbook = set(), {ROOT / "workbook/README.md"}
    expected_workbook.update(ROOT / "workbook" / name for name in COURSE_HANDOUTS)
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
            if path.suffix in {".md", ".py", ".pl", ".mzn", ".dzn", ".txt", ".tex", ".toml"}:
                content = path.read_text(encoding="utf-8")
                if re.search(r"cp-practice-design|(?:\.\./)*(?:teacher|planning)/", content):
                    errors.append(f"公開資料から非公開資料への参照: {relative}")
    return errors


def requirement_lines(path):
    lines = (line.split("#", 1)[0].strip() for line in path.read_text(encoding="utf-8").splitlines())
    return {line for line in lines if line}


def check_python_environment():
    """uv用の全回共通環境と、各回のpip用 requirements.txt の依存がずれていないかを見る。"""
    project, lock = ROOT / "workbook/pyproject.toml", ROOT / "workbook/uv.lock"
    if "pyproject.toml" not in COURSE_HANDOUTS or not project.is_file():
        return []
    errors = []
    dependencies = set(tomllib.loads(project.read_text(encoding="utf-8"))["project"].get("dependencies", []))
    for sample in SAMPLES.values():
        requirements = sample.handout_directory / "requirements.txt"
        if "requirements.txt" in sample.handouts and requirements.is_file():
            if requirement_lines(requirements) != dependencies:
                errors.append(f"requirements.txt と pyproject.toml の依存が不一致: {sample.slug}")
    if "uv.lock" in COURSE_HANDOUTS and lock.is_file():
        packages = tomllib.loads(lock.read_text(encoding="utf-8")).get("package", [])
        locked = {(package["name"], package["version"]) for package in packages}
        # 生成物なので文面の検査から外す代わりに、取得元をPyPIと演習フォルダー自身に限る。
        for package in packages:
            if package.get("source") not in ({"registry": "https://pypi.org/simple"}, {"virtual": "."}):
                errors.append(f"uv.lock にPyPI以外の取得元: {package['name']}")
        for dependency in sorted(dependencies):
            name, _, version = dependency.partition("==")
            if version and (re.sub(r"[-_.]+", "-", name).lower(), version) not in locked:
                errors.append(f"uv.lock が pyproject.toml と不一致（uv lock を実行する）: {dependency}")
    return errors
