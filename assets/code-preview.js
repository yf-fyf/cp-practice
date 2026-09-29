// 配布ファイルを本文の上で読む。元のhrefは保存・修飾クリック・JSなしの操作に使う。
(() => {
  if (!window.HTMLDialogElement || !HTMLDialogElement.prototype.showModal) return;
  const links = document.querySelectorAll('a[data-code-preview]');
  if (!links.length) return;
  const dialog = document.createElement('dialog');
  dialog.className = 'code-preview';
  dialog.setAttribute('aria-labelledby', 'code-preview-name');
  dialog.setAttribute('aria-describedby', 'code-preview-meta');
  dialog.innerHTML = `
    <div class="cp-heading"><div><h2 id="code-preview-name"></h2><p id="code-preview-meta"></p></div>
      <button class="cp-close" type="button" autofocus>閉じる</button></div>
    <div class="cp-toolbar"><button class="cp-copy" type="button">全文コピー</button>
      <a class="cp-download">ダウンロード</a>
      <label class="cp-wrap-control"><input class="cp-wrap" type="checkbox">長い行を折り返す</label></div>
    <div class="cp-scroll" tabindex="0" role="region" aria-label="コードのプレビュー"></div>
    <p class="cp-status" role="status" aria-live="polite"></p>`;
  document.body.append(dialog);
  const name = dialog.querySelector('h2'), meta = dialog.querySelector('#code-preview-meta');
  const view = dialog.querySelector('.cp-scroll'), status = dialog.querySelector('.cp-status');
  const copy = dialog.querySelector('.cp-copy'), wrap = dialog.querySelector('.cp-wrap');
  const download = dialog.querySelector('.cp-download');
  let current, trigger, previousOverflow, controller, generation = 0;

  for (const link of links) {
    link.setAttribute('aria-haspopup', 'dialog');
    link.addEventListener('click', async event => {
      if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      controller?.abort();
      controller = new AbortController();
      const request = ++generation;
      trigger = link;
      current = null;
      name.textContent = decodeURIComponent(new URL(link.href).pathname.split('/').pop());
      meta.textContent = 'プレビュー';
      download.href = link.href;
      download.download = name.textContent;
      copy.disabled = wrap.disabled = true;
      view.textContent = '読み込み中…';
      view.setAttribute('aria-busy', 'true');
      status.textContent = '元のファイルをダウンロードできます。';
      previousOverflow = document.documentElement.style.overflow;
      document.documentElement.style.overflow = 'hidden';
      dialog.showModal();
      try {
        const response = await fetch(link.dataset.codePreview, {signal: controller.signal});
        if (!response.ok) throw new Error('preview unavailable');
        const data = await response.json();
        if (typeof data.code !== 'string' || typeof data.name !== 'string' ||
            !Array.isArray(data.lines) || data.lines.some(line => typeof line !== 'string') ||
            !/^[a-z]+$/.test(data.language) || typeof data.label !== 'string') throw new Error('invalid preview');
        if (request !== generation) return;
        current = data;
        name.textContent = data.name;
        meta.textContent = `${data.label} · ${data.lines.length}行`;
        download.download = data.name;
        const pre = document.createElement('pre'), code = document.createElement('code');
        pre.className = `sourceCode ${data.language}`;
        code.className = `sourceCode ${data.language}`;
        // HTMLは登録した配布物のCodeBlockから生成した構文色のspanだけ。
        data.lines.forEach((line, index) => {
          const span = document.createElement('span');
          span.innerHTML = line;
          code.append(span);
          if (index < data.lines.length - 1) code.append(document.createTextNode('\n'));
        });
        pre.append(code);
        view.replaceChildren(pre);
        view.classList.toggle('cp-wrapped', wrap.checked);
        view.scrollTop = view.scrollLeft = 0;
        copy.disabled = wrap.disabled = false;
      } catch (error) {
        if (request !== generation || error.name === 'AbortError') return;
        view.textContent = 'プレビューを読み込めませんでした。';
        status.textContent = 'ダウンロードから元のファイルを開けます。閉じてもう一度開くと再読み込みします。';
      } finally {
        if (request === generation) view.removeAttribute('aria-busy');
      }
    });
  }
  dialog.querySelector('.cp-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('close', () => {
    generation++;
    controller?.abort();
    current = null;
    document.documentElement.style.overflow = previousOverflow;
    trigger?.focus({preventScroll: true});
  });
  wrap.addEventListener('change', () => view.classList.toggle('cp-wrapped', wrap.checked));
  copy.addEventListener('click', async () => {
    if (!current) return;
    const text = current.code, request = generation;
    let copied = false;
    try { await navigator.clipboard.writeText(text); copied = true; } catch {}
    if (request !== generation) return;
    // LANのHTTP閲覧でも選択内容のコピーを試せるようにする。
    if (!copied) {
      const area = document.createElement('textarea');
      area.value = text;
      area.style.cssText = 'position:fixed;left:0;top:0;width:1px;height:1px;opacity:0';
      dialog.append(area);
      area.select();
      try { copied = document.execCommand('copy'); } catch {}
      area.remove();
      copy.focus({preventScroll: true});
    }
    status.textContent = copied ? 'コード全文をコピーしました。' :
      'コピーできませんでした。コードを選択してコピーするか、ダウンロードしてください。';
  });
})();
