# GitHub Pages：RAG 入門簡報

`index.html`、`styles.css`、`app.js` 是原生 HTML／CSS／JavaScript 簡報，沒有外部依賴，
也不需要 build。

## 本機預覽

直接用瀏覽器開啟 `docs/index.html`，或：

```bash
python3 -m http.server -d docs 8000   # 然後開 http://localhost:8000
```

## 操作

- 換頁：← →、PageUp／PageDown、Space、Home／End、右下角按鈕、左右滑動。
- 網址 `#5` 可直接跳到第 5 張。
- 每張下方「來源」可展開，列出 claim IDs 與 Wiki 頁面。
- 關閉 JavaScript 時，14 張以一般文件形式依序顯示，互動內容改為靜態表格與可展開答案。

## 發布（由使用者執行）

1. GitHub repository → **Settings → Pages**。
2. **Source** 選 *Deploy from a branch*，Branch 選 `main`，資料夾選 `/docs`，按 Save。
3. 約一分鐘後網址會是 `https://koyungching.github.io/rag-paper-wiki/`。

## 檢查

```bash
python3 scripts/validate_wiki.py
python3 scripts/validate_project.py      # 含 HTML slide ↔ outline ↔ Wiki mapping
python3 scripts/test_validators.py
python3 scripts/check_slides_browser.py  # 需要 playwright + chromium
```
