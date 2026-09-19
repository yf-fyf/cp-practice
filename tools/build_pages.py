#!/usr/bin/env python3
"""登録済みの教材と配布ZIPから静的リリースを組み立てる。公開操作はしない。"""
import argparse
from pathlib import Path
import re
import shutil
import subprocess
import sys
import zipfile
from course import ROOT, SAMPLES
from check_publish import check_sources, files
from code_preview import ASSETS, preview_path, text_handouts

WORKBOOK_ARCHIVE_PREFIX = 'cp-practice-workbook'
LEGAL = ('LICENSE', 'LICENSE-MATERIALS', 'THIRD_PARTY_NOTICES.md')


def safe_version(value):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*', value):
        raise ValueError('version must contain only letters, digits, dot, underscore, or hyphen')
    return value


def revision():
    result = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], cwd=ROOT, capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else 'uncommitted'


def workbook_entries():
    # READMEの相対リンク先も同梱し、展開後も本文から作業をたどれるようにする。
    entries = {path.relative_to(ROOT).as_posix(): path for folder in ('workbook', 'materials')
               for path in files(ROOT / folder)}
    entries.update({name: ROOT / name for name in LEGAL})
    return entries


def archive_workbook(destination, version):
    errors = check_sources()
    if errors:
        raise ValueError('\n'.join(errors))
    with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as archive:
        for relative, source in sorted(workbook_entries().items()):
            archive.write(source, f'{WORKBOOK_ARCHIVE_PREFIX}-{version}/{relative}')


def verify_output(output, version):
    expected = {'index.html', '.nojekyll', *LEGAL}
    expected.update('legal/' + name for name in LEGAL)
    expected.update('assets/' + name for name in ('lesson-style.css', 'lesson-syntax.css',
                    'lesson-lightbox.css', 'lesson-lightbox.js', 'course-home.css', 'site-header.css', *ASSETS))
    expected.update(preview_path(url) for url in text_handouts(SAMPLES.values()))
    katex = ROOT / 'site/vendor/katex'
    expected.update('assets/katex/' + p.relative_to(katex).as_posix() for p in katex.rglob('*') if p.is_file())
    for sample in SAMPLES.values():
        expected.update(sample.pages)
        expected.update(f'downloads/session-{sample.number}/{name}' for name in sample.handouts)
        expected.update(f'figures/session-{sample.number}/{p.name}' for p in (sample.source / 'figures').glob('*.svg'))
    archive_name = f'downloads/{WORKBOOK_ARCHIVE_PREFIX}-{version}.zip'
    expected.add(archive_name)
    actual = {p.relative_to(output).as_posix() for p in output.rglob('*') if p.is_file()}
    if actual != expected:
        raise ValueError(f'公開一覧不一致: 不足={sorted(expected-actual)}, 余分={sorted(actual-expected)}')
    with zipfile.ZipFile(output / archive_name) as archive:
        entries = {f'{WORKBOOK_ARCHIVE_PREFIX}-{version}/{name}': path for name, path in workbook_entries().items()}
        if set(archive.namelist()) != entries.keys() or len(archive.namelist()) != len(entries):
            raise ValueError('リリースZIPの登録ファイル不一致')
        for name, source in entries.items():
            if archive.read(name) != source.read_bytes():
                raise ValueError(f'リリースZIPの内容不一致: {name}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('version')
    parser.add_argument('--output', type=Path, default=ROOT / '.pages')
    parser.add_argument('--revision', default=revision())
    args = parser.parse_args()
    try:
        from build_site import output_directory, check_links
        version = safe_version(args.version)
        output = output_directory(args.output)
        subprocess.run([sys.executable, str(ROOT / 'tools/build_site.py'), '--output', str(output),
                        '--release', version, '--revision', args.revision], check=True)
        for name in LEGAL:
            shutil.copyfile(ROOT / name, output / name)
        archive_workbook(output / f'downloads/{WORKBOOK_ARCHIVE_PREFIX}-{version}.zip', version)
        (output / '.nojekyll').touch()
        verify_output(output, version)
        if check_links(output):
            raise ValueError('リリースのリンクを確認してください')
        print(f'PASS: release {version}')
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f'FAIL: {error}')
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
