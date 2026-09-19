--[[
講義ページ用のPandocフィルター。

[サイト設計](../design/site-design.md)に沿って、
次の変換を行う。公開側の site/boxes.lua とは別系統で、新しい部品だけを扱う。

  1. リードの包み込み（H1の後、最初のH2までを header.lead へ）
  2. H2への節番号の付与と、役割クラスの付与
  3. 目次の自前生成（pandocの --toc は使わない。番号を目次にも出すため）
  5. callout 7種の変換（場面・与えるもの・要点・問い・自己確認・ヒント・注意）
     与えるものの器だけはラベルを原稿側で指定する（label 属性）
  6. 旧部品名の警告（変換しない）
  7. ファイル名つきコードの figure 化と、表の横スクロール容器

pandoc は Header の属性を --section-divs の section へ写すので、役割クラスは
Header に付ければ section 側からも使える。
--]]

local SECTION_ROLE = {
  ["目標"]     = "sec-goal",
  ["問題"]     = "sec-problem",
  ["定式化"]   = "sec-model",
  ["解説例"]   = "sec-demo",
  ["結果"]     = "sec-result",
  ["演習"]     = "sec-exercise",
  ["発展"]     = "sec-advanced",
  ["振り返り"] = "sec-review",
  ["参照"]     = "sec-reference",
}

-- 対象レベル（教材が与えるもの）と、それについての語りを分ける。
-- OBJECT_LEVEL の部品だけが地色を持つ。CSS 側と対応させること。
local CALLOUT_LABEL = {
  scenario = "場面",
  point    = "要点",
  ask      = "問い",
  check    = "自己確認",
  caution  = "注意",
}

-- 新しい原稿には混ぜない旧部品。変換せず警告だけ出す。
local RETIRED = {
  note = true, important = true, term = true, predict = true,
  discuss = true, done = true, exercise = true, goal = true, warning = true,
}

-- 固定の節名と番号は回別の講義ページにだけ課す。発展ページなど他の種類では、
-- 見出しの自由な命名を許し、目次と部品の変換だけを行う。
local strict_sections = true

local warnings = {}

