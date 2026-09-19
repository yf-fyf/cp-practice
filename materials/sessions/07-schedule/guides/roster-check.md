# 勤務表の実行と検査

第07回の[本文](../lesson.md)と[発展演習](../advanced-exercises.md)の操作をまとめる。入力は問題の条件であり、出力される勤務表とは別である。前回や前の演習のファイルがなくても、以下の完成した基本モデルから再開できる。

## 基本と技能

MiniZinc IDEでモデルを開き、データファイルを選んで実行する。コマンドを使う場合は、配布ファイルを同じフォルダへ保存し、そこで次を実行する。`-a` は全解を列挙する指定で、一つの勤務表を見るだけなら不要である。

```sh
minizinc --solver gecode roster-basic.mzn base.dzn
minizinc --solver gecode roster-basic.mzn practice.dzn
```

必修1は `practice-start.mzn` に変数と三条件を書く。必修2で再開する場合は `roster-basic.mzn` をコピーし、`skill-start.mzn` の作業をそこへ追加する。完成した必修1を手元に持っている必要はない。技能条件を書いたファイルを `roster-skill.mzn` と保存した例では、次の二つの入力を同時に渡す。

```sh
minizinc --solver gecode roster-skill.mzn practice.dzn skill.dzn
```

発展1・2はそれぞれの出発ファイルのTODOを記入し、次を実行する。発展2に発展1の排他条件や必修2の技能入力を加えない。技能2の必要人数を変更する場合は `skills.dzn` のコピーを作って `skill_required` の第2行だけを書き換える。

```sh
minizinc --solver gecode pair-start.mzn practice.dzn
minizinc --solver gecode two-skill-start.mzn practice.dzn skills.dzn
```

`UNSATISFIABLE` は条件を満たす表がないという判定である。時間切れや `UNKNOWN` は不可能性の証明ではない。充足の一例を公平さの最適解と呼ばない。

## 技能の固定検査

技能条件を書いた自分の`roster-skill.mzn`の末尾へ、次のうち一方の`constraint`{.minizinc}だけを一時的に追加する。行はA〜E、列は1〜4日目である。入力は通常どおり`practice.dzn`と`skill.dzn`を指定する。新しい条件を書くのではなく、特定の表が自分の条件を満たすか調べる操作である。

受理する表（AB／AD／CD／BC）：

```minizinc
constraint work = [| 1, 1, 0, 0
                  | 1, 0, 0, 1
                  | 0, 0, 1, 1
                  | 0, 1, 1, 0
                  | 0, 0, 0, 0 |];
```

拒否する表（DE／AC／BD／BC）：

```minizinc
constraint work = [| 0, 1, 0, 0
                  | 0, 0, 1, 1
                  | 0, 1, 0, 1
                  | 1, 0, 1, 0
                  | 1, 0, 0, 0 |];
```

```sh
minizinc --solver gecode roster-skill.mzn practice.dzn skill.dzn
```

前者は解あり、後者はUNSATISFIABLEが期待される。後者は1日目に技能を持つ人がいない。二つの固定を同時に書くと、技能に関係なく矛盾するので、交換して実行する。確認後は固定の行を外し、自由に勤務表を探すモデルへ戻す。

## 二人の固定検査

