/* Prolog 実行ページ（Tau Prolog 同梱）
 *
 * 設計の要点
 *   - 通信をしない。処理系は vendor/tau-prolog/ から読み込む。
 *   - 長い探索でも画面が固まらないように、推論を「スライス」に刻んで実行する。
 *     Tau Prolog は pl.create(limit) の limit を超えると limit コールバックへ戻り、
 *     状態を保ったまま中断する。そこで setTimeout で制御を返してから再開する。
 *     ステップ数と実時間の関係は問題によって数十倍違うので、1スライスの
 *     実時間を測って次のスライスのステップ数を調整する（目標 SLICE_TARGET_MS）。
 *   - 「中断」は再開を止めるだけでよい。押されるまでの探索は捨てる。
 */

(function () {
  "use strict";

  // ── 実行の刻み ──
  var SLICE_TARGET_MS = 60;    // 1スライスの目標実時間（この間だけ画面が止まる）
  var SLICE_MIN = 2000;        // 1スライスの推論ステップ数の下限
  var SLICE_MAX = 200000;      // 同 上限
  var SLICE_START = 20000;     // 最初のスライス
  var STORAGE_PROGRAM = "cp-practice.prolog.program";
  var STORAGE_QUERY = "cp-practice.prolog.query";

  // ── サンプル ──
  // 登場する人物・地区・データはすべて架空である。
  var SAMPLES = [
    {
      id: "facts",
      label: "第01回 事実と規則（4人の知識ベース）",
      note: "クエリ例: drinks(aoi, X) / club(X, tennis) / teammate(aoi, Y)",
      query: "drinks(aoi, X)",
      program: String.raw`% 第01回 小さな知識ベース（架空のデータ）
% 事実はピリオドで終わる。小文字始まりがアトム、大文字始まりが変数。

% 好きな飲み物
drinks(aoi, cocoa).
drinks(hikaru, coffee).
drinks(tsubasa, tea).
drinks(kaede, cocoa).

% 所属サークル
club(aoi, photo).
club(hikaru, tennis).
club(tsubasa, brass_band).
club(kaede, photo).

% 通学手段
commute(aoi, bicycle).
commute(hikaru, train).
commute(tsubasa, walk).
commute(kaede, train).

% 規則: 同じサークルの2人は teammate である
teammate(X, Y) :- club(X, C), club(Y, C).

% 試すクエリ
%   drinks(aoi, X)          aoi は何を飲むか
%   club(X, tennis)         テニス部は誰か
%   drinks(X, cocoa), commute(X, M)   ココアを飲む人の通学手段
%   teammate(aoi, Y)        「次の解」を押して全部見る
`
    },
    {
      id: "member",
      label: "第02回 リストと member（候補を選ぶ）",
      note: "クエリ例: drink(X) / pair(D, C) / member(X, [train, bicycle, walk])",
      query: "drink(X)",
      program: String.raw`% 第02回 リストから候補を選ぶ
% member/2 は lists ライブラリの述語である。
:- use_module(library(lists)).

drink(D) :- member(D, [coffee, tea, cocoa]).
club(C) :- member(C, [tennis, brass_band, photo]).

% 候補を生成してから条件で絞り込む（生成とテスト）
% \= は「等しくない」。tea 以外の飲み物と、テニス部以外のサークルの組
pair(D, C) :-
    drink(D),
    club(C),
    D \= tea,
    C \= tennis.

% 試すクエリ
%   drink(X)
%   member(X, [train, bicycle, walk])
%   pair(D, C)              「次の解」で候補が次々出る
`
    },
    {
      id: "logic-grid",
      label: "第02回 論理グリッド（4人・3属性）",
      note: "クエリ例: solve(People)。解は1通りしかない（「次の解」を押すと false. になる）",
      query: "solve(People)",
      program: String.raw`% 第02回 論理グリッド（架空のデータ）
% 4人に、飲み物・サークル・通学手段を1つずつ割り当てる。
:- use_module(library(lists)).

% 並べ替え（permutation）で候補を作ると、
% 「同じ飲み物が2人にならない」ことが最初から保証される。
solve(People) :-
    People = [p(aoi,     D1, C1, T1),
              p(hikaru,  D2, C2, T2),
              p(tsubasa, D3, C3, T3),
              p(kaede,   D4, C4, T4)],
    permutation([coffee, tea, cocoa, juice],        [D1, D2, D3, D4]),
    permutation([tennis, brass_band, photo, art],   [C1, C2, C3, C4]),
    permutation([train, bicycle, walk, bus],        [T1, T2, T3, T4]),

    % 手掛かり
    member(p(hikaru, _, _, train), People),              % 1 hikaru は電車通学
    member(p(_, coffee, tennis, _), People),             % 2 コーヒーの人はテニス部
    member(p(_, _, photo, walk), People),                % 3 写真部の人は徒歩通学
    member(p(aoi, _, AoiClub, _), People),
    AoiClub \= photo,                                    % 4 aoi は写真部ではない
    member(p(_, tea, brass_band, _), People),            % 5 吹奏楽部の人は紅茶
    member(p(kaede, _, _, bus), People),                 % 6 kaede はバス通学
    member(p(tsubasa, TsuDrink, _, _), People),
    TsuDrink \= cocoa,                                   % 7 tsubasa はココアを飲まない
    member(p(_, _, art, bicycle), People),               % 8 美術部の人は自転車通学
    member(p(kaede, _, KaeClub, _), People),
    KaeClub \= tennis.                                   % 9 kaede はテニス部ではない

% 試すクエリ
%   solve(People)
% 手掛かりを1つコメントアウトすると解が増える（発展演習）。
`
    },
    {
      id: "logic-grid-5",
      label: "第02回 発展 論理グリッド（5人・4属性）",
      note: "手掛かりを置く位置で実行時間が大きく変わる。まず solve(People) を試す",
      query: "solve(People)",
      program: String.raw`% 第02回 発展 論理グリッド（5人・4属性、架空のデータ）
% 属性を1つ並べ替えるたびに、その属性で分かる手掛かりを試す。
% 全部並べ替えてから手掛かりを試すと候補が 120^4 通りになり、終わらない。
:- use_module(library(lists)).

solve(People) :-
    People = [p(aoi,     D1, C1, T1, S1),
              p(hikaru,  D2, C2, T2, S2),
              p(tsubasa, D3, C3, T3, S3),
              p(kaede,   D4, C4, T4, S4),
              p(minori,  D5, C5, T5, S5)],

    % 飲み物
    permutation([coffee, tea, cocoa, juice, milk], [D1, D2, D3, D4, D5]),
    member(p(tsubasa, TsuDrink, _, _, _), People),
    TsuDrink \= cocoa,                                       % tsubasa はココアを飲まない
    member(p(minori, milk, _, _, _), People),                % minori は牛乳

    % サークル
    permutation([tennis, brass_band, photo, art, drama], [C1, C2, C3, C4, C5]),
    member(p(aoi, _, AoiClub, _, _), People),
    AoiClub \= photo,                                        % aoi は写真部ではない
    member(p(_, coffee, tennis, _, _), People),              % コーヒーの人はテニス部
    member(p(_, tea, brass_band, _, _), People),             % 吹奏楽部の人は紅茶
    member(p(kaede, _, KaeClub, _, _), People),
    KaeClub \= tennis,                                       % kaede はテニス部ではない

    % 通学手段
    permutation([train, bicycle, walk, bus, subway], [T1, T2, T3, T4, T5]),
    member(p(hikaru, _, _, train, _), People),               % hikaru は電車通学
    member(p(_, _, photo, walk, _), People),                 % 写真部の人は徒歩通学
    member(p(kaede, _, _, bus, _), People),                  % kaede はバス通学
    member(p(_, _, art, bicycle, _), People),                % 美術部の人は自転車通学
    member(p(minori, _, _, subway, _), People),              % minori は地下鉄通学

    % 好きな色
    permutation([red, blue, green, yellow, white], [S1, S2, S3, S4, S5]),
    member(p(_, _, drama, _, red), People),                  % 演劇部の人は赤
    member(p(_, juice, _, _, blue), People),                 % ジュースの人は青
    member(p(kaede, _, _, _, green), People),                % kaede は緑
    member(p(aoi, _, _, _, AoiColor), People),
    AoiColor \= yellow,                                      % aoi は黄ではない
    member(p(hikaru, _, _, _, HikColor), People),
    HikColor \= white.                                       % hikaru は白ではない

% 試すクエリ
%   solve(People)
`
    },
    {
      id: "graph-coloring",
      label: "第02回 グラフ彩色（5地区・3色）",
      note: "クエリ例: paint(Kita, Minami, Higashi, Nishi, Chuo)",
      query: "paint(Kita, Minami, Higashi, Nishi, Chuo)",
      program: String.raw`% 第02回 グラフ彩色（架空の市の5地区を3色で塗り分ける）
% 隣り合う地区は違う色にする。論理グリッドと同じ「生成とテスト」の形。

color(red).
color(green).
color(blue).

% 地区のつながり
%   中央区は北区・南区・東区・西区のすべてと隣り合う
%   外側は 北 - 東 - 南 - 西 - 北 の順に隣り合う
paint(Kita, Minami, Higashi, Nishi, Chuo) :-
    color(Kita), color(Minami), color(Higashi), color(Nishi), color(Chuo),
    Kita \= Chuo,
    Minami \= Chuo,
    Higashi \= Chuo,
    Nishi \= Chuo,
    Kita \= Higashi,
    Higashi \= Minami,
    Minami \= Nishi,
    Nishi \= Kita.

% 試すクエリ
%   paint(Kita, Minami, Higashi, Nishi, Chuo)
% 「次の解」で別の塗り分けが出る。色の名前を1つ減らすとどうなるか試す。
`
    }
  ];

  // ── DOM ──
  var el = {};
  var session = null;
  var running = false;
  var aborted = false;
  var sliceSteps = SLICE_START;
  var answerCount = 0;
  var startedAt = 0;

  function $(id) { return document.getElementById(id); }

  function store(key, value) {
    try { window.localStorage.setItem(key, value); } catch (e) { /* 保存できなくても動く */ }
  }
  function restore(key) {
    try { return window.localStorage.getItem(key); } catch (e) { return null; }
  }

  // ── 出力 ──

  function clearOutput() { el.output.textContent = ""; }

  function write(text, cls) {
    var node = document.createElement("span");
    node.className = cls || "ans";
    node.textContent = text + "\n";
    el.output.appendChild(node);
    el.output.scrollTop = el.output.scrollHeight;
  }

  function setStatus(text, state) {
    el.status.textContent = text;
    if (state) { el.status.setAttribute("data-state", state); }
    else { el.status.removeAttribute("data-state"); }
  }

  /* 引数は「押せるかどうか」。探索中だけ「中断」が押せ、
     解が出た直後と中断直後だけ「次の解」が押せる。 */
  function setButtons(runOk, nextOk, stopOk) {
    el.run.disabled = !runOk;
    el.next.disabled = !nextOk;
    el.stop.disabled = !stopOk;
  }

  // ── エラーの読み替え ──
  // Tau Prolog のエラー項をそのまま出すと読めないので、原文に加えて
  // 日本語の手掛かりを添える。原文も残すのは、検索して調べられるようにするため。
  function errorText(err) {
    if (err === undefined || err === null) { return "不明なエラー"; }
    var term = err;
    try {
      // consult / query の失敗は throw(error(...)) の形で渡ってくる
      if (term.indicator === "throw/1" && term.args && term.args.length === 1) {
        term = term.args[0];
      }
      // session を渡すと lieks/2 のように演算子の形で表示される
      return term.toString({ quoted: true, session: session });
    } catch (e) {
      return String(err);
    }
  }

  var HINTS = [
    [/syntax_error/, "構文エラーです。節の終わりのピリオド、条件のつなぎのカンマ、括弧の対応、"
      + "引用符のとじ忘れを確かめてください。日本語をアトムに使うときは 'コーヒー' のように引用符が要ります。"],
    [/existence_error\(\s*procedure\s*,\s*([^)]*)\)/,
      "その述語がまだ定義されていません。綴りと引数の個数を確かめてください。"
      + "member や permutation を使うときは、プログラムの先頭に :- use_module(library(lists)). が要ります。"],
    [/instantiation_error/, "値が決まっていない変数が使われました。先に値が決まる順に条件を並べ替えてみてください。"],
    [/type_error/, "引数の種類が合いません。数とアトム、リストとアトムを取り違えていないか確かめてください。"]
  ];

  function hintFor(text) {
    for (var i = 0; i < HINTS.length; i++) {
      if (HINTS[i][0].test(text)) { return HINTS[i][1]; }
    }
    return null;
  }

  function reportError(where, err) {
    var text = errorText(err);
    var line = /line\(\s*([0-9]+)\s*\)/.exec(text);
    write(where + "でエラーが起きました。"
      + (line ? "（プログラムの " + line[1] + " 行目のあたり）" : ""), "err");
    write("  " + text, "err");
    var hint = hintFor(text);
    if (hint) { write("  → " + hint, "hint"); }
    setStatus("エラー", "error");
    setButtons(true, false, false);
    running = false;
  }

  // ── 実行 ──

  function programText() {
    var text = el.program.value;
    // lists ライブラリを使う書き方をしているのに use_module が無いときだけ補う。
    // 行番号がずれないように末尾へ足す（クエリはロード後に走るので順序は問題ない）。
    if (!/use_module\s*\(\s*library\s*\(\s*lists\s*\)\s*\)/.test(text)
        && /\b(member|permutation|append|nth0|nth1|msort|select|reverse|last|length|maplist|sum_list)\s*\(/.test(text)) {
      text += "\n:- use_module(library(lists)).\n";
    }
    return text + "\n";
  }

  function queryText() {
    var text = el.query.value.trim();
    if (text === "") { return null; }
    return text.replace(/\.\s*$/, "") + ".";
  }

  function elapsed() {
    return ((Date.now() - startedAt) / 1000).toFixed(1);
  }

  function finish(message, state) {
    running = false;
    setStatus(message, state || "done");
    setButtons(true, true, false);
  }

  /* 1スライスぶんだけ解を探し、続きがあれば制御を画面に返してから再開する。 */
  function step() {
    if (aborted) { return; }
    var sliceStart = Date.now();
    session.limit = sliceSteps;
    session.answer({
      success: function (answer) {
        answerCount += 1;
        write("解 " + answerCount + ": " + session.format_answer(answer, { quoted: true }) + ".", "ans");
        finish("解が見つかりました（" + elapsed() + " 秒）。続きは「次の解」。", "done");
      },
      fail: function () {
        if (answerCount === 0) {
          write("false.", "no");
          write("  → 条件を満たすものは見つかりませんでした。", "hint");
        } else {
          write("false.", "no");
          write("  → これ以上の解はありません。", "hint");
        }
        running = false;
        setStatus("終了（" + elapsed() + " 秒）", "done");
        setButtons(true, false, false);
      },
      error: function (err) { reportError("問い合わせ", err); },
      limit: function () {
        // ステップ上限に達しただけ。状態は残っているのでそのまま再開できる。
        var took = Date.now() - sliceStart;
        if (took > 0) {
          var scaled = Math.round(sliceSteps * (SLICE_TARGET_MS / took));
          sliceSteps = Math.min(SLICE_MAX, Math.max(SLICE_MIN, scaled || SLICE_MIN));
        }
        if (aborted) { return; }
        setStatus("探索中… " + elapsed() + " 秒（「中断」で止められます）", "running");
        window.setTimeout(step, 0);
      }
    });
  }

  function run() {
    var goal = queryText();
    if (goal === null) {
      clearOutput();
      write("クエリが空です。問い合わせたいことを1行書いてください。", "err");
      setStatus("クエリが空", "error");
      return;
    }
    store(STORAGE_PROGRAM, el.program.value);
    store(STORAGE_QUERY, el.query.value);

    clearOutput();
    aborted = false;
    running = true;
    answerCount = 0;
    sliceSteps = SLICE_START;
    startedAt = Date.now();
    setStatus("読み込み中…", "running");
    setButtons(false, false, true);

    session = pl.create(sliceSteps);
    session.consult(programText(), {
      success: function () {
        if (aborted) { return; }
        session.query(goal, {
          success: function () { if (!aborted) { step(); } },
          error: function (err) { reportError("クエリの読み取り", err); }
        });
      },
      error: function (err) { reportError("プログラムの読み込み", err); }
    });
  }

  function next() {
    if (session === null) { return; }
    aborted = false;
    running = true;
    sliceSteps = SLICE_START;
    startedAt = Date.now();
    setStatus("探索中…", "running");
    setButtons(false, false, true);
    step();
  }

  function stop() {
    if (!running) { return; }
    aborted = true;
    running = false;
    write("（中断しました。「次の解」を押すと続きから探索を再開できます）", "hint");
    setStatus("中断しました（" + elapsed() + " 秒）", "error");
    setButtons(true, true, false);
  }

  function reset() {
    aborted = true;
    running = false;
    session = null;
    answerCount = 0;
    clearOutput();
    write("リセットしました。プログラムを読み直してから実行します。", "hint");
    setStatus("待機中");
    setButtons(true, false, false);
  }

  // ── サンプル ──

  function sampleById(id) {
    for (var i = 0; i < SAMPLES.length; i++) {
      if (SAMPLES[i].id === id) { return SAMPLES[i]; }
    }
    return null;
  }

  function applySample(sample) {
    el.program.value = sample.program;
    el.query.value = sample.query;
    el.sample.value = sample.id;
    el.sampleNote.textContent = sample.note;
    store(STORAGE_PROGRAM, sample.program);
    store(STORAGE_QUERY, sample.query);
    reset();
    setStatus("サンプルを読み込みました");
  }

  /* ?example=logic-grid でも #logic-grid でも選べる（教材ページから直接張れるように） */
  function requestedSample() {
    var match = /[?&]example=([^&#]+)/.exec(window.location.search);
    var id = match ? decodeURIComponent(match[1]) : window.location.hash.replace(/^#/, "");
    return id ? sampleById(decodeURIComponent(id)) : null;
  }

  // ── 起動 ──

  function init() {
    el.sample = $("sample");
    el.sampleNote = $("sample-note");
    el.program = $("program");
    el.query = $("query");
    el.output = $("output");
    el.status = $("status");
    el.run = $("run");
    el.next = $("next");
    el.stop = $("stop");

    for (var i = 0; i < SAMPLES.length; i++) {
      var option = document.createElement("option");
      option.value = SAMPLES[i].id;
      option.textContent = SAMPLES[i].label;
      el.sample.appendChild(option);
    }

    if (typeof window.pl === "undefined") {
      el.output.textContent =
        "Prolog 処理系（vendor/tau-prolog/）を読み込めませんでした。\n"
        + "ページを再読み込みしても直らないときは、教材ページから案内されている\n"
        + "SWISH（外部サイト）を代わりに使ってください。";
      setStatus("処理系を読み込めません", "error");
      setButtons(false, false, false);
      return;
    }

    el.run.addEventListener("click", run);
    el.next.addEventListener("click", next);
    el.stop.addEventListener("click", stop);
    $("reset").addEventListener("click", reset);
    $("load").addEventListener("click", function () {
      var sample = sampleById(el.sample.value);
      if (sample) { applySample(sample); }
    });
    el.query.addEventListener("keydown", function (event) {
      if (event.key === "Enter") { event.preventDefault(); run(); }
    });

    var requested = requestedSample();
    var savedProgram = restore(STORAGE_PROGRAM);
    var savedQuery = restore(STORAGE_QUERY);
    if (requested) {
      applySample(requested);
    } else if (savedProgram !== null && savedProgram !== "") {
      el.program.value = savedProgram;
      el.query.value = savedQuery || "";
      el.sampleNote.textContent = "前回の編集内容を復元しました。サンプルに戻すときは上から選び直します。";
      setStatus("待機中");
    } else {
      applySample(SAMPLES[0]);
      setStatus("待機中");
    }
    setButtons(true, false, false);

    el.program.addEventListener("input", function () { store(STORAGE_PROGRAM, el.program.value); });
    el.query.addEventListener("input", function () { store(STORAGE_QUERY, el.query.value); });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
