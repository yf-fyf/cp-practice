"""配布漏れ・混入・ZIP不整合を止める検査の回帰テスト。"""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
import zipfile

import course
import check_publish

PYPROJECT = '[project]\nname = "workbook"\nversion = "1"\ndependencies = ["z3-solver==1.0"]\n'
LOCK = ('[[package]]\nname = "workbook"\nversion = "1"\nsource = {{ virtual = "." }}\n\n'
        '[[package]]\nname = "z3-solver"\nversion = "{version}"\nsource = {{ {source} }}\n')
REGISTRY = 'registry = "https://pypi.org/simple"'


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        sample = course.LessonSample("03", "03-search", "search-challenges",
                                     ("solutions.json", "session.zip", "requirements.txt"))
        for module in (course, check_publish):
            patcher = patch.object(module, "ROOT", self.root)
            patcher.start()
            self.addCleanup(patcher.stop)
        patcher = patch.object(check_publish, "SAMPLES", {"03": sample})
        patcher.start()
        self.addCleanup(patcher.stop)
        patcher = patch.object(check_publish, "COURSE_HANDOUTS", ("pyproject.toml", "uv.lock"))
        patcher.start()
        self.addCleanup(patcher.stop)
        self.sample = sample
        self.put("workbook/README.md", "演習ファイル")
        self.put("workbook/sessions/03-search/README.md", "第03回")
        for name in ("lesson.md", "advanced-exercises.md"):
            self.put("materials/sessions/03-search/" + name, "# 第03回")
        self.put("workbook/sessions/03-search/solutions.json", "[]")
        self.put("workbook/sessions/03-search/requirements.txt", "z3-solver==1.0\n")
        self.put("workbook/pyproject.toml", PYPROJECT)
        self.put("workbook/uv.lock", LOCK.format(version="1.0", source=REGISTRY))
        self.bundle()

    def put(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def bundle(self, extra=None):
        with zipfile.ZipFile(self.sample.handout_directory / "session.zip", "w") as archive:
            archive.writestr("solutions.json", "[]")
            if extra:
                archive.writestr(extra, "unexpected")

    def test_explicit_solution_data_is_distributable(self):
        self.assertEqual(check_publish.check_sources(), [])

    def test_unregistered_files_are_rejected(self):
        self.put("workbook/sessions/03-search/extra.txt", "unexpected")
        self.assertTrue(any("未登録" in error for error in check_publish.check_sources()))

    def test_teacher_file_in_bundle_is_rejected(self):
        self.bundle("teacher/answers.py")
        self.assertTrue(any("ZIP内の未登録" in error for error in check_publish.check_sources()))

    def test_changed_handout_requires_updated_bundle(self):
        self.put("workbook/sessions/03-search/solutions.json", "[1]")
        self.assertTrue(any("ZIPと配布元の内容不一致" in error for error in check_publish.check_sources()))

    def test_missing_handout_is_rejected(self):
        (self.sample.handout_directory / "solutions.json").unlink()
        self.assertTrue(any("登録ファイルなし" in error for error in check_publish.check_sources()))

    def test_unregistered_course_file_is_rejected(self):
        self.put("workbook/extra.toml", "")
        self.assertTrue(any("未登録のファイル: workbook/extra.toml" in error for error in check_publish.check_sources()))

    def test_requirements_must_match_course_environment(self):
        self.put("workbook/sessions/03-search/requirements.txt", "z3-solver==2.0\n")
        self.assertTrue(any("requirements.txt と pyproject.toml" in error for error in check_publish.check_sources()))

    def test_stale_lock_is_rejected(self):
        self.put("workbook/uv.lock", LOCK.format(version="0.9", source=REGISTRY))
        self.assertTrue(any("uv.lock が pyproject.toml と不一致" in error for error in check_publish.check_sources()))

    def test_local_lock_source_is_rejected(self):
        self.put("workbook/uv.lock", LOCK.format(version="1.0", source='path = "../z3"'))
        self.assertTrue(any("PyPI以外の取得元" in error for error in check_publish.check_sources()))

    def test_registered_symlink_is_rejected(self):
        path = self.sample.source / "lesson.md"
        path.unlink()
        path.symlink_to(self.sample.source / "advanced-exercises.md")
        self.assertTrue(any("シンボリックリンク" in error for error in check_publish.check_sources()))


if __name__ == "__main__":
    unittest.main()
