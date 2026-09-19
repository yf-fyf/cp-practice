"""科目の入口と講義一覧。題名とリンク先は回別原稿・登録一覧から生成する。"""
from pathlib import Path
import html
import shutil

from render_course import split_title, TOOLS
from course import SAMPLES
from site_header import site_header


def homepage(output: Path) -> None:
    cards, guides = [], []
    for sample in SAMPLES.values():
        title, _ = split_title((sample.source / "lesson.md").read_text(encoding="utf-8"))
        title = title.removeprefix(f"第{sample.number}回").strip()
        cards.append(
            f'<li><a class="lesson-card" href="{sample.lesson_page}">'
            f'<span class="number">第{sample.number}回</span>'
            f'<span class="title">{html.escape(title)}</span></a></li>')
        for page, (source, _, kind) in sample.pages.items():
            if kind != "guide" or source == "guides/course-start.md":
                continue
            title, _ = split_title((sample.source / source).read_text(encoding="utf-8"))
            guides.append(
                f'<li><a href="{page}">{html.escape(title)}</a>'
                f'<span>第{sample.number}回</span></li>')
    content = '''<!DOCTYPE html>
<html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="実践・制約プログラミングの2026年度教材。Prolog、MiniZinc、SAT・SMTを使い、問題の条件をモデル化して解く。">
<title>実践・制約プログラミング | 2026年度</title>
<link rel="stylesheet" href="assets/course-home.css">
<link rel="stylesheet" href="assets/site-header.css"></head><body>
__HEADER__
<main id="main">
<p class="year">2026年度 · 全15回・各100分</p>
<h1>実践・制約プログラミング</h1>
<p class="intro">Prolog・MiniZinc・SAT/SMTで、問題の条件をモデルにし、解いて結果を説明します。</p>
<a class="start" href="guides/course-start/index.html">科目の進め方 →</a>
<section id="lessons"><h2>講義資料</h2>
<ol class="lesson-grid">__CARDS__</ol>
</section>
<section id="project"><h2>第11〜15回　自由課題</h2>
<p>自分が関心を持つ問題を選び、制約プログラミングで解決します。</p>
<p><a href="guides/course-start/index.html">自由課題の進め方と評価 →</a></p>
</section>
<section id="guides"><h2>手引き</h2>
<p>実行方法や結果の確認で迷ったときに。</p>
<ul class="guide-list">__GUIDES__</ul>
</section>
</main>
<footer><p>実践・制約プログラミング · 2026年度</p></footer>
</body></html>
'''
    content = content.replace("__HEADER__", site_header("index.html"))
    content = content.replace("__CARDS__", "".join(cards)).replace("__GUIDES__", "".join(guides))
    (output / "index.html").write_text(content, encoding="utf-8")
    shutil.copyfile(TOOLS / "course-home.css", output / "assets/course-home.css")