local function warn(message)
  warnings[#warnings + 1] = message
  io.stderr:write("[lesson-boxes] " .. message .. "\n")
end

local function has_class(element, name)
  for _, class in ipairs(element.classes or {}) do
    if class == name then return true end
  end
  return false
end

--[[ 1〜4：見出しと目次 ]]

local toc_entries = {}
local section_number = 0

local function collect_and_mark(header)
  if header.level == 2 then
    local text = pandoc.utils.stringify(header.content)
    if not strict_sections then
      toc_entries[#toc_entries + 1] = {level = 2, id = header.identifier, label = text}
      return header
    end
    local role = SECTION_ROLE[text]
    if not role then
      -- 旧名（行動名）の残存を見分けられるようにする。
      if text:match("[るくすうつぬむぶ]$") then
        warn("H2が固定の名詞名でなく、動詞終止形です。旧名の残存を確認してください: " .. text)
      else
        warn("H2が固定の名詞名ではありません: " .. text)
      end
      role = "sec-other"
    end
    header.classes:insert(role)

    local label = text
    if not has_class(header, "unnumbered") then
      section_number = section_number + 1
      label = tostring(section_number) .. ". " .. text
      header.content:insert(1, pandoc.Str(tostring(section_number) .. "."))
      header.content:insert(2, pandoc.Space())
    end
    toc_entries[#toc_entries + 1] = {level = 2, id = header.identifier, label = label}
  elseif header.level == 3 then
    toc_entries[#toc_entries + 1] = {
      level = 3, id = header.identifier,
      label = pandoc.utils.stringify(header.content),
    }
  end
  return header
end

local function toc_html()
  local parts = {'<ul class="toc-list">'}
  local open_child = false
  for _, entry in ipairs(toc_entries) do
    local link = ('<a href="#%s">%s</a>'):format(entry.id, entry.label)
    if entry.level == 2 then
      if open_child then parts[#parts + 1] = "</ul>" ; open_child = false end
      if #parts > 1 then parts[#parts + 1] = "</li>" end
      parts[#parts + 1] = "<li>" .. link
    else
      if not open_child then parts[#parts + 1] = '<ul>' ; open_child = true end
      parts[#parts + 1] = "<li>" .. link .. "</li>"
    end
  end
  if open_child then parts[#parts + 1] = "</ul>" end
  if #parts > 1 then parts[#parts + 1] = "</li>" end
  parts[#parts + 1] = "</ul>"
  return table.concat(parts, "\n")
end

--[[ 5〜6：callout ]]

local function callout(div)
  for _, class in ipairs(div.classes) do
    if CALLOUT_LABEL[class] then
      local blocks = div.content
      if #blocks == 0 or blocks[1].t ~= "Para" then
        warn("calloutの先頭は段落にしてください: " .. class)
      else
        -- ラベルは1行目の行頭に run-in させる。帯は作らない。
        local label = pandoc.Span(pandoc.Str(CALLOUT_LABEL[class]),
                                  pandoc.Attr("", {"callout-label"}))
        blocks[1].content:insert(1, label)
        blocks[1].content:insert(2, pandoc.Space())
      end
      return pandoc.Div(blocks, pandoc.Attr(div.identifier,
        {"callout", "callout-" .. class}, {role = "note"}))
    end
    if class == "given" then
      -- 与えるものの器。レベルの区別は地色が担うので、ラベルは内容に合わせて
      -- 書き分ける（条件／入力／求めるもの／問題など）。
      local label = div.attributes["label"]
      if not label or label == "" then
        warn("givenにはlabelが必要です。何を与えているかを2〜6字で書いてください")
        label = "与えるもの"
      end
      local blocks = div.content
      if #blocks == 0 or blocks[1].t ~= "Para" then
        warn("calloutの先頭は段落にしてください: given")
      else
        blocks[1].content:insert(1, pandoc.Span(pandoc.Str(label),
                                                pandoc.Attr("", {"callout-label"})))
        blocks[1].content:insert(2, pandoc.Space())
      end
      return pandoc.Div(blocks, pandoc.Attr(div.identifier,
        {"callout", "callout-given"}, {role = "note"}))
    end
    if RETIRED[class] then
      warn("旧部品は使えません。設計案の§4.1の6種へ置き換えてください: " .. class)
      return nil
    end
  end
  return nil
end

local function hint(div)
  if not has_class(div, "hint") then return nil end
  local summary = div.attributes["summary"]
  if not summary or summary == "" then
    warn("hintにはsummaryが必要です")
    summary = "ヒント"
  end
  local opening = ('<details class="hint"><summary>%s</summary><div class="hint-body">')
    :format(summary)
  local blocks = pandoc.List({pandoc.RawBlock("html", opening)})
  blocks:extend(div.content)
  blocks:insert(pandoc.RawBlock("html", "</div></details>"))
  return blocks
end

--[[ 7：コードと表 ]]

local function code_block(block)
  local filename = block.attributes["filename"]
  if not filename then return nil end
  local attributes = {}
  for key, value in pairs(block.attributes) do
    if key ~= "filename" then attributes[key] = value end
  end
  local bare = pandoc.CodeBlock(block.text, pandoc.Attr(block.identifier, block.classes, attributes))
  -- Div で包むと section の直下に余分な div が挟まり、幅を広げる指定も届かなくなる。
  -- ブロックの並びを返して figure だけを直下へ置く。
  return pandoc.List({
    pandoc.RawBlock("html", ('<figure class="code"><figcaption>%s</figcaption>'):format(filename)),
    bare,
    pandoc.RawBlock("html", "</figure>"),
  })
end

local function table_scroll(element)
  return pandoc.Div({element}, pandoc.Attr("", {"table-scroll"}))
end

--[[ 組み立て ]]

function Pandoc(document)
  local kind = document.meta["page-kind"]
  if kind and pandoc.utils.stringify(kind) ~= "lesson" then
    strict_sections = false
  end

  local blocks = document.blocks

  -- リード：先頭から最初のH2の手前まで。原稿にH1が残っていればその後から。
  -- 題名はビルド側がpagetitleへ渡すので、通常この段階でH1は無い。
  local lead_start, lead_end = 1, nil
  for index, block in ipairs(blocks) do
    if block.t == "Header" and block.level == 1 and index == lead_start then
      lead_start = index + 1
    elseif block.t == "Header" and block.level == 2 and not lead_end then
      lead_end = index - 1
    end
  end
  if lead_start and lead_end and lead_end >= lead_start then
    local lead = pandoc.List({})
    for index = lead_start, lead_end do lead:insert(blocks[index]) end
    local wrapped = pandoc.List({})
    wrapped:insert(pandoc.RawBlock("html", '<header class="lead">'))
    wrapped:extend(lead)
    wrapped:insert(pandoc.RawBlock("html", "</header>"))
    local rebuilt = pandoc.List({})
    for index = 1, lead_start - 1 do rebuilt:insert(blocks[index]) end
    rebuilt:extend(wrapped)
    for index = lead_end + 1, #blocks do rebuilt:insert(blocks[index]) end
    blocks = rebuilt
  elseif strict_sections then
    warn("リードが見つかりません。題名の直後に本文を置いてください")
  end

  document.blocks = blocks

  document = document:walk({
    Header = collect_and_mark,
    Div = function(div) return callout(div) or hint(div) end,
    CodeBlock = code_block,
    Table = table_scroll,
  })

  document.meta["toc"] = pandoc.MetaBlocks({pandoc.RawBlock("html", toc_html())})
  document.meta["lesson-warnings"] = pandoc.MetaString(tostring(#warnings))
  return document
end
