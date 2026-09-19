#!/usr/bin/env python3
"""各回のTeX/Pythonソースから図を再生成する。引数で回番号を指定できる。"""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from course import SAMPLES


def tikz(number, source, target, definition=''):
    folder = SAMPLES[number].source / 'figures'
    with tempfile.TemporaryDirectory(prefix='course-figure-') as temporary:
        command = ['lualatex', '-interaction=nonstopmode', '-halt-on-error',
                   '-jobname=figure', f'-output-directory={temporary}',
                   definition + '\\input{' + source + '}']
        result = subprocess.run(command, cwd=folder, capture_output=True, text=True)
        if result.returncode:
            raise RuntimeError('\n'.join(result.stdout.splitlines()[-30:]))
        subprocess.run(['pdftocairo', '-svg', str(Path(temporary) / 'figure.pdf'),
                        str(folder / target)], check=True)
    print(f'生成: 第{number}回 {target}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('sessions', nargs='*', help='04 / 07 / 10')
    chosen = parser.parse_args().sessions or ['04', '07', '10']
    if set(chosen) - {'04', '07', '10'}:
        parser.error('回番号は 04 / 07 / 10 から選んでください')
    if set(chosen) & {'04', '07'}:
        for tool in ('lualatex', 'pdftocairo'):
            if not shutil.which(tool):
                parser.error(f'{tool} が必要です')
    if '04' in chosen:
        tikz('04', 'sum-cells.tex', 'puzzle-sum-demo.svg')
        tikz('04', 'sum-cells.tex', 'puzzle-sum-practice.svg', '\\def\\Practice{1}')
    if '07' in chosen:
        tikz('07', 'input-decision.tex', 'input-decision.svg')
        tikz('07', 'aggregation.tex', 'sum-column.svg')
        tikz('07', 'aggregation.tex', 'sum-row.svg', '\\def\\RowSum{1}')
    if '10' in chosen:
        subprocess.run([sys.executable, str(SAMPLES['10'].source / 'figures/make_figures.py')], check=True)


if __name__ == '__main__':
    main()
