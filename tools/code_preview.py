"""登録済みのテキスト配布物から、読み取り専用プレビューを生成する。"""
from html.parser import HTMLParser
import json
import re
import subprocess

from course import ROOT

LANGUAGES = {
    '.pl': ('prolog', 'Prolog'), '.mzn': ('minizinc', 'MiniZinc'),
    '.dzn': ('minizinc', 'MiniZincの入力'), '.py': ('python', 'Python'),
    '.json': ('json', 'JSON'), '.md': ('plaintext', 'Markdown'),
}
ASSETS = ('code-preview.css', 'code-preview.js')


def text_handouts(samples):
    """公開登録されたUTF-8テキストだけを返す。ZIPやバイナリは含めない。"""
    result = {}
    for sample in samples:
        for name in sample.handouts:
            source = sample.handout_directory / name
            if source.suffix.lower() == '.zip':
                continue
            try:
                text = source.read_bytes().decode('utf-8')
            except UnicodeDecodeError:
                continue
            if '\0' not in text:
                result[f'downloads/session-{sample.number}/{name}'] = (source, text)
    return result


def preview_path(download):
    return 'previews/' + download.removeprefix('downloads/') + '.json'


class PlainText(HTMLParser):
    def __init__(self, markup):
        super().__init__()
        self.parts = []
        self.feed(markup)

    def handle_data(self, text):
        self.parts.append(text)


def highlighted_lines(items):
    """一度のPandoc呼出しで全コードを色分けする。本文はCodeBlockとして渡す。"""
    blocks = []
    normalized = [text.replace('\r\n', '\n').replace('\r', '\n') for _, text in items]
    for i, ((language, _), text) in enumerate(zip(items, normalized)):
        blocks.append({'t': 'CodeBlock', 'c': [
            [f'preview-{i}', [language] if language != 'plaintext' else [], []],
            text.removesuffix('\n') + '\nCODE_PREVIEW_END']})
    ast = {'pandoc-api-version': [1, 23, 1], 'meta': {}, 'blocks': blocks}
    rendered = subprocess.run([
        'pandoc', '--from=json', '--to=html5', '--wrap=none', '--preserve-tabs', '--syntax-highlighting=tango',
        '--syntax-definition', str(ROOT / 'site/syntax/minizinc.xml'),
    ], input=json.dumps(ast), text=True, capture_output=True, check=True).stdout
    fragments = re.findall(r'<code(?: class="[^"]*")?>(.*?)</code>', rendered, re.S)
    if len(fragments) != len(items):
        raise ValueError('プレビューの生成件数が一致しません')
    result = []
    for i, (fragment, text) in enumerate(zip(fragments, normalized)):
        lines = []
        for line in fragment.split('\n'):
            # Pandocの行アンカーを除き、選択・コピーへ行番号が混ざらない形にする。
            match = re.fullmatch(r'<span id="preview-\d+-\d+">(.*)</span>', line)
            if match:
                line = re.sub(r'<a href="#[^"]*" aria-hidden="true" tabindex="-1"></a>', '', match[1])
            lines.append(line)
        # 末尾の空行もPandocに保持させるための番兵行を除く。
        if ''.join(PlainText(lines.pop()).parts) != 'CODE_PREVIEW_END':
            raise ValueError('プレビューの終端が一致しません')
        original = text.removesuffix('\n').split('\n')
        if len(lines) != len(original) or any(
                ''.join(PlainText(markup).parts) != source for markup, source in zip(lines, original)):
            raise ValueError(f'プレビューの内容が一致しません: {i}')
        result.append(lines)
    return result


def build_previews(samples, output):
    entries = text_handouts(samples)
    styles = [LANGUAGES.get(source.suffix.lower(), ('plaintext', 'テキスト')) for source, _ in entries.values()]
    rendered = highlighted_lines([(style[0], text) for style, (_, text) in zip(styles, entries.values())])
    for (download, (source, text)), (language, label), lines in zip(entries.items(), styles, rendered):
        destination = output / preview_path(download)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps({
            'name': source.name, 'language': language, 'label': label,
            'code': text, 'lines': lines,
        }, ensure_ascii=False), encoding='utf-8')
    print(f'コードのプレビュー: {len(entries)}ファイル')


def check_previews(samples, output):
    errors = []
    entries = text_handouts(samples)
    expected = {preview_path(download) for download in entries}
    actual = {p.relative_to(output).as_posix() for p in (output / 'previews').rglob('*') if p.is_file()}
    if actual != expected:
        errors.append(f'プレビュー一覧不一致: 不足={sorted(expected-actual)}, 余分={sorted(actual-expected)}')
    for download, (source, text) in entries.items():
        try:
            data = json.loads((output / preview_path(download)).read_text(encoding='utf-8'))
            language, label = LANGUAGES.get(source.suffix.lower(), ('plaintext', 'テキスト'))
            original = text.replace('\r\n', '\n').replace('\r', '\n').removesuffix('\n').split('\n')
            shown = [''.join(PlainText(line).parts) for line in data['lines']]
            if (data['name'], data['language'], data['label'], data['code'], shown) != (source.name, language, label, text, original):
                errors.append(f'プレビュー内容不一致: {download}')
        except (OSError, ValueError, KeyError, TypeError) as error:
            errors.append(f'プレビューを読めません: {download}: {error}')
    return errors
