-- site/boxes.lua
-- 原稿の Markdown をサイト用の HTML へ寄せる pandoc フィルタ。
--
-- やること:
--   1. 先頭の H1 をページタイトルへ移す（本文からは外す）
--   2. "この回の目標" H2 から次の同階層見出しまでを .goal で囲む
--   3. ::: note / important / warning / term / predict / exercise / check /
--      discuss / done を .adm へ変換し、見出し語を付ける
--      （exercise は level=required|standard|advanced で見出し語とクラスを変える）
--   4. ::: {.hint summary="..."} を <details class="hint"> へ変換する
--   5. コードフェンスの言語別名を pandoc のハイライト名へ寄せ、
--      filename= 属性があれば <figure class="code"><figcaption> で包む
--   6. 図の参照を .pdf から .svg へ、パスをページ深さに合わせて書き換える
--   7. .md へのリンクをサイト内 URL へ、サイトに無いものは GitHub へ逃がす
--
-- 見出しレベルの繰り上げはしない。HTML では H1 をそのままページ見出しに使う。

-- 「この回の目標」は tools/check_docs.py の structure 検査も参照する検出語。
-- 変えるときは check_docs.py の GOAL_HEADING も一緒に直す。
local GOAL_HEADING = "この回の目標"

local box_title = {
  note      = "補足",
  important = "重要",
  warning   = "注意",
  term      = "用語",
  predict   = "予想",
  exercise  = "演習",
  check     = "チェックポイント",
  discuss   = "考察",
  done      = "完了チェック",
}

-- 演習の3段階。::: {.exercise level=required} のように書く。
-- 独立したクラスにせず属性で持つのは、演習の本体（本文・完了条件・ヒント）が
-- 段階によらず同じ形をしているため。CSS 側は adm-exercise-<level> で色を変える。
local exercise_level_title = {
  required = "必須演習",
  standard = "標準演習",
  advanced = "発展演習",
}

-- pandoc が知らない綴りを、対応するハイライト名へ寄せる。
-- 原稿側の綴り（z3py 等）は読みやすさのため変えない。
local lang_alias = {
  z3py = "python",   -- Z3Py も Python として着色する
  pl   = "prolog",   -- .pl の拡張子に合わせた綴り
}

-- ハイライトの対象にしないもの（pandoc に渡すと警告が出る）。
-- data-lang 属性だけ付けて素の <pre> にし、ラベルは CSS が出す。
local no_highlight = {
  text = true, plain = true,
  minizinc = true, mzn = true, dzn = true,  -- pandoc 3.x は MiniZinc 非対応
  solver = true,                            -- ソルバーの解・探索統計
}

-- data-lang に出すラベル。綴りをそのまま出すと読み手に通じないものだけ書く。
local lang_label = {
  mzn    = "minizinc",
  dzn    = "minizinc data",
  solver = "ソルバー出力",
  z3py   = "python",
}

local figbase  = "../../figures"
local blobbase = ""
local srcdir   = ""
local linkmap  = {}

