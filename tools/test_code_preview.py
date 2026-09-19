"""配布コードのHTML化で、文字・空白・公開範囲が変わらないことを検証する。"""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import code_preview
from course import LessonSample


class PreviewTests(unittest.TestCase):
    def test_literal_html_fences_and_trailing_blank_lines(self):
        cases = [('python', 's = "</script><img src=x onerror=alert(1)>"\n\t# 日本語 & < >\n\n'),
                 ('plaintext', '# 見出し\n```html\n<button>文字</button>\n```\n\n'),
                 ('json', '{"x": "&<>"}\r\n'), ('plaintext', '')]
        rendered = code_preview.highlighted_lines(cases)
        for (_, source), lines in zip(cases, rendered):
            expected = source.replace('\r\n', '\n').removesuffix('\n').split('\n')
            self.assertEqual([''.join(code_preview.PlainText(line).parts) for line in lines], expected)
            markup = ''.join(lines)
            self.assertNotIn('<img', markup)
            self.assertNotIn('<button', markup)
            self.assertNotIn('</script>', markup)

    def test_only_registered_text_is_previewed(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            sample = LessonSample('01', '01-prolog', 'extra', ('a.py', 'data.txt', 'bundle.zip', 'binary.bin'))
            with patch('course.ROOT', root):
                folder = sample.handout_directory
                folder.mkdir(parents=True)
                for name, content in {'a.py': b'print(1)\n', 'data.txt': b'a\x00b', 'bundle.zip': b'ASCII',
                                      'binary.bin': b'\xff\xfe', 'unregistered.txt': b'private'}.items():
                    (folder / name).write_bytes(content)
                entries = code_preview.text_handouts([sample])
                self.assertEqual(list(entries), ['downloads/session-01/a.py'])


if __name__ == '__main__':
    unittest.main()