発展1では、[技能の固定検査](#技能の固定検査)にある二つの表を、技能なしの自分の`pair-start.mzn`へ一方ずつ固定して使える。渡す入力は`practice.dzn`だけで、技能入力・技能条件は加えない。

| 固定する表 | 発展1での期待 | 理由 |
|---|---|---|
| AB／AD／CD／BC | 拒否 | 1日目にAとBが同時に勤務する |
| DE／AC／BD／BC | 受理 | AとBは同日勤務せず、1日目は二人とも休む |

```sh
minizinc --solver gecode pair-start.mzn practice.dzn
```

技能の検査とは受理・拒否が逆になる。固定した表がどの問題の条件を満たすかを区別する。後者も拒否した場合は、二人の和を等号1にしていないか確かめる。確認後は固定の制約を外す。

## 周期勤務の検査

周期問題の作業を記入したモデルを次のように実行する。表示の最初の一行は、初日から順に二人ずつ並べたJSONである。例えば `[1,5]` は群1の人1と群2の人5を選んだ一日を表す。後続の区切り線を含めず、その一行を自分の `pairs.json` に保存する。

```sh
minizinc --solver gecode cycle-start.mzn cycle-14.dzn
minizinc --solver gecode cycle-start.mzn cycle-16.dzn
python cycle-check-start.py cycle-14.json pairs.json
```

最後のコマンドはPython側のTODOを記入してから使う。16日の出力には `cycle-16.json` を渡す。`.dzn` はMiniZinc用、`.json` は独立検査用で、同じ群人数・期間・勤務日数の境界を持つ。検査結果 `VALID` は全条件を満たし、`INVALID` は少なくとも一つに違反するという意味である。

`cycle-cases.json` は確認用の三つの表と期待判定を持つ。検査関数を記入した後に、同じフォルダで次を実行できる。自分で作った16日の表についても検査し、各人の日数と16組の使い方から上限に達したことを説明する。

```python
import importlib.util
import json
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "checker", "cycle-check-start.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)
for case in json.loads(Path("cycle-cases.json").read_text()):
    data = json.loads(Path(case["input"]).read_text())
    result = checker.valid_schedule(data, case["pairs"])
    print(case["name"], result, "expected", case["valid"])
```

17日は勤務の供給人日と異なる組の数のどちらからも不可能と説明できる。追加で実行を試す入力も用意したが、長い探索を授業内に待ち続ける必要はない。時間上限を付けた次の実行が終了しても、判定がUNKNOWNならUNSATと読み替えない。

```sh
minizinc --solver gecode --time-limit 10000 cycle-start.mzn cycle-17.dzn
```

## 配布一覧

同じフォルダへ保存する。周期勤務の検査に外部のPythonパッケージは必要ない。開始モデルと検査器のTODOは学習者が記入し、完成解答はこの一覧に含めない。

- [roster-basic.mzn](../../../../workbook/sessions/07-schedule/roster-basic.mzn)
- [base.dzn](../../../../workbook/sessions/07-schedule/base.dzn)
- [practice.dzn](../../../../workbook/sessions/07-schedule/practice.dzn)
- [practice-start.mzn](../../../../workbook/sessions/07-schedule/practice-start.mzn)
- [skill.dzn](../../../../workbook/sessions/07-schedule/skill.dzn)
- [skill-start.mzn](../../../../workbook/sessions/07-schedule/skill-start.mzn)
- [skills.dzn](../../../../workbook/sessions/07-schedule/skills.dzn)
- [pair-start.mzn](../../../../workbook/sessions/07-schedule/pair-start.mzn)
- [two-skill-start.mzn](../../../../workbook/sessions/07-schedule/two-skill-start.mzn)
- [cycle-start.mzn](../../../../workbook/sessions/07-schedule/cycle-start.mzn)
- [cycle-14.dzn](../../../../workbook/sessions/07-schedule/cycle-14.dzn)
- [cycle-14.json](../../../../workbook/sessions/07-schedule/cycle-14.json)
- [cycle-16.dzn](../../../../workbook/sessions/07-schedule/cycle-16.dzn)
- [cycle-16.json](../../../../workbook/sessions/07-schedule/cycle-16.json)
- [cycle-17.dzn](../../../../workbook/sessions/07-schedule/cycle-17.dzn)
- [cycle-17.json](../../../../workbook/sessions/07-schedule/cycle-17.json)
- [cycle-check-start.py](../../../../workbook/sessions/07-schedule/cycle-check-start.py)
- [cycle-cases.json](../../../../workbook/sessions/07-schedule/cycle-cases.json)
