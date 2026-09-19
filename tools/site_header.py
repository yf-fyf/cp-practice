"""サイト全体のヘッダーと、各回の資料を切り替えるナビゲーション。"""
from html import escape


def site_header(home):
    return (f'<header class="topbar"><div class="topbar-inner">'
            f'<a class="sitename" href="{escape(home, quote=True)}">実践・制約プログラミング</a>'
            f'<nav class="topnav" aria-label="サイト内の移動">'
            f'<a href="{escape(home, quote=True)}#lessons">講義一覧</a></nav>'
            '</div></header>')


def session_navigation(number, lesson, advanced, current):
    links = []
    for url, label, kind in [(lesson, '通常講義', 'lesson'), (advanced, '発展', 'advanced')]:
        active = ' aria-current="page"' if current == kind else ''
        links.append(f'<a href="{escape(url, quote=True)}"{active}>{label}</a>')
    return (f'<nav class="session-nav" aria-label="第{escape(number)}回の講義資料">'
            + ''.join(links) + '</nav>')
