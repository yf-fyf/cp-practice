"""第05回 パッケージ依存関係（Boolean モデル） — 穴埋め前

教材ページ: 講義（全15回）> 第05回 SAT概説とパッケージ依存関係: Booleanモデル
実行環境:   Python + z3-solver（版は requirements.txt にある）

    python3 deps.py

TODO の4か所を埋めると、インストール可能な組合せが1つ表示される。
TODO(1)〜TODO(4) が必須演習、その先が標準演習である。
"""

from z3 import *

# 架空のパッケージ5つ。この科目のために作った設定である。
PACKAGES = ["app", "gui", "net", "db", "legacy"]

# use[name] が真なら「そのパッケージを入れる」という意味にする。
use = {name: Bool(f"use_{name}") for name in PACKAGES}

s = Solver()

# ── 制約 ────────────────────────────────────────────────────
# TODO(1) 必須演習: app は必ず入れる。
#   「app を入れる」という命題がそのまま制約になる。
# s.add(...)

# TODO(2) 必須演習: 依存関係を2つ書く。
#   app を入れるなら gui も入れる。gui を入れるなら net も入れる。
#   「A ならば B」は Implies(A, B) と書く。
# s.add(...)
# s.add(...)

# TODO(3) 必須演習: app を入れるなら、db か legacy の少なくとも一方を入れる。
#   「少なくとも一方」は Or(...) である。
# s.add(...)

# TODO(4) 必須演習: db と legacy は同時には入れられない（競合する）。
#   「両方は真にならない」は Or(Not(...), Not(...)) と書ける。
# s.add(...)

# ── 標準演習: ここから下に制約を足していく ────────────────────
# 1つ足すと選ばれる組合せが変わり、もう1つ足すと unsat になる、
# という2段階を自分で作る。


# ── 求解と表示 ──────────────────────────────────────────────
result = s.check()
print(result)

if result == sat:
    m = s.model()
    for name in PACKAGES:
        print(f"  {name:6s} {'入れる' if is_true(m[use[name]]) else '入れない'}")
else:
    print("  この条件をすべて満たす入れ方は無い")