--- "a/b/../c" のような相対パスを "a/c" に畳む
local function normalize(path)
  local parts = {}
  for part in path:gmatch("[^/]+") do
    if part == ".." then
      table.remove(parts)
    elseif part ~= "." then
      parts[#parts + 1] = part
    end
  end
  return table.concat(parts, "/")
end

function Meta(meta)
  if meta.figbase  then figbase  = pandoc.utils.stringify(meta.figbase)  end
  if meta.blobbase then blobbase = pandoc.utils.stringify(meta.blobbase) end
  if meta.srcdir   then srcdir   = pandoc.utils.stringify(meta.srcdir)   end
  if meta.linkmap then
    for key, value in pairs(meta.linkmap) do
      linkmap[key] = pandoc.utils.stringify(value)
    end
  end
  -- テンプレートへ渡す必要はないので落とす
  meta.linkmap = nil
  return meta
end

--- ::: {.hint summary="..."} を <details> にする。
--- JavaScript を使わずに開閉できるので、JS 無しでも閲覧できる方針と両立する。
local function hint_details(el)
  local summary = el.attributes["summary"] or "ヒント"
  local out = pandoc.List({
    pandoc.RawBlock("html", '<details class="hint">'),
    pandoc.RawBlock("html",
      "<summary>" .. pandoc.utils.stringify(summary):gsub("&", "&amp;")
        :gsub("<", "&lt;"):gsub(">", "&gt;") .. "</summary>"),
    pandoc.RawBlock("html", '<div class="hint-body">'),
  })
  out:extend(el.content)
  out:insert(pandoc.RawBlock("html", "</div></details>"))
  return out
end

function Div(el)
  if el.classes:includes("hint") then
    return hint_details(el)
  end
  for class, title in pairs(box_title) do
    if el.classes:includes(class) then
      local classes = "adm adm-" .. class
      if class == "exercise" then
        local level = el.attributes["level"]
        local levelled = level and exercise_level_title[level]
        if levelled then
          title = levelled
          classes = classes .. " adm-exercise-" .. level
        end
      end
      local head = pandoc.Div({ pandoc.Plain({ pandoc.Str(title) }) },
                              { class = "adm-title" })
      local body = pandoc.List({ head })
      body:extend(el.content)
      return pandoc.Div(body, { class = classes })
    end
  end
  return nil
end

function CodeBlock(el)
  local lang = el.classes[1]
  if not lang then return nil end

  -- filename= はキャプションに回すので、属性としては消す
  local filename = el.attributes["filename"]
  el.attributes["filename"] = nil

  el.attributes["data-lang"] = lang_label[lang] or lang
  if no_highlight[lang] then
    -- 言語名のクラスだけ落として素の <pre data-lang="..."> にする。
    -- 残したままだと pandoc が「その言語の構文定義が無い」と警告を出す。
    -- ```{.text .error} のような追加のクラス（配色の指定）は残す。
    local rest = pandoc.List({})
    for index = 2, #el.classes do rest:insert(el.classes[index]) end
    el.classes = rest
  else
    local alias = lang_alias[lang]
    if alias then
      el.classes[1] = alias
    end
  end

  if filename then
    local caption = pandoc.utils.stringify(filename)
      :gsub("&", "&amp;"):gsub("<", "&lt;"):gsub(">", "&gt;")
    return pandoc.List({
      pandoc.RawBlock("html", '<figure class="code">'),
      pandoc.RawBlock("html", "<figcaption>" .. caption .. "</figcaption>"),
      el,
      pandoc.RawBlock("html", "</figure>"),
    })
  end
  return el
end

function Image(el)
  -- 原稿は figures/... の相対参照で書かれている
  local src = el.src:gsub("%.pdf$", ".svg")
  src = src:gsub("^figures/", figbase .. "/")
  el.src = src
  return el
end

function Table(el)
  -- 狭い画面では列が潰れて読めなくなる。横スクロールできる容器で包む。
  -- 包むだけでは table の width:100% が効いて縮むので、幅は CSS 側で与える。
  return pandoc.Div({ el }, { class = "table-scroll" })
end

function Link(el)
  local target, anchor = el.target:match("^([^#]*)(#?.*)$")
  if not target or not target:match("%.md$") then
    return nil
  end
  if target:match("^%a+://") then
    return nil
  end
  local resolved = normalize(srcdir .. "/" .. target)
  local site = linkmap[resolved]
  if site then
    el.target = site .. anchor
  elseif blobbase ~= "" then
    -- サイトに載せていない文書はリポジトリ側へ送る
    el.target = blobbase .. resolved .. anchor
  end
  return el
end

function Pandoc(doc)
  local blocks = pandoc.List({})

  -- 先頭 H1 をページタイトルへ移す
  local first = doc.blocks[1]
  local start = 1
  if first and first.t == "Header" and first.level == 1 then
    doc.meta.title = pandoc.MetaInlines(first.content)
    start = 2
  end

  local i = start
  local n = #doc.blocks
  while i <= n do
    local block = doc.blocks[i]

    if block.t == "Header" and block.level == 2
       and pandoc.utils.stringify(block.content) == GOAL_HEADING then
      local inner = pandoc.List({ block })
      i = i + 1
      while i <= n do
        local nxt = doc.blocks[i]
        if nxt.t == "Header" and nxt.level <= 2 then break end
        inner:insert(nxt)
        i = i + 1
      end
      blocks:insert(pandoc.Div(inner, { class = "goal" }))
    else
      blocks:insert(block)
      i = i + 1
    end
  end

  doc.blocks = blocks
  return doc
end

-- Meta を先に走らせてから本体の要素を触る
return {
  { Meta = Meta },
  { Div = Div, CodeBlock = CodeBlock, Image = Image, Link = Link, Table = Table },
  { Pandoc = Pandoc },
}
