.PHONY: site serve check-links check-docs check-publish check figures pages clean

HOST ?= 127.0.0.1
PORT ?= 8000

# 資料サイトを .site/ に生成する（依存: pandoc + PyYAML）。
# 図はコミット済みの SVG を使うので TeX は要らない。
site:
	python3 tools/build_site.py

# ローカル確認用。原稿を保存すると作り直してブラウザを再読み込みする。
# 例: make serve PORT=9000
#     make serve HOST=tailscale   別端末から Tailscale 経由で見る
#     make serve HOST=0.0.0.0     全インターフェース（LAN からも見える）
#
# ページ間のリンクは sessions/03-minizinc-sudoku/ のディレクトリ形式なので、
# file:// で開いても辿れない。ローカル確認は必ずこれを使う。
serve:
	python3 tools/build_site.py --serve --host $(HOST) --port $(PORT)

# 内部リンク・ページ内アンカーの検査（先に make site が要る）
check-links:
	python3 tools/build_site.py --check-links

# 原稿・配布物の整合の機械チェック（除外リストは tools/doc_check_allowlist.yaml）
check-docs:
	python3 tools/check_docs.py

# 公開物に教員用資産・個人情報が混入していないかだけを検査する
check-publish:
	python3 tools/check_docs.py --only publish,privacy

# push 前に一括で通すもの
check: site check-links check-docs

# 図を SVG で生成する（依存: lualatex + poppler-utils）。
# 生成 SVG はコミット対象なので、図の .tex を触ったときだけ実行する。
figures:
	python3 tools/build_figures.py

# GitHub Pages 用の許可リスト済み静的公開物を .pages/ に生成する。
# 例: make pages VERSION=v1.0.0
pages:
ifndef VERSION
	@echo "使い方: make pages VERSION=v1.0.0"
	@exit 1
else
	python3 tools/build_pages.py $(VERSION)
endif

# 生成物のうちコミットしないものだけ消す。
# 図の SVG はコミット対象なので触らない（作り直すなら make figures）。
clean:
	rm -rf .site .pages
